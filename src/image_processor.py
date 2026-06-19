from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile
import html

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:  # pragma: no cover - handled at runtime in GUI
    Image = None
    ImageDraw = None
    ImageFont = None

from app_paths import EXPORTS_DIR


DPI = 300
EXPORT_TARGETS = {
    "Puzzle Print": {"inches": (8.83, 11.77), "pixels": (2649, 3531), "slug": "puzzle-print"},
    "Box Insert": {"inches": (3.75, 5.00), "pixels": (1125, 1500), "slug": "box-insert"},
    "Box Sticker / Label": {"inches": (4.37, 5.10), "pixels": (1311, 1530), "slug": "box-sticker-label"},
}
EXPORT_ALIASES = {
    "Puzzle": "Puzzle Print",
    "Insert": "Box Insert",
    "Sticker": "Box Sticker / Label",
}
IMAGE_FORMATS = ("PNG", "JPG")
OUTPUT_FORMATS = IMAGE_FORMATS + ("DOCX",)
FIT_ENTIRE_ARTWORK = "Fit Entire Artwork / Preserve Full Image"
FILL_PUZZLE_AREA = "Fill Puzzle Area / Crop to Fill"
IMAGE_PLACEMENT_MODES = (FIT_ENTIRE_ARTWORK, FILL_PUZZLE_AREA)
EMU_PER_INCH = 914400


class ImageProcessor:
    def available(self):
        return Image is not None

    def export(
        self,
        source_path,
        export_type,
        output_format,
        copyright_text="",
        placement="Bottom Right",
        opacity=180,
        font_size=42,
        image_placement_mode=FIT_ENTIRE_ARTWORK,
    ):
        if Image is None:
            raise RuntimeError("Pillow is required for image conversion. Install requirements first.")

        source_path = Path(source_path)
        export_type = EXPORT_ALIASES.get(export_type, export_type)
        target = EXPORT_TARGETS[export_type]
        output_format = output_format.upper()
        if output_format == "JPEG":
            output_format = "JPG"
        if output_format not in OUTPUT_FORMATS:
            raise ValueError(f"Unsupported output format: {output_format}")
        if image_placement_mode not in IMAGE_PLACEMENT_MODES:
            raise ValueError(f"Unsupported image placement mode: {image_placement_mode}")
        suffix = output_format.lower()

        EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
        output_path = EXPORTS_DIR / f"{source_path.stem}-{target['slug']}.{suffix}"

        with Image.open(source_path) as image:
            source_image = image.convert("RGBA")
            if image_placement_mode == FILL_PUZZLE_AREA:
                converted = self._fit_center_crop(source_image, target["pixels"])
            else:
                converted = self._fit_entire_image(source_image, target["pixels"])
            if copyright_text:
                converted = self._draw_copyright(converted, copyright_text, placement, opacity, font_size)
            if output_format == "DOCX":
                self._save_docx(output_path, converted, target, export_type)
                return output_path
            if output_format == "JPG":
                converted = converted.convert("RGB")
            save_format = "JPEG" if output_format == "JPG" else output_format
            converted.save(output_path, format=save_format, dpi=(DPI, DPI))
        return output_path

    def _fit_center_crop(self, image, target_size):
        target_w, target_h = target_size
        source_w, source_h = image.size
        scale = max(target_w / source_w, target_h / source_h)
        resized = image.resize((round(source_w * scale), round(source_h * scale)), Image.LANCZOS)
        left = (resized.width - target_w) // 2
        top = (resized.height - target_h) // 2
        return resized.crop((left, top, left + target_w, top + target_h))

    def _fit_entire_image(self, image, target_size):
        target_w, target_h = target_size
        source_w, source_h = image.size
        scale = min(target_w / source_w, target_h / source_h)
        resized = image.resize((round(source_w * scale), round(source_h * scale)), Image.LANCZOS)
        output = Image.new("RGBA", target_size, (255, 255, 255, 255))
        left = (target_w - resized.width) // 2
        top = (target_h - resized.height) // 2
        output.alpha_composite(resized, (left, top))
        return output

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

    def _save_docx(self, output_path, image, target, title):
        image_name = "preset-output.png"
        image_bytes_path = output_path.with_suffix(".docx-image.png")
        try:
            image.save(image_bytes_path, format="PNG", dpi=(DPI, DPI))
            image_bytes = image_bytes_path.read_bytes()
        finally:
            image_bytes_path.unlink(missing_ok=True)

        width_in, height_in = target["inches"]
        width_emu = round(width_in * EMU_PER_INCH)
        height_emu = round(height_in * EMU_PER_INCH)
        page_width = width_emu
        page_height = height_emu
        safe_title = html.escape(title)

        files = {
            "[Content_Types].xml": self._docx_content_types(),
            "_rels/.rels": self._docx_package_rels(),
            "word/document.xml": self._docx_document(safe_title, width_emu, height_emu, page_width, page_height),
            "word/_rels/document.xml.rels": self._docx_document_rels(image_name),
            f"word/media/{image_name}": image_bytes,
        }
        with ZipFile(output_path, "w", ZIP_DEFLATED) as docx:
            for name, content in files.items():
                docx.writestr(name, content)

    def _docx_content_types(self):
        return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Default Extension="png" ContentType="image/png"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
</Types>"""

    def _docx_package_rels(self):
        return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>"""

    def _docx_document_rels(self, image_name):
        return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/{image_name}"/>
</Relationships>"""

    def _docx_document(self, title, width_emu, height_emu, page_width, page_height):
        width_twips = round(page_width / 635)
        height_twips = round(page_height / 635)
        return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">
  <w:body>
    <w:p>
      <w:r>
        <w:drawing>
          <wp:inline distT="0" distB="0" distL="0" distR="0">
            <wp:extent cx="{width_emu}" cy="{height_emu}"/>
            <wp:docPr id="1" name="{title}"/>
            <a:graphic>
              <a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">
                <pic:pic>
                  <pic:nvPicPr>
                    <pic:cNvPr id="0" name="{title}"/>
                    <pic:cNvPicPr/>
                  </pic:nvPicPr>
                  <pic:blipFill>
                    <a:blip r:embed="rId1"/>
                    <a:stretch><a:fillRect/></a:stretch>
                  </pic:blipFill>
                  <pic:spPr>
                    <a:xfrm><a:off x="0" y="0"/><a:ext cx="{width_emu}" cy="{height_emu}"/></a:xfrm>
                    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
                  </pic:spPr>
                </pic:pic>
              </a:graphicData>
            </a:graphic>
          </wp:inline>
        </w:drawing>
      </w:r>
    </w:p>
    <w:sectPr>
      <w:pgSz w:w="{width_twips}" w:h="{height_twips}"/>
      <w:pgMar w:top="0" w:right="0" w:bottom="0" w:left="0" w:header="0" w:footer="0" w:gutter="0"/>
    </w:sectPr>
  </w:body>
</w:document>"""
