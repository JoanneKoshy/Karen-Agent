import os
import io
import tempfile
from typing import Tuple

import pdfplumber
import docx


def extract_text_from_pdf(path: str) -> str:
    """Extract text from a PDF file using pdfplumber.

    Keeps page breaks as '\n\n' between pages.
    """
    texts = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                texts.append(page_text)
    return "\n\n".join(texts).strip()


def extract_text_from_docx(path: str) -> str:
    """Extract text from a .docx file using python-docx."""
    doc = docx.Document(path)
    paragraphs = [p.text for p in doc.paragraphs if p.text and p.text.strip()]
    return "\n\n".join(paragraphs).strip()


def extract_text_from_txt(path: str, encoding: str = "utf-8") -> str:
    """Read plain text files."""
    with open(path, "r", encoding=encoding, errors="ignore") as f:
        return f.read().strip()


def _identify_file_type(filename: str) -> str:
    """Return the lowercased extension (without dot)."""
    return os.path.splitext(filename)[1].lower().lstrip('.')


def parse_resume(file_path: str) -> str:
    """Parse a resume given a file path. Supports PDF, DOCX, TXT.

    Returns:
        Extracted plain text (UTF-8 string).

    Raises:
        ValueError: If file type unsupported or file not found.
    """
    if not os.path.exists(file_path):
        raise ValueError(f"File not found: {file_path}")

    ext = _identify_file_type(file_path)

    if ext == "pdf":
        text = extract_text_from_pdf(file_path)
    elif ext in ("docx", "doc"):
        # python-docx only handles .docx. For old .doc files, consider using textract or libreoffice conversion.
        if ext == "doc":
            raise ValueError(".doc (binary) files are not supported directly. Convert to .docx first.")
        text = extract_text_from_docx(file_path)
    elif ext in ("txt", "md"):
        text = extract_text_from_txt(file_path)
    else:
        raise ValueError(f"Unsupported resume file type: .{ext}")

    return _clean_text(text)


def parse_resume_bytes(file_bytes: bytes, filename: str) -> str:
    """Parse an uploaded file provided as bytes (e.g., from Streamlit upload).

    The function writes bytes to a temporary file and calls parse_resume.
    """
    suffix = os.path.splitext(filename)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(file_bytes)
        tmp_path = tmp.name

    try:
        return parse_resume(tmp_path)
    finally:
        try:
            os.remove(tmp_path)
        except Exception:
            pass


def _clean_text(text: str) -> str:
    """Lightweight cleaning: normalize whitespace and remove long runs of non-informative characters."""
    if not text:
        return ""

    # Normalize whitespace
    text = "\n".join(line.strip() for line in text.splitlines() if line.strip())

    # Remove multiple blank lines
    while "\n\n\n" in text:
        text = text.replace("\n\n\n", "\n\n")

    return text.strip()


if __name__ == "__main__":
    # Quick manual test/demo
    sample = "tests/sample_resume.pdf"
    if os.path.exists(sample):
        print("Parsed text (first 800 chars):\n")
        print(parse_resume(sample)[:800])
    else:
        print("No sample resume found. Drop a sample at tests/sample_resume.pdf to try the parser. not happening")
