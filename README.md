# Intel Turbo Control Tray App

A system tray toggle for Intel CPU Turbo Boost (intel_pstate).

It was mainly done for myself and my laptop.

---

### ⚠️ Intel CPUs only.
Requires the intel_pstate driver.
Will NOT work on AMD systems.

### ⚠️ Only tested on KDE Plasma
I have no idea if it works everywhere. I don't know how QT handles everything.
If you have an intel CPU or Linux and it work/doesn't work, you can create an issue and give your CPU + Distro.
It will help make a compatibility list.

---

## Requirements
- Python 3 (with Qt5)
- Intel CPU (with intel_pstate)
- PyQT5

## Installation
1. Download the `intel-turbo-ctl-tray-app.py` file
2. Move it to any folder you want. Don't forget that the app also creates a save file.
3. Make it a executable by file properties or command: `chmod +x filepath`

Replace "filepath" with the path to the file

### Autostart (Optional)
System Settings -> Startup and Shutdown -> Autostart -> Add Application

Then select the python file

### Disable sudo Password Prompt (Optional)
Open the file `/etc/sudoers` and add this at the end of it: `yourusername ALL=(ALL) NOPASSWD: /usr/bin/tee /sys/devices/system/cpu/intel_pstate/no_turbo`

Replace "yourusername" with your Linux username
