"""Provide one interface to load any supported file type.

'Ingestor' concrete class inherites from 'IngestorInterface' abstract class.
It is a strategy object that encapsulates all the ingestors, including
'TextIngestor', `DocxIngestor`, `PDFIngestor` and `CSVIngestor`.
 abstract class defines the interface for ingestors.
"""
from .ingestor_utils import IngestorInterface, TextIngestor, DocxIngestor, PDFIngestor, CSVIngestor
from .quote_model import QuoteModel
from typing import Iterable


class Ingestor(IngestorInterface):
    """Concrete ingestor class that can load any supported file type."""

    ingestors = [TextIngestor, DocxIngestor, PDFIngestor, CSVIngestor]
    # Implement class inheritance in Python using the strategy object design pattern
    # and apply DRY (don't repeat yourself) principles.
    # All ingestors are packaged into a main Ingestor class.
    # This class encapsulates all the ingestors to provide one interface to load any supported file type.

    @classmethod
    def parse(cls, path: str) -> Iterable[QuoteModel]:
        """Get a iterable of QuoteModel digested from the supplied file.

        :param path: A String path of the file that contains quotes.
        :return: A iterable of QuoteModel digested from the supplied file.
        """
        for ingestor in cls.ingestors:
            if ingestor.can_digest(path):
                return ingestor.parse(path)
        else:
            raise NotImplementedError