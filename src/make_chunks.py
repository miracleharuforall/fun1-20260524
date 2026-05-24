from pathlib import Path
import json
import re
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]

JSON_DIR = BASE_DIR / "data" / "policies_json"
OUTPUT_PATH = BASE_DIR / "data" / "chunks" / "policy_chunks.csv"

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)


def split_text(text, chunk_size=800, overlap=150):
    text = re.sub(r"\s+", " ", str(text)).strip()

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start = end - overlap

    return chunks


def main():
    rows = []

    json_files = sorted(JSON_DIR.glob("*.json"))

    for json_path in json_files:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        company_name = data.get("company_name", "")
        sector = data.get("sector", "")
        file_name = data.get("file_name", "")
        policy_url = data.get("policy_url", "")
        clean_text = data.get("clean_text", "")

        chunks = split_text(clean_text)

        for idx, chunk in enumerate(chunks, start=1):
            rows.append(
                {
                    "chunk_id": f"{company_name}_{idx:04d}",
                    "company_name": company_name,
                    "sector": sector,
                    "file_name": file_name,
                    "policy_url": policy_url,
                    "chunk_no": idx,
                    "chunk_text": chunk,
                }
            )

    df = pd.DataFrame(rows)
    df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")

    print(f"Chunk 생성 완료: {len(df)}개")
    print(f"저장 위치: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()