
import fitz
from docx import Document
from pathlib import Path


# ----------------------------------
# 1. Extract Text From PDF
# ----------------------------------

def extract_text_from_pdf(file_path):

    text = ""

    try:
        pdf_document = fitz.open(file_path)

        for page in pdf_document:
            text += page.get_text()

        pdf_document.close()

        return text.strip()

    except Exception as error:
        raise ValueError(f"PDF reading error: {error}")


# ----------------------------------
# 2. Extract Text From DOCX
# ----------------------------------

def extract_text_from_docx(file_path):

    text = ""

    try:
        document = Document(file_path)

        # Extract paragraphs
        for paragraph in document.paragraphs:
            text += paragraph.text + "\n"

        # Extract table content
        for table in document.tables:
            for row in table.rows:
                for cell in row.cells:
                    text += cell.text + " "

        return text.strip()

    except Exception as error:
        raise ValueError(f"DOCX reading error: {error}")


# ----------------------------------
# 3. Main Resume Parser
# ----------------------------------

def parse_resume(file_path):

    file_path = Path(file_path)

    extension = file_path.suffix.lower()

    if extension == ".pdf":
        extracted_text = extract_text_from_pdf(file_path)

    elif extension == ".docx":
        extracted_text = extract_text_from_docx(file_path)

    else:
        raise ValueError(
            "Unsupported file format. Please upload PDF or DOCX."
        )

    if not extracted_text:
        raise ValueError(
            "No text found. The resume may be scanned or image-based."
        )

    return extracted_text
