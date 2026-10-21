# 🧠 BiasDetector - Détection Intelligente de Biais avec RAG

BiasDetector est un outil d'analyse de documents qui utilise l'Intelligence Artificielle locale pour détecter automatiquement différents types de biais dans les textes.

![100% Local](https://img.shields.io/badge/100%25-Local-green)
![No API Keys](https://img.shields.io/badge/No-API%20Keys-blue)
![Privacy First](https://img.shields.io/badge/Privacy-First-purple)

---

## 📚 Table des Matières

- [Qu'est-ce que BiasDetector?](#-quest-ce-que-biasdetector)
- [Fonctionnalités](#-fonctionnalités)
- [Types de Biais Détectés](#-types-de-biais-détectés)
- [Architecture et Technologie](#-architecture-et-technologie)
- [Installation](#-installation)
- [Lancement Rapide](#-lancement-rapide)
- [Configuration Avancée](#-configuration-avancée)
- [Structure du Projet](#-structure-du-projet)
- [API Documentation](#-api-documentation)
- [Troubleshooting](#-troubleshooting)

---

## 🎯 Qu'est-ce que BiasDetector?

**BiasDetector** est un système d'analyse de documents qui détecte automatiquement les biais cognitifs et sociaux dans les textes. Il utilise:

- **L'IA 100% Locale** - Ollama avec llama3.2 (pas de cloud, pas d'API keys)
- **RAG (Retrieval Augmented Generation)** - Analyse contextuelle basée sur l'historique
- **Base Vectorielle Locale** - LanceDB pour la recherche sémantique
- **Privacy-First** - Vos documents ne quittent jamais votre machine

### Comment ça marche?

1. **Upload** - Tu uploades un document (PDF, TXT, DOCX)
2. **Vectorisation** - Le texte est découpé en chunks et vectorisé
3. **RAG** - Le système cherche des contextes similaires dans tes documents précédents
4. **Analyse IA** - Ollama analyse le document avec le contexte RAG
5. **Résultats** - Tu obtiens un rapport détaillé des biais détectés avec des exemples

---

## ✨ Fonctionnalités

### 🔍 Analyse de Documents
- Upload de PDF, TXT, DOCX
- Détection de 6 types de biais majeurs
- Score global de biais (0-100)
- Instances spécifiques avec citations
- Suggestions d'amélioration

### 🤖 RAG (Retrieval Augmented Generation)
- **Mémoire contextuelle** - Compare avec tes documents précédents
- **Insights comparatifs** - "Ce document est plus biaisé que 80% de ta bibliothèque"
- **Recherche sémantique** - Trouve des documents similaires
- **Q&A intelligent** - Pose des questions sur tes analyses

### 💬 Chat RAG
- Pose des questions sur les patterns de biais
- Obtiens des insights sur ton historique
- Comprends mieux les tendances

### 📊 Historique et Statistiques
- Tous tes documents analysés
- Tendances des biais au fil du temps
- Stats par type de biais
- Évolution du score moyen

---

## 🎭 Types de Biais Détectés

| Biais | Description | Exemple |
|-------|-------------|---------|
| **Genre** | Stéréotypes basés sur le genre | "Les femmes sont trop émotionnelles pour diriger" |
| **Politique** | Orientation politique partisane | "Seuls les conservateurs comprennent l'économie" |
| **Culturel** | Ethnocentrisme, suppositions culturelles | "La culture occidentale est supérieure" |
| **Confirmation** | Cherche des infos qui confirment ses croyances | "J'ai trouvé un article qui prouve que j'ai raison" |
| **Sélection** | Cherry-picking de données | "90% des gens interrogés... (sur 10 personnes)" |
| **Ancrage** | Dépendance excessive à l'info initiale | "Le premier prix annoncé était 1000€, donc 800€ c'est une affaire" |

---

## 🏗️ Architecture et Technologie

### Stack Technique

#### Backend
- **FastAPI** - API REST moderne et rapide
- **Ollama** - Serveur d'IA local (llama3.2 pour l'analyse, nomic-embed-text pour les embeddings)
- **LanceDB** - Base vectorielle locale (768 dimensions)
- **MongoDB** - Stockage des analyses et métadonnées
- **Python 3.11+**

#### Frontend
- **Next.js 14** - Framework React avec App Router
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling moderne avec animations
- **Lucide Icons** - Icônes élégantes
- **Recharts** - Visualisations de données

### Architecture RAG

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend (Next.js)                    │
│  [Upload] [Analyze] [Search] [Chat] [History] [Stats]      │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTP REST API
┌──────────────────────────┴──────────────────────────────────┐
│                    Backend (FastAPI)                         │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐            │
│  │  Ollama    │  │  LanceDB   │  │  MongoDB   │            │
│  │  Service   │  │  Service   │  │  Service   │            │
│  └─────┬──────┘  └─────┬──────┘  └─────┬──────┘            │
│        │               │               │                     │
│  ┌─────┴───────────────┴───────────────┴──────┐            │
│  │          RAG Service                        │            │
│  │  1. Retrieve context from LanceDB          │            │
│  │  2. Enhance prompt with context            │            │
│  │  3. Generate analysis with Ollama          │            │
│  └─────────────────────────────────────────────┘            │
└──────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────┐
│                   Local Services                              │
│  ┌───────────────┐  ┌────────────────┐  ┌────────────────┐ │
│  │ Ollama        │  │ LanceDB        │  │ MongoDB        │ │
│  │ Port: 11434   │  │ ./lancedb      │  │ Port: 27017    │ │
│  │ llama3.2      │  │ (persistent)   │  │ (Docker)       │ │
│  │ nomic-embed   │  │                │  │                │ │
│  └───────────────┘  └────────────────┘  └────────────────┘ │
└──────────────────────────────────────────────────────────────┘
```

### Flux RAG Détaillé

1. **Upload Document** → Text extraction (PDF/DOCX/TXT)
2. **Chunking** → Split en chunks de 1000 chars (200 overlap)
3. **Embedding** → Ollama nomic-embed-text génère des vecteurs 768-dim
4. **Storage** → Vectors stockés dans LanceDB
5. **RAG Retrieval** → Cherche les top-5 chunks similaires
6. **Prompt Enhancement** → Ajoute le contexte au prompt
7. **Analysis** → Ollama llama3.2 analyse avec contexte
8. **Persistence** → Résultats sauvés dans MongoDB

---

## 📦 Installation

### Prérequis

| Logiciel | Version | Lien | Obligatoire |
|----------|---------|------|-------------|
| **Python** | 3.11+ | [python.org](https://python.org) | ✅ Oui |
| **Node.js** | 18+ | [nodejs.org](https://nodejs.org) | ✅ Oui |
| **Docker Desktop** | Latest | [docker.com](https://www.docker.com/products/docker-desktop/) | ✅ Oui |
| **Ollama** | Latest | [ollama.ai](https://ollama.ai) | ✅ Oui |
| **Git** | Latest | [git-scm.com](https://git-scm.com) | ⚠️ Recommandé |

### Installation Étape par Étape

#### 1. Cloner le projet

```bash
git clone https://github.com/your-username/BiasDetector.git
cd BiasDetector
```

Ou télécharge le ZIP et extrais-le.

#### 2. Installer Ollama

**Windows:**
- Télécharge depuis [ollama.ai](https://ollama.ai)
- Installe l'application
- Ouvre un terminal et télécharge les modèles:

```powershell
ollama pull llama3.2
ollama pull nomic-embed-text
```

**macOS/Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull llama3.2
ollama pull nomic-embed-text
```

#### 3. Installer Docker Desktop

- Télécharge depuis [docker.com](https://www.docker.com/products/docker-desktop/)
- Installe et lance Docker Desktop
- Attends que l'icône soit verte (prêt)

#### 4. Installer les dépendances

**Backend:**
```powershell
cd backend
python -m venv venv

# Windows
.\venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
```

**Frontend:**
```powershell
cd ../frontend
npm install
cp .env.example .env.local
```

---

## 🚀 Lancement Rapide

### Option 1: Script Automatique (Recommandé)

**Windows:**
```powershell
.\LANCE-FINAL.ps1
```

Le script fait TOUT automatiquement:
- ✅ Lance Docker et MongoDB
- ✅ Vérifie/lance Ollama
- ✅ Démarre le backend (port 8000)
- ✅ Démarre le frontend (port 3000)
- ✅ Ouvre ton navigateur

### Option 2: Lancement Manuel

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
cd backend
.\venv\Scripts\activate
uvicorn main:app --reload
```

**Terminal 4 - Frontend:**
```powershell
cd frontend
npm run dev
```

### Accès à l'Application

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Docs (Swagger):** http://localhost:8000/docs
- **API Docs (ReDoc):** http://localhost:8000/redoc

---

## ⚙️ Configuration Avancée

### Variables d'Environnement

**Backend (.env):**
```env
# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2              # ou mistral, phi3
OLLAMA_EMBEDDING_MODEL=nomic-embed-text

# LanceDB Configuration
CHROMA_PERSIST_DIR=./lancedb       # Chemin de stockage
EMBEDDING_DIMENSION=768            # Dimension des vecteurs

# MongoDB Configuration
MONGODB_URL=mongodb://localhost:27017
MONGODB_DATABASE=biasdetector

# RAG Configuration
RAG_ENABLED=True
RAG_MAX_CONTEXT_CHUNKS=5          # Nombre de chunks récupérés
RAG_RELEVANCE_THRESHOLD=0.7       # Seuil de similarité

# File Upload
MAX_UPLOAD_SIZE=10485760          # 10MB
UPLOAD_DIR=./uploads
```

**Frontend (.env.local):**
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Changer de Modèle Ollama

Pour utiliser un autre modèle:

```powershell
# Télécharger le modèle
ollama pull mistral

# Modifier .env
OLLAMA_MODEL=mistral
```

Modèles recommandés:
- `llama3.2` - Équilibré (4GB) ⭐ Recommandé
- `mistral` - Très bon (4GB)
- `phi3` - Rapide mais moins précis (2GB)
- `llama3` - Plus puissant (8GB)

---

## 📁 Structure du Projet

```
BiasDetector/
├── backend/                    # Backend FastAPI
│   ├── app/
│   │   ├── api/
│   │   │   └── endpoints/     # Routes API
│   │   │       ├── analysis.py      # Analyse de documents
│   │   │       ├── documents.py     # Gestion documents
│   │   │       ├── rag.py          # RAG Q&A
│   │   │       └── search.py       # Recherche sémantique
│   │   ├── core/
│   │   │   ├── config.py      # Configuration
│   │   │   └── dependencies.py
│   │   ├── models/            # Schémas Pydantic
│   │   ├── services/          # Logique métier
│   │   │   ├── ollama_service.py   # Service IA local
│   │   │   ├── chroma_service.py   # Service LanceDB
│   │   │   ├── rag_service.py      # Service RAG
│   │   │   └── database_service.py # Service MongoDB
│   │   └── utils/
│   ├── main.py               # Point d'entrée FastAPI
│   ├── requirements.txt      # Dépendances Python
│   └── .env                 # Configuration
│
├── frontend/                  # Frontend Next.js
│   ├── src/
│   │   ├── app/
│   │   │   ├── page.tsx      # Page principale
│   │   │   └── layout.tsx
│   │   ├── components/        # Composants React
│   │   │   ├── analysis/     # Composants d'analyse
│   │   │   ├── history/      # Historique
│   │   │   ├── rag/          # Chat RAG
│   │   │   ├── search/       # Recherche
│   │   │   ├── stats/        # Statistiques
│   │   │   └── ui/           # Composants UI
│   │   ├── hooks/            # Custom React hooks
│   │   ├── lib/              # Utilitaires
│   │   ├── styles/           # Styles CSS
│   │   └── types/            # Types TypeScript
│   ├── package.json
│   └── .env.local
│
├── LANCE-FINAL.ps1           # Script de lancement
├── LISEZ-MOI-SIMPLE.txt      # Guide simplifié
└── README.md                 # Ce fichier
```

---

## 📡 API Documentation

### Endpoints Principaux

#### Documents

**Upload Document**
```http
POST /api/v1/documents/upload
Content-Type: multipart/form-data

file: <fichier PDF/TXT/DOCX>
```

**List Documents**
```http
GET /api/v1/documents/list
```

**Delete Document**
```http
DELETE /api/v1/documents/{document_id}
```

#### Analysis

**Analyze Document**
```http
POST /api/v1/analysis/analyze
Content-Type: application/json

{
  "document_id": "abc123",
  "use_rag": true
}
```

Response:
```json
{
  "analysis_id": "xyz789",
  "document_id": "abc123",
  "overall_bias_score": 45.5,
  "bias_instances": [
    {
      "type": "gender",
      "severity": "high",
      "text": "Women are too emotional...",
      "explanation": "...",
      "suggestion": "..."
    }
  ],
  "rag_metadata": {
    "context_used": true,
    "num_reference_chunks": 5,
    "reference_documents": ["doc1", "doc2"]
  },
  "comparative_insights": "This document shows 30% more bias..."
}
```

**Get All Analyses**
```http
GET /api/v1/analysis/all
```

#### Search

**Semantic Search**
```http
POST /api/v1/search
Content-Type: application/json

{
  "query": "documents about gender bias",
  "top_k": 5
}
```

#### RAG

**Ask Question**
```http
POST /api/v1/rag/ask
Content-Type: application/json

{
  "question": "What are the most common bias patterns?"
}
```

**Get Statistics**
```http
GET /api/v1/rag/statistics
```

Pour la documentation complète interactive, visite: http://localhost:8000/docs

---

## 🔧 Troubleshooting

### Problèmes Courants

#### 1. Docker ne démarre pas
**Symptôme:** `docker: error during connect`

**Solutions:**
- Lance Docker Desktop manuellement
- Attends que l'icône soit verte
- Relance le script

#### 2. Ollama ne répond pas
**Symptôme:** `Connection refused on port 11434`

**Solutions:**
```powershell
# Dans un nouveau terminal
ollama serve
```

#### 3. Port déjà utilisé
**Symptôme:** `Port 3000 is already in use`

**Solutions:**
```powershell
# L'app s'ouvre automatiquement sur localhost:3001

# Ou pour tuer le processus:
Get-Process -Id (Get-NetTCPConnection -LocalPort 3000).OwningProcess | Stop-Process
```

#### 4. Modèles Ollama manquants
**Symptôme:** `Model llama3.2 not found`

**Solutions:**
```powershell
ollama pull llama3.2
ollama pull nomic-embed-text
```

#### 5. MongoDB ne démarre pas
**Symptôme:** `MongoServerError: connection refused`

**Solutions:**
```powershell
# Arrêter et supprimer l'ancien conteneur
docker stop mongodb
docker rm mongodb

# Relancer
docker run -d -p 27017:27017 --name mongodb mongo:latest
```

#### 6. Erreurs Backend Python
**Symptôme:** `ModuleNotFoundError`

**Solutions:**
```powershell
cd backend
.\venv\Scripts\activate
pip install -r requirements.txt --upgrade
```

#### 7. Erreurs Frontend npm
**Symptôme:** `Cannot find module`

**Solutions:**
```powershell
cd frontend
rm -rf node_modules package-lock.json
npm install
```

---

## 🎓 Cas d'Usage

### Exemple 1: Analyser un Article de Presse

1. Ouvre l'app sur http://localhost:3000
2. Clique sur "Upload Document"
3. Sélectionne ton article (PDF/TXT)
4. Clique sur "Analyze with Local AI"
5. Consulte les biais détectés avec citations exactes

### Exemple 2: Comparer des Documents

1. Analyse plusieurs documents sur le même sujet
2. Va dans l'onglet "History"
3. Compare les scores de biais
4. Utilise "RAG Chat" pour poser: "Quelles sont les différences de biais entre mes 3 derniers documents?"

### Exemple 3: Recherche Sémantique

1. Onglet "Search"
2. Tape: "documents with gender bias"
3. Le système trouve tous les documents similaires sémantiquement
4. Pas besoin de mots-clés exacts!

---

## 🤝 Contribution

Ce projet est développé pour le cours IA&BD/CCV.

### Améliorations Futures Possibles

- [ ] Support de plus de formats (EPUB, HTML)
- [ ] Export des rapports en PDF
- [ ] Interface multilingue
- [ ] Mode hors-ligne complet
- [ ] Intégration avec d'autres LLMs locaux
- [ ] Dashboard analytics avancé

---

## 📄 Licence

MIT License - Libre d'utilisation

---

## 👥 Auteurs

Projet académique - Spécialisation IA&BD/CCV

---

## 🌟 Pourquoi BiasDetector?

✅ **100% Local** - Pas de cloud, pas de frais, pas de latence
✅ **Privacy-First** - Tes données restent chez toi
✅ **RAG Intelligence** - Apprend de ton historique
✅ **Open Source** - Code transparent et auditable
✅ **Pas d'API Keys** - Aucune dépendance externe
✅ **Rapide** - IA locale = réponse instantanée

---

## 📞 Support

**Pour lancer l'app:**
```powershell
.\LANCE-FINAL.ps1
```

**Documentation complète:** http://localhost:8000/docs (une fois lancé)

**Logs:** Les 4 fenêtres PowerShell montrent tous les logs en temps réel

---

🎉 **Bonne analyse de biais!**
