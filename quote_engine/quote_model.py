"""Provide Quote Model object that contains `body` and `author` properties."""
from __future__ import annotations
from typing import Iterable


class QuoteModel:
    """A base class to handle a quote.

    This class contains `body` and `author` properties,
    and has a method that returns an Iterable of `QuoteModel` instances from an Iterable of strings.
    """

    body: str
    author: str

    def __init__(self, body: str, author: str) -> None:
        """Construct a new `QuoteModel` from quote body and quote author information.

        :param body: A string of the quote body
        :param author: A string of the quote author
        """
        self.body = body
        self.author = author

    def __str__(self):
        """Return `str(self)`."""
        return f"\"{self.body}\" - {self.author}"

    @classmethod
    def from_linestr_iter_gen(cls, iterable: Iterable[str]) -> Iterable[QuoteModel]:
        """Return an Iterable of `QuoteModel` instances.

        :param iterable: A String Iterable that contains a quote and its author joint by " - ".
        :return: A iterable of `QuoteModel` instances.
        """
        for linestring in iterable:
            line_clean = linestring.strip().replace("\"", "")
            if line_clean:
                body, author = line_clean.split(" - ")
                yield cls(body=body, author=author)
            else:
                return
