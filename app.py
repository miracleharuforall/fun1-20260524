
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


# ============================================================
# 기본 설정
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

EDA_PATH = DATA_DIR / "eda_result.xlsx"
EVAL_PATH = DATA_DIR / "evaluation_result_24_threshold.xlsx"
ANALYSIS_PATH = DATA_DIR / "analysis_dataset.xlsx"
COMPANIES_PATH = DATA_DIR / "companies.csv"

st.set_page_config(
    page_title="금융회사 개인정보처리방침 자동 점검",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
    <style>
    .block-container { padding-top: 2rem; padding-bottom: 5rem; max-width: 1280px; }
    section[data-testid="stSidebar"] { background-color: #0f172a; }
    section[data-testid="stSidebar"] * { color: white; }
    .hero {
        background: linear-gradient(135deg, #0f172a 0%, #1d4ed8 55%, #38bdf8 100%);
        padding: 44px 52px; border-radius: 26px; color: white; margin-bottom: 28px;
        box-shadow: 0 16px 40px rgba(15, 23, 42, 0.20);
    }
    .hero-small { font-size: .82rem; font-weight: 800; letter-spacing: .2em; color: #bfdbfe; margin-bottom: 16px; }
    .hero-title { font-size: 2.7rem; line-height: 1.2; font-weight: 900; margin-bottom: 18px; }
    .hero-desc { font-size: 1.05rem; line-height: 1.75; color: #e0f2fe; }
    .section-title { font-size: 2rem; font-weight: 900; color: #0f172a; margin-top: 18px; margin-bottom: 10px; }
    .section-subtitle { font-size: 1rem; color: #64748b; margin-bottom: 20px; line-height: 1.7; }
    .card {
        background: white; border: 1px solid #e2e8f0; border-radius: 20px; padding: 22px 24px;
        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06); margin-bottom: 18px;
    }
    .metric-label { color: #64748b; font-size: .92rem; margin-bottom: 8px; }
    .metric-value { color: #020617; font-size: 2.1rem; font-weight: 900; }
    .info-box {
        background-color: #eff6ff; border: 1px solid #bfdbfe; border-radius: 18px;
        padding: 20px 24px; margin-bottom: 24px; color: #1e3a8a; line-height: 1.7;
    }
    .warning-box {
        background-color: #fff7ed; border: 1px solid #fed7aa; border-radius: 18px;
        padding: 20px 24px; margin-bottom: 24px; color: #9a3412; line-height: 1.7;
    }
    .insight-box {
        background-color: #ffffff; border-left: 6px solid #2563eb; border-radius: 16px;
        padding: 18px 22px; margin-bottom: 14px; box-shadow: 0 6px 18px rgba(15, 23, 42, 0.05);
        line-height: 1.7;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# 공통 함수
# ============================================================

def clean_value(value, default="-"):
    if pd.isna(value):
        return default
    value = str(value).strip()
    if value == "" or value.lower() == "nan":
        return default
    return value



def render_indicator_definition():
    """
    본 프로젝트에서 구성한 파생지표 정의를 화면에 표시한다.
    """
    st.markdown("### 지표 정의")

    st.markdown(
        """
        <div class="info-box">
        <b>디지털 개인정보 처리 투명성 지표</b><br/>
        디지털 개인정보 처리 투명성 지표는 본 프로젝트에서 분석 목적상 구성한 <b>파생지표</b>입니다.
        개인정보 처리방침 작성지침 24개 항목 중 디지털 환경의 개인정보 처리와 관련성이 높은
        <b>C10 개인정보의 국외 수집 및 이전</b>,
        <b>C13 가명정보 처리</b>,
        <b>C14 개인정보 자동 수집 장치 설치·운영 및 거부</b>,
        <b>C15 제3자 행태정보 수집 허용·거부</b>,
        <b>C17 자동화된 결정</b> 항목을 묶어 산출했습니다.
        이 지표는 금융회사가 디지털·신기술 기반 개인정보 처리 내용을 처리방침에 얼마나 명시적으로 공개하고 있는지를 비교하기 위한 목적입니다.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="info-box">
        <b>정보주체 권리보장 지표</b><br/>
        정보주체 권리보장 지표는 본 프로젝트에서 분석 목적상 구성한 <b>파생지표</b>입니다.
        정보주체가 자신의 개인정보 처리에 대해 확인·통제·구제할 수 있는 권리와 관련된
        <b>C14 자동수집장치 거부</b>,
        <b>C16 정보주체와 법정대리인의 권리·의무 및 행사방법</b>,
        <b>C17 자동화된 결정 거부·설명 요구</b>,
        <b>C18 개인정보 보호책임자 및 담당부서</b>,
        <b>C20 정보주체의 권익침해 구제방법</b>,
        <b>C24 개인정보 처리방침의 변경</b> 항목을 묶어 산출했습니다.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="warning-box">
        <b>해석 시 주의</b><br/>
        두 지표는 법령상 공식 평가점수가 아니라, 본 프로젝트에서 공개 개인정보처리방침의 명시 수준을 비교하기 위해 구성한 분석용 지표입니다.
        또한 일부 구성 항목은 <b>해당시 항목</b>이므로, 점수가 낮다고 해서 곧바로 법 위반을 의미하지 않습니다.
        </div>
        """,
        unsafe_allow_html=True,
    )

def style_fig(fig, height=460):
    fig.update_layout(
        height=height,
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(family="Malgun Gothic, Arial", size=14, color="#0f172a"),
        margin=dict(l=20, r=20, t=70, b=30),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(gridcolor="#e2e8f0")
    return fig


def box(kind, title, body):
    cls = {
        "info": "info-box",
        "warning": "warning-box",
        "insight": "insight-box",
        "card": "card",
    }.get(kind, "card")
    st.markdown(f'<div class="{cls}"><b>{title}</b><br/>{body}</div>', unsafe_allow_html=True)


# ============================================================
# 데이터 로딩
# ============================================================

@st.cache_data
def load_data():
    eval_summary = pd.read_excel(EVAL_PATH, sheet_name="summary_matrix")
    eval_detail = pd.read_excel(EVAL_PATH, sheet_name="detail_result")

    sector_summary = pd.read_excel(EDA_PATH, sheet_name="sector_summary")
    requirement_type = pd.read_excel(EDA_PATH, sheet_name="requirement_type")
    sector_required = pd.read_excel(EDA_PATH, sheet_name="sector_required")
    item_summary = pd.read_excel(EDA_PATH, sheet_name="item_summary")
    sector_item = pd.read_excel(EDA_PATH, sheet_name="sector_item_summary")
    digital = pd.read_excel(EDA_PATH, sheet_name="digital_transparency")
    rights = pd.read_excel(EDA_PATH, sheet_name="rights_protection")

    companies = pd.read_csv(COMPANIES_PATH, encoding="utf-8-sig")

    try:
        analysis_summary = pd.read_excel(ANALYSIS_PATH, sheet_name="summary_with_sector")
        analysis_detail = pd.read_excel(ANALYSIS_PATH, sheet_name="detail_with_sector")
    except Exception:
        analysis_summary = None
        analysis_detail = None

    eval_summary["company_name"] = eval_summary["company_name"].astype(str).str.strip()
    eval_detail["company_name"] = eval_detail["company_name"].astype(str).str.strip()
    companies["company_name"] = companies["company_name"].astype(str).str.strip()

    if analysis_summary is not None:
        analysis_summary["company_name"] = analysis_summary["company_name"].astype(str).str.strip()
        summary = analysis_summary.copy()
    else:
        summary = eval_summary.merge(companies, on="company_name", how="left", suffixes=("", "_company"))

    if analysis_detail is not None:
        analysis_detail["company_name"] = analysis_detail["company_name"].astype(str).str.strip()
        detail = analysis_detail.copy()
    else:
        detail = eval_detail.merge(companies, on="company_name", how="left", suffixes=("", "_company"))

    return summary, detail, sector_summary, requirement_type, sector_required, item_summary, sector_item, digital, rights, companies


try:
    summary, detail, sector_summary, requirement_type, sector_required, item_summary, sector_item, digital, rights, company_meta = load_data()
except FileNotFoundError as e:
    st.error("필요한 데이터 파일을 찾을 수 없습니다.")
    st.code(str(e))
    st.stop()
except Exception as e:
    st.error("데이터를 불러오는 중 오류가 발생했습니다.")
    st.code(str(e))
    st.stop()


# ============================================================
# 주요 값 계산
# ============================================================

company_count = len(summary)
checklist_count = 24
overall_avg = round(summary["compliance_rate"].mean(), 1)

def rate_of(req_type):
    s = requirement_type.loc[requirement_type["requirement_type"] == req_type, "pass_rate"]
    return float(s.iloc[0]) if len(s) else 0.0

required_rate = rate_of("required")
conditional_rate = rate_of("conditional")
recommended_rate = rate_of("recommended")
top_missing = item_summary.sort_values("missing_rate", ascending=False).iloc[0]

sector_compare = (
    sector_summary[["sector", "company_count", "avg_compliance_rate"]]
    .merge(sector_required[["sector", "required_compliance_rate"]], on="sector", how="left")
    .merge(digital[["sector", "digital_transparency_score"]], on="sector", how="left")
    .merge(rights[["sector", "rights_protection_score"]], on="sector", how="left")
    .sort_values("avg_compliance_rate", ascending=False)
)

COLOR_SEQ = ["#2563eb", "#38bdf8", "#22c55e", "#f97316", "#8b5cf6", "#ef4444", "#14b8a6", "#eab308", "#64748b"]


# ============================================================
# 사이드바
# ============================================================

with st.sidebar:
    st.markdown("## 🔐 Privacy Policy")
    st.markdown("금융회사 개인정보처리방침  \n자동 점검 및 업권별 기재 수준 분석")
    st.divider()
    page = st.radio("페이지 이동", ["프로젝트 개요", "핵심 지표", "분석 결과", "회사별 상세 조회", "한계 및 결론"])
    st.divider()
    st.markdown("### Data Mining Project")
    st.markdown("최종 분석 대상: **122개**")
    st.markdown("체크리스트: **24개 항목**")


# ============================================================
# 프로젝트 개요
# ============================================================

if page == "프로젝트 개요":
    st.markdown(
        """
        <div class="hero">
            <div class="hero-small">DATA MINING PROJECT</div>
            <div class="hero-title">금융회사 개인정보처리방침<br/>자동 점검 대시보드</div>
            <div class="hero-desc">
                국내 금융회사 홈페이지에 공개된 개인정보처리방침을 수집하고,
                개인정보보호위원회 「개인정보 처리방침 작성지침('26년 4월 24일 기준)」 24개 항목을 기준으로
                업권별 기재 수준을 분석한 결과입니다.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    box("info", "분석 전제", "본 분석은 공개된 개인정보처리방침에 특정 항목이 명시되어 있는지를 기준으로 합니다. 특히 <b>해당시 항목</b>은 실제 해당 개인정보 처리를 수행하는 경우에 기재하는 항목이므로, 미기재를 곧바로 법 위반으로 해석하지 않습니다.")

    st.markdown('<div class="section-title">연구 질문</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="card">
        <b>Q1.</b> 국내 금융회사의 개인정보처리방침은 개인정보보호위원회 작성지침의 주요 기재사항을 얼마나 충족하고 있는가?<br/><br/>
        <b>Q2.</b> 금융회사 업권별로 개인정보처리방침 기재 수준에 차이가 있는가?<br/><br/>
        <b>Q3.</b> 어떤 작성지침 항목이 가장 자주 누락되거나 낮게 기재되는가?<br/><br/>
        <b>Q4.</b> 국외이전, 가명정보, 자동수집장치, 제3자 행태정보, 자동화된 결정 등 디지털·신기술 관련 항목의 공개 수준은 업권별로 어떤 차이를 보이는가?
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="section-title">데이터 수집 및 전처리</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="section-subtitle">
        최초 수집한 금융회사 개인정보처리방침 PDF를 OCR로 텍스트화한 뒤,
        정제 후 텍스트 길이가 1,000자 미만인 문서를 제외하여 최종 분석 표본을 확정했습니다.
        또한 데이터 출처의 재현성을 확보하기 위해 금융회사별 개인정보처리방침 URL을 함께 관리했습니다.
        </div>
        """,
        unsafe_allow_html=True,
    )

    process_df = pd.DataFrame(
        [
            {"단계": "최초 PDF 수집", "문서 수": 130, "설명": "금융회사 홈페이지에서 Print > PDF 방식으로 수동 저장"},
            {"단계": "OCR 및 텍스트 정제", "문서 수": 130, "설명": "Tesseract OCR 및 정규표현식 기반 노이즈 제거"},
            {"단계": "품질 기준 적용", "문서 수": 122, "설명": "정제 후 텍스트 1,000자 미만 문서 제외"},
            {"단계": "URL 병합", "문서 수": 122, "설명": "185개 URL 마스터에서 최종 분석 대상 122개 URL 병합"},
            {"단계": "최종 분석 대상", "문서 수": 122, "설명": "업권 분류 및 threshold 기반 자동평가 대상 확정"},
        ]
    )
    st.dataframe(process_df, use_container_width=True, hide_index=True)

    st.markdown('<div class="section-title">데이터 미리보기</div>', unsafe_allow_html=True)
    p1, p2 = st.columns(2)

    with p1:
        st.markdown("### 회사별 평가 요약")
        st.caption("최종 분석 대상 122개 금융회사의 자동평가 결과 전체를 표시합니다.")
        display_cols = ["company_name", "sector", "total_score", "total_items", "compliance_rate", "policy_url_status"]
        available_cols = [c for c in display_cols if c in summary.columns]
        st.dataframe(summary[available_cols].sort_values("compliance_rate", ascending=False), use_container_width=True, hide_index=True)

    with p2:
        st.markdown("### requirement_type별 충족률")
        st.dataframe(requirement_type, use_container_width=True, hide_index=True)


# ============================================================
# 핵심 지표
# ============================================================

elif page == "핵심 지표":
    st.markdown('<div class="section-title">핵심 지표</div>', unsafe_allow_html=True)

    k1, k2, k3, k4 = st.columns(4)
    metrics = [
        ("최종 분석 대상", f"{company_count}개"),
        ("체크리스트 항목", f"{checklist_count}개"),
        ("전체 평균 준수율", f"{overall_avg}%"),
        ("필수항목 충족률", f"{required_rate:.1f}%"),
    ]

    for col, (label, value) in zip([k1, k2, k3, k4], metrics):
        with col:
            st.markdown(
                f"""
                <div class="card">
                    <div class="metric-label">{label}</div>
                    <div class="metric-value">{value}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("### 기재 유형별 핵심 수치")
    metric_df = pd.DataFrame(
        [
            {"구분": "required", "충족률": required_rate, "해석": "필수 성격의 기본 기재사항"},
            {"구분": "conditional", "충족률": conditional_rate, "해석": "해당 개인정보 처리가 있는 경우 기재"},
            {"구분": "recommended", "충족률": recommended_rate, "해석": "투명성 강화를 위한 권장 항목"},
        ]
    )
    st.dataframe(metric_df, use_container_width=True, hide_index=True)

    fig = px.bar(metric_df, x="구분", y="충족률", color="구분", text="충족률", title="기재 유형별 충족률 요약", color_discrete_sequence=COLOR_SEQ)
    fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    st.plotly_chart(style_fig(fig, height=430), use_container_width=True)

    if "policy_url" in summary.columns:
        url_count = (summary["policy_url"].fillna("").astype(str).str.strip() != "").sum()
        st.markdown("### URL 출처 관리 현황")
        url_df = pd.DataFrame(
            [
                {"구분": "최종 분석 대상", "개수": company_count},
                {"구분": "URL 등록 회사", "개수": int(url_count)},
                {"구분": "URL 미등록 회사", "개수": int(company_count - url_count)},
            ]
        )
        st.dataframe(url_df, use_container_width=True, hide_index=True)

    render_indicator_definition()

    box("insight", "핵심 해석", "전체 평균 준수율은 24개 전체 항목 기준의 종합 기재율입니다. 반면 필수항목 충족률은 required 항목만 대상으로 하므로, 기본 기재사항의 충족 수준을 더 직접적으로 보여줍니다.")


# ============================================================
# 분석 결과
# ============================================================

elif page == "분석 결과":
    st.markdown('<div class="section-title">분석 결과</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="section-subtitle">
        아래 6개 분석 결과는 EDA 핵심 시각화입니다.
        업권별 비교, 필수항목 준수율, 기재 유형별 충족률, 항목별 누락률,
        업권×항목 히트맵, 디지털 투명성·권리보장 관계를 확인할 수 있습니다.
        </div>
        """,
        unsafe_allow_html=True,
    )

    analysis_menu = st.selectbox(
        "분석 결과 선택",
        [
            "1. 업권별 종합 비교",
            "2. 업권별 필수항목 준수율",
            "3. requirement_type별 충족률",
            "4. 체크리스트 항목별 누락률",
            "5. 업권 × 체크리스트 항목 히트맵",
            "6. 디지털 투명성 vs 정보주체 권리보장",
        ],
    )

    if analysis_menu == "1. 업권별 종합 비교":
        st.markdown("## 1. 업권별 종합 비교")
        st.write("전체 평균 준수율, 필수항목 준수율, 디지털 개인정보 처리 투명성 지표, 정보주체 권리보장 지표를 하나의 그래프에서 비교합니다.")

        long_sector = sector_compare.melt(
            id_vars=["sector", "company_count"],
            value_vars=["avg_compliance_rate", "required_compliance_rate", "digital_transparency_score", "rights_protection_score"],
            var_name="indicator",
            value_name="score",
        )
        long_sector["indicator"] = long_sector["indicator"].map(
            {
                "avg_compliance_rate": "전체 평균 준수율",
                "required_compliance_rate": "필수항목 준수율",
                "digital_transparency_score": "디지털 투명성",
                "rights_protection_score": "권리보장 지표",
            }
        )

        fig = px.bar(
            long_sector,
            x="sector",
            y="score",
            color="indicator",
            barmode="group",
            text="score",
            color_discrete_sequence=COLOR_SEQ,
            title="업권별 주요 지표 비교",
            labels={"sector": "업권", "score": "점수", "indicator": "지표"},
        )
        fig.update_traces(texttemplate="%{text:.1f}", textposition="outside")
        st.plotly_chart(style_fig(fig, height=560), use_container_width=True)
        st.dataframe(sector_compare, use_container_width=True, hide_index=True)

        st.markdown("### 그래프 해석")
        box("info", "그래프 읽는 방법", "이 그래프는 업권별로 네 가지 지표를 동시에 비교합니다. 전체 평균 준수율, 필수항목 준수율, 디지털 개인정보 처리 투명성 지표, 정보주체 권리보장 지표를 함께 볼 수 있습니다.")
        box("insight", "주요 해석 1. 전체 평균 준수율과 필수항목 준수율은 차이가 큼", "대부분 업권에서 필수항목 준수율이 전체 평균 준수율보다 높게 나타납니다. 이는 기본 필수 기재사항은 비교적 잘 갖추고 있으나, 해당시 항목과 권장 항목까지 포함하면 전체 기재 수준이 낮아진다는 것을 의미합니다.")
        box("insight", "주요 해석 2. 은행권은 전반적으로 높은 수준", "은행권은 전체 평균 준수율, 필수항목 준수율, 디지털 투명성, 권리보장 지표에서 전반적으로 높은 값을 보입니다.")
        box("insight", "주요 해석 3. 디지털 투명성 지표는 전체적으로 낮음", "디지털 개인정보 처리 투명성 지표는 대부분 업권에서 권리보장 지표보다 낮습니다. 이는 디지털·신기술 관련 개인정보 처리 항목의 공개 수준이 상대적으로 낮다는 점을 보여줍니다.")

    elif analysis_menu == "2. 업권별 필수항목 준수율":
        st.markdown("## 2. 업권별 필수항목 준수율")
        st.write("required 항목만 대상으로 산정한 준수율입니다. 전체 24개 기준 준수율보다 법정 필수 성격의 기본 기재 수준을 더 정확히 보여줍니다.")

        required_sorted = sector_required.sort_values("required_compliance_rate", ascending=True)
        fig = px.bar(
            required_sorted,
            x="required_compliance_rate",
            y="sector",
            orientation="h",
            text="required_compliance_rate",
            color="required_compliance_rate",
            color_continuous_scale="Blues",
            title="업권별 필수항목 준수율",
            labels={"required_compliance_rate": "필수항목 준수율", "sector": "업권"},
        )
        fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig = style_fig(fig, height=520)
        fig.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(sector_required.sort_values("required_compliance_rate", ascending=False), use_container_width=True, hide_index=True)

        st.markdown("### 그래프 해석")
        box("info", "그래프 읽는 방법", "이 그래프는 required 항목만 대상으로 업권별 준수율을 계산한 것입니다. 기본 필수 기재 수준을 직접적으로 보여줍니다.")
        box("insight", "주요 해석 1. 대부분 업권이 70% 이상", "필수항목 준수율은 모든 업권에서 70% 이상으로 나타납니다. 이는 기본적인 처리방침 항목은 대체로 갖추고 있음을 의미합니다.")
        box("insight", "주요 해석 2. 전체 준수율이 낮아도 필수항목은 상대적으로 양호", "일부 업권은 전체 준수율은 낮지만 required 항목만 보면 상대적으로 높은 값을 보입니다. 전체 준수율 하락의 주요 원인은 conditional 및 recommended 항목에 있습니다.")
        box("warning", "해석 시 주의", "이 지표는 required 항목만 대상으로 한 결과입니다. 개인정보처리방침 전체 품질은 해당시 항목과 권장 항목까지 함께 봐야 합니다.")

    elif analysis_menu == "3. requirement_type별 충족률":
        st.markdown("## 3. requirement_type별 충족률")
        st.write("필수항목과 해당시·권장 항목 사이의 충족률 차이를 확인합니다.")

        c1, c2 = st.columns([1.05, 1])
        with c1:
            fig = px.bar(
                requirement_type.sort_values("pass_rate", ascending=True),
                x="pass_rate",
                y="requirement_type",
                orientation="h",
                color="requirement_type",
                text="pass_rate",
                title="기재 유형별 충족률",
                color_discrete_sequence=COLOR_SEQ,
                labels={"pass_rate": "충족률", "requirement_type": "기재 유형"},
            )
            fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
            fig = style_fig(fig, height=420)
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            fig = px.pie(requirement_type, names="requirement_type", values="pass_count", hole=0.55, title="충족 항목 구성", color_discrete_sequence=COLOR_SEQ)
            fig.update_traces(textposition="inside", textinfo="percent+label")
            st.plotly_chart(style_fig(fig, height=420), use_container_width=True)

        st.dataframe(requirement_type, use_container_width=True, hide_index=True)

        st.markdown("### 그래프 해석")
        box("info", "그래프 읽는 방법", "왼쪽 막대그래프는 기재 유형별 충족률, 오른쪽 도넛 차트는 전체 충족 항목 중 각 requirement_type의 비중을 보여줍니다.")
        box("insight", "주요 해석 1. required 항목 충족률이 가장 높음", "required 항목은 82.0% 수준으로 가장 높은 충족률을 보입니다. 기본 법정 고지사항은 비교적 안정적으로 반영되어 있습니다.")
        box("insight", "주요 해석 2. conditional 항목은 상대적으로 낮음", "conditional 항목은 해당 개인정보 처리를 실제 수행하는 경우에 기재하는 항목입니다. 낮은 충족률은 법 위반이 아니라 공개 처리방침상 명시 수준으로 해석해야 합니다.")
        box("insight", "주요 해석 3. conditional_recommended는 매우 낮음", "제3자 행태정보 수집 허용·거부 관련 항목의 충족률이 낮습니다. 이는 광고·추적기술 등 디지털 환경의 투명성 안내가 충분히 정형화되지 않았을 가능성을 보여줍니다.")

    elif analysis_menu == "4. 체크리스트 항목별 누락률":
        st.markdown("## 4. 체크리스트 항목별 누락률")
        st.write("어떤 항목이 가장 자주 미기재 또는 미충족으로 판정되었는지 확인합니다. 색상은 requirement_type을 의미합니다.")

        item_sorted = item_summary.sort_values("missing_rate", ascending=True)
        fig = px.bar(
            item_sorted,
            x="missing_rate",
            y="item_id",
            orientation="h",
            color="requirement_type",
            text="missing_rate",
            hover_data=["item_name", "pass_rate", "total_count"],
            title="체크리스트 항목별 누락률",
            color_discrete_sequence=COLOR_SEQ,
            labels={"missing_rate": "누락률", "item_id": "체크리스트 항목", "requirement_type": "기재 유형"},
        )
        fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        st.plotly_chart(style_fig(fig, height=760), use_container_width=True)

        box("warning", "주의", "누락률 상위 항목은 대부분 해당시 항목입니다. 해당시 항목은 실제 해당 개인정보 처리를 수행하는 경우에 기재하는 항목이므로, 낮은 기재율을 곧바로 법 위반으로 해석하지 않습니다.")
        st.dataframe(item_summary[["item_id", "item_name", "requirement_type", "pass_rate", "missing_rate"]], use_container_width=True, hide_index=True)

        st.markdown("### 그래프 해석")
        box("info", "그래프 읽는 방법", "막대가 길수록 해당 항목이 개인정보처리방침에서 미기재 또는 미충족으로 판정된 비율이 높다는 뜻입니다.")
        box("insight", "주요 해석 1. 누락률 상위 항목은 대부분 조건부 항목", "C19 국내대리인, C22 이동형 영상정보처리기기, C12 민감정보 공개 가능성, C17 자동화된 결정 등은 대부분 conditional 항목입니다.")
        box("insight", "주요 해석 2. 디지털·신기술 관련 항목이 상위에 위치", "C15 제3자 행태정보, C17 자동화된 결정, C10 국외이전 등은 디지털 환경에서 중요한 개인정보 처리 항목입니다.")
        box("insight", "주요 해석 3. required 항목 중 일부도 개선 여지 있음", "required 항목은 전반적으로 높은 충족률을 보였지만, 일부 항목은 문서 표현 방식 차이나 OCR 품질에 따라 미충족으로 판정될 수 있습니다.")

    elif analysis_menu == "5. 업권 × 체크리스트 항목 히트맵":
        st.markdown("## 5. 업권 × 체크리스트 항목 히트맵")
        st.write("행은 업권, 열은 체크리스트 항목이며, 각 셀의 숫자는 해당 업권에서 해당 항목을 충족한 비율입니다.")

        heatmap_df = sector_item.pivot_table(index="sector", columns="item_id", values="pass_rate", aggfunc="mean").fillna(0)
        sector_order = sector_summary.sort_values("avg_compliance_rate", ascending=False)["sector"].tolist()
        heatmap_df = heatmap_df.reindex(sector_order)

        fig = px.imshow(
            heatmap_df,
            text_auto=".0f",
            color_continuous_scale="YlGnBu",
            aspect="auto",
            title="업권 × 체크리스트 항목 충족률 히트맵",
            labels=dict(x="체크리스트 항목", y="업권", color="충족률"),
        )
        st.plotly_chart(style_fig(fig, height=620), use_container_width=True)

        st.markdown("### 히트맵 해석")
        box("info", "히트맵 읽는 방법", "색이 진할수록 해당 업권에서 해당 항목을 많이 기재했다는 뜻이고, 색이 옅을수록 해당 항목의 기재율이 낮다는 뜻입니다.")
        box("insight", "주요 해석 1. 기본 필수항목은 전반적으로 높음", "C01, C02, C05, C11, C16, C18 등 기본적인 개인정보처리방침 구성 항목은 대부분 업권에서 높은 충족률을 보입니다.")
        box("insight", "주요 해석 2. 조건부 항목은 업권별 편차가 큼", "C10 국외이전, C12 민감정보 공개 가능성, C15 제3자 행태정보, C17 자동화된 결정, C21·C22 영상정보처리기기 관련 항목은 업권별 차이가 큽니다.")
        box("insight", "주요 해석 3. 디지털·신기술 관련 항목의 낮은 기재율 확인", "C15 제3자 행태정보, C17 자동화된 결정, C10 국외이전 등은 여러 업권에서 낮은 값을 보입니다.")
        box("warning", "해석 시 주의", "conditional 항목은 실제 해당 개인정보 처리를 수행하는 경우에 기재하는 항목이므로, 낮은 충족률을 법 위반율로 단정하면 안 됩니다.")

    elif analysis_menu == "6. 디지털 투명성 vs 정보주체 권리보장":
        st.markdown("## 6. 디지털 투명성 vs 정보주체 권리보장")
        st.write("각 업권의 디지털 개인정보 처리 투명성 지표와 정보주체 권리보장 지표를 비교합니다. 버블 크기는 해당 업권의 회사 수를 의미합니다.")

        bubble_df = digital[["sector", "digital_transparency_score", "company_count"]].merge(rights[["sector", "rights_protection_score"]], on="sector", how="left")

        fig = px.scatter(
            bubble_df,
            x="digital_transparency_score",
            y="rights_protection_score",
            size="company_count",
            color="sector",
            text="sector",
            size_max=55,
            title="디지털 투명성 지표와 권리보장 지표의 관계",
            color_discrete_sequence=COLOR_SEQ,
            labels={
                "digital_transparency_score": "디지털 개인정보 처리 투명성 지표",
                "rights_protection_score": "정보주체 권리보장 지표",
                "company_count": "회사 수",
                "sector": "업권",
            },
        )
        fig.update_traces(textposition="top center")
        fig.add_vline(x=bubble_df["digital_transparency_score"].mean(), line_dash="dash", line_color="#64748b")
        fig.add_hline(y=bubble_df["rights_protection_score"].mean(), line_dash="dash", line_color="#64748b")
        st.plotly_chart(style_fig(fig, height=560), use_container_width=True)

        render_indicator_definition()

        st.markdown("### 그래프 해석")
        box("info", "그래프 읽는 방법", "X축은 디지털 개인정보 처리 투명성 지표, Y축은 정보주체 권리보장 지표입니다. 버블 크기는 해당 업권의 회사 수이며, 점선은 전체 평균선입니다.")
        box("insight", "주요 해석 1. 권리보장 지표가 디지털 투명성보다 전반적으로 높음", "대부분 업권은 정보주체 권리보장 지표가 디지털 투명성 지표보다 높습니다.")
        box("insight", "주요 해석 2. 은행권은 두 지표 모두 상대적으로 높음", "은행권은 기본 권리보장 안내뿐 아니라 디지털 관련 항목도 상대적으로 많이 포함하고 있습니다.")
        box("insight", "주요 해석 3. 일부 업권은 권리보장 대비 디지털 투명성이 낮음", "보험GA, 전자금융업자, 금융유관기관 등은 권리보장 지표에 비해 디지털 투명성 지표가 낮게 나타납니다.")
        box("warning", "해석 시 주의", "이 지표는 처리방침에 관련 항목이 명시되어 있는지를 기준으로 계산한 것입니다. 실제 개인정보 처리의 적정성을 단정할 수 없습니다.")


# ============================================================
# 회사별 상세 조회
# ============================================================

elif page == "회사별 상세 조회":
    st.markdown('<div class="section-title">회사별 상세 조회</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="section-subtitle">
        특정 회사를 선택하여 24개 체크리스트 항목별 자동평가 결과와 매칭된 키워드,
        그리고 실제 개인정보처리방침 수집 URL을 확인합니다.
        </div>
        """,
        unsafe_allow_html=True,
    )

    company_list = sorted(summary["company_name"].dropna().astype(str).str.strip().unique())

    st.info(
        f"회사 선택 목록은 총 {len(company_list)}개입니다. "
        "Streamlit 선택창은 전체 회사를 한 번에 모두 펼쳐 보여주지 않고 일부만 표시합니다. "
        "드롭다운에서 스크롤하거나 회사명을 직접 입력해서 검색할 수 있습니다."
    )

    with st.expander("전체 회사 목록 보기"):
        st.dataframe(pd.DataFrame({"company_name": company_list}), use_container_width=True, hide_index=True)

    selected_company = st.selectbox("회사 선택", company_list, help="회사명을 직접 입력해서 검색할 수 있습니다.")

    selected_summary = summary[summary["company_name"] == selected_company].copy()
    selected_detail = detail[detail["company_name"] == selected_company].copy()
    selected_meta = company_meta[company_meta["company_name"] == selected_company].copy()

    if not selected_meta.empty:
        meta = selected_meta.iloc[0]
    elif not selected_summary.empty:
        meta = selected_summary.iloc[0]
    else:
        meta = None

    st.markdown("### 수집 출처 정보")

    if meta is not None:
        sector = clean_value(meta.get("sector", "-"))
        file_name = clean_value(meta.get("file_name", "-"))
        policy_url = clean_value(meta.get("policy_url", ""))
        policy_url_status = clean_value(meta.get("policy_url_status", "-"))
        notes = clean_value(meta.get("notes", ""))

        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric("업권", sector)
        with m2:
            st.metric("URL 상태", policy_url_status)
        with m3:
            st.metric("PDF 파일", file_name)

        if policy_url != "-":
            st.markdown(f"**개인정보처리방침 URL:** [{policy_url}]({policy_url})")
        else:
            st.warning("이 회사의 개인정보처리방침 URL이 companies.csv에 없습니다.")

        if notes != "-":
            st.info(f"비고: {notes}")
    else:
        st.warning("회사 메타데이터를 찾을 수 없습니다.")

    st.markdown("### 회사 평가 요약")
    st.dataframe(selected_summary, use_container_width=True, hide_index=True)

    st.markdown("### 항목별 상세 평가")

    with st.expander("항목별 상세 평가 컬럼 설명 보기", expanded=True):
        column_description = pd.DataFrame(
            [
                {"컬럼명": "item_id", "설명": "개인정보 처리방침 작성지침을 기준으로 만든 체크리스트 항목 ID입니다. C01부터 C24까지 총 24개 항목입니다."},
                {"컬럼명": "item_name", "설명": "체크리스트 항목명입니다. 예: 개인정보의 처리 목적, 개인정보의 제3자 제공, 개인정보 보호책임자 등."},
                {"컬럼명": "requirement_type", "설명": "항목의 기재 성격입니다. required는 필수항목, conditional은 해당시 항목, recommended는 권장항목, conditional_recommended는 해당시 권장항목입니다."},
                {"컬럼명": "score", "설명": "자동평가 결과입니다. 1은 해당 항목을 충족한 것으로 판정, 0은 충족하지 못한 것으로 판정했다는 의미입니다."},
                {"컬럼명": "matched_count", "설명": "해당 항목의 평가 키워드 중 실제 개인정보처리방침 텍스트에서 발견된 키워드 개수입니다."},
                {"컬럼명": "min_match_count", "설명": "해당 항목을 충족으로 판정하기 위해 필요한 최소 키워드 매칭 개수입니다. matched_count가 이 값 이상이면 score가 1이 됩니다."},
                {"컬럼명": "matched_keywords", "설명": "실제 개인정보처리방침 텍스트에서 발견된 키워드 목록입니다. 자동평가의 근거로 활용됩니다."},
            ]
        )
        st.dataframe(column_description, use_container_width=True, hide_index=True)
        st.info("예를 들어 matched_count가 3이고 min_match_count가 2이면, 필요한 최소 기준을 넘었기 때문에 score는 1로 판정됩니다. 반대로 matched_count가 1이고 min_match_count가 3이면 score는 0으로 판정됩니다.")

    detail_cols = ["item_id", "item_name", "requirement_type", "score", "matched_count", "min_match_count", "matched_keywords"]
    available_cols = [col for col in detail_cols if col in selected_detail.columns]
    st.dataframe(selected_detail[available_cols], use_container_width=True, hide_index=True)

    selected_plot = selected_detail.copy()
    selected_plot["판정"] = selected_plot["score"].map({1: "충족", 0: "미충족"})

    fig = px.bar(
        selected_plot,
        x="item_id",
        y="score",
        color="판정",
        hover_data=["item_name", "requirement_type", "matched_keywords"],
        title=f"{selected_company} 항목별 평가 결과",
        color_discrete_map={"충족": "#2563eb", "미충족": "#ef4444"},
        labels={"item_id": "체크리스트 항목", "score": "점수", "판정": "판정"},
    )
    fig = style_fig(fig, height=420)
    fig.update_yaxes(range=[0, 1.15])
    st.plotly_chart(fig, use_container_width=True)


# ============================================================
# 한계 및 결론
# ============================================================

elif page == "한계 및 결론":
    st.markdown('<div class="section-title">주요 인사이트</div>', unsafe_allow_html=True)

    box("insight", "1. 필수항목은 비교적 안정적으로 기재", f"required 항목 충족률은 약 <b>{required_rate:.1f}%</b>로 나타났습니다. 금융회사들이 개인정보 처리 목적, 처리 항목, 보유기간, 파기, 보호책임자 등 기본 필수항목은 비교적 충실히 기재하고 있음을 의미합니다. 다만 일부 required 항목에서도 누락률이 존재하므로, 표현 방식 차이나 OCR 품질에 따른 자동평가 한계를 함께 고려해야 합니다.")
    box("insight", "2. 전체 준수율을 낮추는 요인은 해당시·권장 항목", f"conditional 항목 충족률은 약 <b>{conditional_rate:.1f}%</b>로 required 항목보다 낮게 나타났습니다. 이는 모든 회사에 일률적으로 적용되는 항목이 아니라, 특정 개인정보 처리가 있는 경우 기재되는 항목이 많기 때문입니다. 따라서 이 결과는 법 위반율이 아니라 공개 처리방침상 명시적 기재 수준으로 해석해야 합니다.")
    box("insight", "3. 디지털·신기술 관련 개인정보 처리 투명성은 상대적으로 낮음", "국외이전, 가명정보, 자동수집장치, 제3자 행태정보, 자동화된 결정 등 디지털·신기술 관련 항목은 업권별 편차가 크게 나타났습니다. 특히 디지털 투명성 지표는 정보주체 권리보장 지표보다 전반적으로 낮아, 디지털 환경에서의 개인정보 처리 방식은 상대적으로 덜 구체적으로 공개되고 있음을 시사합니다.")
    box("insight", "4. 정보주체 권리보장 항목은 상대적으로 양호", "정보주체 권리보장 지표는 대부분 업권에서 디지털 투명성 지표보다 높게 나타났습니다. 권리행사 방법, 개인정보 보호책임자, 권익침해 구제방법, 처리방침 변경 안내 등 이용자 권리 관련 기본 정보는 비교적 잘 기재되어 있음을 보여줍니다.")
    box("insight", "5. 누락률 상위 항목은 ‘취약 항목’이 아니라 ‘추가 확인 필요 항목’으로 해석", f"누락률이 가장 높은 항목은 <b>{top_missing['item_id']} {top_missing['item_name']}</b>이며, 누락률은 <b>{top_missing['missing_rate']:.1f}%</b>입니다. 다만 누락률 상위 항목은 대부분 조건부 항목이므로, 단순히 미준수로 해석하기보다는 공개 처리방침상 해당 항목이 명시되지 않았다는 의미로 해석하는 것이 타당합니다.")

    st.markdown('<div class="section-title">분석 한계 및 해석 주의</div>', unsafe_allow_html=True)
    box("warning", "해석 주의", "본 프로젝트는 공개된 개인정보처리방침의 텍스트를 기준으로 자동평가를 수행했습니다. 따라서 조건부 항목의 미기재를 곧바로 법 위반으로 판단하지 않습니다. 해당 항목은 실제 개인정보 처리 여부가 확인되는 경우에만 기재 의무 또는 권장 여부를 판단할 수 있습니다.")
    box("card", "한계", "- OCR 기반 분석이므로 PDF 품질에 따라 일부 텍스트 추출 오류가 발생할 수 있습니다.<br/>- 키워드 및 threshold 기반 자동평가는 문맥적 의미를 완전히 반영하지 못할 수 있습니다.<br/>- 실제 개인정보 처리 현황과 처리방침 기재 내용의 일치 여부는 별도 실태조사나 감사가 필요합니다.<br/>- 조건부 항목은 외부 공개문서만으로 실제 해당 여부를 완전히 판단하기 어렵습니다.<br/>- 동일 금융회사가 여러 개인정보처리방침 URL을 운영하는 경우, 본 연구는 실제 PDF로 저장하여 분석한 URL을 기준으로 관리했습니다.")

    st.markdown('<div class="section-title">제출 정보</div>', unsafe_allow_html=True)
    box("card", "GitHub Repository", '<a href="https://github.com/miracleharuforall/fun1-20260524" target="_blank">https://github.com/miracleharuforall/fun1-20260524</a><br/><br/><b>최종 제출물</b><br/>- 결과 보고서 PDF<br/>- 발표자료 PPT<br/>- Streamlit 대시보드<br/>- GitHub Repository 및 README.md')
