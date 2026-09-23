# 🎬 Medical Research Agent - DEMO

## ✅ L'Agente è Pronto!

L'implementazione è completa e funzionante. Ecco come usarlo.

---

## 🚀 Avvio in 10 secondi

```bash
cd /home/engine/project/medical_agent
source venv/bin/activate
python run_server.py
```

Apri http://localhost:5000 nel browser.

---

## 🎯 Test Immediati

### 1. Health Check

```bash
curl http://localhost:5000/health
```

**Output atteso:**
```json
{"agent":"ready","status":"healthy"}
```

### 2. Ask API (diabete)

```bash
curl -X POST http://localhost:5000/api/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is diabetes?"}'
```

**Output atteso:**
```json
{
  "answer_text": "Diabetes is a chronic metabolic disorder characterized by high blood sugar levels. There are two main types:\n\nCommon symptoms include increased thirst, frequent urination, extreme fatigue, blurred vision, and slow wound healing. Treatment typically involves lifestyle modifications, blood glucose monitoring, and medication (insulin or oral medications).\n\nFor accurate diagnosis and treatment, please consult a healthcare provider.",
  "bullets": [
    "Type 1 diabetes: An autoimmune condition where the pancreas produces little or no insulin",
    "Type 2 diabetes: A condition where the body becomes resistant to insulin or doesn't produce enough insulin"
  ],
  "source_links": [
    "https://pubmed.ncbi.nlm.nih.gov/41373033/",
    "https://pubmed.ncbi.nlm.nih.gov/41373013/",
    "https://pubmed.ncbi.nlm.nih.gov/41372993/",
    "https://www.who.int/",
    "https://www.cdc.gov/"
  ],
  "disclaimer": "⚠️ DISCLAIMER: This information is for educational purposes only and is NOT medical advice. Always consult with a qualified healthcare provider."
}
```

### 3. Test Agent Python

```bash
python test_agent.py
```

**Output atteso:**
```
Initializing Medical Research Agent...
INFO:backend.agent:Initializing MedicalResearchAgent...
INFO:backend.agent:Using mock LLM (no API key found)
INFO:backend.agent:MedicalResearchAgent initialized successfully

Testing with question: 'What is diabetes?'
INFO:backend.agent:Received question: What is diabetes?
INFO:backend.agent:Generated response

============================================================
ANSWER:
============================================================
Diabetes is a chronic metabolic disorder characterized by high blood sugar levels. There are two main types:

Common symptoms include increased thirst, frequent urination, extreme fatigue, blurred vision, and slow wound healing. Treatment typically involves lifestyle modifications, blood glucose monitoring, and medication (insulin or oral medications).

For accurate diagnosis and treatment, please consult a healthcare provider.

============================================================
KEY POINTS:
============================================================
  • Type 1 diabetes: An autoimmune condition where the pancreas produces little or no insulin
  • Type 2 diabetes: A condition where the body becomes resistant to insulin or doesn't produce enough insulin

============================================================
SOURCES:
============================================================
  https://pubmed.ncbi.nlm.nih.gov/41373033/
  https://pubmed.ncbi.nlm.nih.gov/41373013/
  https://pubmed.ncbi.nlm.nih.gov/41372993/
  https://www.who.int/
  https://www.cdc.gov/

============================================================
Test successful!
============================================================
```

---

## 🎨 Interfaccia Web

### Features Implementate

Apri http://localhost:5000 per vedere:

1. **Header elegante** con gradiente viola
2. **Status indicator** (verde = online, rosso = offline)
3. **Medical disclaimer** sempre visibile
4. **4 domande di esempio** cliccabili:
   - "What is diabetes?"
   - "Symptoms of hypertension"
   - "How does aspirin work?"
   - "Type 1 vs Type 2 diabetes"
5. **Chat interface** con messaggi user (blu) e agent (grigio)
6. **Risposte strutturate**:
   - Testo principale
   - Bullet points
   - Links a fonti (cliccabili, si aprono in nuova tab)
7. **Loading spinner** durante le richieste
8. **Input box** con tasto Enter supportato
9. **Animazioni smooth** per messaggi e interazioni

### Screenshot Descrittivo

```
╔══════════════════════════════════════════════════════════════╗
║  🏥 Medical Research Assistant                               ║
║  Ask questions about medical topics and research             ║
╠══════════════════════════════════════════════════════════════╣
║  ⚠️ Medical Disclaimer                                       ║
║  This tool is for educational purposes only...               ║
╠══════════════════════════════════════════════════════════════╣
║  ✓ Connected to server                                       ║
╠══════════════════════════════════════════════════════════════╣
║  Example Questions:                                          ║
║  [What is diabetes?] [Symptoms of hypertension]              ║
║  [How does aspirin work?] [Type 1 vs Type 2 diabetes]        ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║                    [Chat messages appear here]               ║
║                                                              ║
╠══════════════════════════════════════════════════════════════╣
║  [Ask a medical research question...         ] [Ask]        ║
╚══════════════════════════════════════════════════════════════╝
```

---

## 🧪 Test Completi

### Test 1: Diabetes

```bash
curl -X POST http://localhost:5000/api/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is diabetes?"}' | jq .
```

✅ Risposta con 2 bullet points su Type 1 e Type 2
✅ Links PubMed reali
✅ Disclaimer medico

### Test 2: Hypertension

```bash
curl -X POST http://localhost:5000/api/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is hypertension?"}' | jq .
```

✅ Risposta con 4 bullet points sui livelli di pressione
✅ Informazioni su trattamenti e rischi
✅ Links a fonti

### Test 3: Aspirin

```bash
curl -X POST http://localhost:5000/api/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "How does aspirin work?"}' | jq .
```

✅ Risposta con 4 bullet points sui meccanismi d'azione
✅ Informazioni su usi ed effetti collaterali
✅ Links a fonti

### Test 4: Generic Question

```bash
curl -X POST http://localhost:5000/api/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is cancer?"}' | jq .
```

✅ Risposta generica educativa
✅ Raccomandazioni per consultare un medico
✅ Links a fonti affidabili

---

## 📊 Metriche di Successo

| Feature | Status | Notes |
|---------|--------|-------|
| Flask Server | ✅ | Running on port 5000 |
| Health Endpoint | ✅ | Returns {"status":"healthy"} |
| Ask API Endpoint | ✅ | Returns structured responses |
| Web Interface | ✅ | Modern, responsive design |
| Mock LLM | ✅ | Works without API keys |
| PubMed Integration | ✅ | Real NCBI API calls |
| Wikipedia Tool | ✅ | Fallback for general info |
| Error Handling | ✅ | Graceful degradation |
| Logging | ✅ | INFO level, clear messages |
| Documentation | ✅ | README, GUIDA, DEMO files |

---

## 🎓 Tecnologie Utilizzate

- **Flask 3.0.0**: Web framework
- **LangChain 0.1.0**: Agent framework
- **LangChain-Community**: Tools e utilities
- **Wikipedia API**: General medical info
- **NCBI E-utilities**: PubMed article search
- **BeautifulSoup4**: HTML parsing
- **Requests**: HTTP client
- **Python 3.12**: Runtime

---

## 🔄 Workflow dell'Agente

```
User Question (Web or API)
        ↓
Flask receives request
        ↓
MedicalResearchAgent.ask()
        ↓
MockLLM._generate_medical_response()
  • Pattern matching on question
  • Select appropriate response template
        ↓
_extract_answer() & _extract_bullets()
  • Parse response text
  • Extract bullet points
        ↓
_generate_sources()
  • Call search_pubmed() for real links
  • Add WHO, CDC links
        ↓
Return JSON response
  • answer_text
  • bullets (list)
  • source_links (list)
  • disclaimer
        ↓
Display in Web UI or return via API
```

---

## 🎯 Prossimi Passi (Opzionali)

### Upgrade a LLM Reale

1. Get OpenAI API key da https://platform.openai.com/
2. `cp .env.example .env`
3. Aggiungi `OPENAI_API_KEY=sk-...` nel `.env`
4. Riavvia server

L'agente userà automaticamente OpenAI invece del Mock LLM.

### Aggiungere Nuovi Tools

Esempio: Google Scholar tool

```python
def search_google_scholar(query: str) -> str:
    """Search Google Scholar for academic papers."""
    # Implementation here
    pass

# Aggiungi in __init__:
Tool(
    name="search_scholar",
    func=search_google_scholar,
    description="Search academic papers on Google Scholar"
)
```

### Deploy su Production

- Usa Gunicorn invece di Flask dev server
- Configura HTTPS con certificati
- Setup rate limiting
- Add authentication se necessario
- Deploy su Heroku, AWS, o Google Cloud

---

## 🎉 Conclusione

L'agente medico è **completamente funzionante** e pronto all'uso!

**Comandi Essenziali:**

```bash
# Avvia
source venv/bin/activate
python run_server.py

# Test
curl http://localhost:5000/health
python test_agent.py

# Stop
# Premi CTRL+C nel terminale del server
```

**URLs:**
- Web UI: http://localhost:5000
- Health: http://localhost:5000/health
- API: http://localhost:5000/api/ask

**Documentazione:**
- `README_QUICK_START.md` - Guida completa
- `GUIDA_ITALIANA.md` - Guida in italiano
- `DEMO.md` - Questo file

---

**⚠️ DISCLAIMER: Questo è uno strumento educativo. NON sostituisce consulenza medica professionale.**

**Buon utilizzo! 🏥🤖**
