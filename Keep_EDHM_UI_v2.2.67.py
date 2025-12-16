import os
import re
import shutil
import winreg
import sys
import zipfile
import tempfile
import ctypes
import subprocess

# ======================================================
# Common helpers
# ======================================================

def log(msg):
    print(f"[INFO] {msg}")

def error(msg):
    print(f"[ERROR] {msg}")

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    log("Request for admin rights...")
    params = ' '.join([f'"{arg}"' for arg in sys.argv])
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, params, None, 1
    )
    sys.exit()

# ======================================================
# PART 1 - UI v3 History files migration
# ======================================================

REG_PATH = r"Software\Elte Dangerous\Mods\EDHM"
REG_VALUE = "EDHM_DOCS"

VALID_JSON_REGEX = re.compile(r"^\d{14}\.json$")

def get_registry_value():
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH) as key:
        value, _ = winreg.QueryValueEx(key, REG_VALUE)
        return value

def move_history_files():
    log("Starting UI v3 History files migration...")

    try:
        raw_path = get_registry_value()
        expanded_path = os.path.expandvars(raw_path)
        history_path = os.path.join(expanded_path, "ODYSS", "History")

        if not os.path.isdir(history_path):
            error(f"History folder not found : {history_path}")
            return

        save_folder = os.path.join(history_path, "save_v3_history")
        os.makedirs(save_folder, exist_ok=True)

        moved_files = 0

        for filename in os.listdir(history_path):
            if not filename.lower().endswith(".json"):
                continue

            if VALID_JSON_REGEX.match(filename):
                continue

            src = os.path.join(history_path, filename)
            dst = os.path.join(save_folder, filename)

            shutil.move(src, dst)
            moved_files += 1
            log(f"Moved : {filename}")

        log(f"UI v3 History migration finished ({moved_files} file(s) moved)")

    except Exception as e:
        error(f"UI v3 History migration failed : {e}")
        log("Continuing with EDHM installation anyway...")

# ======================================================
# PART 2 - UI Update
# ======================================================

def get_embedded_file_bytes(name):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_path, name)
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Missing embedded file : {name}")
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
    subprocess.run(
        ["taskkill", "/f", "/im", process_name],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    log(f"'{process_name}' stopped (if running).")

def launch_exe(path):
    subprocess.Popen([path], shell=True)
    log(f"Starting : {path}")

# ======================================================
# MAIN
# ======================================================

def main():
    # Request admin rights only once, for both parts
    if not is_admin():
        run_as_admin()

    # ---- PART 1 ----
    move_history_files()

    # ---- PART 2 ----
    kill_process("EDHM_UI_mk2.exe")
    kill_process("EDHM_UI_Patcher.exe")

    log("Starting installation...")

    local_appdata = os.getenv("LOCALAPPDATA")
    if not local_appdata:
        error("Unable to retrieve path : %LOCALAPPDATA%.")
        input("Press Enter to exit...")
        return

    ui_folder = os.path.join(local_appdata, "EDHM_UI")
    os.makedirs(ui_folder, exist_ok=True)

    log(f"Extraction in : {ui_folder}")

    try:
        zip_bytes = get_embedded_file_bytes("ui_update.zip")
        extract_zip_to_folder(zip_bytes, ui_folder)
    except Exception as e:
        error(f"Extraction failed : {e}")
        input("Press Enter to exit...")
        return

    log("✅ Extraction successful...")

    exe_path = os.path.join(ui_folder, "EDHM_UI_mk2.exe")
    if not os.path.isfile(exe_path):
        error(f"File not found : {exe_path}")
        input("Press Enter to exit...")
        return

    launch_exe(exe_path)

    log("➡️ New version of EDHM added.")
    input("\nYou can close this window.")

if __name__ == "__main__":
    main()
