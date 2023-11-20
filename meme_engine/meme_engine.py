import os
import random
import textwrap
from typing import List, Optional, Tuple
from PIL import Image, ImageDraw, ImageFont

MAX_IMAGE_WIDTH_PX = 500
BODY_AUTHOR_SHIFT = (0, 0)


class TextOnImage:
    text: str
    image_draw: ImageDraw.ImageDraw
    image_font: ImageFont.FreeTypeFont
    font_size: int
    textlength: int
    fill: Tuple[int, int, int]
    multiline_text: List[str]
    multiline_textwidth: int
    multiline_textheight: int
    multiline_spacing: int

    def __init__(
            self,
            text: str,
            image_draw: ImageDraw.ImageDraw,
            font: str = "FreeMonoBold.ttf",
            font_size: int = 16,
            fill: Optional[Tuple[int, int, int]] = None,
        ) -> None:
        self.text = text
        self.image_draw = image_draw
        self.image_font = ImageFont.truetype(font, font_size)
        self.font_size = font_size
        self.textlength = int(self.image_draw.textlength(self.text, self.image_font, features=["-kern"]))
        self.fill = fill if fill else (0, 0, 0)

    def set_multiline_text(self, max_textlength):
        max_char = int(max_textlength / self.font_size * 1.5)
        self.multiline_text = textwrap.wrap(self.text, width=max_char)
        self.multiline_textwidth = int(self.image_draw.textlength(self.multiline_text[0], self.image_font, features=["-kern"]))
        self.multiline_textheight = self.font_size * len(self.multiline_text)
        self.multiline_spacing = int(self.font_size / 5)

    def draw_on_image(self, anchor_coord:Tuple[int, int]):
        _coord = anchor_coord
        _offset = (0, self.font_size)
        for line in self.multiline_text:
            self.image_draw.multiline_text(
                xy=_coord,
                text=line,
                font=self.image_font,
                fill=self.fill,
                stroke_width=1,
                stroke_fill=(255,255,255),
                spacing=self.multiline_spacing,
            )
            _coord = tuple(map(sum, zip(_coord, _offset)))

class DrawQuoteOnImage:
    body: TextOnImage
    author: TextOnImage
    max_textlength: int
    quote_bbox: Tuple[int, int]
    quote_bbox_coord: Tuple[int, int]

    def __init__(self, body: TextOnImage, author: TextOnImage, image_size: Tuple[int, int]) -> None:
        self.body = body
        self.author = author
        self.max_textlength = self._compute_max_textlength(image_size)
        self._create_multiline_text()
        self.quote_bbox = self._compute_quote_bbox()
        self.quote_bbox_coord = self._pick_random_bbox_coord(image_size)
        self._draw_quote_on_image()

    def _compute_max_textlength(self, image_size: Tuple[int, int]) -> int:
        if max(self.body.textlength, self.author.textlength) >= image_size[0]:
            max_textlength = int(image_size[0] / 1.5)
        else:
            max_textlength = image_size[0]
        return max_textlength

    def _create_multiline_text(self) -> None:
        self.body.set_multiline_text(self.max_textlength)
        self.author.set_multiline_text(self.max_textlength)

    def _compute_quote_bbox(self) -> Tuple[int, int]:
        bbox_width = max(self.body.multiline_textwidth, self.author.multiline_textwidth + BODY_AUTHOR_SHIFT[0])
        bbox_height = self.body.multiline_textheight + self.author.multiline_textheight + BODY_AUTHOR_SHIFT[1]
        return (bbox_width, bbox_height)

    def _pick_random_bbox_coord(self, image_size: Tuple[int, int]) -> Tuple[int, int]:
        max_col_id = image_size[0] - self.quote_bbox[0]
        max_row_id = image_size[1] - self.quote_bbox[1]
        return (random.randint(0, max_col_id), random.randint(0, max_row_id))

    def _draw_quote_on_image(self) -> None:
        self.body.draw_on_image(self.quote_bbox_coord)
        self.author.draw_on_image(tuple(map(sum, zip(self.quote_bbox_coord, (0, self.body.multiline_textheight), BODY_AUTHOR_SHIFT))))


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
    image_draw = ImageDraw.Draw(image)
    body_text_basic = TextOnImage(
        text=f"\"{quote_body}\"",
        image_draw=image_draw,
        font="LiberationMono-Bold.ttf",
        font_size=20,
        fill=(0, 80, 0),
    )
    author_text_basic = TextOnImage(
        text=f"- {quote_author}",
        image_draw=image_draw,
        font="FreeMonoBold.ttf",
        font_size=16,
        fill=(0, 0, 0),
    )
    DrawQuoteOnImage(body=body_text_basic, author=author_text_basic, image_size=image.size)
