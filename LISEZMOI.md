# BiasDetector - Guide de Demarrage Rapide

## Prerequis a Installer

### 1. Ollama (IA Locale)
Telecharger et installer depuis: https://ollama.ai

### 2. Docker Desktop (pour MongoDB)
Telecharger et installer depuis: https://www.docker.com/products/docker-desktop/

---

## Premiere Installation (une seule fois)

### Etape 1: Telecharger les modeles Ollama
Ouvrir PowerShell et executer:
```powershell
ollama pull llama3.2
ollama pull nomic-embed-text
```

### Etape 2: Installer les dependances Backend
```powershell
cd C:\Users\youss\ProjetAyoub\BiasDetector\backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### Etape 3: Installer les dependances Frontend
```powershell
cd C:\Users\youss\ProjetAyoub\BiasDetector\frontend
npm install
```

---

## Demarrage Rapide (chaque fois)

### Option 1: Script Automatique
```powershell
cd C:\Users\youss\ProjetAyoub\BiasDetector
.\start.ps1
```

### Option 2: Demarrage Manuel

**Terminal 1 - Ollama:**
```powershell
ollama serve
```

**Terminal 2 - MongoDB:**
```powershell
docker run -d -p 27017:27017 --name mongodb mongo:latest
```

**Terminal 3 - Backend:**
```powershell
cd C:\Users\youss\ProjetAyoub\BiasDetector\backend
.\venv\Scripts\activate
uvicorn main:app --reload
```

**Terminal 4 - Frontend:**
```powershell
cd C:\Users\youss\ProjetAyoub\BiasDetector\frontend
npm run dev
```

---

## Acces a l'Application

- **Application:** http://localhost:3000
- **API Backend:** http://localhost:8000
- **Documentation API:** http://localhost:8000/docs

---

## En cas de probleme

### Erreur "port deja utilise"
```powershell
# Arreter MongoDB
docker stop mongodb
docker rm mongodb

# Relancer
docker run -d -p 27017:27017 --name mongodb mongo:latest
```

### Erreur "Ollama non connecte"
Verifier qu'Ollama est lance:
```powershell
ollama serve
```

### Reinstaller les dependances
```powershell
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

---

## Architecture du Projet

```
BiasDetector/
├── backend/          # API FastAPI + Ollama + LanceDB
├── frontend/         # Interface Next.js
├── start.ps1         # Script de demarrage automatique
└── LISEZMOI.md       # Ce fichier
```

## Technologies Utilisees

- **Ollama** - IA locale (llama3.2, nomic-embed-text)
- **LanceDB** - Base de donnees vectorielle locale
- **MongoDB** - Stockage des analyses
- **FastAPI** - Backend Python
- **Next.js** - Frontend React
