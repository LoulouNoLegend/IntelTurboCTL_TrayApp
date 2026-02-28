#!/usr/bin/env python3
import sys
import subprocess
import os
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer

TURBO = "/sys/devices/system/cpu/intel_pstate/no_turbo"
saveFile = 'itctl-trayApp-save.txt'
incompatibleDevice = bool()

def checkCompatibility():
    global incompatibleDevice

    try:
        with open(TURBO) as file:
            return file.read().strip()
    except FileNotFoundError:
        print("Intel pstate file not found. Your device may not support Intel Turbo.")
        incompatibleDevice = True

def getStateTurbo():
    global incompatibleDevice

    if incompatibleDevice:
        return
    else:
        try:
            with open(TURBO) as file:
                return file.read().strip()
        except PermissionError:
            print("Permission denied.")
        except Exception as e:
            print(f"An error occurred: {e}")

def setStateTurbo(val):
    # echo *value* | sudo tee /sys/devices/system/cpu/intel_pstate/no_turbo
    subprocess.run(
        ["sudo", "tee", TURBO],
        input=str(val),
        text=True,
        stdout=subprocess.DEVNULL
    )
    print("Saving state: ", str(val))
    with open(saveFile, 'w') as file:
        file.write(str(val))


def toggleTurbo():
    state = getStateTurbo()
    # 0 = Enabled
    # 1 = Disabled
    if state == "0":
        setStateTurbo(1)
    elif state == "1":
        setStateTurbo(0)
    refreshState()

def refreshState():
    state = getStateTurbo()
    if state == "0":
        tray.setIcon(QIcon.fromTheme("speedometer"))
        status.setText("Turbo: Enabled")
        toggle_action.setText("Disable Turbo")
    elif state == "1":
        tray.setIcon(QIcon.fromTheme("speedometer"))
        status.setText("Turbo: Disabled")
        toggle_action.setText("Enable Turbo")
    else:
        tray.setIcon(QIcon.fromTheme("dialog-warning"))
        status.setText("Tool incompatible with your CPU")
        toggle_action.setEnabled(False)
        toggle_action.setVisible(False)

# On start, check the last saved state to restore it, since every reboot generally re-enables Turbo.
def checkLastState():
    global incompatibleDevice

    if incompatibleDevice:
        return
    else:
        if not os.path.exists(saveFile):
            print("Save file not found. Creating one...")
            with open(saveFile, 'w') as file:
                file.write('')
        else:
            with open(saveFile, 'r+') as file:
                state = file.read()
                if state == "" or state == None:
                    print("No state found in saved file. Current value saved.")
                    state = getStateTurbo()
                    file.write(state)
                elif int(state) == 0 or int(state) == 1:
                    print("State found in save file: ", state)
                    setStateTurbo(int(state))

# Defs
app = QApplication(sys.argv)
tray = QSystemTrayIcon()
menu = QMenu()

status = QAction("Checking...")
status.setEnabled(False)
menu.addAction(status)
menu.addSeparator()

toggle_action = QAction("Toggle Turbo")
toggle_action.triggered.connect(toggleTurbo)
menu.addAction(toggle_action)
menu.addSeparator()
menu.addAction("Close").triggered.connect(app.quit)

tray.setContextMenu(menu)
tray.show()

checkCompatibility()

if incompatibleDevice:
    pass
else:
    checkLastState()

    timer = QTimer()
    timer.timeout.connect(refreshState)
    timer.start(5000)

refreshState()

sys.exit(app.exec_())