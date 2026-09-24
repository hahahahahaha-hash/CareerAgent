from langchain_chroma import Chroma

from app.rag.loader import load_resume
from app.rag.embedding import embeddings


CHROMA_PATH = "./data/chroma"
COLLECTION_NAME = "resume"
RESUME_PATH = "data/resume.pdf"


def rebuild_resume_vector_store():
    # 1. 连接现有的 Chroma
    vector_store = Chroma(
        persist_directory=CHROMA_PATH,
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
    )

    # 2. 删除旧的简历向量
    vector_store.delete_collection()

    # 3. 重新读取简历并切分
    chunks = load_resume(RESUME_PATH)

    # 4. 重新建立向量库
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_PATH,
        collection_name=COLLECTION_NAME,
    )

    return vector_store