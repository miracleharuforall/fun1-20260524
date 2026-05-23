from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]

COMPANIES_PATH = BASE_DIR / "data" / "companies.csv"
URL_MASTER_PATH = BASE_DIR / "data" / "policy_url_master_185.xlsx"

BACKUP_PATH = BASE_DIR / "data" / "companies_before_url_merge.csv"
OUTPUT_PATH = BASE_DIR / "data" / "companies.csv"
CHECK_PATH = BASE_DIR / "data" / "policy_url_merge_check.xlsx"


def normalize_name(value):
    if pd.isna(value):
        return ""

    value = str(value).strip()
    value = value.replace(" ", "")
    value = value.replace("\n", "")
    value = value.replace("\t", "")

    return value


def load_url_master(path):
    """
    URL 마스터 엑셀을 안정적으로 읽는다.
    현재 파일은 컬럼명이 Unnamed로 잡히고,
    첫 번째 행에 실제 컬럼명이 들어 있는 구조이므로 이를 보정한다.
    """
    df = pd.read_excel(path, sheet_name="datalist")

    print("\nURL master 원본 컬럼:")
    print(df.columns.tolist())

    # 컬럼명이 Unnamed로 잡힌 경우: 첫 번째 행을 컬럼명으로 승격
    if all(str(col).startswith("Unnamed") for col in df.columns):
        new_columns = df.iloc[0].tolist()
        df = df.iloc[1:].copy()
        df.columns = new_columns

    # 컬럼명 공백 제거
    df.columns = [str(col).strip() for col in df.columns]

    # 혹시 한글 컬럼명이 섞여 있을 경우 대비
    rename_map = {
        "업권": "sector",
        "회사명": "company_name",
        "금융회사명": "company_name",
        "기관명": "company_name",
        "업체명": "company_name",
        "개인정보처리방침 URL": "policy_url",
        "개인정보처리방침URL": "policy_url",
        "URL": "policy_url",
        "url": "policy_url",
        "링크": "policy_url",
        "비고": "notes",
        "메모": "notes",
    }

    df = df.rename(columns=rename_map)

    print("\nURL master 보정 후 컬럼:")
    print(df.columns.tolist())

    return df


def main():
    companies = pd.read_csv(COMPANIES_PATH, encoding="utf-8-sig")
    url_master = load_url_master(URL_MASTER_PATH)

    print("\ncompanies.csv 행 수:", len(companies))
    print("URL master 행 수:", len(url_master))

    required_cols = ["company_name", "policy_url"]

    for col in required_cols:
        if col not in url_master.columns:
            raise ValueError(
                f"URL master에 {col} 컬럼이 없습니다. 현재 컬럼: {url_master.columns.tolist()}"
            )

    # 기존 companies 백업
    companies.to_csv(BACKUP_PATH, index=False, encoding="utf-8-sig")

    # 병합 키 생성
    companies["company_key"] = companies["company_name"].apply(normalize_name)
    url_master["company_key"] = url_master["company_name"].apply(normalize_name)

    # URL master에 status/notes 컬럼이 없으면 생성
    if "policy_url_status" not in url_master.columns:
        url_master["policy_url_status"] = ""

    if "notes" not in url_master.columns:
        url_master["notes"] = ""

    # 결측치 정리
    url_master["policy_url"] = url_master["policy_url"].fillna("").astype(str).str.strip()
    url_master["policy_url_status"] = url_master["policy_url_status"].fillna("").astype(str).str.strip()
    url_master["notes"] = url_master["notes"].fillna("").astype(str).str.strip()

    # policy_url이 실제 URL 형식인지 확인
    url_master["policy_url_is_valid_format"] = url_master["policy_url"].str.startswith(
        ("http://", "https://")
    )

    # URL 형식이 아닌 값은 notes로 이동하고 policy_url은 비움
    mask_non_url = ~url_master["policy_url_is_valid_format"]

    url_master.loc[mask_non_url & (url_master["policy_url"] != ""), "notes"] = (
        url_master.loc[mask_non_url & (url_master["policy_url"] != ""), "notes"]
        + " "
        + url_master.loc[mask_non_url & (url_master["policy_url"] != ""), "policy_url"]
    ).str.strip()

    url_master.loc[mask_non_url, "policy_url"] = ""

    # policy_url_status 자동 부여
    url_master.loc[
        (url_master["policy_url"] != "") & (url_master["policy_url_status"] == ""),
        "policy_url_status"
    ] = "checked"

    url_master.loc[
        (url_master["policy_url"] == "") & (url_master["policy_url_status"] == ""),
        "policy_url_status"
    ] = "unknown"

    # 필요한 컬럼만 사용
    url_cols = [
        "company_key",
        "policy_url",
        "policy_url_status",
        "notes"
    ]

    url_df = url_master[url_cols].copy()

    # company_key 빈 값 제거
    url_df = url_df[url_df["company_key"] != ""].copy()

    # 중복 회사명 확인
    duplicated_url = url_df[url_df["company_key"].duplicated(keep=False)].copy()

    # 중복이 있으면 첫 번째만 사용
    url_df = url_df.drop_duplicates(subset=["company_key"], keep="first")

    # 병합
    merged = companies.merge(
        url_df,
        on="company_key",
        how="left",
        suffixes=("", "_from_master")
    )

    # 기존 companies에 policy_url 컬럼이 없을 경우 생성
    if "policy_url" not in merged.columns:
        merged["policy_url"] = ""

    if "policy_url_status" not in merged.columns:
        merged["policy_url_status"] = ""

    if "notes" not in merged.columns:
        merged["notes"] = ""

    # master에서 가져온 값 반영
    if "policy_url_from_master" in merged.columns:
        merged["policy_url"] = merged["policy_url_from_master"].combine_first(
            merged["policy_url"]
        )

    if "policy_url_status_from_master" in merged.columns:
        merged["policy_url_status"] = merged["policy_url_status_from_master"].combine_first(
            merged["policy_url_status"]
        )

    if "notes_from_master" in merged.columns:
        merged["notes"] = merged["notes"].fillna("").astype(str)
        merged["notes_from_master"] = merged["notes_from_master"].fillna("").astype(str)

        merged["notes"] = merged.apply(
            lambda row: row["notes"]
            if row["notes_from_master"] == ""
            else (row["notes"] + " " + row["notes_from_master"]).strip(),
            axis=1
        )

    # URL 매칭 여부
    merged["url_matched"] = merged["policy_url"].fillna("").astype(str).str.strip() != ""

    missing_url = merged[~merged["url_matched"]].copy()
    matched_url = merged[merged["url_matched"]].copy()

    # 임시 컬럼 제거
    drop_cols = [
        "company_key",
        "policy_url_from_master",
        "policy_url_status_from_master",
        "notes_from_master",
        "url_matched",
    ]

    existing_drop_cols = [col for col in drop_cols if col in merged.columns]
    merged = merged.drop(columns=existing_drop_cols)

    # 저장
    merged.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")

    with pd.ExcelWriter(CHECK_PATH, engine="openpyxl") as writer:
        merged.to_excel(writer, sheet_name="companies_with_url", index=False)
        matched_url.to_excel(writer, sheet_name="matched_url", index=False)
        missing_url.to_excel(writer, sheet_name="missing_url", index=False)
        duplicated_url.to_excel(writer, sheet_name="duplicated_url_source", index=False)
        url_master.to_excel(writer, sheet_name="url_master_cleaned", index=False)

    print("\nURL 병합 완료")
    print("최종 companies 저장:", OUTPUT_PATH)
    print("검토 파일 저장:", CHECK_PATH)
    print("URL 매칭 성공:", len(matched_url))
    print("URL 미매칭:", len(missing_url))

    if len(missing_url) > 0:
        print("\nURL 미매칭 회사:")
        print(missing_url[["company_name", "sector", "policy_url_status", "notes"]])


if __name__ == "__main__":
    main()