# ⚡ Quick Start - Prova un Agente in 5 Minuti

## Per i Frrettolosi ⏱️

### 🎯 Opzione 1: Medical Agent (Più Facile)

```bash
# 1. Entra nella cartella
cd medical_agent

# 2. Setup ambiente
python3 -m venv venv && source venv/bin/activate

# 3. Installa dipendenze
pip install -r requirements.txt

# 4. Copia config (non hai bisogno di API key per testare!)
cp .env.example .env

# 5. Avvia!
python backend/app.py

# 6. Apri nel browser
# http://localhost:5000
```

**Fatto!** 🎉 Hai il tuo primo agente AI funzionante!

---

### 🎯 Opzione 2: Notebook Interattivi (Educativo)

```bash
# Dalla root del progetto
cd /home/engine/project

# Installa Jupyter
pip install jupyter

# Avvia
jupyter notebook

# Apri: Day_1b_Agent_Architectures.ipynb
```

**Leggi, modifica, impara!**

---

### 🎯 Opzione 3: BookSum Dataset (Dati)

```bash
cd alignments

# Vedi i dati
zcat chapter_summary_aligned_train.jsonl.gz | head -3 | python -m json.tool
```

---

## Cosa Puoi Fare Adesso?

| Azione | Comando |
|--------|---------|
| Modificare il prompts | Edit `backend/agent.py` |
| Aggiungere un nuovo tool | Crea una funzione in `backend/agent.py` |
| Cambiare il modello LLM | Modifica `OPENAI_API_KEY` in `.env` |
| Testare da CLI | `curl -X POST http://localhost:5000/api/ask -H "Content-Type: application/json" -d '{"question":"..."}' ` |

---

## 🆘 Problemi Comuni?

| Errore | Soluzione |
|--------|-----------|
| `ModuleNotFoundError` | `pip install -r requirements.txt` |
| `Address already in use` | `PORT=5001 python backend/app.py` |
| `No module named 'flask'` | Verifica che `(venv)` sia attivo nel prompt |
| API key error | Aggiungi il tuo API key in `.env` |

---

## 📚 Voglio Imparare di Più?

Leggi: **`COME_PROVARE_AGENTI_NOVIZIO.md`** (guida completa in italiano)

---

**Buona Fortuna! 🚀**
