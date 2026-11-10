# Policy Support Agent

A small web app for asking questions of a Pinecone Assistant and adding policy
documents to it. The app uses FastAPI for its backend and serves a browser-based
chat interface.

## What you need

- Python 3.10 or newer
- A Pinecone account, API key, and an Assistant that has already been created
- Git, if you are cloning the project

The default Assistant name is `policy-support-agent`. If your Assistant has a
different name, set `PINECONE_ASSISTANT_NAME` as described below.

## Set up

1. Get the project on your computer and open a terminal in the project folder
   (the folder containing `requirements.txt`).
2. Create and activate a virtual environment.

   **Windows (PowerShell):**

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   **macOS or Linux:**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install the project dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

4. Create a file named `.env` in the project folder and add your Pinecone
   settings:

   ```dotenv
   PINECONE_API_KEY=your-pinecone-api-key
   PINECONE_ASSISTANT_NAME=policy-support-agent
   ```

   Replace the example API key and, if needed, the Assistant name. Keep this
   file private; `.env` is excluded from Git. The Assistant must already exist
   in the Pinecone project associated with your API key.

## Run

With the virtual environment active, start the app from the project folder:

```bash
python -m uvicorn app.main:app --reload
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser. Press
`Ctrl+C` in the terminal to stop the server.

## Using the app

- Enter a question in the chat to get a response from the configured Assistant.
- Use **Add file** to upload `.txt`, `.pdf`, `.json`, `.md`, or `.docx` files
  to that Assistant.
- Visit [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for the API
  documentation. The `/health` endpoint reports whether the web app is running.

The chat UI is local to your browser; the server needs an internet connection
to communicate with Pinecone. Keep your API key private and do not expose the
development server to untrusted networks.
