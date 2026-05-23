from pathlib import Path
import pandas as pd
import re

BASE_DIR = Path(__file__).resolve().parents[1]

POLICY_PATH = BASE_DIR / "data" / "processed_policies_cleaned_v3.xlsx"
CHECKLIST_PATH = BASE_DIR / "data" / "checklist.csv"

OUTPUT_XLSX = BASE_DIR / "data" / "evaluation_result_24_threshold.xlsx"
OUTPUT_CSV = BASE_DIR / "data" / "evaluation_result_24_threshold.csv"


def normalize_text(text):
    if pd.isna(text):
        return ""

    text = str(text).lower()

    text = text.replace("cookies", "쿠키")
    text = text.replace("cookie", "쿠키")
    text = text.replace("cctv", "영상정보처리기기")
    text = text.replace("google analytics", "행태정보")
    text = text.replace("googleanalytics", "행태정보")

    text = re.sub(r"\s+", "", text)
    text = re.sub(r"[^가-힣a-z0-9]", "", text)

    return text


def parse_keywords(value):
    if pd.isna(value):
        return []

    parts = re.split(r"\||,", str(value))

    keywords = []
    for part in parts:
        kw = normalize_text(part)
        if kw:
            keywords.append(kw)

    keywords = list(dict.fromkeys(keywords))

    return keywords


def get_min_match_count(row):
    if "min_match_count" not in row.index:
        return 1

    value = row.get("min_match_count", 1)

    if pd.isna(value):
        return 1

    try:
        return int(value)
    except Exception:
        return 1


def evaluate_with_threshold(rule_text, keywords, min_match_count):
    matched = []

    for kw in keywords:
        if kw in rule_text:
            matched.append(kw)

    matched_count = len(matched)
    score = 1 if matched_count >= min_match_count else 0

    return score, matched_count, "|".join(matched)


def main():
    policies = pd.read_excel(POLICY_PATH)
    checklist = pd.read_csv(CHECKLIST_PATH, encoding="utf-8-sig")

    if "regex_keywords" not in checklist.columns:
        raise ValueError("checklist.csv에 regex_keywords 컬럼이 없습니다.")

    if "rule_text" not in policies.columns:
        policies["rule_text"] = policies["clean_text_v3"].apply(normalize_text)
    else:
        policies["rule_text"] = policies["rule_text"].apply(normalize_text)

    wide_rows = []
    detail_rows = []

    for _, policy in policies.iterrows():
        company = policy["company_name"]
        rule_text = policy["rule_text"]

        wide_row = {
            "company_name": company
        }

        total_score = 0

        for _, item in checklist.iterrows():
            item_id = item["item_id"]
            item_name = item["item_name"]
            requirement_type = item.get("requirement_type", "")

            keywords = parse_keywords(item["regex_keywords"])
            min_match_count = get_min_match_count(item)

            score, matched_count, matched_keywords = evaluate_with_threshold(
                rule_text=rule_text,
                keywords=keywords,
                min_match_count=min_match_count
            )

            wide_row[item_id] = score
            total_score += score

            detail_rows.append({
                "company_name": company,
                "item_id": item_id,
                "item_name": item_name,
                "requirement_type": requirement_type,
                "score": score,
                "matched_count": matched_count,
                "min_match_count": min_match_count,
                "matched_keywords": matched_keywords,
                "all_keywords": "|".join(keywords)
            })

        wide_row["total_score"] = total_score
        wide_row["total_items"] = len(checklist)
        wide_row["compliance_rate"] = round(total_score / len(checklist) * 100, 1)

        wide_rows.append(wide_row)

    wide_df = pd.DataFrame(wide_rows)
    detail_df = pd.DataFrame(detail_rows)

    with pd.ExcelWriter(OUTPUT_XLSX, engine="openpyxl") as writer:
        wide_df.to_excel(writer, sheet_name="summary_matrix", index=False)
        detail_df.to_excel(writer, sheet_name="detail_result", index=False)
        checklist.to_excel(writer, sheet_name="checklist", index=False)

    wide_df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")

    print("threshold 기반 24개 체크리스트 자동평가 완료")
    print(f"엑셀 저장: {OUTPUT_XLSX}")
    print(f"CSV 저장: {OUTPUT_CSV}")
    print(wide_df[["company_name", "total_score", "total_items", "compliance_rate"]].head())
    print("\n회사 수:", len(wide_df))


if __name__ == "__main__":
    main()