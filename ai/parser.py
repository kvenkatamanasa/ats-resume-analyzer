import os
import tempfile

import pymupdf
from docx import Document


# ============================================================
# PDF TEXT EXTRACTION
# ============================================================

def extract_text_from_pdf(file_path):
    """
    Extract text from a PDF using a filesystem path.

    Works on Windows and Linux/Vercel.
    """

    file_path = os.fspath(file_path)

    document = pymupdf.open(file_path)

    try:
        text_parts = []

        for page in document:
            page_text = page.get_text()

            if page_text:
                text_parts.append(page_text)

        return "\n".join(text_parts).strip()

    finally:
        document.close()


# ============================================================
# DOCX TEXT EXTRACTION
# ============================================================

def extract_text_from_docx(file_path):
    """
    Extract text from a DOCX using a filesystem path.
    """

    file_path = os.fspath(file_path)

    document = Document(file_path)

    paragraphs = []

    for paragraph in document.paragraphs:
        content = paragraph.text.strip()

        if content:
            paragraphs.append(content)

    return "\n".join(paragraphs).strip()


# ============================================================
# SAVE DJANGO UPLOADED FILE TO TEMPORARY STORAGE
# ============================================================

def _save_upload_to_temp(uploaded_file):
    """
    Save a Django UploadedFile to a temporary file.

    IMPORTANT:
    Do not hard-code /tmp.

    tempfile automatically chooses the correct temporary
    directory for the operating system.

    Windows:
        C:\\Users\\...\\AppData\\Local\\Temp\\...

    Linux/Vercel:
        /tmp/...
    """

    if not uploaded_file:
        raise ValueError("No file was uploaded.")

    original_name = uploaded_file.name or "resume"

    # Get the uploaded file extension
    suffix = os.path.splitext(original_name)[1].lower()

    # Only allow supported formats
    if suffix not in (".pdf", ".docx"):
        raise ValueError(
            "Only PDF and DOCX files are supported."
        )

    # Let Python automatically choose the correct
    # temporary directory for Windows/Linux.
    temp_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=suffix,
    )

    temp_path = temp_file.name

    try:
        # Django UploadedFile provides chunks()
        for chunk in uploaded_file.chunks():
            temp_file.write(chunk)

        temp_file.flush()

    except Exception:
        # Close the file before deleting it
        temp_file.close()

        try:
            os.remove(temp_path)
        except OSError:
            pass

        raise

    finally:
        temp_file.close()

    return temp_path


# ============================================================
# PDF UPLOADED FILE EXTRACTION
# ============================================================

def extract_text_from_pdf_file(uploaded_file):
    """
    Extract text from a Django UploadedFile containing a PDF.

    The uploaded file is temporarily stored, processed,
    and deleted afterwards.
    """

    temp_path = _save_upload_to_temp(uploaded_file)

    try:
        return extract_text_from_pdf(temp_path)

    finally:
        try:
            if os.path.exists(temp_path):
                os.remove(temp_path)
        except OSError:
            pass


# ============================================================
# DOCX UPLOADED FILE EXTRACTION
# ============================================================

def extract_text_from_docx_file(uploaded_file):
    """
    Extract text from a Django UploadedFile containing DOCX.

    The uploaded file is temporarily stored, processed,
    and deleted afterwards.
    """

    temp_path = _save_upload_to_temp(uploaded_file)

    try:
        return extract_text_from_docx(temp_path)

    finally:
        try:
            if os.path.exists(temp_path):
                os.remove(temp_path)
        except OSError:
            pass


# ============================================================
# MAIN UPLOADED RESUME EXTRACTION FUNCTION
# ============================================================

def extract_resume_text_from_upload(uploaded_file):
    """
    Extract text from a Django UploadedFile.

    Supported:
        PDF
        DOCX
    """

    if not uploaded_file:
        raise ValueError(
            "No resume file was uploaded."
        )

    filename = (
        uploaded_file.name or ""
    ).lower()

    # PDF
    if filename.endswith(".pdf"):
        return extract_text_from_pdf_file(
            uploaded_file
        )

    # DOCX
    if filename.endswith(".docx"):
        return extract_text_from_docx_file(
            uploaded_file
        )

    # Unsupported format
    raise ValueError(
        "Unsupported file format. "
        "Please upload a PDF or DOCX file."
    )


# ============================================================
# PATH-BASED EXTRACTION
# ============================================================

def extract_resume_text(file_path):
    """
    Extract resume text from an existing filesystem path.

    Kept for compatibility with other parts of the project.
    """

    if not file_path:
        raise ValueError(
            "No resume file path was provided."
        )

    file_path = os.fspath(file_path)

    lower_path = file_path.lower()

    # PDF
    if lower_path.endswith(".pdf"):
        return extract_text_from_pdf(
            file_path
        )

    # DOCX
    if lower_path.endswith(".docx"):
        return extract_text_from_docx(
            file_path
        )

    raise ValueError(
        "Unsupported file format. "
        "Please upload a PDF or DOCX file."
    )
