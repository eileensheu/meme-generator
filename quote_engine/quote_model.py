from pydantic import BaseModel


class QuoteModel(BaseModel):
    body: str
    author: str

    def __str__(self):
        """Return `str(self)`."""
        return f"\"{self.body}\" - {self.author}"
