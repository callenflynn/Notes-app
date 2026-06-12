# Notes-app

Just a notes app :)

Website: [Here](https://Shadowniko1.github.io)

It can say it's a virus but it's open source

## Installation ( not working now (((( )

### Windows
- **MSI Installer (Recommended)**: Download the latest `.msi` from [releases](https://github.com/Shadowniko1/Notes-app/releases/latest)
- **Portable EXE**: Download `notes-app.exe` from [releases](https://github.com/Shadowniko1/Notes-app/releases/latest) and run directly

### Linux
Download the latest `.deb` package from [releases](https://github.com/Shadowniko1/Notes-app/releases/latest):
```bash
sudo dpkg -i notes-app.deb
notes-app
```

### macOS
Download the latest binary from [releases](https://github.com/Shadowniko1/Notes-app/releases/latest):
```bash
chmod +x notes-app
./notes-app
```
> **Note:** If macOS blocks the app, go to **System Settings → Privacy & Security** and click **Open Anyway**

### Build from Source
For other platforms or to build yourself:

1. **Install Python 3.12+**
   ```bash
   python3 --version
   ```

2. **Clone the repository**
   ```bash
   git clone https://github.com/Shadowniko1/Notes-app.git
   cd Notes-app
   ```

3. **Install dependencies**
   ```bash
   pip3 install -r requirements.txt
   ```

4. **Run the app**
   ```bash
   python3 main.py
   ```

### Platform-Specific Notes

**macOS** - If Tkinter is missing:
```bash
brew install python-tk
```

**Linux (Fedora/RHEL)**:
```bash
sudo dnf install python3-tkinter
```

**Linux (Debian/Ubuntu)**:
```bash
sudo apt-get install python3-tk
```

**BSD**:
```bash
pkg install py311-tkinter
```
*(Replace `py311` with your installed Python version)*

## Nightly Builds

Nightly builds are automatically created on every commit to `main`. Download the latest nightly release [here](https://github.com/Shadowniko1/Notes-app/releases/latest).
