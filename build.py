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
        # Zip the .app bundle for distribution
        app_path = f"dist/{APP_NAME}.app"
        zip_path = f"dist/{APP_NAME}-macOS"
        if os.path.exists(f"{zip_path}.zip"):
            os.remove(f"{zip_path}.zip")
        shutil.make_archive(zip_path, "zip", "dist", f"{APP_NAME}.app")
        print(f"\n[OK] macOS app: dist/{APP_NAME}.app")
        print(f"[OK] Zip ready: {zip_path}.zip")
    elif system == "Windows":
        print(f"\n[OK] Windows exe: dist\\{APP_NAME}.exe")
    else:
        print(f"\n[OK] Linux binary: dist/{APP_NAME}")


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    build()
