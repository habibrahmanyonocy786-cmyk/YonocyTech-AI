import pandas as pd
from pypdf import PdfReader
from docx import Document
import openpyxl
from typing import Optional

class FileProcessor:
    """
    Provides utility methods to process various file formats.
    """
    @staticmethod
    def read_pdf(filepath: str) -> Optional[str]:
        try:
            reader = PdfReader(filepath)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text.strip()
        except Exception as e:
            return f"PDF Error: {e}"

    @staticmethod
    def read_docx(filepath: str) -> Optional[str]:
        try:
            doc = Document(filepath)
            return "\n".join([para.text for para in doc.paragraphs])
        except Exception as e:
            return f"DOCX Error: {e}"

    @staticmethod
    def read_excel(filepath: str) -> Optional[str]:
        try:
            df = pd.read_excel(filepath)
            return df.to_string()
        except Exception as e:
            return f"Excel Error: {e}"

    @staticmethod
    def read_csv(filepath: str) -> Optional[str]:
        try:
            df = pd.read_csv(filepath)
            return df.to_string()
        except Exception as e:
            return f"CSV Error: {e}"

    @staticmethod
    def read_text(filepath: str) -> Optional[str]:
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            return f"Text Error: {e}"

    @classmethod
    def auto_read(cls, filepath: str) -> Optional[str]:
        """
        Detects file type by extension and uses the appropriate reader.
        """
        ext = filepath.split('.')[-1].lower()
        if ext == 'pdf': return cls.read_pdf(filepath)
        if ext == 'docx': return cls.read_docx(filepath)
        if ext in ['xlsx', 'xls']: return cls.read_excel(filepath)
        if ext == 'csv': return cls.read_csv(filepath)
        return cls.read_text(filepath)
