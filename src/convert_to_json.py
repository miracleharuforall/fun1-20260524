from pathlib import Path
import json
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]

POLICY_PATH = BASE_DIR / "data" / "processed_policies_cleaned_v3.xlsx"
COMPANY_PATH = BASE_DIR / "data" / "companies.csv"
EVAL_PATH = BASE_DIR / "data" / "evaluation_result_24_threshold.xlsx"

OUTPUT_DIR = BASE_DIR / "data" / "policies_json"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def safe_value(value):
    if pd.isna(value):
        return ""
    return str(value).strip()


def main():
    policies = pd.read_excel(POLICY_PATH)
    companies = pd.read_csv(COMPANY_PATH, encoding="utf-8-sig")
    detail = pd.read_excel(EVAL_PATH, sheet_name="detail_result")

    policies["company_name"] = policies["company_name"].astype(str).str.strip()
    companies["company_name"] = companies["company_name"].astype(str).str.strip()
    detail["company_name"] = detail["company_name"].astype(str).str.strip()

    merged = policies.merge(
        companies,
        on="company_name",
        how="left",
        suffixes=("", "_company")
    )

    count = 0

    for _, row in merged.iterrows():
        company_name = safe_value(row.get("company_name"))
        file_name = safe_value(row.get("file_name"))
        sector = safe_value(row.get("sector"))
        policy_url = safe_value(row.get("policy_url"))
        clean_text = safe_value(row.get("clean_text_v3"))
        rule_text = safe_value(row.get("rule_text"))
        text_length = len(clean_text)

        company_detail = detail[detail["company_name"] == company_name]

        checklist_results = []

        for _, drow in company_detail.iterrows():
            checklist_results.append(
                {
                    "item_id": safe_value(drow.get("item_id")),
                    "item_name": safe_value(drow.get("item_name")),
                    "requirement_type": safe_value(drow.get("requirement_type")),
                    "score": int(drow.get("score", 0)),
                    "matched_count": int(drow.get("matched_count", 0)),
                    "min_match_count": int(drow.get("min_match_count", 0)),
                    "matched_keywords": safe_value(drow.get("matched_keywords")),
                }
            )

        json_data = {
            "company_name": company_name,
            "sector": sector,
            "file_name": file_name,
            "policy_url": policy_url,
            "clean_text": clean_text,
            "rule_text": rule_text,
            "checklist_results": checklist_results,
            "metadata": {
                "text_length": text_length,
                "source_type": safe_value(row.get("source_type")),
                "pdf_path": safe_value(row.get("pdf_path")),
            },
        }

        output_path = OUTPUT_DIR / f"{company_name}.json"

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)

        count += 1

    print(f"JSON 변환 완료: {count}개")
    print(f"저장 위치: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()