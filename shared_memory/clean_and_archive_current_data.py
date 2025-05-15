"""
Project: SoulSketch
File   : shared_memory/clean_and_archive_current_data.py
Author : Itay Vazana

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
    Deletes all content under shared_memory/* except:
    - The '8_History' directory
    - Python scripts (*.py)
    - Markdown files (*.md)

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
            shutil.rmtree(item)
            print(f"[DEL DIR] {item}")

    print("[DONE] Cleanup complete.")


# === Entry Point ===

if __name__ == "__main__":
    current_dir = Path(__file__).resolve().parent
    archive_current_process(current_dir)
    clean_all_except_history(current_dir)
