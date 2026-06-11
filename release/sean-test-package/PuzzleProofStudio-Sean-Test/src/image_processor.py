from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:  # pragma: no cover - handled at runtime in GUI
    Image = None
    ImageDraw = None
    ImageFont = None

from app_paths import EXPORTS_DIR


DPI = 300
EXPORT_TARGETS = {
    "Puzzle": {"inches": (8.83, 11.77), "pixels": (2649, 3531)},
    "Sticker": {"inches": (4.37, 5.10), "pixels": (1311, 1530)},
    "Insert": {"inches": (3.75, 5.00), "pixels": (1125, 1500)},
}


class ImageProcessor:
    def available(self):
        return Image is not None

    def export(self, source_path, export_type, output_format, copyright_text="", placement="Bottom Right", opacity=180, font_size=42):
        if Image is None:
            raise RuntimeError("Pillow is required for image conversion. Install requirements first.")

        source_path = Path(source_path)
        target = EXPORT_TARGETS[export_type]
        output_format = output_format.upper()
        suffix = "jpg" if output_format == "JPEG" else output_format.lower()

        EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
        output_path = EXPORTS_DIR / f"{source_path.stem}-{export_type.lower()}.{suffix}"

        with Image.open(source_path) as image:
            converted = self._fit_center_crop(image.convert("RGBA"), target["pixels"])
            if copyright_text:
                converted = self._draw_copyright(converted, copyright_text, placement, opacity, font_size)
            if output_format == "JPEG":
                converted = converted.convert("RGB")
            converted.save(output_path, format=output_format, dpi=(DPI, DPI))
        return output_path

    def _fit_center_crop(self, image, target_size):
        target_w, target_h = target_size
        source_w, source_h = image.size
        scale = max(target_w / source_w, target_h / source_h)
        resized = image.resize((round(source_w * scale), round(source_h * scale)), Image.LANCZOS)
        left = (resized.width - target_w) // 2
        top = (resized.height - target_h) // 2
        return resized.crop((left, top, left + target_w, top + target_h))

    def _draw_copyright(self, image, text, placement, opacity, font_size):
        overlay = Image.new("RGBA", image.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(overlay)
        try:
            font = ImageFont.truetype("DejaVuSans.ttf", font_size)
        except OSError:
            font = ImageFont.load_default()

        bbox = draw.textbbox((0, 0), text, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        margin = max(24, font_size)
        y = image.height - text_h - margin
        if placement == "Bottom Left":
            x = margin
        elif placement == "Bottom Center":
            x = (image.width - text_w) // 2
        else:
            x = image.width - text_w - margin

        draw.text((x + 2, y + 2), text, font=font, fill=(0, 0, 0, min(180, opacity)))
        draw.text((x, y), text, font=font, fill=(255, 255, 255, opacity))
        return Image.alpha_composite(image, overlay)
