# 금융회사 개인정보처리방침 자동 검토 및 업권별 분석

국내 금융회사 122개 개인정보처리방침을 OCR로 수집·정제하고, 개인정보보호위원회 「개인정보 처리방침 작성지침('26년 4월 기준)」 24개 항목을 기준으로 자동평가 및 업권별 EDA를 수행한 데이터마이닝 프로젝트입니다.

## Dashboard

* Streamlit Dashboard: https://fun1-20260524.streamlit.app
* GitHub Repository: https://github.com/miracleharuforall/fun1-20260524

\---

## Key Results

|항목|결과|
|-|-:|
|최초 수집 PDF|130개|
|최종 분석 대상|122개|
|체크리스트 항목|24개|
|전체 평균 준수율|54.5%|
|필수항목 충족률|82.0%|
|conditional 항목 충족률|38.1%|

주요 인사이트는 다음과 같습니다.

1. 필수항목은 비교적 안정적으로 기재되어 있습니다.
2. 전체 준수율을 낮추는 주요 요인은 해당시 항목과 권장 항목입니다.
3. 디지털·신기술 관련 개인정보 처리 투명성은 상대적으로 낮게 나타났습니다.
4. 조건부 항목의 낮은 기재율은 법 위반율이 아니라 공개 처리방침상 명시 수준으로 해석해야 합니다.

\---

## Dataset

분석 대상은 다음 업권의 금융회사 개인정보처리방침입니다.

* 은행
* 금융투자
* 보험
* 금융유관기관
* 중소서민
* 가상자산사업자
* 전자금융업자
* 핀테크
* 보험GA

데이터 수집 및 정제 흐름은 다음과 같습니다.

```text
PDF 수집
→ OCR 텍스트 추출
→ OCR 노이즈 제거
→ 1,000자 미만 문서 제외
→ 최종 122개 문서 확정
→ 24개 체크리스트 기반 자동평가
→ EDA 및 Streamlit 시각화
```

\---

## Method

### 1\. OCR 및 텍스트 정제

금융회사 홈페이지의 개인정보처리방침을 PDF로 저장한 뒤, Tesseract OCR과 Poppler를 활용하여 텍스트를 추출했습니다. 이후 정규표현식 기반으로 웹 메뉴, 특수문자, 반복 문자열 등 OCR 노이즈를 제거했습니다.

### 2\. 체크리스트 기반 자동평가

개인정보보호위원회 작성지침을 기준으로 24개 체크리스트 항목을 구성하고, 항목별 키워드 매칭 수가 기준값 이상이면 충족으로 판정하는 threshold 기반 평가를 수행했습니다.

### 3\. EDA

업권별 종합 준수율, 필수항목 준수율, 기재 유형별 충족률, 항목별 누락률, 업권 × 체크리스트 항목 히트맵, 디지털 투명성 vs 정보주체 권리보장 지표를 시각화했습니다.

\---

## Derived Indicators

본 프로젝트에서는 24개 체크리스트 전체 점수 외에 두 개의 분석용 파생지표를 구성했습니다.

|지표|구성 항목|목적|
|-|-|-|
|디지털 개인정보 처리 투명성 지표|C10, C13, C14, C15, C17|국외이전, 가명정보, 자동수집장치, 행태정보, 자동화된 결정 등 디지털 처리 공개 수준 비교|
|정보주체 권리보장 지표|C14, C16, C17, C18, C20, C24|정보주체의 확인·통제·구제 관련 기재 수준 비교|

두 지표는 법령상 공식 평가점수가 아니라, 공개 개인정보처리방침의 명시 수준을 비교하기 위해 구성한 분석용 지표입니다.

\---

## RAG Prototype

기본 분석 대시보드 외에 RAG 기반 질의응답 프로토타입을 로컬 환경에서 추가 구현했습니다.

```text
정제 텍스트
→ JSON 구조화
→ chunk 분할
→ sentence-transformers 임베딩
→ ChromaDB VectorDB 저장
→ OpenAI API 기반 자연어 답변 생성
```

RAG 기능은 로컬 환경에서 실행 가능한 프로토타입입니다. Streamlit Cloud 배포본에는 `data/vector\_db/`를 포함하지 않아, Cloud에서는 기본 분석 대시보드 중심으로 제공합니다.

\---

## Project Structure

```text
privacy-policy-mining/
├─ app.py
├─ README.md
├─ requirements.txt
├─ .gitignore
├─ data/
│  ├─ companies.csv
│  ├─ checklist.csv
│  ├─ processed\_policies\_ocr.csv
│  ├─ processed\_policies\_cleaned\_v3.csv
│  ├─ evaluation\_result\_24\_threshold.xlsx
│  ├─ analysis\_dataset.xlsx
│  ├─ eda\_result.xlsx
│  └─ chunks/
│     └─ policy\_chunks.csv
├─ figures/
│  ├─ sector\_avg\_compliance\_rate.png
│  ├─ sector\_required\_compliance\_rate.png
│  ├─ item\_missing\_rate.png
│  ├─ digital\_transparency\_by\_sector.png
│  └─ rights\_protection\_by\_sector.png
└─ src/
   ├─ extract\_pdf\_ocr.py
   ├─ clean\_ocr\_text\_v3.py
   ├─ make\_checklist\_v2.py
   ├─ evaluation\_engine\_v3.py
   ├─ make\_analysis\_dataset.py
   ├─ eda\_analysis.py
   ├─ convert\_to\_json.py
   ├─ make\_chunks.py
   ├─ build\_vectordb.py
   ├─ search\_vectordb.py
   ├─ rag\_answer.py
   └─ rag\_engine.py
```

GitHub에는 아래 파일 및 폴더를 포함하지 않습니다.

```text
.env
data/raw\_pdf/
data/vector\_db/
```

\---

## How to Run

### 1\. 패키지 설치

```bash
pip install -r requirements.txt
```

### 2\. Streamlit 대시보드 실행

```bash
streamlit run app.py
```

### 3\. RAG 프로토타입 실행

OpenAI API 키를 프로젝트 최상위 `.env` 파일에 저장합니다.

```text
OPENAI\_API\_KEY=your\_api\_key
```

그다음 아래 순서로 실행합니다.

```bash
python src/convert\_to\_json.py
python src/make\_chunks.py
python src/build\_vectordb.py
python src/search\_vectordb.py
python src/rag\_answer.py
```

\---

## Limitations

* OCR 기반 분석이므로 PDF 품질에 따라 텍스트 추출 오류가 발생할 수 있습니다.
* 키워드 및 threshold 기반 자동평가는 문맥적 의미를 완전히 반영하지 못할 수 있습니다.
* 조건부 항목은 실제 해당 개인정보 처리 여부를 별도로 확인해야 하므로, 낮은 기재율을 곧바로 법 위반으로 해석할 수 없습니다.
* RAG 답변은 VectorDB에서 검색된 문서 조각을 기반으로 생성되므로, 검색 근거에 없는 내용은 답변할 수 없습니다.
* Streamlit Cloud 배포본에서는 VectorDB 파일을 포함하지 않아 RAG 기능이 제한될 수 있습니다.

\---

## Tech Stack

* Python
* Pandas
* Tesseract OCR
* Poppler
* Plotly
* Streamlit
* ChromaDB
* Sentence Transformers
* OpenAI API

