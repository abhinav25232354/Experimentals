from pathlib import Path

from PIL import Image


SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png"}
QUALITY = 80


def find_images(folder_path: Path) -> list[Path]:
    return [
        item
        for item in folder_path.iterdir()
        if item.is_file() and item.suffix.lower() in SUPPORTED_EXTENSIONS
    ]


def convert_image(image_path: Path) -> Path:
    output_path = image_path.with_suffix(".webp")

    with Image.open(image_path) as image:
        if image.mode in ("RGBA", "LA") or (
            image.mode == "P" and "transparency" in image.info
        ):
            converted = image.convert("RGBA")
        else:
            converted = image.convert("RGB")

        converted.save(output_path, "WEBP", quality=QUALITY)

    image_path.unlink()
    return output_path


def main() -> None:
    folder_input = input("Enter folder path: ").strip().strip('"')

    if not folder_input:
        raise SystemExit("No folder path was provided.")

    folder_path = Path(folder_input).expanduser().resolve()

    if not folder_path.exists():
        raise SystemExit(f"Folder does not exist: {folder_path}")

    if not folder_path.is_dir():
        raise SystemExit(f"Path is not a folder: {folder_path}")

    images = find_images(folder_path)

    if not images:
        raise SystemExit("No JPG, JPEG, or PNG files were found in that folder.")

    for image_path in images:
        output_path = convert_image(image_path)
        print(f"Converted and removed original: {image_path.name} -> {output_path.name}")


if __name__ == "__main__":
    main()
