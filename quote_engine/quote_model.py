from __future__ import annotations
from typing import Iterable


class QuoteModel:
    body: str
    author: str

    def __init__(self, body: str, author: str) -> None:
        self.body = body
        self.author = author

    def __str__(self):
        """Return `str(self)`."""
        return f"\"{self.body}\" - {self.author}"

    @classmethod
    def from_linestr_iter_gen(cls, iterable: Iterable[str]) -> Iterable[QuoteModel]:
        for linestring in iterable:
            line_clean = linestring.strip().replace("\"", "")
            if line_clean:
                body, author = line_clean.split(" - ")
                yield cls(body=body, author=author)
            else:
                return
