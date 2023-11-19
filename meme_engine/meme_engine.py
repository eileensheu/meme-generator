import os
import random
from typing import Optional, Tuple
from PIL import Image, ImageDraw, ImageFont

MAX_IMAGE_WIDTH_PX = 500
BODY_AUTHOR_ROW_SHIFT = (20, 30)


class TextOnImage:
    text: str
    image: Image.Image
    _image_draw: ImageDraw.ImageDraw
    font: str
    font_size: int
    _image_font: ImageFont.FreeTypeFont
    coord: Tuple[int, int]
    fill: Tuple[int, int, int]

    def __init__(
            self,
            text: str,
            image: Image.Image,
            font: str = "FreeMonoBold.ttf",
            font_size: int = 16,
            coord: Optional[Tuple[int, int]] = None,
            fill: Optional[Tuple[int, int, int]] = None,
        ) -> None:
        self.text = text
        self.image = image
        self._image_draw = ImageDraw.Draw(image)
        self.font = font
        self.font_size = font_size
        self._image_font = ImageFont.truetype(font, font_size)
        self.coord = coord if coord else self._decide_coord(image.size)
        self.fill = fill if fill else (0, 0, 0)

    def _decide_coord(self, image_size: Tuple[int, int]):
        text_length = self._image_draw.textlength(self.text, self._image_font, features=["-kern"])
        max_col_id = image_size[0] - int(text_length)
        max_row_id = image_size[1] - self.font_size - BODY_AUTHOR_ROW_SHIFT[1]
        return (random.randint(0, max_col_id), random.randint(0, max_row_id))
        # return (max_col_id, max_row_id)

    def draw_on_image(self):
        self._image_draw.text(
            xy=self.coord,
            text=self.text,
            font=self._image_font,
            fill=self.fill,
            stroke_width=1,
            stroke_fill=(255,255,255),
        )


class MemeEngine:
    output_image_path: str

    def __init__(self, output_dir) -> None:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        self.output_image_path = str(os.path.join(output_dir, "output.jpg"))

    def make_meme(self, image_path: str, quote_body: str, quote_author: str, width_px: int = MAX_IMAGE_WIDTH_PX) -> str:
        img = Image.open(image_path)
        _resize_image_with_aspect_ratio_maintained(img, width_px)
        _add_quote_in_image(img, quote_body, quote_author)
        img.save(self.output_image_path)

        return self.output_image_path


def _resize_image_with_aspect_ratio_maintained(image: Image.Image, max_width_px: int) -> None:
    w_percent = (max_width_px / float(image.size[0]))
    h_px = int((float(image.size[1]) * float(w_percent)))
    image.thumbnail((max_width_px, h_px), Image.Resampling.LANCZOS)


def _add_quote_in_image(image: Image.Image, quote_body: str, quote_author: str) -> None:
    body_text = TextOnImage(
        text=f"\"{quote_body}\"",
        image=image,
        font="Waree-Bold.ttf",
        font_size=20,
        fill=(0, 80, 0),
    )
    author_text = TextOnImage(
        text=f"- {quote_author}",
        image=image,
        font="FreeMonoBold.ttf",
        font_size=16,
        coord=tuple(map(sum, zip(body_text.coord, BODY_AUTHOR_ROW_SHIFT))),
        fill=(0, 0, 0),
    )
    body_text.draw_on_image()
    author_text.draw_on_image()
