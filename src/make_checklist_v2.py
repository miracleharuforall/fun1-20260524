from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
OUTPUT_PATH = BASE_DIR / "data" / "checklist.csv"

rows = [
    {
        "item_id": "C01",
        "item_name": "제목 및 서문",
        "requirement_type": "required",
        "regex_keywords": "개인정보처리방침|개인정보처리방침을수립공개|개인정보보호법제30조",
        "min_match_count": 1
    },
    {
        "item_id": "C02",
        "item_name": "개인정보의 처리 목적",
        "requirement_type": "required",
        "regex_keywords": "개인정보의처리목적|개인정보처리목적|처리목적|수집이용목적|이용목적",
        "min_match_count": 1
    },
    {
        "item_id": "C03",
        "item_name": "처리하는 개인정보의 항목",
        "requirement_type": "required",
        "regex_keywords": "처리하는개인정보의항목|개인정보의항목|개인정보항목|처리항목|수집항목|수집이용항목|동의없이처리하는개인정보|동의를받아처리하는개인정보",
        "min_match_count": 2
    },
    {
        "item_id": "C04",
        "item_name": "14세 미만 아동의 개인정보 처리",
        "requirement_type": "conditional",
        "regex_keywords": "14세미만아동|아동의개인정보|법정대리인동의|법정대리인의동의|법정대리인의성명|법정대리인의연락처|동의확인방법",
        "min_match_count": 2
    },
    {
        "item_id": "C05",
        "item_name": "개인정보의 처리 및 보유 기간",
        "requirement_type": "required",
        "regex_keywords": "개인정보의처리및보유기간|처리및보유기간|보유기간|이용기간|보유이용기간|회원탈퇴시까지|목적달성시까지|관련법령에따른보유기간",
        "min_match_count": 2
    },
    {
        "item_id": "C06",
        "item_name": "개인정보의 파기 절차 및 방법",
        "requirement_type": "required",
        "regex_keywords": "개인정보의파기절차및방법|파기절차|파기방법|지체없이파기|복구재생할수없도록파기|분쇄|소각|별도데이터베이스|분리보관",
        "min_match_count": 2
    },
    {
        "item_id": "C07",
        "item_name": "개인정보의 제3자 제공",
        "requirement_type": "conditional",
        "regex_keywords": "개인정보의제3자제공|제3자제공|개인정보를제3자에게제공|제공받는자|제공목적|제공항목|제공하는개인정보의항목|보유및이용기간",
        "min_match_count": 3
    },
    {
        "item_id": "C08",
        "item_name": "추가적인 이용·제공 판단 기준",
        "requirement_type": "conditional",
        "regex_keywords": "추가적인이용제공|추가적이용제공|추가적인이용제공판단기준|판단기준|당초수집목적과관련성|예측가능성|정보주체의이익|안전성확보조치",
        "min_match_count": 3
    },
    {
        "item_id": "C09",
        "item_name": "개인정보 처리업무의 위탁",
        "requirement_type": "conditional",
        "regex_keywords": "개인정보처리업무의위탁|개인정보처리의위탁|처리업무의위탁|위탁|수탁자|위탁받는자|위탁업무|위탁하는업무|재수탁자|재위탁",
        "min_match_count": 2
    },
    {
        "item_id": "C10",
        "item_name": "개인정보의 국외 수집 및 이전",
        "requirement_type": "conditional",
        "regex_keywords": "개인정보의국외수집및이전|국외수집|국외이전|국외로이전|이전국가|이전받는자|이전시기및방법|국외이전의법적근거|이전되는개인정보항목|국외이전거부",
        "min_match_count": 3
    },
    {
        "item_id": "C11",
        "item_name": "개인정보의 안전성 확보조치",
        "requirement_type": "required",
        "regex_keywords": "개인정보의안전성확보조치|안전성확보조치|관리적조치|기술적조치|물리적조치|내부관리계획|접근권한|접근통제|암호화|접속기록|보안프로그램",
        "min_match_count": 3
    },
    {
        "item_id": "C12",
        "item_name": "민감정보의 공개 가능성 및 비공개 선택 방법",
        "requirement_type": "conditional",
        "regex_keywords": "민감정보의공개가능성|민감정보공개가능성|비공개를선택하는방법|비공개선택방법|민감정보가공개될수있다는사실|공개가능성|비공개여부설정",
        "min_match_count": 2
    },
    {
        "item_id": "C13",
        "item_name": "가명정보 처리",
        "requirement_type": "conditional",
        "regex_keywords": "가명정보처리|가명정보의처리|가명처리|가명정보의처리목적|가명정보처리기간|가명처리한개인정보의항목|가명정보의안전성확보조치|통계작성|과학적연구|공익적기록보존",
        "min_match_count": 2
    },
    {
        "item_id": "C14",
        "item_name": "개인정보 자동 수집 장치 설치·운영 및 거부",
        "requirement_type": "conditional",
        "regex_keywords": "개인정보자동수집장치|자동수집장치|자동수집장치의설치운영및거부|쿠키|cookie|cookies|쿠키거부|쿠키차단|브라우저옵션|자동전송",
        "min_match_count": 2
    },
    {
        "item_id": "C15",
        "item_name": "제3자 행태정보 수집 허용·거부",
        "requirement_type": "conditional_recommended",
        "regex_keywords": "제3자가수집해가는행태정보|제3자행태정보|행태정보수집허용|자동수집장치를통해제3자가행태정보를수집|수집장치명칭|수집장치종류|수집해가는사업자|수집해가는행태정보|거부방법",
        "min_match_count": 3
    },
    {
        "item_id": "C16",
        "item_name": "정보주체와 법정대리인의 권리·의무 및 행사방법",
        "requirement_type": "required",
        "regex_keywords": "정보주체와법정대리인의권리의무및행사방법|정보주체의권리|법정대리인의권리|권리행사|열람|전송요구|정정삭제|처리정지|동의철회|행사방법|위임장",
        "min_match_count": 3
    },
    {
        "item_id": "C17",
        "item_name": "자동화된 결정",
        "requirement_type": "conditional",
        "regex_keywords": "자동화된결정|자동화된결정에관한사항|완전히자동화된시스템|자동화된결정의거부|자동화된결정에대한설명|설명요구|검토요구|자동화된결정에사용되는주요개인정보|인공지능기술을적용한시스템",
        "min_match_count": 2
    },
    {
        "item_id": "C18",
        "item_name": "개인정보 보호책임자 및 담당부서",
        "requirement_type": "required",
        "regex_keywords": "개인정보보호책임자|개인정보보호업무담당부서|개인정보업무담당부서|고충사항을처리하는부서|개인정보보호담당부서|성명|부서명|연락처|전자우편",
        "min_match_count": 2
    },
    {
        "item_id": "C19",
        "item_name": "국내대리인 지정",
        "requirement_type": "conditional",
        "regex_keywords": "국내대리인|국내대리인지정|국내대리인의성명|국내대리인의주소|국내대리인의전화번호|국내대리인의전자우편주소|해외사업자",
        "min_match_count": 2
    },
    {
        "item_id": "C20",
        "item_name": "정보주체의 권익침해 구제방법",
        "requirement_type": "recommended",
        "regex_keywords": "권익침해구제방법|권익침해에대한구제방법|개인정보침해신고센터|개인정보분쟁조정위원회|분쟁조정위원회|경찰청|대검찰청|118|18336972",
        "min_match_count": 2
    },
    {
        "item_id": "C21",
        "item_name": "고정형 영상정보처리기기 운영·관리",
        "requirement_type": "conditional",
        "regex_keywords": "고정형영상정보처리기기|영상정보처리기기운영관리|cctv|설치목적|설치대수|설치위치|촬영범위|촬영시간|보관기간|보관장소|영상정보열람|개인영상정보",
        "min_match_count": 3
    },
    {
        "item_id": "C22",
        "item_name": "이동형 영상정보처리기기 운영·관리",
        "requirement_type": "conditional",
        "regex_keywords": "이동형영상정보처리기기|이동형영상정보처리기기운영관리|이동형영상정보|운영대수|촬영시간|보관기간|보관장소|처리방법|영상정보열람|개인영상정보",
        "min_match_count": 3
    },
    {
        "item_id": "C23",
        "item_name": "자율적 개인정보 보호활동",
        "requirement_type": "recommended",
        "regex_keywords": "추가적인개인정보보호노력|개인정보보호활동|자율적개인정보보호활동|isms-p|isms|iso27001|iso27701|cbpr|개인정보영향평가|투명성보고서|자율규제|개인정보보호인증",
        "min_match_count": 1
    },
    {
        "item_id": "C24",
        "item_name": "개인정보 처리방침의 변경",
        "requirement_type": "required",
        "regex_keywords": "개인정보처리방침의변경|처리방침변경|개정일|시행일|변경이력|이전개인정보처리방침|이전처리방침|개정전후비교|변경사항|적용일",
        "min_match_count": 2
    }
]

df = pd.DataFrame(rows)
df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")

print(f"checklist.csv 생성 완료: {OUTPUT_PATH}")
print(df[["item_id", "item_name", "min_match_count"]])