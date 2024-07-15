import platform
from tempfile import TemporaryDirectory
from pathlib import Path
import hashlib
import pytesseract
from pdf2image import convert_from_path
from PIL import Image

if platform.system() == "Windows":
    # Windows needs to download tesseract from https://github.com/UB-Mannheim/tesseract/wiki/Downloading-Tesseract-OCR-Engine and set the path to the tesseract.exe file
    pytesseract.pytesseract.tesseract_cmd = (
        r"S:\tessertact\tesseract.exe"
    )
    # Windows also needs poppler_exe
    path_to_poppler_exe = Path(r"S:\poppler-24.02.0\Library\bin")

def pdf2text(pdf_path: str):
    image_file_list = []
    pdf_file = Path(pdf_path)
    with TemporaryDirectory() as tempdir:
        if platform.system() == "Windows":
            pdf_pages = convert_from_path(pdf_file, 500, poppler_path=path_to_poppler_exe)
        else:
            pdf_pages = convert_from_path(pdf_file, 500)

        # Iterate through all the pages stored above, enumerate() counts the pages.
        for page_enumeration, page in enumerate(pdf_pages, start=1):
            filename = f"{tempdir}\\page_{page_enumeration:03}.png"
            page.save(filename, "PNG")
            image_file_list.append(filename)

        res = ""
        for image_file in image_file_list:
            text = str(((pytesseract.image_to_string(Image.open(image_file), lang="chi_sim"))))
            text = text.replace("-\n", "")
            res += text

    return res

def img2text(img_path: str):
    img_file = Path(img_path)
    text = str(((pytesseract.image_to_string(Image.open(img_file), lang="chi_sim"))))
    return text

def is_img(file_path: str):
    return file_path.endswith(".png") or file_path.endswith(".jpg") or file_path.endswith(".jpeg") or file_path.endswith(".webp")

def convert2text(file_path: str):
    file_path = str(file_path)
    if file_path.endswith(".pdf"):
        return pdf2text(file_path)
    elif is_img(file_path):
        return img2text(file_path)
    else:
        return None

def md5_filename(filename: str) -> str:
    md5_hash = hashlib.md5(filename.encode()).hexdigest()
    ext = Path(filename).suffix
    return f"{md5_hash}{ext}"

if __name__ == "__main__":
    print(pdf2text(r"D:\Code\py_summer\Problem-E.pdf"))