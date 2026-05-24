from pathlib import Path
import chromadb
from sentence_transformers import SentenceTransformer

BASE_DIR = Path(__file__).resolve().parents[1]

VECTOR_DB_DIR = BASE_DIR / "data" / "vector_db"
COLLECTION_NAME = "privacy_policy_chunks"


def search(query, top_k=5):
    model = SentenceTransformer("jhgan/ko-sroberta-multitask")

    client = chromadb.PersistentClient(path=str(VECTOR_DB_DIR))
    collection = client.get_collection(COLLECTION_NAME)

    query_embedding = model.encode([query]).tolist()[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return results


def main():
    query = input("질문을 입력하세요: ")

    results = search(query)

    print("\n검색 결과")
    print("=" * 80)

    for i in range(len(results["documents"][0])):
        metadata = results["metadatas"][0][i]
        document = results["documents"][0][i]

        print(f"\n[{i + 1}]")
        print(f"회사명: {metadata.get('company_name')}")
        print(f"업권: {metadata.get('sector')}")
        print(f"파일명: {metadata.get('file_name')}")
        print(f"chunk 번호: {metadata.get('chunk_no')}")
        print(f"URL: {metadata.get('policy_url')}")
        print("-" * 80)
        print(document[:800])


if __name__ == "__main__":
    main()