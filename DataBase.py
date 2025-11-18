import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
import os
from CreateCustomPlaylist import create_custom_playlist


class SimpleChannelDB:
    def __init__(self):
        self.db_path = "simple_channels.db"
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS channels (
                id INTEGER PRIMARY KEY,
                name TEXT,
                group_name TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def get_all_channels(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM channels")
        # cursor.execute("DELETE FROM channels")
        results = cursor.fetchall()
        conn.close()
        return results

    def add_channel_from_file(self, name, group_name):
        """Add a channel from file data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT OR IGNORE INTO channels (name, group_name) VALUES (?, ?)",
                           (name, group_name))
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False
        finally:
            conn.close()


class SimpleGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("IPTV Channel Manager")
        self.root.geometry("800x600")

        self.db = SimpleChannelDB()
        self.file_data = []  # Store file data
        self.setup_gui()

    def on_selection_change(self, event):
        """Update status when selection changes"""
        selected_items = self.tree.selection()
        if selected_items:
            self.status_label.config(text=f"Selected {len(selected_items)} channels")
        else:
            self.status_label.config(text="Ready")

    def setup_gui(self):
        # Header
        header = ttk.Label(self.root, text="TV Search Index", font=("Arial", 16, "bold"))
        header.pack(pady=10)

        # Button frame
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=5)

        # Buttons
        ttk.Button(button_frame, text="Load from File", command=self.load_from_file).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Import Selected", command=self.import_selected_to_database).pack(side="left",
                                                                                                        padx=5)
        ttk.Button(button_frame, text="Clear View", command=self.clear_view).pack(side="left", padx=5)

        # Selection label
        self.selection_label = ttk.Label(self.root,
                                         text="Ctrl+Click to select multiple items, Shift+Click for range selection")
        self.selection_label.pack(pady=2)

        # Status label
        self.status_label = ttk.Label(self.root, text="Ready", relief="sunken")
        self.status_label.pack(fill="x", side="bottom", pady=2)

        # Create frame for treeview and scrollbars
        tree_frame = ttk.Frame(self.root)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Treeview
        self.tree = ttk.Treeview(tree_frame, columns=("ID", "Name", "Group"), show="headings", height=20,
                                 selectmode="extended")
        # self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Vertical scrollbar
        v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=v_scrollbar.set)

        # Horizontal scrollbar
        h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(xscrollcommand=h_scrollbar.set)

        # Grid layout for treeview and scrollbars
        self.tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")

        # Configure grid weights so treeview expands
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        # Column headers
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Channel Name")
        self.tree.heading("Group", text="Group")

        # Column widths
        self.tree.column("ID", width=50)
        self.tree.column("Name", width=300)
        self.tree.column("Group", width=200)

        # Bind selection event to update status
        self.tree.bind("<<TreeviewSelect>>", self.on_selection_change)

    def load_from_file(self):
        """Load data from search_results.txt file"""
        filename = "search_results.txt"

        if not os.path.exists(filename):
            messagebox.showerror("Error", f"File '{filename}' not found!")
            return

        try:
            self.clear_view()
            self.file_data = []

            with open(filename, 'r') as file:
                lines = file.readlines()

            file_count = 0
            for line in lines:
                # Skip comments and empty lines
                if line.startswith('#') or not line.strip():
                    continue

                # Parse the line format: ID|Channel_Name|Group_Name
                parts = line.strip().split('|')
                if len(parts) >= 3:
                    file_id = parts[0].strip()
                    channel_name = parts[1].strip()
                    group_name = parts[2].strip() if parts[2].strip() != "Unknown" else "No Group"

                    # Store in file_data
                    self.file_data.append((file_id, channel_name, group_name))

                    # Display in tree
                    self.tree.insert("", "end", values=(file_id, channel_name, group_name))
                    file_count += 1

            self.status_label.config(text=f"Loaded {file_count} channels from {filename}")

        except Exception as e:
            messagebox.showerror("Error", f"Error reading file: {e}")

    def clear_view(self):
        """Clear the treeview"""
        for item in self.tree.get_children():
            self.tree.delete(item)

    def import_selected_to_database(self):
        """Import only selected channels to database"""
        if not self.file_data:
            messagebox.showwarning("Warning", "No file data to import. Load from file first!")
            return

        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("Warning", "No channels selected! Select channels first.")
            return

        imported_count = 0
        skipped_count = 0
        mode_switch = "selected_channels"

        # Get selected channel data
        selected_channels = []
        for item in selected_items:
            values = self.tree.item(item, 'values')
            file_id, channel_name, group_name = values
            selected_channels.append((file_id, channel_name, group_name))

        # Import selected channels
        for file_id, channel_name, group_name in selected_channels:
            # Try to add channel to database
            if self.db.add_channel_from_file(channel_name, group_name):
                imported_count += 1
            else:
                skipped_count += 1

        selected_channel_names = [channel[1] for channel in selected_channels]
        new_selected_channels = f"{'\n'.join(selected_channel_names)}"

        create_custom_playlist(new_selected_channels, mode_switch)

        # print(f"{'\n'.join(selected_channel_names)}")
        # print(selected_channels[0][1])

        message = f"Import complete!\n"
        message += f"✅ Imported: {imported_count} channels\n"
        message += f"⚠️ Skipped (duplicates): {skipped_count} channels"

        messagebox.showinfo("Import Complete", message)
        self.status_label.config(text=f"Imported {imported_count} selected channels to database")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = SimpleGUI()
    app.run()
