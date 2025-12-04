# Build-Your-Own-IPTV

An IPTV playlist builder that works like a modular conveyor belt. Start by selecting a source playlist, then search channels or groups in batches. After every 5 searches, a GUI pops up so you can precisely choose what to import.
The tool outputs a clean, custom M3U using regex matching and sed, while preserving the integrity of your original files.

1. ***Setup for fedora***

   ```bash
   dnf -y install python3-tkinter tk
   ```
2. ***Clone the repo***

   ```bash
   cd /home/$USER/src
   git clone https://github.com/Tyonnchie-Berry-1996/Build-Your-Own-IPTV.git
   cd Build-Your-Own-IPTV
   ```

3. ***Auto-generate a requirements file***

   ```bash
   pip install --upgrade pip
   pip install pipreqs
   pipreqs .
   ```
   >>Or try this
   
   ```bash
   python3 -m pip install --upgrade pip
   python3 -m pip install pipreqs
   pipreqs .
   ```
   >Check what deps you need

   ```bash
   cat requirements.txt
   ```      

4. ***Create a venv and install deps***

   ```bash
   python3 -m venv IPBOX
   source IPBOX/bin/activate
   ```

5. ***Upgrade pip and install the requirements file***

   ```bash
    python3 -m pip install --upgrade pip
    python3 -m pip install -r requirements.txt
   ```
   >Or try this

   ```bash
    pip install --upgrade pip
    pip install -r requirements.txt
   ```

