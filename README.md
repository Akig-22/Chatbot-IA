# Chatbot IA

Application web de chatbot en francais construite avec `FastAPI`, `TailwindCSS` et un backend LLM configurable.

## Liens

- Demo : `https://chatbot-ia-4d9r.onrender.com`
- GitHub : `https://github.com/Akig-22/Chatbot-IA`

## Apercu

Ce projet propose une interface de chat moderne avec reponse en streaming, memoire de conversation et lecture de PDF.  
Il peut fonctionner avec `Ollama` en local ou avec une API compatible OpenAI comme `OpenAI` ou `OpenRouter`.

## Fonctionnalites

- Interface web responsive avec TailwindCSS
- Reponses en streaming
- Memoire conversationnelle simple
- Upload et lecture de fichiers PDF
- Backend FastAPI
- Deploiement en ligne possible sur Render
- Support de plusieurs providers LLM

## Stack technique

- Frontend : HTML, TailwindCSS, JavaScript
- Backend : FastAPI, Python
- LLM : Ollama, OpenAI, OpenRouter
- Deploiement : Render

## Lancer le projet en local

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Application disponible sur :

```text
http://127.0.0.1:8000
```

## Variables d'environnement

Copie `.env.example` vers `.env` puis adapte selon ton provider.

Variables principales :

- `LLM_PROVIDER` : `ollama` ou `openai`
- `OLLAMA_URL`
- `OLLAMA_MODEL`
- `OPENAI_API_KEY`
- `OPENAI_BASE_URL`
- `OPENAI_MODEL`
- `OPENAI_MAX_OUTPUT_TOKENS`
- `OPENAI_APP_URL`
- `OPENAI_APP_NAME`

## Exemple avec OpenRouter

Pour utiliser une option gratuite ou low-cost en ligne :

```text
LLM_PROVIDER=openai
OPENAI_API_KEY=ma_cle_openrouter
OPENAI_BASE_URL=https://openrouter.ai/api/v1
OPENAI_MODEL=openrouter/free
OPENAI_MAX_OUTPUT_TOKENS=512
OPENAI_APP_URL=https://chatbot-ia-4d9r.onrender.com
OPENAI_APP_NAME=Chatbot IA
```

## Deploiement sur Render

Build command :

```text
pip install -r requirements.txt
```

Start command :

```text
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Endpoint de sante :

```text
/health
```

## Structure du projet

```text
app/
  chatbot.py
  main.py
  pdf_reader.py
frontend/
  index.html
  styles.css
requirements.txt
render.yaml
```

## Notes

- Mon fichier `.env` ne doit jamais etre pousse sur GitHub.
- Si une cle API a ete exposee, il faut la revoquer et en generer une nouvelle.
