from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]

EVAL_PATH = BASE_DIR / "data" / "evaluation_result_24_threshold.xlsx"
COMPANY_PATH = BASE_DIR / "data" / "companies.csv"

OUTPUT_PATH = BASE_DIR / "data" / "analysis_dataset.xlsx"


def main():
    summary = pd.read_excel(EVAL_PATH, sheet_name="summary_matrix")
    detail = pd.read_excel(EVAL_PATH, sheet_name="detail_result")

    companies = pd.read_csv(COMPANY_PATH, encoding="utf-8-sig")

    summary["company_name"] = summary["company_name"].astype(str).str.strip()
    detail["company_name"] = detail["company_name"].astype(str).str.strip()
    companies["company_name"] = companies["company_name"].astype(str).str.strip()

    required_company_cols = ["company_name", "sector"]

    for col in required_company_cols:
        if col not in companies.columns:
            raise ValueError(f"companies.csv에 {col} 컬럼이 없습니다.")

    # 선택 컬럼: 있으면 병합, 없으면 무시
    merge_cols = ["company_name", "sector"]

    optional_cols = [
        "file_name",
        "policy_url",
        "policy_url_status",
        "source_type",
        "pdf_path",
        "notes",
    ]

    for col in optional_cols:
        if col in companies.columns and col not in merge_cols:
            merge_cols.append(col)

    company_meta = companies[merge_cols].copy()

    summary_merged = summary.merge(
        company_meta,
        on="company_name",
        how="left"
    )

    detail_merged = detail.merge(
        company_meta,
        on="company_name",
        how="left"
    )

    missing_sector = summary_merged[
        summary_merged["sector"].isna()
    ][["company_name"]]

    if "policy_url" in summary_merged.columns:
        missing_url = summary_merged[
            summary_merged["policy_url"].isna()
            | (summary_merged["policy_url"].astype(str).str.strip() == "")
        ][["company_name", "sector"]]
    else:
        missing_url = pd.DataFrame(columns=["company_name", "sector"])

    with pd.ExcelWriter(OUTPUT_PATH, engine="openpyxl") as writer:
        summary_merged.to_excel(writer, sheet_name="summary_with_sector", index=False)
        detail_merged.to_excel(writer, sheet_name="detail_with_sector", index=False)
        missing_sector.to_excel(writer, sheet_name="missing_sector", index=False)
        missing_url.to_excel(writer, sheet_name="missing_url", index=False)

    print("분석용 데이터셋 생성 완료")
    print(f"저장 위치: {OUTPUT_PATH}")
    print(f"업권 매칭 실패 회사 수: {len(missing_sector)}")
    print(f"URL 미매칭 회사 수: {len(missing_url)}")


if __name__ == "__main__":
    main()