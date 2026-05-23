from pathlib import Path
import pandas as pd
import re


BASE_DIR = Path(__file__).resolve().parents[1]

PDF_DIR = BASE_DIR / "data" / "raw_pdf"
OUTPUT_PATH = BASE_DIR / "data" / "companies.csv"
REVIEW_PATH = BASE_DIR / "data" / "companies_review_needed.csv"


VALID_SECTORS = [
    "은행",
    "금융투자",
    "보험",
    "금융유관기관",
    "중소서민",
    "가상자산사업자",
    "전자금융업자",
    "핀테크",
    "보험GA",
]


def clean_company_name(file_stem: str) -> str:
    """
    PDF 파일명에서 회사명을 추출.
    예:
    KB국민은행.pdf -> KB국민은행
    신한은행_개인정보처리방침.pdf -> 신한은행
    """
    name = str(file_stem).strip()

    # 자주 붙는 불필요한 표현 제거
    remove_patterns = [
        "개인정보처리방침",
        "개인정보 처리방침",
        "개인정보",
        "처리방침",
        "privacy_policy",
        "privacy",
        "policy",
        "최종",
        "수정",
        "출력",
        "print",
        "pdf",
    ]

    for pattern in remove_patterns:
        name = name.replace(pattern, "")

    # 괄호 안 날짜 제거: 회사명(2026.05.17), 회사명[2026-05-17] 등
    name = re.sub(r"\(\s*\d{4}.*?\)", "", name)
    name = re.sub(r"\[\s*\d{4}.*?\]", "", name)

    # 파일명 뒤에 붙은 날짜 제거
    name = re.sub(r"\d{4}[-_.]\d{1,2}[-_.]\d{1,2}", "", name)
    name = re.sub(r"\d{6,8}$", "", name)

    # 앞뒤 특수문자 제거
    name = re.sub(r"^[\s_\-\(\)\[\]]+", "", name)
    name = re.sub(r"[\s_\-\(\)\[\]]+$", "", name)

    # 연속 공백 정리
    name = re.sub(r"\s+", " ", name)

    return name.strip()


def infer_sector(company_name: str) -> str:
    """
    PDF 파일명 기반 업권 1차 자동 추정.
    최종 sector는 아래 9개 중 하나로 통일:
    은행 / 금융투자 / 보험 / 금융유관기관 / 중소서민 /
    가상자산사업자 / 전자금융업자 / 핀테크 / 보험GA
    """
    name = str(company_name).lower()

    # 1. 가상자산사업자
    if (
        "업비트" in company_name
        or "두나무" in company_name
        or "빗썸" in company_name
        or "코인원" in company_name
        or "코빗" in company_name
        or "고팍스" in company_name
        or "가상자산" in company_name
        or "crypto" in name
        or "coin" in name
    ):
        return "가상자산사업자"

    # 2. 전자금융업자
    if (
        "페이" in company_name
        or "pay" in name
        or "페이먼츠" in company_name
        or "결제" in company_name
        or "전자결제" in company_name
        or "pg" in name
        or "선불" in company_name
        or "간편결제" in company_name
        or "토스페이먼츠" in company_name
        or "카카오페이" in company_name
        or "네이버페이" in company_name
        or "쿠팡페이" in company_name
        or "나이스페이" in company_name
        or "kg이니시스" in name
        or "이니시스" in company_name
        or "다날" in company_name
        or "헥토파이낸셜" in company_name
    ):
        return "전자금융업자"

    # 3. 핀테크
    if (
        "핀테크" in company_name
        or "마이데이터" in company_name
        or "로보어드바이저" in company_name
        or "온라인투자연계" in company_name
        or "온투" in company_name
        or "렌딧" in company_name
        or "피플펀드" in company_name
        or "핀다" in company_name
        or "뱅크샐러드" in company_name
        or "비바리퍼블리카" in company_name
        or "토스" in company_name
    ):
        return "핀테크"

    # 4. 금융유관기관
    if (
        "거래소" in company_name
        or "넥스트레이드" in company_name
        or "예탁결제원" in company_name
        or "금융결제원" in company_name
        or "신용정보원" in company_name
        or "신용보증" in company_name
        or "서울보증" in company_name
        or "sgi" in name
        or "신용회복" in company_name
        or "금융보안원" in company_name
        or "금융연수원" in company_name
        or "금융투자협회" in company_name
        or "생명보험협회" in company_name
        or "손해보험협회" in company_name
        or "여신금융협회" in company_name
        or "은행연합회" in company_name
        or "저축은행중앙회" in company_name
        or "보험개발원" in company_name
        or "보험연수원" in company_name
        or "한국자금중개" in company_name
    ):
        return "금융유관기관"

    # 5. 보험GA
    if (
        "보험대리점" in company_name
        or "보험판매" in company_name
        or "ga" in name
        or "에이전시" in company_name
        or "금융서비스" in company_name
        or "에셋" in company_name and "보험" not in company_name
    ):
        return "보험GA"

    # 6. 보험
    if (
        "생명" in company_name
        or "생명보험" in company_name
        or "손해보험" in company_name
        or "화재" in company_name
        or "보험" in company_name
        or "손보" in company_name
        or "해상" in company_name
    ):
        return "보험"

    # 7. 중소서민
    # 저축은행, 카드, 캐피탈, 상호금융, 여전사 등
    if (
        "저축은행" in company_name
        or "캐피탈" in company_name
        or "카드" in company_name
        or "신협" in company_name
        or "새마을금고" in company_name
        or "농협" in company_name
        or "수협" in company_name
        or "산림조합" in company_name
        or "대부" in company_name
        or "리싱" in company_name
        or "리스" in company_name
    ):
        return "중소서민"

    # 8. 금융투자
    if (
        "증권" in company_name
        or "자산운용" in company_name
        or "선물" in company_name
        or "투자자문" in company_name
        or "투자일임" in company_name
        or "운용" in company_name
        or "자문" in company_name
        or "펀드" in company_name
    ):
        return "금융투자"

    # 9. 은행
    # 저축은행은 위에서 이미 중소서민으로 분류됨
    if (
        "은행" in company_name
        or "뱅크" in company_name
        or "bank" in name
    ):
        return "은행"

    return "확인필요"


def main():
    pdf_files = sorted(PDF_DIR.glob("*.pdf"))

    if not pdf_files:
        raise FileNotFoundError(f"PDF 파일이 없습니다: {PDF_DIR}")

    rows = []

    for idx, pdf_path in enumerate(pdf_files, start=1):
        company_name = clean_company_name(pdf_path.stem)
        sector = infer_sector(company_name)

        rows.append({
            "company_id": f"F{idx:03d}",
            "file_name": pdf_path.name,
            "company_name": company_name,
            "sector": sector,
            "policy_url": "",
            "source_type": "manual_pdf",
            "pdf_path": str(pdf_path.relative_to(BASE_DIR)),
            "review_needed": "Y" if sector == "확인필요" or company_name == "" else "N",
            "notes": ""
        })

    df = pd.DataFrame(rows)

    # 중복 company_name 확인
    duplicated_mask = df["company_name"].duplicated(keep=False)
    if duplicated_mask.any():
        df.loc[duplicated_mask, "review_needed"] = "Y"
        df.loc[duplicated_mask, "notes"] = "중복 company_name 확인 필요"

    # sector 값 검증
    invalid_sector_mask = ~df["sector"].isin(VALID_SECTORS + ["확인필요"])
    if invalid_sector_mask.any():
        df.loc[invalid_sector_mask, "review_needed"] = "Y"
        df.loc[invalid_sector_mask, "notes"] = (
            df.loc[invalid_sector_mask, "notes"].astype(str)
            + " sector 값 확인 필요"
        )

    # 저장
    df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")

    review_df = df[df["review_needed"] == "Y"].copy()
    review_df.to_csv(REVIEW_PATH, index=False, encoding="utf-8-sig")

    print("companies.csv 생성 완료")
    print(f"PDF 수: {len(df)}")
    print(f"저장 위치: {OUTPUT_PATH}")
    print(f"확인 필요 수: {len(review_df)}")
    print(f"확인 필요 파일: {REVIEW_PATH}")

    print("\n업권별 개수:")
    print(df["sector"].value_counts())

    if len(review_df) > 0:
        print("\n확인 필요 회사 목록:")
        print(review_df[["file_name", "company_name", "sector", "notes"]])


if __name__ == "__main__":
    main()