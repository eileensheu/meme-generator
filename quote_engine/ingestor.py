from .ingestor_utils import IngestorInterface, TextIngestor, DocxIngestor, PDFIngestor, CSVIngestor
from .quote_model import QuoteModel
from typing import Iterable


class Ingestor(IngestorInterface):
    ingestors = [TextIngestor, DocxIngestor, PDFIngestor, CSVIngestor]
    # Implement class inheritance in Python using the strategy object design pattern
    # and apply DRY (don't repeat yourself) principles.
    # All ingestors are packaged into a main Ingestor class.
    # This class encapsulates all the ingestors to provide one interface to load any supported file type.

    @classmethod
    def parse(cls, path: str) -> Iterable[QuoteModel]:
        for ingestor in cls.ingestors:
            if ingestor.can_digest(path):
                return ingestor.parse(path)
        else:
            raise NotImplementedError