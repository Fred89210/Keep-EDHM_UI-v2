import os
import re
import shutil
import winreg
import sys
import ctypes

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
# UI v3 History files migration ONLY
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

# ======================================================
# MAIN
# ======================================================

def main():
    if not is_admin():
        run_as_admin()

    move_history_files()
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
