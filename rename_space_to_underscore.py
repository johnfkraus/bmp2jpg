import os
from pathlib import Path

def rename_spaces(root_dir: str) -> None:
    root_path = Path(root_dir)

    # Walk bottom‑up so we rename children before their parent directories
    for dirpath, dirnames, filenames in os.walk(root_path, topdown=False):
        dirpath = Path(dirpath)

        # Rename files
        for name in filenames:
            if " " in name:
                old_path = dirpath / name
                new_name = name.replace(" ", "_")
                new_path = dirpath / new_name
                # Skip if target already exists to avoid collisions
                if not new_path.exists():
                    print(f"File: {old_path} -> {new_path}")
                    old_path.rename(new_path)

        # Rename directories
        for name in dirnames:
            if " " in name:
                old_path = dirpath / name
                new_name = name.replace(" ", "_")
                new_path = dirpath / new_name
                if not new_path.exists():
                    print(f"Dir:  {old_path} -> {new_path}")
                    old_path.rename(new_path)

if __name__ == "__main__":
    # Change this to the directory you want to process
    target_directory = "/path/to/your/directory"
    target_directory = Path.home() / 'Documents'

    rename_spaces(target_directory)
