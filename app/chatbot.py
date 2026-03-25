import httpx
import json
import os
from pathlib import Path
from typing import Generator, Optional, Union

from app.pdf_reader import read_pdf

MEMORY_PATH = Path("memory.json")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "phi3:latest")


def load_memory() -> list:
    try:
        if MEMORY_PATH.exists():
            return json.loads(MEMORY_PATH.read_text(encoding="utf-8"))
    except Exception:
        pass
    return []


def save_memory(mem: list):
    try:
        MEMORY_PATH.write_text(
            json.dumps(mem, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
    except Exception:
        pass


memory = load_memory()


def ask_bot(
    question: str,
    document_text: Optional[str] = None,
    stream: bool = False,
) -> Union[str, Generator[str, None, None]]:
    """Envoie une question a Ollama et retourne la reponse."""

    if document_text is None:
        try:
            document_text = read_pdf("document.pdf")
        except Exception:
            document_text = ""

    history_text = ""
    for msg in memory[-10:]:
        role = "User" if msg["role"] == "user" else "Assistant"
        history_text += f"{role}: {msg['content']}\n"

    prompt = f"""Tu es un assistant utile et sympathique. Reponds toujours en francais.

{f"Contexte du document :{chr(10)}{document_text}{chr(10)}" if document_text else ""}
{f"Historique :{chr(10)}{history_text}" if history_text else ""}
User: {question}
Assistant:"""

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": True,
    }

    def _iter_stream() -> Generator[str, None, None]:
        try:
            timeout = httpx.Timeout(15.0, read=300.0)
            with httpx.stream("POST", OLLAMA_URL, json=payload, timeout=timeout) as response:
                response.raise_for_status()
                buffer = ""
                done = False

                while not done:
                    for chunk in response.iter_text(chunk_size=1024):
                        if not chunk:
                            continue
                        buffer += chunk
                        while "\n" in buffer:
                            line, buffer = buffer.split("\n", 1)
                            line = line.strip()
                            if not line:
                                continue
                            try:
                                part = json.loads(line)
                            except json.JSONDecodeError:
                                continue

                            if "response" in part and part["response"]:
                                yield part["response"]

                            if part.get("done") is True:
                                done = True
                                break
                    if done:
                        break

                if buffer.strip() and not done:
                    try:
                        part = json.loads(buffer)
                        if "response" in part and part["response"]:
                            yield part["response"]
                    except json.JSONDecodeError:
                        pass

        except Exception as e:
            yield (
                f"Erreur de connexion a Ollama : {e}. "
                f"Verifie que le service repond sur {OLLAMA_URL} avec le modele {OLLAMA_MODEL}."
            )

    if stream:
        def stream_with_memory():
            chunks = []
            for chunk in _iter_stream():
                chunks.append(chunk)
                yield chunk
            response_text = "".join(chunks)
            memory.append({"role": "user", "content": question})
            memory.append({"role": "assistant", "content": response_text})
            save_memory(memory)

        return stream_with_memory()

    response_text = "".join(_iter_stream())
    memory.append({"role": "user", "content": question})
    memory.append({"role": "assistant", "content": response_text})
    save_memory(memory)
    return response_text
