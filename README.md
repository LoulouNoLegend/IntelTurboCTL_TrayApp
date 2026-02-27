# Intel Turbo Control Tray App

A system tray toggle for Intel CPU Turbo Boost (intel_pstate).

It was mainly done for myself and my laptop.

---

### ⚠️ Intel CPUs only.
Requires the intel_pstate driver.
Will NOT work on AMD systems.

### ⚠️ Only tested on KDE Plasma
I have no idea if it works everywhere.

---

## Requirements
- Python 3 (with Qt5)
- Intel CPU with intel_pstate

**Install QT:**
```sudo dnf install python3-qt5```

## Installation
1. Download the `intel-turbo-ctl-tray-app.py` file
2. Move it to any folder you want
3. Make it a executable by file properties or command: `chmod +x filepath`

Replace "filepath" with the path to the file

### Autostart (Optional)
System Settings -> Startup and Shutdown -> Autostart -> Add Application

Then select the python file

### Disable sudo Password Prompt (Optional)
Open the file `/etc/sudoers` and add this at the end of it: `yourusername ALL=(ALL) NOPASSWD: /usr/bin/tee /sys/devices/system/cpu/intel_pstate/no_turbo`

Replace "yourusername" with your Linux username
