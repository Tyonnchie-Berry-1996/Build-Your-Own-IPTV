# Build-Your-Own-IPTV

An IPTV playlist builder that works like a modular conveyor belt. Start by selecting a source playlist, then search channels or groups in batches. After every 5 searches, a GUI pops up so you can precisely choose what to import.
The tool outputs a clean, custom M3U using regex matching and sed, while preserving the integrity of your original files.

By default the module expects your files to be live at <code>$HOME/src</code>

1. ***Setup for fedora***

   ```bash
   dnf -y install python3-tkinter tk
   ```
2. ***Clone the repo***

   ```bash
   cd $HOME/src
   git clone https://github.com/Tyonnchie-Berry-1996/Build-Your-Own-IPTV.git
   cd Build-Your-Own-IPTV
   ```

3. ***Auto-generate a requirements file***

   ```bash
   pip install pipreqs
   pipreqs .
   ```
   >Or try this
   
   ```bash
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

You have to run <code>PlaylistRunner.py</code> to build a playlist for  <code>ListBuilder.py</code> to use. 

 6. ***Build a playlist***

    ```bash
     python3 PlaylistRunner.py
    ```
   
7. ***Search and Customize your playlist***

    ```bash
     python3 ListBuilder.py
    ``` 
    >Now you have a customized m3u playlist ready to pull streams for IPTV.
    
    >Don't believe me copy and paste this command <code> cat custom_playlist.m3u</code>

8. ***When ready deactivate your venv***

    ```bash
     deactivate
    ``` 

How do I use this?
 ---
   <p>There are some quick plug and play methods for a m3u file but I recommend using <code>Jellyfin</code> and <code>NextPVR</code> that's just my preference. I will add a video tutorial/visual demo with these steps and an explaination on how I use this in my daily life; I will also explain how you can use the m3u file with other apps outside of jellyfin.</p>
