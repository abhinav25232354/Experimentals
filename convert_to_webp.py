from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError as import_error:
    raise SystemExit(
        "Pillow is required to run this script. Install it with `pip install pillow`."
    ) from import_error

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png"}
QUALITY = 80


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert JPG/JPEG/PNG images to WebP and remove originals."
    )
    parser.add_argument(
        "folder",
        nargs="?",
        help="Folder path containing images to convert. If omitted, the script will prompt for one.",
    )
    parser.add_argument(
        "-r",
        "--recursive",
        action="store_true",
        help="Search for images recursively in subfolders.",
    )
    return parser.parse_args()


def find_images(folder_path: Path, recursive: bool = False) -> list[Path]:
    iterator = folder_path.rglob("*") if recursive else folder_path.iterdir()
    return sorted(
        item
        for item in iterator
        if item.is_file() and item.suffix.lower() in SUPPORTED_EXTENSIONS
    )


def get_folder_path(folder_arg: str | None) -> Path:
    if folder_arg:
        folder_input = folder_arg.strip().strip('"')
    else:
        folder_input = input("Enter folder path: ").strip().strip('"')

    if not folder_input:
        raise SystemExit("No folder path was provided.")

    folder_path = Path(folder_input).expanduser().resolve()

    if not folder_path.exists():
        raise SystemExit(f"Folder does not exist: {folder_path}")

    if not folder_path.is_dir():
        raise SystemExit(f"Path is not a folder: {folder_path}")

    return folder_path


def convert_image(image_path: Path) -> Path:
    output_path = image_path.with_suffix(".webp")
    temp_path = output_path.with_name(f"{output_path.stem}.tmp{output_path.suffix}")

    with Image.open(image_path) as image:
        if image.mode in ("RGBA", "LA") or (
            image.mode == "P" and "transparency" in image.info
        ):
            converted = image.convert("RGBA")
        else:
            converted = image.convert("RGB")

        converted.save(temp_path, "WEBP", quality=QUALITY)

    temp_path.replace(output_path)
    image_path.unlink()
    return output_path


def main() -> None:
    args = parse_args()
    folder_path = get_folder_path(args.folder)
    images = find_images(folder_path, recursive=args.recursive)

    if not images:
        raise SystemExit(
            "No JPG, JPEG, or PNG files were found in that folder."
        )

    success = 0
    failed = 0

    for image_path in images:
        try:
            output_path = convert_image(image_path)
            print(
                f"Converted and removed original: {image_path.name} -> {output_path.name}"
            )
            success += 1
        except Exception as error:
            print(
                f"Failed to convert {image_path}: {error}",
                file=sys.stderr,
            )
            failed += 1

    print(
        f"Finished conversion: {success} succeeded, {failed} failed."
    )


if __name__ == "__main__":
    main()
