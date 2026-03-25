from pypdf import PdfReader

def read_pdf(path: str) -> str:
    """Lire un PDF et retourner son texte"""
    reader = PdfReader(path)
    text = ""

    for page in reader.pages:
        text += page.extract_text()

    return text