# 국내 금융회사 개인정보처리방침 준수 여부 자동 검토

국내 금융회사 122개사의 개인정보처리방침 PDF를 OCR로 수집·정제하고, 개인정보보호위원회 「개인정보 처리방침 작성지침」 24개 항목을 기준으로 자동평가 및 업권별 EDA를 수행한 데이터마이닝 프로젝트입니다.

분석 결과는 Streamlit 대시보드로 시각화했으며, 추가로 JSON 구조화·ChromaDB·OpenAI API 기반 RAG 질의응답 프로토타입을 구현했습니다.

\---

## Links

* Streamlit Dashboard: https://fun1-20260524.streamlit.app
* GitHub Repository: https://github.com/miracleharuforall/fun1-20260524

\---

## Final Submission Files

최종 제출본은 `reports/` 폴더에 포함했습니다.

|파일|설명|
|-|-|
|`reports/결과보고서.pdf`|최종 결과보고서|
|`reports/결과발표자료.pdf`|최종 발표자료|

\---

## Key Results

|항목|결과|
|-|-:|
|최초 수집 PDF|130개|
|최종 분석 대상|122개사|
|체크리스트 항목|24개|
|전체 평균 준수율|54.5%|
|필수항목 충족률|82.0%|
|conditional 항목 충족률|38.1%|
|recommended 항목 충족률|54.9%|
|conditional\_recommended 항목 충족률|4.1%|

주요 해석은 다음과 같습니다.

1. 개인정보 처리 목적, 처리 항목, 보유기간, 파기, 보호책임자 등 필수항목은 비교적 안정적으로 기재되어 있습니다.
2. 전체 평균 준수율이 필수항목 충족률보다 낮은 이유는 conditional, recommended, conditional\_recommended 항목의 낮은 기재율 때문입니다.
3. 국외이전, 가명정보, 제3자 행태정보, 자동화된 결정 등 디지털·신기술 관련 항목은 상대적으로 낮은 공개 수준을 보였습니다.
4. conditional 항목의 낮은 기재율은 법 위반율이 아니라, 공개된 개인정보처리방침상 명시 여부로 해석해야 합니다.

\---

## Dataset

분석 대상은 국내 금융회사 홈페이지에 공개된 개인정보처리방침 PDF입니다.

분석 업권은 다음과 같습니다.

* 은행
* 금융투자
* 보험
* 금융유관기관
* 중소서민
* 가상자산사업자
* 전자금융업자
* 핀테크
* 보험GA

데이터 처리 흐름은 다음과 같습니다.

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

금융회사 홈페이지의 개인정보처리방침을 PDF로 저장한 뒤, Tesseract OCR과 Poppler를 활용해 텍스트를 추출했습니다. 이후 정규표현식 기반으로 웹 메뉴, 특수문자, 반복 문자열, URL 등 OCR 노이즈를 제거했습니다.

### 2\. 체크리스트 기반 자동평가

개인정보보호위원회 작성지침을 기준으로 24개 체크리스트 항목을 구성했습니다. 항목별 평가 키워드가 정제 텍스트에서 최소 매칭 수 이상 발견되면 해당 항목을 충족한 것으로 판정했습니다.

```text
if matched\_count >= min\_match\_count:
    score = 1
else:
    score = 0
```

### 3\. EDA

다음 분석 결과를 Streamlit 대시보드에서 확인할 수 있도록 구성했습니다.

* 업권별 종합 비교
* 업권별 필수항목 준수율
* requirement\_type별 충족률
* 체크리스트 항목별 누락률
* 업권 × 체크리스트 항목 히트맵
* 디지털 투명성 vs 정보주체 권리보장

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

기본 분석 대시보드 외에 RAG 기반 질의응답 프로토타입을 로컬 환경에서 구현했습니다.

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

## LDA Theory Mapping

발표 요구사항에 따라 LDA(Latent Dirichlet Allocation)를 개인정보처리방침 분석과 연결했습니다.

LDA는 여러 문서 안에 숨어 있는 주제(topic)를 자동으로 찾아내는 토픽 모델링 기법입니다. 본 프로젝트에서는 실제 LDA 모델링 결과를 산출하지는 않았지만, 향후 개인정보처리방침 내 수집·이용 목적, 제3자 제공, 위탁, 국외이전, 쿠키·행태정보, 정보주체 권리행사 등 숨은 주제를 자동 분류하는 확장 방향으로 제시했습니다.

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
├─ reports/
│  ├─ 2025720229\_결과보고서.pdf
│  └─ 2025720229\_결과발표자료.pdf
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
data/policies\_json/
backup\_before\_rag/
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

## AWS Extension Design

현재 구현은 로컬 Python 환경과 Streamlit Community Cloud 기반입니다. 향후 운영 환경으로 확장할 경우 다음과 같은 AWS 구조를 적용할 수 있습니다.

|구성요소|AWS 서비스 예시|역할|
|-|-|-|
|PDF 및 JSON 저장|S3|PDF 원본, JSON 문서, 분석 결과 저장|
|OCR/전처리 실행|EC2 또는 Lambda|OCR, 텍스트 정제, JSON 변환, chunk 생성|
|분석 결과 저장|S3 또는 RDS|평가 결과 및 EDA 결과 저장|
|VectorDB|OpenSearch Vector Engine 또는 RDS PostgreSQL pgvector|문서 임베딩 저장 및 검색|
|LLM 연동|Amazon Bedrock 또는 OpenAI API|자연어 질의응답 생성|
|대시보드|Streamlit on EC2 또는 Streamlit Cloud|사용자 화면 제공|
|모니터링|CloudWatch|실행 로그 및 오류 모니터링|

\---

## Limitations

* OCR 기반 분석이므로 PDF 품질에 따라 텍스트 추출 오류가 발생할 수 있습니다.
* 키워드 및 threshold 기반 자동평가는 문맥적 의미를 완전히 반영하지 못할 수 있습니다.
* conditional 항목은 실제 해당 개인정보 처리 여부를 별도로 확인해야 하므로, 낮은 기재율을 곧바로 법 위반으로 해석할 수 없습니다.
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
* GitHub

