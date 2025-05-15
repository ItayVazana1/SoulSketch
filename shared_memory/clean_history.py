"""
Project: SoulSketch
File   : shared_memory/clean_history.py
Authors: Itay Vazana & Oriya Even Chen

Description:
This script deletes all contents under `shared_memory/8_History`,
preserving the folder itself.
"""

from pathlib import Path
import shutil

EXCLUDED_FOLDER = "8_History"

def clear_history_folder(base_path: Path) -> None:
    """
    Completely empties the contents of the '8_History' folder inside shared_memory.
    Deletes all subdirectories and files within it, but preserves the folder itself.
    """
    history_path = base_path / EXCLUDED_FOLDER

    if not history_path.exists():
        print("[INFO] History folder does not exist. Nothing to clear.")
        return

    for item in history_path.iterdir():
        try:
            if item.is_file():
                item.unlink()
                print(f"[DEL FILE] {item}")
            elif item.is_dir():
                shutil.rmtree(item)
                print(f"[DEL DIR] {item}")
        except Exception as e:
            print(f"[ERROR] Failed to delete {item}: {e}")

    print("[DONE] '8_History' folder emptied.")


if __name__ == "__main__":
    # Resolve project root from current file location
    shared_memory_path = Path(__file__).resolve().parent
    clear_history_folder(shared_memory_path)
