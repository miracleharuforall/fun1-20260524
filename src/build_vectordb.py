from pathlib import Path
import pandas as pd
import chromadb
from sentence_transformers import SentenceTransformer

BASE_DIR = Path(__file__).resolve().parents[1]

CHUNK_PATH = BASE_DIR / "data" / "chunks" / "policy_chunks.csv"
VECTOR_DB_DIR = BASE_DIR / "data" / "vector_db"

COLLECTION_NAME = "privacy_policy_chunks"


def main():
    df = pd.read_csv(CHUNK_PATH)

    print("임베딩 모델 로딩 중...")
    model = SentenceTransformer("jhgan/ko-sroberta-multitask")

    print("ChromaDB 초기화 중...")
    client = chromadb.PersistentClient(path=str(VECTOR_DB_DIR))

    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    collection = client.create_collection(name=COLLECTION_NAME)

    documents = df["chunk_text"].astype(str).tolist()
    ids = df["chunk_id"].astype(str).tolist()

    metadatas = df[
        [
            "company_name",
            "sector",
            "file_name",
            "policy_url",
            "chunk_no",
        ]
    ].to_dict(orient="records")

    print("임베딩 생성 중...")
    embeddings = model.encode(
        documents,
        show_progress_bar=True,
        batch_size=32
    ).tolist()

    print("VectorDB 저장 중...")
    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    print("VectorDB 구축 완료")
    print(f"저장 위치: {VECTOR_DB_DIR}")
    print(f"저장 chunk 수: {len(df)}")


if __name__ == "__main__":
    main()