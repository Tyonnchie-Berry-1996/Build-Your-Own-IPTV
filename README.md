# Build-Your-Own-IPTV

An IPTV playlist builder that works like a modular conveyor belt. Start by selecting a source playlist, then search channels or groups in batches. After every 5 searches, a GUI pops up so you can precisely choose what to import.
The tool outputs a clean, custom M3U using regex matching and sed, while preserving the integrity of your original files.

## Quick Start

1. **Clone the repo**

   ```bash
   docker pull tyonnchieberry/dev-env
   ```
2. **Run It**
   ```bash
   docker run -it tyonnchieberry/dev-env:latest
   ```
3. **Test out some repo automation**
   ```bash
   git clone https://github.com/Tyonnchie-Berry-1996/Container-Repo-Automation.git
   ```
