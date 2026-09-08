import pymupdf
from docx import Document


def extract_text_from_pdf(file_path):
    """
    Extract text from a PDF resume using PyMuPDF.
    """

    text = ""

    document = pymupdf.open(file_path)

    try:
        for page in document:
            text += page.get_text()
    finally:
        document.close()

    return text.strip()


def extract_text_from_docx(file_path):
    """
    Extract text from a DOCX resume.
    """

    document = Document(file_path)

    paragraphs = []

    for paragraph in document.paragraphs:
        content = paragraph.text.strip()

        if content:
            paragraphs.append(content)

    return "\n".join(paragraphs)


def extract_resume_text(file_path):
    """
    Detect the file extension and extract
    readable text from the resume.
    """

    file_path = str(file_path).lower()

    if file_path.endswith(".pdf"):
        return extract_text_from_pdf(file_path)

    if file_path.endswith(".docx"):
        return extract_text_from_docx(file_path)

    raise ValueError(
        "Unsupported file format. "
        "Please upload a PDF or DOCX file."
    )