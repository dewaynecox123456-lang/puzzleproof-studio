from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZipFile
import os
import sys

from PIL import Image

ROOT_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = ROOT_DIR / "src"
sys.path.insert(0, str(SRC_DIR))

from image_processor import EXPORT_TARGETS, FILL_PUZZLE_AREA, FIT_ENTIRE_ARTWORK, ImageProcessor  # noqa: E402


def near(actual, expected, tolerance=24):
    return all(abs(a - e) <= tolerance for a, e in zip(actual[:3], expected))


def assert_fit_markers_visible(image_path):
    with Image.open(image_path) as output:
        output = output.convert("RGB")
        target_w, target_h = output.size

        source_w, source_h = 600, 1000
        scale = min(target_w / source_w, target_h / source_h)
        resized_w = round(source_w * scale)
        resized_h = round(source_h * scale)
        left = (target_w - resized_w) // 2
        top = (target_h - resized_h) // 2
        right = left + resized_w
        bottom = top + resized_h

        probes = {
            "top red edge": ((left + resized_w // 2, top + 8), (220, 20, 20)),
            "bottom blue edge": ((left + resized_w // 2, bottom - 9), (20, 45, 220)),
            "left green edge": ((left + 8, top + resized_h // 2), (25, 150, 70)),
            "right gold edge": ((right - 9, top + resized_h // 2), (220, 170, 30)),
        }
        for label, (point, expected) in probes.items():
            actual = output.getpixel(point)
            if not near(actual, expected):
                raise AssertionError(f"{label} was not preserved in {image_path}: expected {expected}, got {actual}")


def extract_docx_image(docx_path, output_path):
    with ZipFile(docx_path) as docx:
        output_path.write_bytes(docx.read("word/media/preset-output.png"))


def create_source(path):
    image = Image.new("RGB", (600, 1000), (246, 238, 222))
    pixels = image.load()
    for y in range(image.height):
        for x in range(image.width):
            if y < 50:
                pixels[x, y] = (220, 20, 20)
            elif y >= image.height - 50:
                pixels[x, y] = (20, 45, 220)
            elif x < 50:
                pixels[x, y] = (25, 150, 70)
            elif x >= image.width - 50:
                pixels[x, y] = (220, 170, 30)
            elif 240 <= x <= 360 and 420 <= y <= 580:
                pixels[x, y] = (105, 55, 145)
    image.save(path)


def main():
    processor = ImageProcessor()
    prefix = f"crop-safe-validation-{os.getpid()}"
    with TemporaryDirectory() as tmp:
        source = Path(tmp) / f"{prefix}.png"
        create_source(source)

        png_path = processor.export(
            source,
            "Puzzle Print",
            "PNG",
            image_placement_mode=FIT_ENTIRE_ARTWORK,
        )
        assert_fit_markers_visible(png_path)

        docx_path = processor.export(
            source,
            "Puzzle Print",
            "DOCX",
            image_placement_mode=FIT_ENTIRE_ARTWORK,
        )
        extracted = Path(tmp) / "docx-embedded.png"
        extract_docx_image(docx_path, extracted)
        assert_fit_markers_visible(extracted)

        fill_path = processor.export(
            source,
            "Puzzle Print",
            "PNG",
            image_placement_mode=FILL_PUZZLE_AREA,
        )
        with Image.open(fill_path) as fill_output:
            if fill_output.size != EXPORT_TARGETS["Puzzle Print"]["pixels"]:
                raise AssertionError(f"Fill output size mismatch: {fill_output.size}")

    print("Crop-safe export validation passed for PNG and DOCX fit mode.")


if __name__ == "__main__":
    main()
