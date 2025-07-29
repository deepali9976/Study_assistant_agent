from typing import List
from phi.tools import Toolkit
from phi.utils.log import logger
import fitz  # PyMuPDF

class PDFReaderToolkit(Toolkit):
    def __init__(self):
        super().__init__(name="pdf_reader_tools")
        self.register(self.read_pdf)

    def read_pdf(self, path: str, max_chars: int = 2000) -> str:
        """
        Reads and returns text from a PDF file.

        Args:
            path (str): The file path to the PDF document.
            max_chars (int): Limit the number of characters returned (for token control).

        Returns:
            str: Extracted text from the PDF.
        """
        logger.info(f"Reading PDF: {path}")
        text = ""
        try:
            doc = fitz.open(path)
            for page in doc:
                text += page.get_text()
            doc.close()
        except Exception as e:
            logger.warning(f"Failed to read PDF: {e}")
            return f"Error reading PDF: {e}"

        return text[:max_chars] + ("..." if len(text) > max_chars else "")
