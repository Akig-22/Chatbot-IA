from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from app.chatbot import ask_bot
from app.pdf_reader import read_pdf
import json
import shutil
import os

app = FastAPI()

# Sert les fichiers statiques (styles.css, etc.)
app.mount("/static", StaticFiles(directory="frontend"), name="static")


@app.get("/", response_class=HTMLResponse)
def read_root():
    with open("frontend/index.html", "r", encoding="utf-8") as file:
        return file.read()


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/chat")
async def chat(question: str):
    """Route pour poser une question au chatbot en streaming."""

    def generate_response():
        for chunk in ask_bot(question, stream=True):
            yield json.dumps({"response": chunk}) + "\n"

    return StreamingResponse(generate_response(), media_type="application/json")


@app.delete("/memory")
def clear_memory():
    from app.chatbot import memory, save_memory

    memory.clear()
    save_memory(memory)
    return {"message": "Mémoire effacée"}


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Permet d'uploader un PDF et d'en extraire l'info clé."""
    try:
        if not file.filename.endswith(".pdf"):
            return {"error": "Seuls les fichiers PDF sont acceptés."}

        os.makedirs("uploaded_files", exist_ok=True)
        file_location = f"uploaded_files/{file.filename}"

        with open(file_location, "wb") as f:
            shutil.copyfileobj(file.file, f)

        document_text = read_pdf(file_location)
        question = "Quelle est l'information clé dans ce fichier ?"
        response = ask_bot(question, document_text)

        return {"filename": file.filename, "response": response}

    except Exception as e:
        return {"error": f"Erreur lors du traitement : {e}"}
