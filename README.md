# Chatbot AI

Petit chatbot en francais avec interface web statique, backend FastAPI, lecture de PDF et generation via Ollama ou OpenAI.

## Lancer en local

### Backend

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

L'application sera disponible sur `http://127.0.0.1:8000`.

### Provider LLM

Le projet peut fonctionner avec `ollama` en local ou `openai` en ligne.

Exemple local :

```powershell
ollama pull phi3
ollama run phi3
```

Variables disponibles :

- `LLM_PROVIDER` : `ollama` ou `openai`
- `OLLAMA_URL` : URL de l'API Ollama. Par defaut `http://localhost:11434/api/generate`
- `OLLAMA_MODEL` : modele Ollama. Par defaut `phi3:latest`
- `OPENAI_API_KEY` : cle API OpenAI
- `OPENAI_MODEL` : modele OpenAI. Par defaut `gpt-4.1-mini`

Copier `.env.example` vers `.env` si besoin.

## Mettre le projet sur GitHub

1. Cree un nouveau depot vide sur GitHub.
2. Dans le dossier du projet, initialise Git :

```powershell
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/TON-UTILISATEUR/TON-REPO.git
git push -u origin main
```

Important :

- Ne pousse pas `.env`, `venv`, `.venv`, `node_modules`, `uploaded_files` ni les executables.
- Si Git n'est pas installe sur ta machine, installe Git for Windows avant ces commandes.

## Deploiement

### Option 1 : VPS avec Ollama

C'est l'option la plus simple si tu veux garder Ollama.

1. Prendre un VPS ou une machine ou Ollama peut tourner.
2. Installer Python, les dependances du projet et Ollama.
3. Lancer l'app avec :

```powershell
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

4. Mettre un reverse proxy devant si besoin.

### Option 2 : Render ou Railway avec OpenAI

Pour un deploiement simple, configure :

1. `LLM_PROVIDER=openai`
2. `OPENAI_API_KEY=...`
3. `OPENAI_MODEL=gpt-4.1-mini`
4. Start command :

```powershell
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Sur Render :

- Build command : `pip install -r requirements.txt`
- Start command : `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Variables : `LLM_PROVIDER`, `OPENAI_API_KEY`, `OPENAI_MODEL`

Sur Railway :

- Variables : `LLM_PROVIDER`, `OPENAI_API_KEY`, `OPENAI_MODEL`
- Start command : `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Sante applicative

Un endpoint de verification est disponible sur `/health`.
