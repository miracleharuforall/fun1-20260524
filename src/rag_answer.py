from pathlib import Path
import os

import chromadb
from sentence_transformers import SentenceTransformer
from openai import OpenAI
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[1]

VECTOR_DB_DIR = BASE_DIR / "data" / "vector_db"
COLLECTION_NAME = "privacy_policy_chunks"

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)


def search_chunks(query, top_k=5):
    model = SentenceTransformer("jhgan/ko-sroberta-multitask")

    db_client = chromadb.PersistentClient(path=str(VECTOR_DB_DIR))
    collection = db_client.get_collection(COLLECTION_NAME)

    query_embedding = model.encode([query]).tolist()[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    contexts = []

    for i in range(len(results["documents"][0])):
        metadata = results["metadatas"][0][i]
        text = results["documents"][0][i]

        contexts.append(
            {
                "company_name": metadata.get("company_name"),
                "sector": metadata.get("sector"),
                "file_name": metadata.get("file_name"),
                "policy_url": metadata.get("policy_url"),
                "chunk_no": metadata.get("chunk_no"),
                "text": text,
            }
        )

    return contexts


def make_prompt(query, contexts):
    context_text = ""

    for idx, ctx in enumerate(contexts, start=1):
        context_text += f"""
[근거 {idx}]
회사명: {ctx['company_name']}
업권: {ctx['sector']}
파일명: {ctx['file_name']}
chunk 번호: {ctx['chunk_no']}
URL: {ctx['policy_url']}
내용:
{ctx['text']}
"""

    prompt = f"""
너는 금융회사 개인정보처리방침 분석 도우미다.

아래 검색 근거만 사용해서 사용자 질문에 답변하라.
검색 근거에 없는 내용은 추측하지 말고 "제공된 문서만으로는 확인하기 어렵다"고 답하라.

답변에는 가능한 경우 다음을 포함하라.
1. 결론
2. 근거 회사명
3. 근거 chunk 번호
4. 관련 개인정보처리방침 URL
5. 해석상 주의점

조건부 항목은 곧바로 법 위반으로 단정하지 말고, 공개 처리방침상 명시 여부로 해석하라.

[검색 근거]
{context_text}

[사용자 질문]
{query}

[답변]
"""

    return prompt


def answer_question(query):
    contexts = search_chunks(query)
    prompt = make_prompt(query, contexts)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    answer = response.choices[0].message.content

    return answer, contexts


def main():
    if not OPENAI_API_KEY:
        raise ValueError(
            "OPENAI_API_KEY가 없습니다. 프로젝트 최상위 폴더에 .env 파일을 만들고 OPENAI_API_KEY=키값 을 입력하세요."
        )

    query = input("질문을 입력하세요: ")

    answer, contexts = answer_question(query)

    print("\n[LLM 답변]")
    print("=" * 80)
    print(answer)

    print("\n[사용 근거]")
    print("=" * 80)

    for ctx in contexts:
        print(f"- {ctx['company_name']} / chunk {ctx['chunk_no']} / {ctx['policy_url']}")


if __name__ == "__main__":
    main()