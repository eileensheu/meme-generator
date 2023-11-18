import abc
import os
import subprocess
import docx
import pandas as pd
import pathlib

from typing import Iterable
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
    def parse(cls, path: str) -> Iterable[QuoteModel]:
        """Get a iterable of QuoteModel digested from the supplied file

        Concrete subclasses must override this method to get the parsed
        QuoteModel digested from the supplied file.

        :param path: A String path of the file that contains quotes.
        :return: A iterable of QuoteModel digested from the supplied file
        """
        raise NotImplementedError


class TextIngestor(IngestorInterface):
    allowed_file_extensions = [".txt"]

    @classmethod
    def parse(cls, path: str) -> Iterable[QuoteModel]:
        if not cls.can_digest(path):
            raise Exception('Cannot ingest exception')

        with open(path, 'r') as f:
            return QuoteModel.from_linestr_iter_gen(f.readlines())


class DocxIngestor(IngestorInterface):
    allowed_file_extensions = [".docx"]

    # depends on the python-docx library to complete the defined, abstract method signatures to parse DOCX files.
    @classmethod
    def parse(cls, path: str) -> Iterable[QuoteModel]:
        if not cls.can_digest(path):
            raise Exception('Cannot ingest exception')

        doc = docx.Document(path)
        return QuoteModel.from_linestr_iter_gen([para.text for para in doc.paragraphs])


class PDFIngestor(IngestorInterface):
    # utilizes the subprocess module to call the pdftotext CLI utility, which
    # creates a pipeline that converts PDFs to text and then ingests the text.
    # The class handles deleting temporary files.
    allowed_file_extensions = [".pdf"]

    @classmethod
    def parse(cls, path: str) -> Iterable[QuoteModel]:
        if not cls.can_digest(path):
            raise Exception('Cannot ingest exception')

        tmp_txt_path = "_tmp_pdf_content.txt"
        cmd = ['pdftotext', path, tmp_txt_path]
        process = subprocess.run(cmd)
        if process.returncode != 0:
            raise RuntimeError(f"Conversion of {path} from .pdf to .txt has failed.")

        try:
            with open(tmp_txt_path, 'r') as f:
                return QuoteModel.from_linestr_iter_gen(f.readlines())
        finally:
            os.remove(tmp_txt_path)


class CSVIngestor(IngestorInterface):
    # depends on the pandas library to complete the defined, abstract method signatures to parse CSV files
    allowed_file_extensions = [".csv"]

    @classmethod
    def parse(cls, path: str) -> Iterable[QuoteModel]:
        if not cls.can_digest(path):
            raise Exception('Cannot ingest exception')

        data = pd.read_csv(path, header=0).to_dict('split').get('data')
        if data:
            return [QuoteModel(body=quote[0], author=quote[1]) for quote in data]
        else:
            raise Exception('Failed to read csv with python \"panda\" library.')
