"""Provide utilities to draw a quote on an image.

'TextOnImage' base class could be use to draw a string with a desired font.

Four concrete classes that realize the 'IngestorInterface' abstract class including:
'TextIngestor', `DocxIngestor`, `PDFIngestor` and `CSVIngestor`.
"""
import random
import textwrap
from typing import List, Optional, Tuple

from PIL import ImageDraw, ImageFont

BODY_AUTHOR_SHIFT = (0, 0)


class TextOnImage:
    """Base class that helps to draw text on an image."""

    _text: str
    _image_draw: ImageDraw.ImageDraw
    _image_font: ImageFont.FreeTypeFont
    _font_size: int
    _textlength: int
    _fill: Tuple[int, int, int]
    _multiline_text: List[str]
    _multiline_textwidth: int
    _multiline_textheight: int
    _multiline_spacing: int

    def __init__(
            self,
            text: str,
            image_draw: ImageDraw.ImageDraw,
            font: str = "FreeMonoBold.ttf",
            font_size: int = 16,
            fill: Optional[Tuple[int, int, int]] = None,
        ) -> None:
        """Construct a new `TextOnImage` that could be passed to `QuoteOnImage` class as `body` or `author` argument.

        :param text: A string of text, can be quote body or quote author.
        :param image_draw: A ImageDraw.ImageDraw instance.
        :param font: A string of font that is avaiable on the system.
        :param font_size: An integer of font size.
        :param fill: A tuple of three integers within the range 0~255, representing the RGB values that the text should be colored.
        """
        self._text = text
        self._image_draw = image_draw
        self._image_font = ImageFont.truetype(font, font_size)
        self._font_size = font_size
        self._textlength = int(self._image_draw.textlength(self._text, self._image_font, features=["-kern"]))
        self._fill = fill if fill else (0, 0, 0)

    @property
    def textlength(self) -> int:
        """Get single-line text length in pixels."""
        return self._textlength

    @property
    def multiline_textwidth(self) -> int:
        """Get multi-line text length in pixels."""
        return self._multiline_textwidth

    @property
    def multiline_textheight(self) -> int:
        """Get multi-line text height in pixels."""
        return self._multiline_textheight

    def set_multiline_text_attributes(self, max_textlength: int) -> None:
        """Set the attributes for multi-line text.

        :param max_textlength: An integer of maximum text-length in pixels.
        """
        max_char = int(max_textlength / self._font_size * 1.5)
        self._multiline_text = textwrap.wrap(self._text, width=max_char)
        self._multiline_textwidth = int(self._image_draw.textlength(self._multiline_text[0], self._image_font, features=["-kern"]))
        self._multiline_textheight = self._font_size * len(self._multiline_text)
        self._multiline_spacing = int(self._font_size / 5)

    def draw_on_image(self, anchor_coord: Tuple[int, int]) -> None:
        """Draw the text on the image.

        :param anchor_coord: A tuple of two integers representing the coordinate on the image
        """
        _coord = anchor_coord
        _offset = (0, self._font_size)
        for line in self._multiline_text:
            self._image_draw.multiline_text(
                xy=_coord,
                text=line,
                font=self._image_font,
                fill=self._fill,
                stroke_width=1,
                stroke_fill=(255,255,255),
                spacing=self._multiline_spacing,
            )
            _coord = tuple(map(sum, zip(_coord, _offset)))


class QuoteOnImage:
    """Base class that helps to draw a quote with its author on an image."""

    _body: TextOnImage
    _author: TextOnImage
    _image_size: Tuple[int, int]

    def __init__(self, body: TextOnImage, author: TextOnImage, image_size: Tuple[int, int]) -> None:
        """Construct a new `QuoteOnImage` instance that has a `draw()` method to draw a quote with its author on an image.

        :param body: A TextOnImage instance of quote body
        :param author: A TextOnImage instance of quote author
        :param image_size: A tuple of two integers (width, height) representing the size of the image in pixels.
        """
        self._body = body
        self._author = author
        self._image_size = image_size

    def draw(self) -> None:
        """Draw the quote with its author on the image."""
        max_textlength = self._compute_max_textlength()
        self._body.set_multiline_text_attributes(max_textlength)
        self._author.set_multiline_text_attributes(max_textlength)

        quote_bbox = self._compute_quote_bbox()
        quote_bbox_coord = self._pick_random_bbox_coord(quote_bbox)

        self._draw_quote_on_image(quote_bbox_coord)

    def _compute_max_textlength(self) -> int:
        if max(self._body.textlength, self._author.textlength) >= self._image_size[0]:
            max_textlength = int(self._image_size[0] / 1.5)
        else:
            max_textlength = self._image_size[0]
        return max_textlength

    def _compute_quote_bbox(self) -> Tuple[int, int]:
        bbox_width = max(self._body.multiline_textwidth, self._author.multiline_textwidth + BODY_AUTHOR_SHIFT[0])
        bbox_height = self._body.multiline_textheight + self._author.multiline_textheight + BODY_AUTHOR_SHIFT[1]
        return (bbox_width, bbox_height)

    def _pick_random_bbox_coord(self, quote_bbox: Tuple[int, int]) -> Tuple[int, int]:
        max_col_id = self._image_size[0] - quote_bbox[0]
        max_row_id = self._image_size[1] - quote_bbox[1]
        return (random.randint(0, max_col_id), random.randint(0, max_row_id))

    def _draw_quote_on_image(self, quote_bbox_coord: Tuple[int, int]) -> None:
        body_coord = quote_bbox_coord
        author_coord = tuple(map(sum, zip(quote_bbox_coord, (0, self._body.multiline_textheight), BODY_AUTHOR_SHIFT)))
        self._body.draw_on_image(body_coord)
        self._author.draw_on_image(author_coord)
