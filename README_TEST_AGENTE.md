# Test Agente Medical Research Assistant

Questa guida spiega come testare l'agente e verificare che funzioni correttamente.

## 🚀 Test Rapido (Senza Server)

Per testare solo la funzionalità base dell'agente senza avviare il server:

```bash
python test_agente.py
```

Questo script:
- ✓ Verifica che i moduli si importino correttamente
- ✓ Inizializza l'agente
- ✓ Invia domande di test
- ✓ Verifica la struttura delle risposte

## 🌐 Test Completo (Con Server API)

Per testare il server Flask e gli endpoint API:

```bash
python test_agente_api.py
```

Questo script:
- ✓ Avvia automaticamente il server Flask
- ✓ Testa l'endpoint `/health`
- ✓ Testa l'endpoint `/api/ask` con varie domande
- ✓ Verifica la gestione degli errori
- ✓ Mantiene il server attivo per test manuali

**Nota:** Il server resterà attivo dopo i test. Premi `Ctrl+C` per terminarlo.

## 📝 Test Manuali

### 1. Avvia il server manualmente

```bash
cd medical_agent
python backend/app.py
```

### 2. Testa con curl

**Health check:**
```bash
curl http://localhost:5000/health
```

**Invia una domanda:**
```bash
curl -X POST http://localhost:5000/api/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Cos'\''è il diabete?"}'
```

### 3. Testa dal browser

Apri il browser e vai su:
- Health check: http://localhost:5000/health

## 🧪 Test con pytest

Se hai pytest installato, puoi eseguire i test automatici:

```bash
cd medical_agent
pytest tests/ -v
```

## 📊 Risultati Attesi

### Test Base (`test_agente.py`)

```
============================================================
TEST AGENTE MEDICAL RESEARCH ASSISTANT
============================================================

Test 1: Verifica importazione moduli...
✓ Modulo agent importato con successo

Test 2: Inizializzazione agente...
✓ Agente inizializzato con successo

Test 3: Invio domanda all'agente...
✓ Risposta ricevuta con successo

TUTTI I TEST COMPLETATI CON SUCCESSO! ✓
```

### Test API (`test_agente_api.py`)

```
============================================================
TEST API MEDICAL RESEARCH ASSISTANT
============================================================

Test 1: Avvio del server Flask...
✓ Server avviato con successo

Test 2: Health check endpoint...
✓ Health check OK

Test 3: Endpoint /api/ask con domanda valida...
✓ Test domanda valida OK

TUTTI I TEST API COMPLETATI CON SUCCESSO! ✓
```

## ⚠️ Risoluzione Problemi

### Errore: "ModuleNotFoundError"

Installa le dipendenze:
```bash
cd medical_agent
pip install -r requirements.txt
```

### Errore: "Address already in use" (porta 5000 occupata)

Termina il processo che usa la porta 5000:
```bash
# Linux/Mac
lsof -ti:5000 | xargs kill -9

# Oppure usa una porta diversa
PORT=5001 python backend/app.py
```

### Il server non si avvia

Verifica la versione di Python:
```bash
python --version  # Deve essere 3.8+
```

## 📚 Risorse Aggiuntive

- README completo: `medical_agent/README.md`
- Test automatici: `medical_agent/tests/`
- Documentazione API: `medical_agent/docs/`

## ⚕️ Disclaimer

Questo agente è solo per scopi educativi e di ricerca. Non sostituisce il consiglio medico professionale.
