# Pinecone Assistant Chat

A small browser chat UI backed by a Pinecone Assistant and a FastAPI server.

## Requirements

- Python 3.10 or newer
- A Pinecone API key and an existing Pinecone Assistant

Create and activate a virtual environment, then install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Create a `.env` file and set `PINECONE_API_KEY`. Optionally set
`PINECONE_ASSISTANT_NAME` to your assistant's name (defaults to
`policy-support-agent`).
Keep `.env` private; it is excluded from Git. The API key stays on the server
and is never sent to the browser.

The assistant must already exist in your Pinecone project.

## Run

```powershell
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/` for the chat UI. The `/health` endpoint checks
that the API is running, and interactive API documentation is available at
`http://127.0.0.1:8000/docs`.

Use **Add file** in the chat UI to upload `.txt`, `.pdf`, `.json`, `.md`, or
`.docx` files to the configured Pinecone Assistant. The UI shows upload
processing status and a temporary "Thinking..." message while chat replies
are being generated.
