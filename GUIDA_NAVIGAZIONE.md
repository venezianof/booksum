# 🗺️ Mappa di Navigazione - BookSum Repository

Benvenuto nel repository BookSum! Questa guida ti aiuta a navigare tutti i file e risorse disponibili.

---

## 📚 Quello che Puoi Fare Qui

Questo repository contiene:

1. **🤖 AI Agents per Learning** - Prova agenti AI per imparare (Medical Research Agent, ecc.)
2. **📖 BookSum Dataset** - Riassunti di libri per training/evaluation di modelli
3. **📓 Jupyter Notebooks** - Tutorial interattivi su agenti AI e architetture LLM
4. **🔧 Data Pipeline** - Script per raccogliere, pulire e allineare dati di riassunti

---

## 🚀 Punto di Partenza Suggerito

### Sei un Principiante?

**Scegli il tuo percorso:**

```
┌─────────────────────────────────────────┐
│  Voglio provare un Agente AI SUBITO!   │
│  (5 minuti)                            │
└────────────┬────────────────────────────┘
             │
             └─→ Leggi: QUICK_START_AGENTI.md
             │
             └─→ Comandi:
                 cd medical_agent
                 python3 -m venv venv
                 source venv/bin/activate
                 pip install -r requirements.txt
                 python backend/app.py
                 # Apri http://localhost:5000

┌─────────────────────────────────────────┐
│  Voglio IMPARARE come funzionano!      │
│  (30 minuti)                           │
└────────────┬────────────────────────────┘
             │
             └─→ Leggi: COME_PROVARE_AGENTI_NOVIZIO.md
             │
             └─→ Segui Opzione 2: Jupyter Notebooks
                 (Day_1b_Agent_Architectures.ipynb è il migliore!)

┌─────────────────────────────────────────┐
│  Voglio CREARE il mio Agente!          │
│  (1-2 ore)                             │
└────────────┬────────────────────────────┘
             │
             └─→ Leggi: ESEMPI_AGENTI.md
             │
             └─→ Usa Medical Agent come template
             │
             └─→ Modifica backend/agent.py
             │
             └─→ Aggiungi i tuoi Tools
             │
             └─→ Testa!
```

---

### Sei un Ricercatore / Data Scientist?

**Vuoi lavorare con il Dataset BookSum:**

```
ROADMAP:
1. Leggi: README.md (sezione Usage)
2. Scarica il dataset:
   gsutil cp gs://sfr-books-dataset-chapters-research/all_chapterized_books.zip .
3. Esplora gli script in:
   scripts/data_collection/     (scarica riassunti)
   scripts/data_cleaning/       (pulisci i dati)
   alignments/                  (allinea paragrafi)
4. Usa i notebooks in:
   notebooks/                   (analizza il dataset)
```

---

## 📁 Struttura del Repository

```
/home/engine/project/
│
├── 📄 README.md                          # Overview principale (LEGGI PRIMA!)
├── 📄 COME_PROVARE_AGENTI_NOVIZIO.md     # ⭐ Guida COMPLETA per principianti
├── 📄 QUICK_START_AGENTI.md              # ⚡ Guida VELOCE (5 min)
├── 📄 ESEMPI_AGENTI.md                   # 📖 Esempi pratici e codice
├── 📄 GUIDA_NAVIGAZIONE.md               # 🗺️ Questo file
│
├── 🤖 medical_agent/                     # AI Agent per ricerca medica
│   ├── README.md                         # Setup e troubleshooting dettagliato
│   ├── requirements.txt                  # Dipendenze Python
│   ├── .env.example                      # Configurazione di esempio
│   ├── backend/
│   │   ├── app.py                        # App Flask (SERVER)
│   │   ├── agent.py                      # Logica agente (MODIFICA QUESTO)
│   │   └── static/index.html             # Interfaccia web
│   ├── tests/
│   │   └── test_api.py                   # Test automatici
│   └── docs/
│       └── manual_test_plan.md           # Guida ai test manuali
│
├── 📚 alignments/                        # Dataset e alignment tools
│   ├── *.jsonl.gz                        # Dati pre-processati
│   ├── gather_data.py                    # Raccogli dati
│   └── align_data_bi_encoder_paraphrase.py  # Allinea paragrafi
│
├── 📚 scripts/
│   ├── data_collection/                  # Script per scaricare riassunti
│   │   ├── cliffnotes/
│   │   ├── sparknotes/
│   │   ├── shmoop/
│   │   └── [altre fonti]
│   └── data_cleaning_scripts/            # Script per pulire dati
│       ├── basic_clean.py
│       ├── split_aggregate_chaps_all_sources.py
│       └── clean_summaries.py
│
├── 📓 notebooks/                         # Notebook Jupyter per analisi
│   └── [vari notebook di analisi]
│
├── 📓 Day_1b_Agent_Architectures.ipynb   # ⭐ START HERE per imparare
├── 📓 Day_3b_Agent_Memory.ipynb          # Memory management
├── 📓 Day_4b_Agent_Evaluation.ipynb      # Evaluation techniques
├── 📓 Day_5b_Agent_Deployment.ipynb      # Deployment in production
├── 📓 Bonus_Day_Extra_API_features_to_try.ipynb  # Feature avanzate
│
├── 🧠 smolagents_doc/                    # Documentazione smolagents
│
├── 📚 examples/                          # Esempi vari di codice
│
└── 📄 requirements.txt                   # Dipendenze globali
```

---

## 🎯 Guide Veloci per Task Specifici

### Task: "Voglio Provare il Medical Agent"
1. Leggi: **QUICK_START_AGENTI.md**
2. Comando: `cd medical_agent && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt && python backend/app.py`
3. Browser: `http://localhost:5000`

### Task: "Voglio Capire come Funzionano gli Agenti"
1. Leggi: **COME_PROVARE_AGENTI_NOVIZIO.md** (sezione "Cos'è un Agente AI?")
2. Apri Notebook: **Day_1b_Agent_Architectures.ipynb**
3. Segui il notebook passo dopo passo

### Task: "Voglio Creare il Mio Agente Personalizzato"
1. Leggi: **ESEMPI_AGENTI.md** (sezione "Creare il Tuo Agente Personalizzato")
2. Copia `medical_agent/backend/agent.py`
3. Modifica il SYSTEM_PROMPT e i Tools
4. Testa!

### Task: "Voglio Usare il Dataset BookSum"
1. Leggi: **README.md** (sezione "Usage")
2. Scarica dati: `gsutil cp gs://sfr-books-dataset-chapters-research/all_chapterized_books.zip .`
3. Script di raccolta: `scripts/data_collection/*/get_summaries.py`
4. Script di pulizia: `scripts/data_cleaning_scripts/*.py`
5. Allineamento: `alignments/align_data_bi_encoder_paraphrase.py`

### Task: "Voglio Leggere la Documentazione Medica dell'Agent"
1. Vai in: `medical_agent/README.md`
2. Sezioni utili:
   - Architecture (come funziona)
   - Configuration (come configurarlo)
   - Troubleshooting (errori comuni)
   - Running Tests (verificare che funzioni)

---

## 🎓 Percorsi di Apprendimento Consigliati

### Percorso 1: Principiante (4 ore)
```
1. QUICK_START_AGENTI.md (5 min)
   ↓
2. Prova Medical Agent (10 min)
   ↓
3. COME_PROVARE_AGENTI_NOVIZIO.md - Sezione "Cos'è" (15 min)
   ↓
4. Day_1b_Agent_Architectures.ipynb (1 ora)
   ↓
5. ESEMPI_AGENTI.md - Esercizio 1 (45 min)
   ↓
6. Fai il tuo primo agente personalizzato! (1.5 ore)
```

### Percorso 2: Intermedio (6 ore)
```
1. Day_1b_Agent_Architectures.ipynb (1 ora)
   ↓
2. Day_3b_Agent_Memory.ipynb (1 ora)
   ↓
3. Day_4b_Agent_Evaluation.ipynb (1 ora)
   ↓
4. ESEMPI_AGENTI.md - Tutti gli Esercizi (2 ore)
   ↓
5. Crea un agente con Memory e Evaluation (1 ora)
```

### Percorso 3: Avanzato (8+ ore)
```
1. Day_5b_Agent_Deployment.ipynb (1 ora)
   ↓
2. Bonus_Day_Extra_API_features_to_try.ipynb (1 ora)
   ↓
3. Leggi il codice di medical_agent completo (1 ora)
   ↓
4. Crea un agente multi-tool con API esterne (2 ore)
   ↓
5. Aggiungi Memory, Evaluation, Error Handling (2 ore)
   ↓
6. Deploy il tuo agente (1 ora)
```

### Percorso 4: Ricercatore Data Science (10+ ore)
```
1. README.md - Sezione Usage (30 min)
   ↓
2. Scarica e analizza BookSum dataset (1 ora)
   ↓
3. Usa gli script di data collection (1 ora)
   ↓
4. Usa gli script di data cleaning (1 ora)
   ↓
5. Usa gli script di alignment (1 ora)
   ↓
6. Analizza i dati con i notebooks (2 ore)
   ↓
7. Crea il tuo script di analisi (2 ore)
   ↓
8. Scrivi un paper / report (2+ ore)
```

---

## 🆘 Ho un Problema!

**Dove cercare aiuto:**

| Problema | Leggi |
|----------|-------|
| Non riesco a installare le dipendenze | medical_agent/README.md - Troubleshooting |
| Errore: "Address already in use" | COME_PROVARE_AGENTI_NOVIZIO.md - Troubleshooting |
| Non capisco come funzionano gli agenti | Day_1b_Agent_Architectures.ipynb |
| Voglio aggiungere un nuovo tool | ESEMPI_AGENTI.md - Sezione "Creare il Tuo Agente" |
| Il Medical Agent non risponde | medical_agent/README.md - Sezione "Runtime Issues" |
| BookSum dataset non scarica | README.md - Sezione "Troubleshooting" |

---

## 🔗 Link Utili

### Documentazione Ufficiale
- **LangChain:** https://python.langchain.com/
- **Flask:** https://flask.palletsprojects.com/
- **OpenAI API:** https://platform.openai.com/docs/
- **BookSum Paper:** https://arxiv.org/abs/2105.08209

### Community & Support
- **LangChain Discord:** https://discord.gg/langchain
- **GitHub Issues:** Per segnalare bug
- **Stack Overflow:** Tag `langchain` o `llm`

### Video Tutorial
- Cerca "LangChain tutorial" su YouTube
- "AI Agents beginners guide"

---

## 📊 File Summary

```
📄 README.md
   └─→ Overview del progetto BookSum e Medical Agent

📄 COME_PROVARE_AGENTI_NOVIZIO.md (PRINCIPALE)
   ├─→ Cos'è un Agente AI?
   ├─→ 3 opzioni per provare (facile → avanzato)
   ├─→ Setup completo passo-passo
   ├─→ Troubleshooting dettagliato
   └─→ Prossimi step

📄 QUICK_START_AGENTI.md (VELOCE)
   └─→ Prova in 5 minuti

📄 ESEMPI_AGENTI.md (PRATICO)
   ├─→ Esempi di utilizzo del Medical Agent
   ├─→ Come creare agenti personalizzati
   ├─→ Esercizi pratici
   └─→ Codice copy-paste ready

📄 GUIDA_NAVIGAZIONE.md (QUESTO FILE)
   └─→ Mappa completa del repository

📓 Notebook
   ├─→ Day_1b: Architetture Agenti (START HERE!)
   ├─→ Day_3b: Memory management
   ├─→ Day_4b: Evaluation
   ├─→ Day_5b: Deployment
   └─→ Bonus: Feature avanzate
```

---

## ✅ Checklist di Completamento

Completa questa checklist per assicurarti di aver capito il repository:

- [ ] Ho letto il README.md
- [ ] Ho scelto un percorso di apprendimento (Principiante/Intermedio/Avanzato)
- [ ] Ho letto almeno una delle guide (QUICK_START o COME_PROVARE)
- [ ] Ho provato il Medical Agent (even se è solo `curl` test)
- [ ] Ho aperto un Jupyter Notebook (Day_1b)
- [ ] Capisco cosa è un "Tool" in un Agente
- [ ] Capisco il pattern ReAct (Reasoning + Acting)
- [ ] Ho un'idea per il mio primo agente personalizzato
- [ ] So dove trovare aiuto se ho problemi
- [ ] Ho bookmarkato i file utili

---

**Pronto a iniziare? 🚀**

**Scegli uno dei file sopra e inizia a leggere!**
