import logging
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from pinecone import Pinecone
from pinecone.exceptions import PineconeException
from pinecone.models.assistant.streaming import ChatStream

from app.config import settings

app = FastAPI(title="Policy Support Agent by pinecone")
logger = logging.getLogger(__name__)
FRONTEND_FILE = Path(__file__).parent / "static" / "index.html"


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(min_length=1, max_length=10_000)


class ChatRequest(BaseModel):
    messages: list[ChatMessage] = Field(min_length=1)


@app.get("/")
def frontend() -> FileResponse:
    return FileResponse(FRONTEND_FILE)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/chat")
def chat(request: ChatRequest) -> dict[str, str]:
    if not settings.pinecone_api_key:
        raise HTTPException(
            status_code=503,
            detail="Pinecone is not configured. Set PINECONE_API_KEY in .env.",
        )

    try:
        pc = Pinecone(api_key=settings.pinecone_api_key)
        result = pc.assistants.chat(
            assistant_name=settings.pinecone_assistant_name,
            messages=[message.model_dump() for message in request.messages],
            stream=True,
        )
        if isinstance(result, ChatStream):
            answer = "".join(result.text())
        else:
            answer = result.message.content
    except PineconeException as exc:
        logger.exception("Pinecone assistant request failed")
        raise HTTPException(
            status_code=502,
            detail="The Pinecone assistant request failed. Check the server logs.",
        ) from exc

    return {"response": answer}


@app.post("/api/files")
def upload_file(file: UploadFile = File(...)) -> dict[str, str | None]:
    if not settings.pinecone_api_key:
        raise HTTPException(
            status_code=503,
            detail="Pinecone is not configured. Set PINECONE_API_KEY in .env.",
        )

    filename = file.filename
    if not filename or Path(filename).suffix.lower() not in {
        ".txt",
        ".pdf",
        ".json",
        ".md",
        ".docx",
    }:
        raise HTTPException(
            status_code=400,
            detail="Upload a .txt, .pdf, .json, .md, or .docx file.",
        )

    try:
        pc = Pinecone(api_key=settings.pinecone_api_key)
        uploaded_file = pc.assistants.upload_file(
            assistant_name=settings.pinecone_assistant_name,
            file_stream=file.file,
            file_name=filename,
            timeout=None,
        )
    except PineconeException as exc:
        logger.exception("Pinecone assistant file upload failed")
        raise HTTPException(
            status_code=502,
            detail="The Pinecone file upload failed. Check the server logs.",
        ) from exc

    return {
        "id": uploaded_file.id,
        "name": uploaded_file.name,
        "status": uploaded_file.status,
    }
