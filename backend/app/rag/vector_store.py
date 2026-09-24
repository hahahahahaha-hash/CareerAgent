from langchain_chroma import Chroma

from app.rag.embedding import embeddings

def create_vector_store(chunks):
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory="./data/chroma",
        collection_name="resume",
    )

    return vector_store

#检索函数
def search_resume(query: str, k: int = 3):
    vector_store = Chroma(
        persist_directory="./data/chroma",
        collection_name="resume",
        embedding_function=embeddings,
    )

    results = vector_store.similarity_search(
        query,
        k=k,
    )

    return results