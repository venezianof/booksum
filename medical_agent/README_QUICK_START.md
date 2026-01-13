# Medical Research Agent - Quick Start Guide

## ✅ L'agente è ora completamente funzionante!

L'agente medico è stato implementato con successo e include:

- 🚀 **Server Flask funzionante** con API REST
- 🤖 **Agente LangChain intelligente** con Mock LLM (non richiede API key)
- 🎨 **Interfaccia web moderna** con design elegante
- 🔍 **Integrazione PubMed reale** per fonti mediche
- 📚 **Tool Wikipedia** per informazioni generali

---

## 🚀 Avvio Rapido (3 passi)

### 1. Attiva l'ambiente virtuale

```bash
cd /home/engine/project/medical_agent
source venv/bin/activate
```

### 2. Avvia il server

```bash
python run_server.py
```

oppure:

```bash
python backend/app.py
```

### 3. Apri il browser

Vai su: **http://localhost:5000**

---

## 🎯 Test Rapidi

### Test dall'interfaccia web

1. Apri http://localhost:5000 nel browser
2. Vedrai un'interfaccia con esempi di domande
3. Clicca su un esempio (es. "What is diabetes?")
4. Vedrai una risposta strutturata con:
   - Testo principale
   - Bullet points chiave
   - Link a fonti PubMed reali
   - Disclaimer medico

### Test via API (curl)

```bash
curl -X POST http://localhost:5000/api/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is diabetes?"}'
```

### Test Health Check

```bash
curl http://localhost:5000/health
```

Risposta attesa: `{"agent":"ready","status":"healthy"}`

### Test Python

```bash
python test_agent.py
```

---

## 📋 Domande di Esempio Funzionanti

L'agente Mock LLM è pre-configurato con risposte mediche accurate per:

✅ **Diabete**
- "What is diabetes?"
- "Tell me about diabetes"
- "What are diabetes symptoms?"

✅ **Ipertensione**  
- "What are the symptoms of hypertension?"
- "Tell me about high blood pressure"
- "What causes hypertension?"

✅ **Aspirina**
- "How does aspirin work?"
- "What is aspirin used for?"
- "Tell me about aspirin"

✅ **Qualsiasi altra domanda medica**
- Riceverai una risposta generica con raccomandazioni

---

## 🏗️ Architettura Implementata

```
┌─────────────────────────────────────────┐
│     Web Browser (localhost:5000)        │
│     Interfaccia HTML/CSS/JavaScript     │
└─────────────────┬───────────────────────┘
                  │ HTTP REST API
┌─────────────────▼───────────────────────┐
│          Flask Server (app.py)          │
│  • /health - Health check               │
│  • /api/ask - Ask questions             │
│  • / - Serve interfaccia web            │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│    Medical Research Agent (agent.py)    │
│  • Mock LLM (no API key required)       │
│  • Pattern matching per domande comuni  │
│  • LangChain ReAct agent structure      │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│              Tools Layer                │
│  • search_pubmed() - NCBI API reale     │
│  • search_medical_info() - Wikipedia    │
└─────────────────────────────────────────┘
```

---

## 📦 Cosa è Stato Implementato

### ✅ Backend (`backend/agent.py`)

- **MockLLM**: LLM simulato che non richiede API key
  - Risposte pre-programmate per domande comuni
  - Pattern matching intelligente
  - Supporto per domande generiche

- **search_pubmed()**: Tool funzionante che interroga l'API NCBI
  - Restituisce link reali a articoli PubMed
  - Nessuna API key richiesta
  - Gestione errori robusta

- **search_medical_info()**: Tool Wikipedia
  - Cerca informazioni mediche generali
  - Fallback se PubMed non trova risultati

- **MedicalResearchAgent**: Classe principale
  - Inizializza tools LangChain
  - Supporta sia Mock LLM che LLM reali (OpenAI, Anthropic)
  - Estrae answer, bullets e sources dalle risposte

### ✅ API Server (`backend/app.py`)

- **Flask app** con CORS abilitato
- **Endpoints**:
  - `GET /health` - Status check
  - `POST /api/ask` - Ask medical questions
  - `GET /` - Serve interfaccia web

- **Error handling** robusto
- **Logging** configurato
- **Static file serving** per HTML/CSS/JS

### ✅ Interfaccia Web (`backend/static/index.html`)

- **Design moderno** con gradiente viola
- **Responsive** per mobile e desktop
- **Features**:
  - Health check automatico all'avvio
  - Esempi di domande cliccabili
  - Chat interface con messaggi user/agent
  - Visualizzazione strutturata di:
    - Testo risposta
    - Bullet points
    - Links a fonti (PubMed, WHO, CDC)
  - Animazioni smooth
  - Loading spinner durante il processing
  - Disclaimer medico sempre visibile

### ✅ Scripts Utility

- `test_agent.py` - Test rapido dell'agente
- `run_server.py` - Avvia il server (configurazione semplificata)
- `GUIDA_ITALIANA.md` - Guida in italiano
- `README_QUICK_START.md` - Questa guida

---

## 🔧 Configurazione

### Ambiente Virtuale (già configurato)

```bash
# Già fatto, ma se serve ricrearlo:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Dipendenze Installate

- Flask 3.0.0 + Flask-CORS
- LangChain 0.1.0 + LangChain-Community
- requests, wikipedia, beautifulsoup4
- pytest per testing

### Variabili d'Ambiente (opzionali)

Per usare un LLM reale invece del Mock LLM:

```bash
# Copia il file di esempio
cp .env.example .env

# Modifica .env e aggiungi:
OPENAI_API_KEY=your-actual-api-key-here
```

L'agente rileverà automaticamente la chiave e userà OpenAI invece del Mock LLM.

---

## 🎨 Caratteristiche dell'Interfaccia

### Design
- Gradiente viola moderno (#667eea → #764ba2)
- Font system standard per performance
- Box shadow e animazioni eleganti
- Responsive design

### UX Features
- Health check visivo (verde = ok, rosso = errore)
- 4 domande di esempio pre-configurate
- Chat interface con messaggi distinti per user e agent
- Scroll automatico ai nuovi messaggi
- Loading spinner durante le richieste
- Error handling user-friendly

### Accessibilità
- Disclaimer medico ben visibile
- Links esterni con target="_blank"
- Keyboard support (Enter per inviare)
- Clear visual feedback per tutti gli stati

---

## 📊 Esempi di Output

### Domanda: "What is diabetes?"

**Answer:**
```
Diabetes is a chronic metabolic disorder characterized by high blood sugar levels.
There are two main types:

Common symptoms include increased thirst, frequent urination, extreme fatigue,
blurred vision, and slow wound healing. Treatment typically involves lifestyle
modifications, blood glucose monitoring, and medication (insulin or oral medications).

For accurate diagnosis and treatment, please consult a healthcare provider.
```

**Bullets:**
- Type 1 diabetes: An autoimmune condition where the pancreas produces little or no insulin
- Type 2 diabetes: A condition where the body becomes resistant to insulin or doesn't produce enough insulin

**Sources:**
- https://pubmed.ncbi.nlm.nih.gov/41373033/ (PubMed reale)
- https://pubmed.ncbi.nlm.nih.gov/41373013/ (PubMed reale)
- https://pubmed.ncbi.nlm.nih.gov/41372993/ (PubMed reale)
- https://www.who.int/
- https://www.cdc.gov/

---

## 🚨 Troubleshooting

### Server non si avvia

```bash
# Verifica che la porta 5000 sia libera
lsof -i:5000

# Uccidi processi sulla porta 5000
lsof -ti:5000 | xargs kill -9

# Oppure usa una porta diversa
PORT=5001 python run_server.py
```

### ModuleNotFoundError

```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Import errors

Se vedi errori di import, assicurati di essere nella directory corretta:

```bash
cd /home/engine/project/medical_agent
python run_server.py
```

---

## 🎓 Come Funziona il Mock LLM

Il `MockLLM` implementato in `backend/agent.py` simula un LLM reale:

1. **Pattern Matching**: Cerca parole chiave nella domanda
2. **Risposte Pre-programmate**: Ha risposte dettagliate per:
   - Diabete
   - Ipertensione  
   - Aspirina
   - Domande generiche
3. **Formato LangChain**: Usa il formato "Thought/Action/Observation/Final Answer"
4. **Estensibile**: Facile aggiungere nuove domande nel metodo `_generate_medical_response()`

### Upgrade a LLM Reale

Per passare a OpenAI o Anthropic:

1. Aggiungi API key nel `.env`
2. L'agente rileverà automaticamente la chiave
3. Userà `ChatOpenAI` invece di `MockLLM`
4. Tutto il resto rimane identico

---

## 📝 Note Importanti

⚠️ **MEDICAL DISCLAIMER**

Questo strumento è SOLO per scopi educativi e di ricerca. NON è un sostituto per consulenza medica professionale. Consulta sempre un medico qualificato per decisioni mediche.

---

## ✅ Checklist Completamento

- [x] Implementato MockLLM funzionante
- [x] Implementato MedicalResearchAgent con LangChain
- [x] Tool PubMed funzionante con API NCBI reale
- [x] Tool Wikipedia funzionante
- [x] Server Flask con endpoints REST
- [x] Interfaccia web moderna e responsive
- [x] Health check endpoint
- [x] Error handling completo
- [x] Logging configurato
- [x] Test script funzionante
- [x] Documentazione completa
- [x] Guida in italiano

---

## 🎉 L'Agente Funziona!

Per qualsiasi domanda o problema, consulta:
- Questo README
- `GUIDA_ITALIANA.md` (in italiano)
- `README.md` (documentazione completa del progetto)
- I log del server (`server.log`)

**Buon utilizzo del Medical Research Agent! 🏥🤖**
