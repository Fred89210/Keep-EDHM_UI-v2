import os
import sys
import zipfile
import shutil
import tempfile
import ctypes
import subprocess

def log(msg):
    print(f"[INFO] {msg}")

def error(msg):
    print(f"[ERROR] {msg}")
    input("Press Enter to exit...")
    sys.exit(1)

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    log("Request for admin rights...")
    params = ' '.join([f'"{arg}"' for arg in sys.argv])
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)
    sys.exit()

def get_embedded_file_bytes(name):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_path, name)
    if not os.path.isfile(file_path):
        error(f"Missing embedded file : {name}")
    with open(file_path, 'rb') as f:
        return f.read()

def extract_zip_to_folder(zip_bytes, dest_folder):
    with tempfile.TemporaryDirectory() as tmpdir:
        zip_path = os.path.join(tmpdir, 'ui_update.zip')
        with open(zip_path, 'wb') as f:
            f.write(zip_bytes)

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            for member in zip_ref.namelist():
                target = os.path.join(dest_folder, member)
                if member.endswith('/'):
                    os.makedirs(target, exist_ok=True)
                else:
                    os.makedirs(os.path.dirname(target), exist_ok=True)
                    with open(target, 'wb') as outfile, zip_ref.open(member) as infile:
                        shutil.copyfileobj(infile, outfile)

def kill_process(process_name):
    try:
        subprocess.run(["taskkill", "/f", "/im", process_name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        log(f"'{process_name}' stopped...")
    except Exception as e:
        error(f"Error while stopping '{process_name}' : {e}")

def launch_exe(path):
    try:
        subprocess.Popen([path], shell=True)
        log(f"Starting : {path}")
    except Exception as e:
        error(f"Failed to start {path} : {e}")

def main():
    if not is_admin():
        run_as_admin()

    kill_process("EDHM_UI_mk2.exe")
    kill_process("EDHM_UI_Patcher.exe")

    log("Starting installation...")

    local_appdata = os.getenv("LOCALAPPDATA")
    if not local_appdata:
        error("Unable to retrieve path : %LOCALAPPDATA%.")

    ui_folder = os.path.join(local_appdata, "EDHM_UI")
    os.makedirs(ui_folder, exist_ok=True)

    log(f"Extraction in : {ui_folder}")

    try:
        zip_bytes = get_embedded_file_bytes("ui_update.zip")
        extract_zip_to_folder(zip_bytes, ui_folder)
    except Exception as e:
        error(f"Extraction failed : {e}")

    log("✅ Extraction successful...")

    exe_path = os.path.join(ui_folder, "EDHM_UI_mk2.exe")
    if not os.path.isfile(exe_path):
        error(f"File not found : {exe_path}")

    launch_exe(exe_path)

    log("➡️ EDHM v21.00 has been added.")
    input("\nYou can close this window.")

if __name__ == "__main__":
    main()
