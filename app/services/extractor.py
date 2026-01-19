import pytesseract
from PIL import Image
import pdfplumber
from pathlib import Path

def extract_text_from_pdf(file_path: Path) -> str:
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def extract_text_from_image(file_path: str) -> str:
    image = Image.open(file_path)
    text = pytesseract.image_to_string(image)
    return text

def extract_text(file_path: Path) -> str:
    path = Path(file_path)

    if path.suffix.lower() == ".pdf":
        return extract_text_from_pdf(file_path)
    elif path.suffix.lower() in [".jpg", ".jpeg", ".png"]:
        return extract_text_from_image(str(file_path))
    else:
        raise ValueError(f"Unsupported file type: {path.suffix}")
    
    