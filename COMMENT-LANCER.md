# BiasDetector - Comment Lancer l'Application

## Version Ultra-Simple (Recommandé)

### Etape 1: Lance Docker Desktop
Ouvre l'application **Docker Desktop** sur ton ordinateur.
Attends qu'il soit completement demarre (l'icone devient verte).

### Etape 2: Lance le script
Ouvre PowerShell dans le dossier du projet et tape:

```powershell
.\LANCE-MOI.ps1
```

**C'EST TOUT!** Le script fait TOUT automatiquement:
- Lance MongoDB
- Verifie Ollama
- Lance le backend
- Lance le frontend
- Ouvre ton navigateur

---

## Problemes Courants

### Docker ne marche pas
**Solution:** Lance Docker Desktop manuellement, attends qu'il soit pret (icone verte), puis relance le script.

### Ollama ne marche pas
**Solution:**
1. Ouvre un terminal
2. Tape: `ollama serve`
3. Relance le script

### Les modeles ne sont pas telecharges
**Solution:** Le script les telecharge automatiquement. Si ca ne marche pas:
```powershell
ollama pull llama3.2
ollama pull nomic-embed-text
```

---

## Acces a l'Application

Une fois lance:
- **Application:** http://localhost:3000
- **API Backend:** http://localhost:8000
- **Documentation API:** http://localhost:8000/docs

---

## Pour Arreter

Ferme toutes les fenetres PowerShell qui se sont ouvertes.

Pour arreter MongoDB:
```powershell
docker stop mongodb
```

---

## Premiere Installation

Si c'est la premiere fois, installe d'abord:

1. **Docker Desktop:** https://www.docker.com/products/docker-desktop/
2. **Ollama:** https://ollama.ai

Ensuite lance le script d'installation:
```powershell
.\install.ps1
```

Puis lance l'application:
```powershell
.\LANCE-MOI.ps1
```
