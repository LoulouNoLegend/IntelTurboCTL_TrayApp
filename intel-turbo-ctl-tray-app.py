#!/usr/bin/env python3
import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer

TURBO = "/sys/devices/system/cpu/intel_pstate/no_turbo"

def getStateTurbo():
    with open(TURBO) as f:
            return f.read().strip()

def setStateTurbo(val):
    # echo *value* | sudo tee /sys/devices/system/cpu/intel_pstate/no_turbo
    subprocess.run(
        ["sudo", "tee", TURBO],
        input=str(val),
        text=True,
        stdout=subprocess.DEVNULL
    )

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
        status.setText("Turbo: Not Available")
        toggle_action.setEnabled(False)

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
menu.addAction("Close Tool").triggered.connect(app.quit)

tray.setContextMenu(menu)
tray.show()

timer = QTimer()
timer.timeout.connect(refreshState)
timer.start(3000)

refreshState()
sys.exit(app.exec_())