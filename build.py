import os
import shutil
import platform
import subprocess

APP_NAME = "checkmate"
MAIN_SCRIPT = "main.py"
BUILD_DIR = "dist"
BUILD_OPTS = ["--onefile", "--clean", "--name", APP_NAME]

# Path to PyInstaller (adjust if necessary)
PYINSTALLER_PATH = r"C:\Users\safra\AppData\Roaming\Python\Python313\Scripts\pyinstaller.exe"  # Adjust the path to your environment

def clean():
    print("[*] Cleaning old builds...")
    for folder in ["build", "dist", "__pycache__"]:
        if os.path.exists(folder):
            shutil.rmtree(folder)
    spec_file = f"{APP_NAME}.spec"
    if os.path.exists(spec_file):
        os.remove(spec_file)

def build():
    print(f"[*] Building {APP_NAME} with PyInstaller...")
    cmd = [PYINSTALLER_PATH] + BUILD_OPTS + [MAIN_SCRIPT]
    subprocess.run(cmd, check=True)

def move_output():
    platform_folder = {
        "Windows": "windows",
        "Linux": "linux",
        "Darwin": "macos"
    }

    system = platform.system()
    target_dir = os.path.join("builds", platform_folder.get(system, "unknown"))

    os.makedirs(target_dir, exist_ok=True)

    binary_name = APP_NAME + (".exe" if system == "Windows" else "")
    src = os.path.join(BUILD_DIR, binary_name)
    dest = os.path.join(target_dir, binary_name)

    if os.path.exists(src):
        shutil.move(src, dest)
        print(f"[+] Built binary moved to: {dest}")
    else:
        print("[!] Build failed or output not found.")

def create_deb_package():
    print("[*] Creating .deb package...")
    cmd = ["fpm", "-s", "dir", "-t", "deb", "--name", APP_NAME, "--version", "1.0", "--architecture", "amd64", "--prefix", "/usr/local", f"--path={BUILD_DIR}/{APP_NAME}"]
    subprocess.run(cmd, check=True)

def create_rpm_package():
    print("[*] Creating .rpm package...")
    cmd = ["fpm", "-s", "dir", "-t", "rpm", "--name", APP_NAME, "--version", "1.0", "--architecture", "x86_64", "--prefix", "/usr/local", f"--path={BUILD_DIR}/{APP_NAME}"]
    subprocess.run(cmd, check=True)

def create_msi_package():
    print("[*] Creating .msi package...")
    cmd = ["candle", f"{APP_NAME}.wxs"]  # Requires Wix Toolset (for Windows)
    subprocess.run(cmd, check=True)
    cmd = ["light", f"{APP_NAME}.wixobj"]
    subprocess.run(cmd, check=True)

if __name__ == "__main__":
    clean()
    build()
    move_output()

    # Optionally create .deb, .rpm, .msi packages
    if platform.system() == "Linux":
        create_deb_package()
        create_rpm_package()
    elif platform.system() == "Windows":
        create_msi_package()
