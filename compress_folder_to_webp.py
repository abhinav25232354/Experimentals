from pathlib import Path

from PIL import Image


SUPPORTED_EXTENSIONS = {".webp"}


def find_images(folder_path: Path) -> list[Path]:
    return sorted(
        item
        for item in folder_path.iterdir()
        if item.is_file() and item.suffix.lower() in SUPPORTED_EXTENSIONS
    )


def get_compression_percentage() -> int:
    user_input = input("Enter compression percentage (0-100): ").strip()

    if not user_input:
        raise SystemExit("No compression percentage was provided.")

    try:
        compression = int(user_input)
    except ValueError as error:
        raise SystemExit("Compression percentage must be a whole number.") from error

    if not 0 <= compression <= 100:
        raise SystemExit("Compression percentage must be between 0 and 100.")

    return compression


def compression_to_quality(compression: int) -> int:
    # Higher compression means lower quality, but keep quality above zero.
    return max(1, 100 - compression)


def convert_for_webp(image: Image.Image) -> Image.Image:
    if image.mode in ("RGBA", "LA") or (
        image.mode == "P" and "transparency" in image.info
    ):
        return image.convert("RGBA")
    return image.convert("RGB")


def compress_image(image_path: Path, quality: int) -> Path:
    output_path = image_path.with_name(f"{image_path.stem}.tmp.webp")

    with Image.open(image_path) as image:
        converted = convert_for_webp(image)
        converted.save(output_path, "WEBP", quality=quality, optimize=True)

    image_path.unlink()
    output_path.replace(image_path)

    return image_path


def main() -> None:
    folder_input = input("Enter folder path: ").strip().strip('"')

    if not folder_input:
        raise SystemExit("No folder path was provided.")

    folder_path = Path(folder_input).expanduser().resolve()

    if not folder_path.exists():
        raise SystemExit(f"Folder does not exist: {folder_path}")

    if not folder_path.is_dir():
        raise SystemExit(f"Path is not a folder: {folder_path}")

    compression = get_compression_percentage()
    quality = compression_to_quality(compression)
    images = find_images(folder_path)

    if not images:
        raise SystemExit("No WebP files were found in that folder.")

    print(f"Using WebP quality: {quality}")

    for image_path in images:
        output_path = compress_image(image_path, quality)
        print(f"Compressed: {image_path.name} -> {output_path.name}")


if __name__ == "__main__":
    main()
