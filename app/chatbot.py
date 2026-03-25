import json
import os
from pathlib import Path
from typing import Generator, Optional, Union

import httpx
from dotenv import load_dotenv
from openai import OpenAI

from app.pdf_reader import read_pdf

load_dotenv()

MEMORY_PATH = Path("memory.json")
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama").lower()
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "phi3:latest")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
OPENAI_APP_URL = os.getenv("OPENAI_APP_URL")
OPENAI_APP_NAME = os.getenv("OPENAI_APP_NAME", "Chatbot IA")


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


def build_prompt(question: str, document_text: str) -> str:
    history_text = ""
    for msg in memory[-10:]:
        role = "User" if msg["role"] == "user" else "Assistant"
        history_text += f"{role}: {msg['content']}\n"

    return f"""Tu es un assistant utile et sympathique. Reponds toujours en francais.

{f"Contexte du document :{chr(10)}{document_text}{chr(10)}" if document_text else ""}
{f"Historique :{chr(10)}{history_text}" if history_text else ""}
User: {question}
Assistant:"""


def iter_ollama_response(prompt: str) -> Generator[str, None, None]:
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": True,
    }

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


def iter_openai_response(prompt: str) -> Generator[str, None, None]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        yield "Erreur : la variable d'environnement OPENAI_API_KEY est absente."
        return

    default_headers = {}
    if OPENAI_APP_URL:
        default_headers["HTTP-Referer"] = OPENAI_APP_URL
    if OPENAI_APP_NAME:
        default_headers["X-Title"] = OPENAI_APP_NAME

    client = OpenAI(
        api_key=api_key,
        base_url=OPENAI_BASE_URL,
        default_headers=default_headers or None,
    )

    try:
        with client.responses.stream(
            model=OPENAI_MODEL,
            input=prompt,
        ) as stream:
            for event in stream:
                if event.type == "response.output_text.delta":
                    yield event.delta
    except Exception as e:
        yield f"Erreur OpenAI : {e}"


def ask_bot(
    question: str,
    document_text: Optional[str] = None,
    stream: bool = False,
) -> Union[str, Generator[str, None, None]]:
    """Envoie une question au fournisseur de LLM configure et retourne la reponse."""

    if document_text is None:
        try:
            document_text = read_pdf("document.pdf")
        except Exception:
            document_text = ""

    prompt = build_prompt(question, document_text)

    if LLM_PROVIDER == "openai":
        response_generator = iter_openai_response(prompt)
    else:
        response_generator = iter_ollama_response(prompt)

    if stream:
        def stream_with_memory():
            chunks = []
            for chunk in response_generator:
                chunks.append(chunk)
                yield chunk
            response_text = "".join(chunks)
            memory.append({"role": "user", "content": question})
            memory.append({"role": "assistant", "content": response_text})
            save_memory(memory)

        return stream_with_memory()

    response_text = "".join(response_generator)
    memory.append({"role": "user", "content": question})
    memory.append({"role": "assistant", "content": response_text})
    save_memory(memory)
    return response_text
