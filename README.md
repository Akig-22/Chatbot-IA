# Chatbot AI

Petit chatbot en francais avec interface web statique, backend FastAPI, lecture de PDF et generation via Ollama.

## Lancer en local

### Backend

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

L'application sera disponible sur `http://127.0.0.1:8000`.

### Ollama

Le projet attend un serveur Ollama accessible sur `OLLAMA_URL`.

Exemple local :

```powershell
ollama pull phi3
ollama run phi3
```

Variables disponibles :

- `OLLAMA_URL` : URL de l'API Ollama. Par defaut `http://localhost:11434/api/generate`
- `OLLAMA_MODEL` : modele Ollama. Par defaut `phi3:latest`

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

### Option 2 : Render/Railway avec une API LLM distante

Si tu veux deployer sur une plateforme type Render, Railway ou Fly.io, il faut en general remplacer Ollama local par une API distante, sinon `localhost:11434` ne sera pas disponible.

Dans ce cas :

1. Heberger le modele ailleurs.
2. Configurer `OLLAMA_URL` pour pointer vers ce serveur.
3. Definir `OLLAMA_MODEL` dans les variables d'environnement de la plateforme.

### Sante applicative

Un endpoint de verification est disponible sur `/health`.
