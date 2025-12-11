# 🚀 Guida Rapida - Come Testare l'Agente

Questa è una guida rapida per testare l'agente Medical Research Assistant in modo semplice e veloce.

## 📋 Prerequisiti

Assicurati di avere:
- ✅ Python 3.8 o superiore installato
- ✅ Le dipendenze installate (vedi sotto se necessario)

## 🎯 Metodo 1: Script Bash (PIÙ SEMPLICE)

```bash
# Test base (veloce)
./testa_agente.sh base

# Test completo con API
./testa_agente.sh api

# Avvia server per test manuali
./testa_agente.sh manuale

# Mostra aiuto
./testa_agente.sh help
```

## 🐍 Metodo 2: Script Python

### Test Base (senza server)
```bash
python test_agente.py
```

**Tempo:** ~2 secondi  
**Output:** Test dell'agente con domande di esempio

### Test API (con server)
```bash
python test_agente_api.py
```

**Tempo:** ~10 secondi per i test, poi il server resta attivo  
**Output:** Test completi degli endpoint API

## 🌐 Metodo 3: Test Manuale con Server

### Passo 1: Avvia il server
```bash
cd medical_agent
python backend/app.py
```

### Passo 2: Apri un nuovo terminale e testa

**Health check:**
```bash
curl http://localhost:5000/health
```

**Esempio risposta:**
```json
{
  "status": "healthy",
  "agent": "ready"
}
```

**Fai una domanda:**
```bash
curl -X POST http://localhost:5000/api/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Cos'\''è il diabete?"}'
```

**Esempio risposta:**
```json
{
  "answer_text": "Processed answer for: Cos'è il diabete?...",
  "bullets": [
    "Observation 1: The input was received successfully.",
    "Observation 2: This is a placeholder...",
    "Observation 3: Always consult a qualified healthcare provider..."
  ],
  "source_links": [
    "https://pubmed.ncbi.nlm.nih.gov/",
    "https://www.who.int/"
  ],
  "disclaimer": "⚠️ DISCLAIMER: This information is for educational purposes only..."
}
```

## 🧪 Esempi di Domande da Testare

### Domande in Italiano
```bash
# Domanda generale
curl -X POST http://localhost:5000/api/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Quali sono i sintomi dell'\''influenza?"}'

# Domanda su trattamenti
curl -X POST http://localhost:5000/api/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Come si cura l'\''ipertensione?"}'

# Domanda su prevenzione
curl -X POST http://localhost:5000/api/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Come prevenire il raffreddore?"}'
```

### Domande in Inglese
```bash
curl -X POST http://localhost:5000/api/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What are the symptoms of diabetes?"}'

curl -X POST http://localhost:5000/api/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "How is hypertension treated?"}'
```

## 📊 Cosa Verificare

Quando esegui i test, verifica che:

✅ Il server si avvia senza errori  
✅ L'endpoint `/health` risponde con status 200  
✅ L'endpoint `/api/ask` accetta domande e risponde  
✅ La risposta contiene i campi: `answer_text`, `bullets`, `source_links`, `disclaimer`  
✅ Il disclaimer medico è presente  
✅ Le domande vuote vengono rifiutate (status 400)

## 🔧 Installazione Dipendenze (se necessario)

Se ricevi errori di moduli mancanti:

```bash
cd medical_agent
pip install -r requirements.txt
```

Oppure installa solo i pacchetti essenziali:

```bash
pip install flask flask-cors
```

## ⚡ Test Rapido in 30 Secondi

Esegui questo comando per un test completo automatico:

```bash
./testa_agente.sh base && echo "✅ AGENTE FUNZIONA CORRETTAMENTE!"
```

## 🆘 Problemi Comuni

### Errore: "command not found: ./testa_agente.sh"
```bash
chmod +x testa_agente.sh
```

### Errore: "ModuleNotFoundError"
```bash
cd medical_agent
pip install -r requirements.txt
```

### Errore: "Address already in use"
```bash
# Uccidi il processo sulla porta 5000
lsof -ti:5000 | xargs kill -9
```

### Porta 5000 già occupata
```bash
# Usa una porta diversa
PORT=5001 python backend/app.py
```

## 📚 Documentazione Completa

Per maggiori dettagli, consulta:
- **README Test Agente:** `README_TEST_AGENTE.md`
- **README Medical Agent:** `medical_agent/README.md`
- **Test Automatici (pytest):** `medical_agent/tests/`

## ✨ Risultato Atteso

Quando tutto funziona correttamente, dovresti vedere:

```
============================================================
TUTTI I TEST COMPLETATI CON SUCCESSO! ✓
============================================================
```

---

**🎉 Buon testing!**

⚠️ **Ricorda:** Questo agente è solo per scopi educativi e di ricerca.
Non sostituisce il consiglio medico professionale.
