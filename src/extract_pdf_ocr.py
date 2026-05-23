from pathlib import Path
import re
import pandas as pd
import pytesseract
from pdf2image import convert_from_path

# Tesseract 설치 경로
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

BASE_DIR = Path(__file__).resolve().parents[1]

PDF_DIR = BASE_DIR / "data" / "raw_pdf"
# PDF_DIR = BASE_DIR / "data" / "raw_pdf_test"
OUTPUT_PATH = BASE_DIR / "data" / "processed_policies_ocr.csv"

POPPLER_PATH = r"C:\poppler\poppler-26.02.0\Library\bin"


def clean_text(text):
    text = text.replace("\u00a0", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_ocr_text(pdf_path):
    try:

        images = convert_from_path(
            pdf_path,
            dpi=300,
            poppler_path=POPPLER_PATH
        )

        page_texts = []

        for img in images:

            text = pytesseract.image_to_string(
                img,
                lang="kor+eng"
            )

            page_texts.append(text)

        raw_text = "\n".join(page_texts)

        clean = clean_text(raw_text)

        return {
            "file_name": pdf_path.name,
            "company_name": pdf_path.stem,
            "page_count": len(images),
            "clean_text": clean,
            "text_length": len(clean),
            "extract_status": "success",
            "error_message": ""
        }

    except Exception as e:

        return {
            "file_name": pdf_path.name,
            "company_name": pdf_path.stem,
            "page_count": 0,
            "clean_text": "",
            "text_length": 0,
            "extract_status": "fail",
            "error_message": str(e)
        }


def main():

    pdf_files = sorted(PDF_DIR.glob("*.pdf"))

    results = []

    for i, pdf_path in enumerate(pdf_files, start=1):

        print(f"[{i}/{len(pdf_files)}] OCR 처리 중: {pdf_path.name}")

        result = extract_ocr_text(pdf_path)

        results.append(result)

    df = pd.DataFrame(results)

    df.to_csv(
        OUTPUT_PATH,
        index=False,
        encoding="utf-8-sig"
    )

    print("\nOCR 완료")
    print(f"저장 위치: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()