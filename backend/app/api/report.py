from pathlib import Path
import uuid

from fastapi import APIRouter
from fastapi.responses import FileResponse
from pydantic import BaseModel

from app.report.word_generator import create_word_report


router = APIRouter(
    prefix="/report",
    tags=["Report"]
)


class ReportRequest(BaseModel):
    content: str


@router.post("/download")
def download_report(request: ReportRequest):

    output_dir = Path("data/reports")
    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    filename = (
        f"AI岗位匹配分析报告_"
        f"{uuid.uuid4().hex[:8]}.docx"
    )

    output_path = output_dir / filename

    create_word_report(
        title="AI 岗位匹配分析报告",
        content=request.content,
        output_path=str(output_path)
    )

    return FileResponse(
        path=output_path,
        filename="AI岗位匹配分析报告.docx",
        media_type=(
            "application/"
            "vnd.openxmlformats-officedocument."
            "wordprocessingml.document"
        )
    )