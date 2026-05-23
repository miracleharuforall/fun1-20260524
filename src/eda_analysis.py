from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# =========================
# 기본 경로 설정
# =========================

BASE_DIR = Path(__file__).resolve().parents[1]

INPUT_PATH = BASE_DIR / "data" / "analysis_dataset.xlsx"
OUTPUT_PATH = BASE_DIR / "data" / "eda_result.xlsx"
FIG_DIR = BASE_DIR / "figures"

FIG_DIR.mkdir(exist_ok=True)

# =========================
# 한글 폰트 설정
# =========================
# Windows 기본 한글 폰트
plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False


def main():
    # =========================
    # 데이터 불러오기
    # =========================

    summary = pd.read_excel(INPUT_PATH, sheet_name="summary_with_sector")
    detail = pd.read_excel(INPUT_PATH, sheet_name="detail_with_sector")

    # sector 없는 데이터 제외
    summary = summary.dropna(subset=["sector"])
    detail = detail.dropna(subset=["sector"])

    # =========================
    # 1. 업권별 전체 평균 준수율
    # =========================

    sector_summary = (
        summary
        .groupby("sector")
        .agg(
            company_count=("company_name", "count"),
            avg_compliance_rate=("compliance_rate", "mean"),
            min_compliance_rate=("compliance_rate", "min"),
            max_compliance_rate=("compliance_rate", "max")
        )
        .reset_index()
    )

    sector_summary["avg_compliance_rate"] = (
        sector_summary["avg_compliance_rate"].round(1)
    )

    # =========================
    # 2. requirement_type별 충족률
    # =========================

    requirement_type_summary = (
        detail
        .groupby("requirement_type")
        .agg(
            pass_count=("score", "sum"),
            total_count=("score", "count")
        )
        .reset_index()
    )

    requirement_type_summary["pass_rate"] = (
        requirement_type_summary["pass_count"]
        / requirement_type_summary["total_count"]
        * 100
    ).round(1)

    requirement_type_summary["missing_rate"] = (
        100 - requirement_type_summary["pass_rate"]
    ).round(1)

    # =========================
    # 3. 업권별 required 항목 준수율
    # =========================

    required_detail = detail[
        detail["requirement_type"] == "required"
    ].copy()

    sector_required_summary = (
        required_detail
        .groupby("sector")
        .agg(
            required_pass_count=("score", "sum"),
            required_total_count=("score", "count"),
            company_count=("company_name", "nunique")
        )
        .reset_index()
    )

    sector_required_summary["required_compliance_rate"] = (
        sector_required_summary["required_pass_count"]
        / sector_required_summary["required_total_count"]
        * 100
    ).round(1)

    # =========================
    # 4. 항목별 충족률 / 누락률
    # =========================

    item_summary = (
        detail
        .groupby(["item_id", "item_name", "requirement_type"])
        .agg(
            pass_count=("score", "sum"),
            total_count=("score", "count")
        )
        .reset_index()
    )

    item_summary["pass_rate"] = (
        item_summary["pass_count"]
        / item_summary["total_count"]
        * 100
    ).round(1)

    item_summary["missing_rate"] = (
        100 - item_summary["pass_rate"]
    ).round(1)

    item_summary = item_summary.sort_values(
        "missing_rate",
        ascending=False
    )

    # =========================
    # 5. 업권별 × 항목별 충족률
    # =========================

    sector_item_summary = (
        detail
        .groupby(["sector", "item_id", "item_name", "requirement_type"])
        .agg(
            pass_count=("score", "sum"),
            total_count=("score", "count")
        )
        .reset_index()
    )

    sector_item_summary["pass_rate"] = (
        sector_item_summary["pass_count"]
        / sector_item_summary["total_count"]
        * 100
    ).round(1)

    # =========================
    # 6. 디지털 개인정보 처리 투명성 지표
    # =========================
    # C10: 국외 수집 및 이전
    # C13: 가명정보 처리
    # C14: 자동 수집 장치
    # C15: 제3자 행태정보 수집 허용
    # C17: 자동화된 결정

    digital_items = ["C10", "C13", "C14", "C15", "C17"]

    digital_detail = detail[
        detail["item_id"].isin(digital_items)
    ].copy()

    digital_sector_summary = (
        digital_detail
        .groupby("sector")
        .agg(
            digital_score=("score", "sum"),
            digital_total=("score", "count"),
            company_count=("company_name", "nunique")
        )
        .reset_index()
    )

    digital_sector_summary["digital_transparency_score"] = (
        digital_sector_summary["digital_score"]
        / digital_sector_summary["digital_total"]
        * 100
    ).round(1)

    # =========================
    # 7. 정보주체 권리보장 지표
    # =========================
    # C14: 자동 수집 장치 거부
    # C16: 정보주체 권리·의무 및 행사방법
    # C17: 자동화된 결정 거부·설명 요구
    # C18: 개인정보 보호책임자
    # C20: 권익침해 구제방법
    # C24: 처리방침 변경

    rights_items = ["C14", "C16", "C17", "C18", "C20", "C24"]

    rights_detail = detail[
        detail["item_id"].isin(rights_items)
    ].copy()

    rights_sector_summary = (
        rights_detail
        .groupby("sector")
        .agg(
            rights_score=("score", "sum"),
            rights_total=("score", "count"),
            company_count=("company_name", "nunique")
        )
        .reset_index()
    )

    rights_sector_summary["rights_protection_score"] = (
        rights_sector_summary["rights_score"]
        / rights_sector_summary["rights_total"]
        * 100
    ).round(1)

    # =========================
    # 8. 엑셀 저장
    # =========================

    with pd.ExcelWriter(OUTPUT_PATH, engine="openpyxl") as writer:
        sector_summary.to_excel(
            writer,
            sheet_name="sector_summary",
            index=False
        )

        requirement_type_summary.to_excel(
            writer,
            sheet_name="requirement_type",
            index=False
        )

        sector_required_summary.to_excel(
            writer,
            sheet_name="sector_required",
            index=False
        )

        item_summary.to_excel(
            writer,
            sheet_name="item_summary",
            index=False
        )

        sector_item_summary.to_excel(
            writer,
            sheet_name="sector_item_summary",
            index=False
        )

        digital_sector_summary.to_excel(
            writer,
            sheet_name="digital_transparency",
            index=False
        )

        rights_sector_summary.to_excel(
            writer,
            sheet_name="rights_protection",
            index=False
        )

    # =========================
    # 9. 그래프 생성
    # =========================

    # 그래프 1. 업권별 전체 평균 준수율
    plt.figure(figsize=(10, 6))
    plt.bar(
        sector_summary["sector"],
        sector_summary["avg_compliance_rate"]
    )
    plt.title("업권별 전체 평균 준수율")
    plt.xlabel("업권")
    plt.ylabel("평균 준수율")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(
        FIG_DIR / "sector_avg_compliance_rate.png",
        dpi=200
    )
    plt.close()

    # 그래프 2. 항목별 누락률
    plt.figure(figsize=(12, 7))
    plt.bar(
        item_summary["item_id"],
        item_summary["missing_rate"]
    )
    plt.title("체크리스트 항목별 누락률")
    plt.xlabel("체크리스트 항목")
    plt.ylabel("누락률")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(
        FIG_DIR / "item_missing_rate.png",
        dpi=200
    )
    plt.close()

    # 그래프 3. 업권별 디지털 개인정보 처리 투명성 지표
    plt.figure(figsize=(10, 6))
    plt.bar(
        digital_sector_summary["sector"],
        digital_sector_summary["digital_transparency_score"]
    )
    plt.title("업권별 디지털 개인정보 처리 투명성 지표")
    plt.xlabel("업권")
    plt.ylabel("점수")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(
        FIG_DIR / "digital_transparency_by_sector.png",
        dpi=200
    )
    plt.close()

    # 그래프 4. 업권별 정보주체 권리보장 지표
    plt.figure(figsize=(10, 6))
    plt.bar(
        rights_sector_summary["sector"],
        rights_sector_summary["rights_protection_score"]
    )
    plt.title("업권별 정보주체 권리보장 지표")
    plt.xlabel("업권")
    plt.ylabel("점수")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(
        FIG_DIR / "rights_protection_by_sector.png",
        dpi=200
    )
    plt.close()

    # 그래프 5. 업권별 required 항목 준수율
    plt.figure(figsize=(10, 6))
    plt.bar(
        sector_required_summary["sector"],
        sector_required_summary["required_compliance_rate"]
    )
    plt.title("업권별 필수항목 준수율")
    plt.xlabel("업권")
    plt.ylabel("필수항목 준수율")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(
        FIG_DIR / "sector_required_compliance_rate.png",
        dpi=200
    )
    plt.close()

    # =========================
    # 10. 실행 결과 출력
    # =========================

    print("EDA 분석 완료")
    print(f"EDA 결과 저장: {OUTPUT_PATH}")
    print(f"그래프 저장 폴더: {FIG_DIR}")

    print("\n[업권별 전체 평균 준수율]")
    print(sector_summary)

    print("\n[업권별 required 항목 준수율]")
    print(sector_required_summary)

    print("\n[requirement_type별 충족률]")
    print(requirement_type_summary)

    print("\n[항목별 누락률 TOP 10]")
    print(item_summary.head(10))


if __name__ == "__main__":
    main()