"""
Project: SoulSketch
File   : shared_memory/clean_and_archive_current_data.py
Authors: Itay Vazana & Oriya Even Chen

Description:
Archives and cleans all contents under shared_memory/* except for:
- The '8_History' folder
- Python scripts (*.py)
- Markdown files (*.md)

It first creates a timestamped snapshot under '8_History',
then deletes all other content (files and folders).
"""

import sys
from pathlib import Path

# === Auto-injected project root resolver ===
PROJECT_ROOT = Path(__file__).resolve().parent
while PROJECT_ROOT.name != "SoulSketch":
    if PROJECT_ROOT.parent == PROJECT_ROOT:
        break
    PROJECT_ROOT = PROJECT_ROOT.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import shutil
from datetime import datetime

# === Constants ===
EXCLUDED_FOLDER = "8_History"
EXCLUDED_EXTENSIONS = [".py", ".md"]


# === Archive Function ===

def archive_current_process(base_path: Path) -> None:
    """
    Archives the current shared_memory folder (excluding Python and markdown files)
    into a timestamped subdirectory under '8_History'.

    Args:
        base_path (Path): The shared_memory folder path.
    """
    history_dir = base_path / EXCLUDED_FOLDER
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    archive_path = history_dir / timestamp

    history_dir.mkdir(exist_ok=True)
    archive_path.mkdir()

    for item in base_path.iterdir():
        if item.name == EXCLUDED_FOLDER:
            continue
        if item.suffix in EXCLUDED_EXTENSIONS:
            continue
        destination = archive_path / item.name
        if item.is_dir():
            shutil.copytree(item, destination)
        elif item.is_file():
            shutil.copy2(item, destination)

    print(f"[ARCHIVE] Snapshot created at: {archive_path}")


# === Cleanup Function ===

def clean_all_except_history(base_path: Path) -> None:
    """
    Empties all folders under shared_memory/* except:
    - The '8_History' folder
    - Python scripts (*.py)
    - Markdown files (*.md)

    Folder structures are preserved.
    Args:
        base_path (Path): The shared_memory folder path.
    """
    for item in base_path.iterdir():
        if item.name == EXCLUDED_FOLDER:
            continue

        if item.suffix in EXCLUDED_EXTENSIONS:
            continue

        if item.is_file():
            item.unlink()
            print(f"[DEL FILE] {item}")

        elif item.is_dir():
            for sub_item in item.iterdir():  # Iterate over files in the folder
                if sub_item.suffix in EXCLUDED_EXTENSIONS and sub_item.is_file():
                    continue
                if sub_item.is_file():
                    sub_item.unlink()
                    print(f"[DEL FILE] {sub_item}")
                elif sub_item.is_dir():
                    shutil.rmtree(sub_item)  # Remove subdirectories' contents

    print("[DONE] Folder content cleanup complete.")


# === Entry Point ===

if __name__ == "__main__":
    current_dir = Path(__file__).resolve().parent
    archive_current_process(current_dir)
    clean_all_except_history(current_dir)
