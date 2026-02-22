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
import shutil
import sys
import os

APP_NAME = "Antigravity-OAuth"
SCRIPT = "app.py"


def build():
    system = platform.system()
    print(f"Building for {system}...")

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name", APP_NAME,
        "--clean",
        "--noconfirm",
    ]

    if system == "Darwin":
        # macOS: .app bundle so users can double-click
        cmd.extend(["--onedir", "--windowed"])
    else:
        # Windows / Linux: single file
        cmd.append("--onefile")
        if system == "Windows":
            cmd.append("--windowed")  # no console flash

    cmd.append(SCRIPT)

    print("Running:", " ".join(cmd))
    subprocess.check_call(cmd)

    if system == "Darwin":
        # Create DMG for macOS distribution
        app_path = f"dist/{APP_NAME}.app"
        dmg_path = f"dist/{APP_NAME}-macOS.dmg"
        if os.path.exists(dmg_path):
            os.remove(dmg_path)
        subprocess.check_call([
            "hdiutil", "create",
            "-volname", APP_NAME,
            "-srcfolder", app_path,
            "-ov", "-format", "UDZO",
            dmg_path,
        ])
        print(f"\n[OK] macOS app: {app_path}")
        print(f"[OK] DMG ready: {dmg_path}")
    elif system == "Windows":
        print(f"\n[OK] Windows exe: dist\\{APP_NAME}.exe")
    else:
        print(f"\n[OK] Linux binary: dist/{APP_NAME}")


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    build()
