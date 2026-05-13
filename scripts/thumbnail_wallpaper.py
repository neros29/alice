import hashlib
import subprocess
from pathlib import Path
# --- CONFIGURATION ---
# Change these paths to suit your setup
HOME = Path("~").expanduser()
SOURCE_DIR = HOME / "Pictures" / "Wallpapers"
OUTPUT_DIR = HOME  / "Wallpapers"
THUMB_DIR = OUTPUT_DIR / "thumb"
CACHE_DIR = HOME / ".cache"/ "Wallpapers"
CACHE_THUMB_DIR = CACHE_DIR / "thumb"

# Target resolution for the "Fill" effect
TARGET_W = 1920
TARGET_H = 1080
THUMB_SCALE = 40

def hash_image(image: Path):
    if not  image.is_file():
        return None
    hash = hashlib.sha256()
    with open(image, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            hash.update(byte_block)
    return hash.hexdigest()

def get_scale(image: Path):
    orig_w, orig_h = get_image_dimensions(image)
    assert orig_h is not None, "The image height seems to be None"
    assert orig_w is not None, "The image width seems to be None"
    # Formula: max(1920/width, 1080/height)
    # This ensures the smallest dimension meets the target,
    # causing the larger dimension to overflow (Fill effect)
    scale_factor_w = TARGET_W / orig_w
    scale_factor_h = TARGET_H / orig_h
    scale_val = max(scale_factor_w, scale_factor_h)
    return scale_val * 100

def scale_image(image: Path, new_name: str):
    target_path = OUTPUT_DIR / new_name
    target_thumb_path = THUMB_DIR / new_name
    hash = hash_image(image)
    assert hash is not None, "This image should exists"
    output_path = CACHE_DIR / f"{hash}.png"
    percentage = get_scale(image)
    print(f"Processing [{image.name}]: Scaling to {percentage:.2f}%")
    if not output_path.is_file():
        try:
            subprocess.run([
                'magick',
                str(image),
                '-resize', f'{percentage}%',
                str(output_path)
            ], check=True)
            create_thumbnail(output_path)
        except subprocess.CalledProcessError as e:
            print(f"Failed to process {image.name}: {e}")
            return
    else:
        print(f"Cache hit {hash}")
    output_path.copy(target_path)
    output_thumb_path = (CACHE_THUMB_DIR / output_path.name)
    if output_thumb_path.is_file():
        output_thumb_path.copy(target_thumb_path)
    else:
        create_thumbnail(output_path)

def create_thumbnail(image: Path):
    if not image.is_file():
        print("thumbnail file dose not exist.")
        exit()
    ouput_path = CACHE_THUMB_DIR / image.name
    subprocess.run([
        'magick',
        str(image),
        '-resize', f'{THUMB_SCALE}%',
        str(ouput_path)
    ], check=True)


def init_paths():
    assert HOME.exists(), "Home dose not exists, this should not happen"
    assert SOURCE_DIR.exists(), "Source Dir dose not exists, please create a valid source directory."

    # check main output dir
    if not OUTPUT_DIR.exists():
        confirm = input("The ouput directory specifed dose not exist, would you like to create it? (N/y)")
        if confirm.lower().strip() == "y":
            OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
            print("Output dir was created")
        else:
            exit()
    elif OUTPUT_DIR.exists():
        for file in OUTPUT_DIR.iterdir():
            if file.is_file():
                file.unlink()
        print("Cleared output directory.")
    else:
        assert True, "unreachable code"

    # check thumb dir
    if not THUMB_DIR.exists():
        THUMB_DIR.mkdir(parents=True, exist_ok=True)
    elif THUMB_DIR.exists():
        for file in THUMB_DIR.iterdir():
            if file.is_file():
                file.unlink()
        print("Cleared Thumbnail directory.")
    else:
        assert True, "unreachable code"

    # check if cache dir exists
    if not CACHE_DIR.exists():
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
    if not CACHE_THUMB_DIR.exists():
        CACHE_THUMB_DIR.mkdir(parents=True, exist_ok=True)


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
    image_files = [Path(i) for i in subprocess.getoutput(f"sort_by_color {SOURCE_DIR}").split("\n")]

    if not image_files:
        print("No images found in source directory.")
        return

    print(f"Found {len(image_files)} images. Starting processing...")

    # 4. Process each image
    for index, img_path in enumerate(image_files, start=1):
        if img_path.is_file():
            if img_path.suffix.lower() in [".png", ".jpg", ".webp", ".jpeg"]:
                new_name = f"{index:03d}.png"
                scale_image(img_path, new_name)

if __name__ == "__main__":
    init_paths()
    process_images()
