"""Provide meme engine that makes meme."""
import os
from PIL import Image, ImageDraw
from .draw_quote_utils import TextOnImage, QuoteOnImage

MAX_IMAGE_WIDTH_PX = 500


class MemeEngine:
    """Base class that creates memes."""

    output_image_path: str

    def __init__(self, output_dir) -> None:
        """Construct a new `MemeEngine` that would write output images to the specified directory.

        :param output_dir: A string of output directory path
        """
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        self.output_image_path = str(os.path.join(output_dir, "output.jpg"))

    def make_meme(
            self,
            image_path: str,
            quote_body: str,
            quote_author: str,
            width_px: int = MAX_IMAGE_WIDTH_PX
        ) -> str:
        """Create a meme image with the supplied quote and return the output file path.

        :param image_path: A String path of the supplied image file.
        :param quote_body: A String of quote body.
        :param quote_author: A String of quote author.
        :param width_px: A integer of image width in pixels that the image should be resized to. Defaults to `MAX_IMAGE_WIDTH_PX`.
        :return: A String path of the produced meme image file with a quote caption.
        """
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
    quote_on_image = QuoteOnImage(
        body=TextOnImage(
            text=f"\"{quote_body}\"",
            image_draw=image_draw,
            font="LiberationMono-Bold",
            font_size=20,
            fill=(0, 80, 0),
        ),
        author=TextOnImage(
            text=f"- {quote_author}",
            image_draw=image_draw,
            font="FreeMonoBold",
            font_size=16,
            fill=(0, 0, 0),
        ),
        image_size=image.size,
    )
    quote_on_image.draw()
