import abc
import pathlib
from typing import List
from quote_model import QuoteModel


class IngestorInterface(abc.ABC):
    allowed_file_extensions = []  # class attribute, which can be redefined by children classes.

    # Hint: Classmethods can access class attribute
    @classmethod
    def can_digest(cls, path: str) -> bool:
        """Check if the supplied file can be digested or not

        :param path: A String path of the file that contains quotes.
        :return: A boolean result whether the supplied 'path' file can be digested or not.
        """
        file_extension = pathlib.Path(path).suffix
        return file_extension in cls.allowed_file_extensions

    @classmethod
    @abc.abstractmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Get a list of QuoteModel digested from the supplied file

        Concrete subclasses must override this method to get the parsed
        QuoteModel digested from the supplied file.

        :param path: A String path of the file that contains quotes.
        :return: A list of QuoteModel digested from the supplied file
        """
        raise NotImplementedError


class TextIngestor(IngestorInterface):
    allowed_file_extensions = [".txt"]

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        if not cls.can_digest(path):
            raise Exception('Cannot ingest exception')
        quotemodel_list = []
        with open(path, 'r') as f:
            for line in f.readlines():
                line_clean = line.strip().replace("\"", "")
                if line_clean:
                    body, author = line_clean.split(" - ")
                    quotemodel_list.append(QuoteModel(body=body, author=author))
        return quotemodel_list


class DocxIngestor(IngestorInterface):
    allowed_file_extensions = [".docx"]

    # depends on the python-docx library to complete the defined, abstract method signatures to parse DOCX files.
    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        return []


class PDFIngestor(IngestorInterface):
    # utilizes the subprocess module to call the pdftotext CLI utility, which
    # creates a pipeline that converts PDFs to text and then ingests the text.
    # The class handles deleting temporary files.
    allowed_file_extensions = [".pdf"]

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        return []


class CSVIngestor(IngestorInterface):
    # depends on the pandas library to complete the defined, abstract method signatures to parse CSV files
    allowed_file_extensions = [".csv"]

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        return []

