
import os
import sys
from io import BytesIO
from pathlib import Path
import shutil

from PIL import Image  # pip install pillow or conda install pillow

myhome = Path.home()
# print(Path.home())
input_path = "Downloads/allison"
output_path = input_path + "/jpgs_from_bmps"
INPUT_DIR = myhome / input_path
OUTPUT_DIR = Path.home() / Path(output_path)

print(f"{INPUT_DIR=}")
print(f"{OUTPUT_DIR=}")

# user_command = None
# user_commmand = input("Proceed? (Y/N)?").lower()
# if user_command != 'y':
#     print(f"{user_commmand}")
#     sys.exit(0)

MAX_SIZE_BYTES = 200 * 1024  # 200 KB
MIN_QUALITY = 10             # don't go below this
QUALITY_STEP = 5             # decrement step
DOWNSCALE_FACTOR = 0.9       # 10% smaller each time if needed
print(OUTPUT_DIR)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def compress_to_target_size(img: Image.Image, out_path: Path):
    """
    Save `img` as JPEG at `out_path` with size <= MAX_SIZE_BYTES.
    Tries lowering quality and then resolution if needed.
    """
    # Ensure RGB (BMP can be paletted, RGBA, etc.)
    img = img.convert("RGB")  # conversion used when saving JPEG [web:1][web:4]

    quality = 95  # start high; Pillow recommended max is 95 [web:3]
    width, height = img.size

    while True:
        # Try saving to an in‑memory buffer first
        buf = BytesIO()
        img.save(buf, format="JPEG", quality=quality, optimize=True)  # quality parameter controls compression [web:3][web:9]
        size = buf.tell()

        if size <= MAX_SIZE_BYTES:
            # Write to disk once it fits
            with open(out_path, "wb") as f:
                f.write(buf.getvalue())
            return True

        # If too big, first reduce quality, then resolution
        if quality > MIN_QUALITY + QUALITY_STEP:
            quality -= QUALITY_STEP
        else:
            # Quality is already low; downscale the image
            new_width = int(width * DOWNSCALE_FACTOR)
            new_height = int(height * DOWNSCALE_FACTOR)
            if new_width < 50 or new_height < 50:
                # Give up if image would become too small
                print(f"Could not reach target size for {out_path.name}, final size ~{size/1024:.1f} KB")
                with open(out_path, "wb") as f:
                    f.write(buf.getvalue())
                return False

            width, height = new_width, new_height
            img = img.resize((width, height), Image.LANCZOS)  # typical Pillow resizing approach [web:8]
            # Reset quality a bit higher after resizing, then loop
            quality = 85


def convert_directory_bmp_to_jpg(input_dir: Path, output_dir: Path):
    for bmp_path in input_dir.glob("*.bmp", case_sensitive=False):
        out_name = bmp_path.stem + ".jpg"
        out_path = output_dir / out_name

        try:
            with Image.open(bmp_path) as img:  # opening then saving in new format [web:4]
                print(f"Processing {bmp_path.name} -> {out_name}")
                compress_to_target_size(img, out_path)
        except Exception as e:
            print(f"Error processing {bmp_path}: {e}")




def move_file_to_folder(source_file, destination_folder):
    """
    Moves a file to a destination folder, creating the folder if necessary.

    Args:
        source_file (str): The path to the source file.
        destination_folder (str): The path to the destination folder.
    """
    # 1. Create the destination folder(s) if they do not exist
    # exist_ok=True prevents an error if the directory already exists
    try:
        os.makedirs(destination_folder, exist_ok=True)
        print(f"Ensured destination folder '{destination_folder}' exists or was created.")
    except OSError as e:
        print(f"Error creating directory {destination_folder}: {e}")
        return

    # 2. Construct the full destination path for the file
    file_name = os.path.basename(source_file)
    destination_path = os.path.join(destination_folder, file_name)

    # 3. Move the file
    try:
        shutil.move(source_file, destination_path)
        print(f"Successfully moved '{source_file}' to '{destination_path}'.")
    except FileNotFoundError:
        print(f"Error: Source file '{source_file}' not found.")
    except Exception as e:
        print(f"Error moving file: {e}")

# # --- Example Usage ---
# # Define source file and destination folder paths
# source = "my_file.txt"
# destination = "path/to/new_folder"

# # Create a dummy file for testing purposes
# with open(source, 'w') as f:
#     f.write("This is a test file.")

# # Call the function to move the file
# move_file_to_folder(source, destination)



if __name__ == "__main__":
    convert_directory_bmp_to_jpg(INPUT_DIR, OUTPUT_DIR)
