from pathlib import Path

from fastapi import APIRouter, UploadFile, File, HTTPException

from app.rag.manager import rebuild_resume_vector_store


router = APIRouter(
    prefix="/resume",
    tags=["Resume"]
)

RESUME_PATH = Path("data/resume.pdf")


@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    # 1. 检查文件类型
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="目前只支持 PDF 格式的简历"
        )

    # 2. 读取文件
    content = await file.read()

    # 3. 检查文件大小
    max_size = 10 * 1024 * 1024

    if len(content) > max_size:
        raise HTTPException(
            status_code=400,
            detail="简历文件不能超过 10MB"
        )

    # 4. 保存新的简历
    RESUME_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    RESUME_PATH.write_bytes(content)

    # 5. 重建向量数据库
    rebuild_resume_vector_store()

    # 6. 返回结果
    return {
        "success": True,
        "filename": file.filename,
        "size": len(content),
        "message": "简历及向量知识库更新成功"
    }