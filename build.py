import os
import shutil
import platform
import subprocess

APP_NAME = "checkmate"
MAIN_SCRIPT = "main.py"
BUILD_DIR = "dist"
BUILD_OPTS = ["--onefile", "--clean", "--name", APP_NAME]

def clean():
    for folder in ["build", "dist", "__pycache__"]:
        shutil.rmtree(folder, ignore_errors=True)
    spec_file = f"{APP_NAME}.spec"
    if os.path.exists(spec_file):
        os.remove(spec_file)

def build():
    print(f"[+] Building {APP_NAME}...")
    cmd = ["pyinstaller"] + BUILD_OPTS + [MAIN_SCRIPT]
    subprocess.run(cmd, check=True)

def move_output():
    platforms = {
        "Windows": "windows",
        "Linux": "linux",
        "Darwin": "macos"
    }

    system = platform.system()
    bin_name = APP_NAME + (".exe" if system == "Windows" else "")
    src_path = os.path.join(BUILD_DIR, bin_name)
    out_dir = os.path.join("builds", platforms.get(system, "unknown"))

    os.makedirs(out_dir, exist_ok=True)
    dest_path = os.path.join(out_dir, bin_name)

    if os.path.exists(src_path):
        shutil.move(src_path, dest_path)
        print(f"[✓] Executable moved to: {dest_path}")
    else:
        print("[!] Build failed or executable not found.")

if __name__ == "__main__":
    clean()
    build()
    move_output()
