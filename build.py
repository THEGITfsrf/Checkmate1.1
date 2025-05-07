import os
import shutil
import platform
import subprocess

OUTPUT_DIR = input("path")

def ensure_output_dir():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

def build_exe():
    print("[*] Building binary with PyInstaller...")
    os.system("pyinstaller --onefile main.py")

    system = platform.system()
    binary_name = "main.exe" if system == "Windows" else "main"
    output_name = "checkmateproxy.exe" if system == "Windows" else "checkmateproxy"

    binary_path = os.path.join("dist", binary_name)
    if os.path.exists(binary_path):
        shutil.move(binary_path, os.path.join(OUTPUT_DIR, output_name))
    else:
        print(f"[!] Error: Expected binary not found: {binary_path}")

    # Cleanup
    shutil.rmtree("build", ignore_errors=True)
    shutil.rmtree("dist", ignore_errors=True)
    if os.path.exists("main.spec"):
        os.remove("main.spec")

def build_tar_gz():
    print("[*] Creating .tar.gz archive...")
    tar_file = os.path.join(OUTPUT_DIR, 'checkmateproxy.tar.gz')
    os.system(f"tar -czvf {tar_file} main.py requirements.txt setup.py")

def build_python_package():
    print("[*] Packaging Python setuptools .tar.gz...")
    if os.path.exists('dist'):
        shutil.rmtree('dist')
    os.system("python setup.py sdist")
    for f in os.listdir('dist'):
        if f.endswith('.tar.gz'):
            shutil.move(os.path.join('dist', f), os.path.join(OUTPUT_DIR, f))
    shutil.rmtree('dist')

def build_deb():
    print("[*] Building .deb package...")
    os.system("fpm -s dir -t deb -n checkmateproxy -v 1.0.0 --prefix /usr/local/bin main.py")

def build_rpm():
    print("[*] Building .rpm package...")
    os.system("fpm -s dir -t rpm -n checkmateproxy -v 1.0.0 --prefix /usr/local/bin main.py")

def build_msi():
    print("[*] Building .msi package...")
    os.system("python -m build")
    # Adjust this to use msilib or similar tools for Windows

def main():
    ensure_output_dir()
    
    # Build Executable
    build_exe()

    # Build Archive (tar.gz)
    build_tar_gz()

    # Build Python Package
    build_python_package()

    # Build .deb, .rpm, .msi if applicable
    if platform.system() == "Linux":
        build_deb()
        build_rpm()
    elif platform.system() == "Windows":
        build_msi()

    print(f"\n✅ All outputs are in the '{OUTPUT_DIR}/' folder.")

if __name__ == '__main__':
    main()
