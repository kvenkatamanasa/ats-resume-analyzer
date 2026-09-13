import os
import tempfile

import pymupdf
from docx import Document


ALLOWED_EXTENSIONS = {".pdf", ".docx"}

MAX_FILE_SIZE = 4 * 1024 * 1024


def validate_uploaded_file(uploaded_file):
    """
    Validate the uploaded resume before processing.
    """

    if not uploaded_file:
        raise ValueError("No resume file was uploaded.")

    filename = uploaded_file.name or ""

    extension = os.path.splitext(filename)[1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError(
            "Only PDF and DOCX files are supported."
        )

    if uploaded_file.size > MAX_FILE_SIZE:
        raise ValueError(
            "Resume file must be smaller than 4 MB."
        )

    return extension


def _save_to_temp(uploaded_file):
    """
    Save uploaded file temporarily.
    This is safe for Vercel because /tmp is temporary.
    """

    extension = validate_uploaded_file(uploaded_file)

    temp_path = None

    try:

        with tempfile.NamedTemporaryFile(
            mode="wb",
            suffix=extension,
            delete=False
        ) as temp_file:

            temp_path = temp_file.name

            for chunk in uploaded_file.chunks():
                temp_file.write(chunk)

        return temp_path, extension

    except Exception:

        if temp_path and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except OSError:
                pass

        raise


def extract_resume_text_from_upload(uploaded_file):
    """
    Extract text from PDF or DOCX.

    The original uploaded file is NOT permanently stored.
    """

    temp_path = None

    try:

        temp_path, extension = _save_to_temp(
            uploaded_file
        )

        # -------------------------
        # PDF
        # -------------------------

        if extension == ".pdf":

            document = pymupdf.open(temp_path)

            try:

                pages = []

                for page in document:
                    text = page.get_text()

                    if text:
                        pages.append(text)

                extracted_text = "\n".join(
                    pages
                ).strip()

            finally:

                document.close()

        # -------------------------
        # DOCX
        # -------------------------

        else:

            document = Document(temp_path)

            paragraphs = []

            for paragraph in document.paragraphs:

                text = paragraph.text.strip()

                if text:
                    paragraphs.append(text)

            extracted_text = "\n".join(
                paragraphs
            ).strip()

        # -------------------------
        # Validate extraction
        # -------------------------

        if not extracted_text:

            raise ValueError(
                "No readable text was found in the resume."
            )

        return extracted_text

    finally:

        if temp_path and os.path.exists(temp_path):

            try:
                os.remove(temp_path)

            except OSError:
                pass
