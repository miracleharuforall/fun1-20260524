# 금융회사 개인정보처리방침 자동 점검 및 업권별 분석

## 1\. 프로젝트 개요

본 프로젝트는 국내 금융회사 홈페이지에 공개된 개인정보처리방침 PDF를 수집하고, 개인정보보호위원회 「개인정보 처리방침 작성지침」의 주요 기재사항을 기준으로 자동 평가 및 탐색적 데이터 분석(EDA)을 수행한 데이터마이닝 프로젝트입니다.

수집한 개인정보처리방침 문서는 OCR을 통해 텍스트로 변환하였고, 정제 후 텍스트 길이가 1,000자 미만인 문서는 분석 신뢰도가 낮다고 판단하여 제외했습니다. 최종 분석 대상은 122개 금융회사입니다.

분석 결과는 Streamlit 대시보드로 시각화하여 업권별 준수율, 필수항목 준수율, 항목별 누락률, 업권 × 체크리스트 항목 히트맵, 디지털 개인정보 처리 투명성 지표, 정보주체 권리보장 지표 등을 확인할 수 있도록 구성했습니다.

> 결과보고서 PDF와 발표자료 PPT는 교수님께 별도 제출하며, GitHub Repository에는 포함하지 않습니다.

\---

## 2\. 연구 질문

본 프로젝트의 주요 연구 질문은 다음과 같습니다.

1. 국내 금융회사의 개인정보처리방침은 개인정보보호위원회 작성지침의 주요 기재사항을 얼마나 충족하고 있는가?
2. 금융회사 업권별로 개인정보처리방침 기재 수준에 차이가 있는가?
3. 어떤 작성지침 항목이 가장 자주 누락되거나 낮게 기재되는가?
4. 국외이전, 가명정보, 자동수집장치, 제3자 행태정보, 자동화된 결정 등 디지털·신기술 관련 항목의 공개 수준은 업권별로 어떤 차이를 보이는가?

\---

## 3\. 데이터 수집

### 3.1 수집 대상

* 국내 금융회사 개인정보처리방침 PDF
* 최초 수집 PDF: 130개
* OCR 정제 후 최종 분석 대상: 122개
* 제외 기준: 정제 후 텍스트 길이 1,000자 미만

### 3.2 수집 방식

각 금융회사 홈페이지에서 개인정보처리방침 페이지를 확인한 뒤, 브라우저의 `Print > PDF 저장` 방식으로 수동 수집했습니다.

데이터 출처의 재현성을 확보하기 위해 금융회사별 개인정보처리방침 URL을 별도 엑셀 파일로 관리하였고, 이를 `companies.csv`의 `policy\_url` 컬럼에 병합했습니다.

### 3.3 URL 관리

본 프로젝트는 185개 금융회사 URL 마스터 파일을 기준으로, 최종 분석 대상 122개 회사에 해당하는 개인정보처리방침 URL을 병합했습니다.

관련 파일:

* `data/policy\_url\_master\_185.xlsx`: 금융회사별 URL 마스터 파일
* `data/policy\_url\_merge\_check.xlsx`: URL 병합 검토 파일
* `data/companies.csv`: 최종 분석 대상 122개 회사의 메타데이터 및 URL 정보

\---

## 4\. 분석 대상 업권

분석 대상 금융회사는 다음 업권으로 분류했습니다.

* 은행
* 금융투자
* 보험
* 금융유관기관
* 중소서민
* 가상자산사업자
* 전자금융업자
* 핀테크
* 보험GA

\---

## 5\. 분석 방법

### 5.1 전체 처리 흐름

```text
PDF 수집
→ OCR 텍스트 추출
→ OCR 노이즈 제거
→ clean\_text\_v3 생성
→ rule\_text 생성
→ 24개 체크리스트 기반 자동평가
→ 업권 정보 및 URL 병합
→ EDA 분석
→ Streamlit 대시보드 시각화
```

### 5.2 OCR 및 정제

PDF 문서는 Tesseract OCR과 Poppler를 활용해 텍스트로 변환했습니다. OCR 결과에는 웹사이트 메뉴, 특수문자, 깨진 문자열, URL 등 노이즈가 포함될 수 있으므로 정규표현식 기반 전처리를 수행했습니다.

주요 정제 결과:

* 최종 정제 대상 PDF 수: 122개
* 평균 정제 텍스트 길이: 약 10,837자
* 최소 정제 텍스트 길이: 3,060자

### 5.3 체크리스트 자동평가

개인정보 처리방침 작성지침을 기준으로 24개 체크리스트 항목을 구성했습니다.

각 항목은 다음 정보를 포함합니다.

* `item\_id`: 체크리스트 항목 ID
* `item\_name`: 항목명
* `requirement\_type`: 기재 유형
* `regex\_keywords`: 평가 키워드
* `min\_match\_count`: 충족 판정을 위한 최소 키워드 매칭 수

자동평가는 개인정보처리방침의 정제 텍스트에서 항목별 키워드가 일정 개수 이상 발견되면 해당 항목을 충족한 것으로 판정하는 threshold 기반 방식으로 수행했습니다.

\---

## 6\. 체크리스트 기재 유형

본 프로젝트의 24개 체크리스트 항목은 다음과 같은 기재 유형으로 구분됩니다.

|기재 유형|의미|
|-|-|
|`required`|필수항목|
|`conditional`|해당 개인정보 처리를 수행하는 경우 기재하는 해당시 항목|
|`recommended`|투명성 강화를 위한 권장항목|
|`conditional\_recommended`|해당시 권장항목|

분석 해석 시 `conditional` 항목의 낮은 기재율은 곧바로 법 위반을 의미하지 않습니다. 본 프로젝트에서는 공개된 개인정보처리방침상 명시 여부를 기준으로 해석했습니다.

\---

## 7\. 파생지표 정의

본 프로젝트는 24개 체크리스트 항목을 단순 합산하는 것 외에, 개인정보처리방침의 디지털 환경 대응 수준과 정보주체 권리보장 수준을 비교하기 위해 두 개의 파생지표를 구성했습니다.

### 7.1 디지털 개인정보 처리 투명성 지표

디지털 개인정보 처리 투명성 지표는 디지털 환경의 개인정보 처리와 관련성이 높은 다음 5개 항목을 묶어 산출했습니다.

|항목 ID|항목명|
|-|-|
|C10|개인정보의 국외 수집 및 이전|
|C13|가명정보 처리|
|C14|개인정보 자동 수집 장치 설치·운영 및 거부|
|C15|제3자 행태정보 수집 허용·거부|
|C17|자동화된 결정|

이 지표는 금융회사가 디지털·신기술 기반 개인정보 처리 내용을 개인정보처리방침에 얼마나 명시적으로 공개하고 있는지를 비교하기 위한 분석용 지표입니다.

### 7.2 정보주체 권리보장 지표

정보주체 권리보장 지표는 정보주체가 자신의 개인정보 처리에 대해 확인·통제·구제할 수 있는 권리와 관련된 다음 6개 항목을 묶어 산출했습니다.

|항목 ID|항목명|
|-|-|
|C14|개인정보 자동 수집 장치 설치·운영 및 거부|
|C16|정보주체와 법정대리인의 권리·의무 및 행사방법|
|C17|자동화된 결정|
|C18|개인정보 보호책임자 및 담당부서|
|C20|정보주체의 권익침해 구제방법|
|C24|개인정보 처리방침의 변경|

두 지표는 법령상 공식 평가점수가 아니라, 본 프로젝트에서 공개 개인정보처리방침의 명시 수준을 비교하기 위해 구성한 분석용 파생지표입니다.

\---

## 8\. 주요 결과 요약

### 8.1 전체 결과

* 최종 분석 대상: 122개 금융회사
* 체크리스트 항목 수: 24개
* 전체 평균 준수율: 약 54.5%
* 필수항목 충족률: 약 82.0%

### 8.2 기재 유형별 충족률

|기재 유형|충족률|
|-|-:|
|required|82.0%|
|conditional|38.1%|
|recommended|54.9%|
|conditional\_recommended|4.1%|

### 8.3 주요 인사이트

1. 필수항목은 비교적 안정적으로 기재되어 있습니다.
2. 전체 준수율을 낮추는 주요 요인은 해당시 항목과 권장 항목입니다.
3. 디지털·신기술 관련 개인정보 처리 투명성은 상대적으로 낮게 나타났습니다.
4. 정보주체 권리보장 항목은 디지털 투명성 항목보다 상대적으로 양호했습니다.
5. 누락률 상위 항목은 대부분 조건부 항목이므로, 단순히 법 위반으로 해석하기보다 추가 확인이 필요한 항목으로 해석해야 합니다.

\---

## 9\. Streamlit 대시보드

Streamlit 대시보드는 다음 메뉴로 구성되어 있습니다.

1. 프로젝트 개요
2. 핵심 지표
3. 분석 결과
4. 회사별 상세 조회
5. 한계 및 결론

### 주요 기능

* 최종 분석 대상 122개 회사 요약
* 업권별 종합 비교
* 업권별 필수항목 준수율
* requirement\_type별 충족률
* 체크리스트 항목별 누락률
* 업권 × 체크리스트 항목 히트맵
* 디지털 투명성 vs 정보주체 권리보장 비교
* 회사별 상세 평가 결과 조회
* 개인정보처리방침 원문 URL 확인

### 실행 방법

```bash
pip install -r requirements.txt
streamlit run app.py
```

Streamlit 배포 URL:

```text
배포 후 Streamlit URL을 여기에 입력하세요.
```

\---

## 10\. 프로젝트 파일 구조

```text
privacy-policy-mining/
├─ app.py
├─ README.md
├─ requirements.txt
├─ .gitignore
├─ data/
│  ├─ companies.csv
│  ├─ checklist.csv
│  ├─ policy\_url\_master\_185.xlsx
│  ├─ policy\_url\_merge\_check.xlsx
│  ├─ processed\_policies\_ocr.csv
│  ├─ processed\_policies\_cleaned\_v3.csv
│  ├─ processed\_policies\_cleaned\_v3.xlsx
│  ├─ evaluation\_result\_24\_threshold.csv
│  ├─ evaluation\_result\_24\_threshold.xlsx
│  ├─ analysis\_dataset.xlsx
│  ├─ eda\_result.xlsx
│  └─ required\_items\_result.xlsx
├─ figures/
│  ├─ digital\_transparency\_by\_sector.png
│  ├─ item\_missing\_rate.png
│  ├─ rights\_protection\_by\_sector.png
│  ├─ sector\_avg\_compliance\_rate.png
│  └─ sector\_required\_compliance\_rate.png
└─ src/
   ├─ extract\_pdf\_ocr.py
   ├─ clean\_ocr\_text\_v3.py
   ├─ make\_companies\_from\_pdf.py
   ├─ merge\_policy\_urls\_from\_master.py
   ├─ make\_checklist\_v2.py
   ├─ evaluation\_engine\_v3.py
   ├─ make\_analysis\_dataset.py
   ├─ extract\_required\_results.py
   └─ eda\_analysis.py
```

> `reports/` 폴더의 결과보고서 PDF와 발표자료 PPT는 교수님께 별도 제출하며, GitHub Repository에는 포함하지 않습니다.

\---

## 11\. 주요 파일 설명

|파일|설명|
|-|-|
|`app.py`|Streamlit 대시보드 실행 파일|
|`requirements.txt`|실행에 필요한 Python 패키지 목록|
|`data/companies.csv`|최종 분석 대상 122개 회사 메타데이터 및 URL|
|`data/checklist.csv`|24개 체크리스트 평가 기준|
|`data/processed\_policies\_ocr.csv`|OCR 추출 결과|
|`data/processed\_policies\_cleaned\_v3.csv`|정제 후 개인정보처리방침 텍스트|
|`data/evaluation\_result\_24\_threshold.xlsx`|threshold 기반 자동평가 결과|
|`data/analysis\_dataset.xlsx`|업권 및 URL이 결합된 분석용 데이터셋|
|`data/eda\_result.xlsx`|EDA 결과 요약|
|`src/extract\_pdf\_ocr.py`|PDF OCR 추출 코드|
|`src/clean\_ocr\_text\_v3.py`|OCR 텍스트 정제 코드|
|`src/evaluation\_engine\_v3.py`|자동평가 코드|
|`src/eda\_analysis.py`|EDA 분석 및 시각화 코드|

\---

## 12\. 실행 순서

프로젝트 전체를 재현하려면 아래 순서로 실행합니다.

```bash
python src/make\_companies\_from\_pdf.py
python src/extract\_pdf\_ocr.py
python src/clean\_ocr\_text\_v3.py
python src/merge\_policy\_urls\_from\_master.py
python src/make\_checklist\_v2.py
python src/evaluation\_engine\_v3.py
python src/make\_analysis\_dataset.py
python src/extract\_required\_results.py
python src/eda\_analysis.py
streamlit run app.py
```

\---

## 13\. 분석 한계

본 프로젝트에는 다음과 같은 한계가 있습니다.

1. OCR 기반 분석이므로 PDF 품질에 따라 일부 텍스트 추출 오류가 발생할 수 있습니다.
2. 키워드 및 threshold 기반 자동평가는 문맥적 의미를 완전히 반영하지 못할 수 있습니다.
3. 실제 개인정보 처리 현황과 처리방침 기재 내용의 일치 여부는 별도 실태조사나 감사가 필요합니다.
4. 조건부 항목은 외부 공개문서만으로 실제 해당 여부를 완전히 판단하기 어렵습니다.
5. 동일 금융회사가 여러 개인정보처리방침 URL을 운영하는 경우, 본 연구는 실제 PDF로 저장하여 분석한 URL을 기준으로 관리했습니다.

\---

## 14\. 제출 정보

* GitHub Repository: `https://github.com/miracleharuforall/fun1-20260524`
* Streamlit Dashboard: 배포 후 URL 입력

\---

## 15\. 사용 기술

* Python
* Pandas
* Tesseract OCR
* Poppler
* Regular Expression
* Plotly
* Streamlit
* Excel / CSV 기반 데이터 처리

