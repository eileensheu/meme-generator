import argparse
import os
import random
import sys
from typing import List

from quote_engine.quote_model import QuoteModel
from quote_engine.ingestor import Ingestor
from meme_engine.meme_engine import MemeEngine

def generate_meme(path=None, body=None, author=None):
    """ Generate a meme given an path and a quote """
    img = None
    quote = None

    if path is None:
        images = "./_data/photos/dog/"
        imgs = []
        for root, dirs, files in os.walk(images):
            imgs = [os.path.join(root, name) for name in files]

        img = random.choice(imgs)
    else:
        img = path

    if body is None:
        quote_files = ['./_data/DogQuotes/DogQuotesTXT.txt',
                       './_data/DogQuotes/DogQuotesDOCX.docx',
                       './_data/DogQuotes/DogQuotesPDF.pdf',
                       './_data/DogQuotes/DogQuotesCSV.csv']
        quotes = []
        for f in quote_files:
            quotes.extend(Ingestor.parse(f))

        quote = random.choice(quotes)
    else:
        if author is None:
            raise Exception('Author Required if Body is Used')
        quote = QuoteModel(body, author)

    meme = MemeEngine('./tmp')
    path = meme.make_meme(img, quote.body, quote.author)
    return path


def parse_args(argv: List[str] = sys.argv[1:]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--path",
        type=str,
        required=False,
        help="Path to an image file",
    )

    parser.add_argument(
        "--body",
        type=str,
        required=False,
        help="Quote body to add to the image",
    )

    parser.add_argument(
        "--author",
        type=str,
        required=False,
        help="Quote author to add to the image",
    )
    return parser.parse_args(argv)


if __name__ == "__main__":
    args = parse_args()
    print("Generated meme image locates at: " + generate_meme(args.path, args.body, args.author))
