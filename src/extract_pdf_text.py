from pathlib import Path
import re
import pandas as pd
import fitz  # PyMuPDF


BASE_DIR = Path(__file__).resolve().parents[1]
PDF_DIR = BASE_DIR / "data" / "raw_pdf"
OUTPUT_PATH = BASE_DIR / "data" / "processed_policies.csv"


def clean_text(text: str) -> str:
    """PDF에서 추출한 텍스트를 분석하기 쉬운 형태로 정리"""
    if not text:
        return ""

    text = text.replace("\u00a0", " ")
    text = re.sub(r"\s+", " ", text)
    text = text.strip()

    return text


def extract_text_from_pdf(pdf_path: Path) -> dict:
    """PDF 한 개에서 텍스트 추출"""
    try:
        doc = fitz.open(pdf_path)
        page_texts = []

        for page_no, page in enumerate(doc, start=1):
            text = page.get_text("text")
            page_texts.append(text)

        raw_text = "\n".join(page_texts)
        clean = clean_text(raw_text)

        return {
            "file_name": pdf_path.name,
            "company_name": pdf_path.stem,
            "page_count": len(doc),
            "raw_text": raw_text,
            "clean_text": clean,
            "text_length": len(clean),
            "extract_status": "success",
            "error_message": "",
        }

    except Exception as e:
        return {
            "file_name": pdf_path.name,
            "company_name": pdf_path.stem,
            "page_count": 0,
            "raw_text": "",
            "clean_text": "",
            "text_length": 0,
            "extract_status": "fail",
            "error_message": str(e),
        }


def main():
    pdf_files = sorted(PDF_DIR.glob("*.pdf"))

    if not pdf_files:
        print(f"PDF 파일이 없습니다: {PDF_DIR}")
        return

    results = []

    for i, pdf_path in enumerate(pdf_files, start=1):
        print(f"[{i}/{len(pdf_files)}] 처리 중: {pdf_path.name}")
        result = extract_text_from_pdf(pdf_path)
        results.append(result)

    df = pd.DataFrame(results)
    df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")

    print("\n완료")
    print(f"처리 PDF 수: {len(df)}")
    print(f"성공: {(df['extract_status'] == 'success').sum()}")
    print(f"실패: {(df['extract_status'] == 'fail').sum()}")
    print(f"저장 위치: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()