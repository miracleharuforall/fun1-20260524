from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]

INPUT_PATH = BASE_DIR / "data" / "evaluation_result_24_threshold.xlsx"
OUTPUT_PATH = BASE_DIR / "data" / "required_items_result.xlsx"


def main():
    detail_df = pd.read_excel(INPUT_PATH, sheet_name="detail_result")

    required_detail = detail_df[
        detail_df["requirement_type"].astype(str).str.strip().str.lower() == "required"
    ].copy()

    required_summary = (
        required_detail
        .groupby("company_name")
        .agg(
            required_score=("score", "sum"),
            required_total=("item_id", "count")
        )
        .reset_index()
    )

    required_summary["required_compliance_rate"] = (
        required_summary["required_score"]
        / required_summary["required_total"]
        * 100
    ).round(1)

    required_matrix = required_detail.pivot_table(
        index="company_name",
        columns="item_id",
        values="score",
        aggfunc="first"
    ).reset_index()

    required_matrix = required_matrix.merge(
        required_summary,
        on="company_name",
        how="left"
    )

    with pd.ExcelWriter(OUTPUT_PATH, engine="openpyxl") as writer:
        required_summary.to_excel(writer, sheet_name="required_summary", index=False)
        required_matrix.to_excel(writer, sheet_name="required_matrix", index=False)
        required_detail.to_excel(writer, sheet_name="required_detail", index=False)

    print("required 항목 결과 추출 완료")
    print(f"저장 위치: {OUTPUT_PATH}")
    print(required_summary.head())


if __name__ == "__main__":
    main()