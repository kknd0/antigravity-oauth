#!/usr/bin/env python3
"""
Build script for Antigravity OAuth App.
Creates standalone executables for macOS, Windows, and Linux.

Usage:
    pip install pyinstaller
    python build.py
"""

import platform
import subprocess
import sys
import os

APP_NAME = "Antigravity-OAuth"
SCRIPT = "app.py"


def build():
    system = platform.system()
    print(f"Building for {system}...")

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--name", APP_NAME,
        "--clean",
        "--noconfirm",
        SCRIPT,
    ]

    print("Running:", " ".join(cmd))
    subprocess.check_call(cmd)

    if system == "Darwin":
        print(f"\n[OK] macOS binary: dist/{APP_NAME}")
        print("     Double-click or run: ./dist/" + APP_NAME)
    elif system == "Windows":
        print(f"\n[OK] Windows exe:  dist\\{APP_NAME}.exe")
        print("     Double-click to run!")
    else:
        print(f"\n[OK] Linux binary: dist/{APP_NAME}")
        print("     Run: ./dist/" + APP_NAME)


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    build()
