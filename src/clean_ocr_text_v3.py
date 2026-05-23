from pathlib import Path
import pandas as pd
import re
import csv
import unicodedata


BASE_DIR = Path(__file__).resolve().parents[1]

INPUT_PATH = BASE_DIR / "data" / "processed_policies_ocr.csv"
OUTPUT_CSV = BASE_DIR / "data" / "processed_policies_cleaned_v3.csv"
OUTPUT_XLSX = BASE_DIR / "data" / "processed_policies_cleaned_v3.xlsx"


KEEP_ENGLISH = {
    "cookie", "cookies", "cctv", "ip", "mac", "ci", "di",
    "aws", "google", "analytics", "visa", "mastercard",
    "apple", "pay", "app", "web", "id", "sms", "url",
    "ai", "api", "pdf", "db"
}

NOISE_WORDS = {
    "ro", "ko", "xo", "x0", "of", "th", "ww", "gu", "ok",
    "ry", "fy", "wr", "dn", "zl", "ol", "fo", "ss", "hh",
    "jo", "ho", "ot", "wo", "oe", "io", "fe", "ae", "ke",
    "ulo", "oll", "oo", "lo", "xo", "xx"
}


def clean_text_v3(text):
    if pd.isna(text):
        return ""

    text = str(text)

    # 유니코드 정규화
    text = unicodedata.normalize("NFKC", text)

    text = text.lower()

    # URL만 제거. 줄 전체 삭제 금지
    text = re.sub(r"https?://\S+", " ", text)
    text = re.sub(r"www\.\S+", " ", text)

    # 날짜/시간만 제거. 줄 전체 삭제 금지
    text = re.sub(
        r"\d{1,2}/\d{1,2}/\d{2,4},?\s*\d{1,2}:\d{2}\s*(am|pm)?",
        " ",
        text
    )

    # 브라우저 print 흔적 제거
    text = re.sub(r"\d+\s*/\s*\d+", " ", text)

    # 자주 나오는 메뉴성 노이즈 일부 제거
    menu_noise = [
        "로그인", "회원가입", "사이트맵", "english",
        "고객센터", "회사소개", "전체메뉴"
    ]
    for word in menu_noise:
        text = text.replace(word, " ")

    # 허용 문자만 유지
    text = re.sub(
        r"[^가-힣a-z0-9\s\.\,\:\;\(\)\[\]\/\-]",
        " ",
        text
    )

    tokens = text.split()
    cleaned_tokens = []

    for token in tokens:
        token_clean = re.sub(r"[^가-힣a-z0-9]", "", token)

        if not token_clean:
            continue

        # 명확한 OCR 쓰레기 제거
        if token_clean in NOISE_WORDS:
            continue

        # 한글이 들어 있으면 보존
        if re.search(r"[가-힣]", token_clean):
            cleaned_tokens.append(token)
            continue

        # 의미 있는 영문은 보존
        if token_clean in KEEP_ENGLISH:
            cleaned_tokens.append(token)
            continue

        # 1~3글자 영문 조각은 대부분 OCR 노이즈라 제거
        if re.fullmatch(r"[a-z]{1,3}", token_clean):
            continue

        # 숫자만 있는 토큰은 너무 짧으면 제거, 긴 숫자는 보존
        if re.fullmatch(r"\d+", token_clean):
            if len(token_clean) >= 2:
                cleaned_tokens.append(token)
            continue

        # 나머지 긴 영문/숫자 혼합은 보존
        if len(token_clean) >= 4:
            cleaned_tokens.append(token)

    text = " ".join(cleaned_tokens)

    # 반복 문자 축소
    text = re.sub(r"(.)\1{3,}", r"\1", text)

    # 공백 정리
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def make_rule_text(text):
    if pd.isna(text):
        return ""

    text = str(text).lower()

    # 자동판정 보강
    text = text.replace("cookies", "쿠키")
    text = text.replace("cookie", "쿠키")
    text = text.replace("cctv", "영상정보처리기기")
    text = text.replace("google analytics", "행태정보")
    text = text.replace("googleanalytics", "행태정보")

    # 공백 제거
    text = re.sub(r"\s+", "", text)

    # 한글, 영문, 숫자만 유지
    text = re.sub(r"[^가-힣a-z0-9]", "", text)

    return text


def main():
    df = pd.read_csv(INPUT_PATH)

    df = df[df["file_name"].astype(str).str.endswith(".pdf")].copy()

    print(f"정제 대상 PDF 수: {len(df)}")

    df["clean_text_v3"] = df["clean_text"].apply(clean_text_v3)
    df["rule_text"] = df["clean_text_v3"].apply(make_rule_text)
    df["clean_length_v3"] = df["clean_text_v3"].apply(len)

    df.to_csv(
        OUTPUT_CSV,
        index=False,
        encoding="utf-8-sig",
        quoting=csv.QUOTE_ALL
    )

    df.to_excel(
        OUTPUT_XLSX,
        index=False
    )

    print("정제 완료")
    print(f"CSV 저장: {OUTPUT_CSV}")
    print(f"XLSX 저장: {OUTPUT_XLSX}")
    print(df["clean_length_v3"].describe())


if __name__ == "__main__":
    main()