import os
import subprocess
from pathlib import Path

# --- CONFIGURATION ---
# Change these paths to suit your setup
BASEDIR = Path("~/Wallpapers/").expanduser()
SOURCE_DIR = BASEDIR 
OUTPUT_DIR = BASEDIR 
THUMB_DIR = BASEDIR / "thumb"

# Target resolution for the "Fill" effect
TARGET_W = 1920
TARGET_H = 1080

def get_image_dimensions(image_path):
    """Uses ImageMagick 'identify' to get width and height."""
    try:
        # 'magick identify -format "%w %h"' returns 'width height'
        result = subprocess.run(
            ['magick', 'identify', '-format', '%w %h', str(image_path)],
            capture_output=True,
            text=True,
            check=True
        )
        dimensions = result.stdout.strip().split()
        return int(dimensions[0]), int(dimensions[1])
    except subprocess.CalledProcessError as e:
        print(f"Error reading dimensions for {image_path}: {e}")
        return None, None

def process_images():
    # 1. Prepare Directories
    if not SOURCE_DIR.exists():
        print(f"Source directory {SOURCE_DIR} does not exist. Creating it...")
        SOURCE_DIR.mkdir(parents=
        True, exist_ok=True)
        return

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # 2. Clear Thumb Directory
    if THUMB_DIR.exists():
        print(f"Cleaning thumb directory: {THUMB_DIR}")
        for file in THUMB_DIR.iterdir():
            if file.is_file():
                file.unlink()
    else:
        THUMB_DIR.mkdir(parents=True, exist_ok=True)

    # 3. Get all images from source (common extensions)
    image_files = [Path(i) for i in subprocess.getoutput(f"sort_by_color {SOURCE_DIR}").split("\n")]

    if not image_files:
        print("No images found in source directory.")
        return

    print(f"Found {len(image_files)} images. Starting processing...")

    # 4. Process each image
    for index, img_path in enumerate(image_files, start=1):
        # Create new filename: 001.png, 002.png, etc.
        new_name = f"{index:03d}.png"
        output_path = OUTPUT_DIR / new_name
        thumb_path = THUMB_DIR / new_name

        # Get original dimensions
        orig_w, orig_h = get_image_dimensions(img_path)
        if orig_w is None:
            continue

        # 5. Calculate Scale Factor for "Fill"
        # Formula: max(1920/width, 1080/height)
        # This ensures the smallest dimension meets the target,
        # causing the larger dimension to overflow (Fill effect)
        scale_factor_w = TARGET_W / orig_w
        scale_factor_h = TARGET_H / orig_h
        scale_val = max(scale_factor_w, scale_factor_h)

        # Convert to percentage for ImageMagick (e.g., 0.54 -> 54%)
        percentage = scale_val * 100

        try:
            print(f"Processing [{new_name}]: Scaling to {percentage:.2f}%")

            # 6. Main Image: Convert to PNG and Resize
            # Command: magick input.ext -resize [percentage]% output.png
            if percentage < 100:
                subprocess.run([
                    'magick',
                    str(img_path),
                    '-resize', f'{percentage}%',
                    str(output_path)
                ], check=True)
            else:
                os.rename(img_path, output_path)

            # 7. Thumbnail: 40% of ORIGINAL, same name, in thumb/ folder
            subprocess.run([
                'magick',
                str(output_path),
                '-resize', '40%',
                str(thumb_path)
            ], check=True)

        except subprocess.CalledProcessError as e:
            print(f"Failed to process {img_path.name}: {e}")
        if img_path != output_path:
            img_path.unlink(missing_ok=True)

    print("\nProcessing Complete.")
    print(f"Main images: {OUTPUT_DIR}")
    print(f"Thumbnails:  {THUMB_DIR}")

if __name__ == "__main__":
    process_images()
