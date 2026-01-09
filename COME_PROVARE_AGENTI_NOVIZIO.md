# 🤖 Come Provare gli Agenti AI - Guida per Principianti

Se sei nuovo ai **Agenti AI** e vuoi imparare, sei nel posto giusto! Questa guida ti porterà passo dopo passo a far funzionare il tuo primo agente AI.

## 📖 Sommario

1. [Cos'è un Agente AI?](#cosè-un-agente-ai)
2. [Come Iniziare - 3 Opzioni](#come-iniziare---3-opzioni)
3. [Opzione 1: Medical Research Agent (Facile - Consigliato)](#opzione-1-medical-research-agent-facile--consigliato)
4. [Opzione 2: Notebook Interattivi (Educativo)](#opzione-2-notebook-interattivi-educativo)
5. [Opzione 3: Linea di Comando (Avanzato)](#opzione-3-linea-di-comando-avanzato)
6. [Troubleshooting](#troubleshooting-faq)

---

## Cos'è un Agente AI?

Un **Agente AI** è un programma intelligente che:

- 🧠 **Capisce** le tue domande in linguaggio naturale
- 🛠️ **Sceglie** quali strumenti usare (ricerca web, database, API, ecc.)
- ⚙️ **Esegue** le azioni necessarie
- 📝 **Combina** i risultati e ti risponde in modo chiaro

**Esempio:**
```
Tu:     "Quanti figli aveva Napoleone?"
Agent:  [Cerca in Wikipedia] [Legge l'articolo] [Estrae l'informazione]
Agent:  "Napoleone aveva 1 figlio legittimo: Napoleone Francesco Giuseppe Carlo..."
```

### Come funziona internamente?

```
Domanda dell'utente
       ↓
[Agente AI]
    ├─→ Decide quale strumento usare
    ├─→ Chiama l'API/Database/Tool
    ├─→ Riceve i risultati
    ├─→ Elabora la risposta
    └─→ Ti risponde
```

---

## Come Iniziare - 3 Opzioni

Scegli l'opzione che preferisci:

| Opzione | Difficoltà | Tempo | Miglior Per | Cosa Impari |
|---------|-----------|-------|-----------|-----------|
| **Medical Agent** | ⭐ Facile | 10 min | Chi vuole subito una app funzionante | LangChain, Flask, Tools, API |
| **Notebook** | ⭐⭐ Medio | 30 min | Chi ama imparare interattivamente | Architetture Agenti, Memory, Evaluation |
| **CLI** | ⭐⭐⭐ Avanzato | 20 min | Chi preferisce linea di comando | BookSum Dataset, Alignment, spaCy |

---

## Opzione 1: Medical Research Agent (Facile - Consigliato)

Il **Medical Research Agent** è una web app che risponde domande mediche. È perfetto per iniziare!

### ✅ Cosa Ti Serve

- **Python 3.8+** (verifica con: `python3 --version`)
- **Un editor di testo** (VS Code, nano, vim, ecc.)
- **Un browser web** (Chrome, Firefox, Safari)
- **Un API Key** (opzionale - spiegato sotto)

### 🚀 Setup in 5 Step

#### Step 1: Entra nella Cartella
```bash
cd /home/engine/project/medical_agent
```

#### Step 2: Crea un Ambiente Isolato (Virtual Environment)
```bash
python3 -m venv venv
```
Questo crea una cartella `venv` con tutto isolato. Perfetto per evitare conflitti!

#### Step 3: Attiva l'Ambiente
```bash
# Su macOS/Linux:
source venv/bin/activate

# Su Windows (PowerShell):
venv\Scripts\activate

# Dovresti vedere (venv) nel prompt del terminale
```

#### Step 4: Installa le Librerie
```bash
pip install -r requirements.txt
```
Questo scarica Flask, LangChain, e altre librerie necessarie.

#### Step 5: Configura l'API Key

##### Opzione A: Con API Key (Consigliato)

```bash
# Copia il file di esempio
cp .env.example .env

# Modifica con il tuo editor preferito
nano .env
# Oppure apri direttamente in VS Code:
# code .env
```

Devi trovare questa linea e cambiare il valore:
```
OPENAI_API_KEY=your_key_here
```

Sostituisci `your_key_here` con il tuo vero API key. Se non hai un API key:

1. **Per OpenAI:**
   - Vai a: https://platform.openai.com/api-keys
   - Crea un nuovo secret key
   - Copia e incolla in `.env`

2. **Per Anthropic (Claude):**
   - Vai a: https://console.anthropic.com/
   - Crea un nuovo API key
   - Modifica `.env` per usare Anthropic:
   ```
   LLM_PROVIDER=anthropic
   ANTHROPIC_API_KEY=your_key_here
   ```

##### Opzione B: Senza API Key (Demo)

Se non vuoi un API key (es. per testare solo la struttura), puoi usare un modello open-source:

```bash
# Installa una libreria per modelli locali
pip install ollama

# In .env:
LLM_PROVIDER=ollama
```

### ▶️ Avvia l'Applicazione

```bash
python backend/app.py
```

Dovresti vedere:
```
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

### 🌐 Apri nel Browser

1. Apri un browser web
2. Vai a: **http://localhost:5000**
3. Vedrai un'interfaccia belle e amichevole!
4. Digita una domanda, es: "Cosa è il diabete?"
5. L'agente risponderà! 🎉

### 🧪 Test da Terminale (Alternativa)

Se preferisci non usare il browser, puoi testare direttamente:

```bash
# In un ALTRO terminale (con venv attivo):
curl -X POST http://localhost:5000/api/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is diabetes?"}'
```

Dovresti ricevere una risposta JSON:
```json
{
  "answer_text": "Diabetes is...",
  "source_links": [...],
  "disclaimer": "⚠️ This tool is for educational purposes only..."
}
```

### ⏹️ Fermare l'Agente

```bash
# Nel terminale dove gira l'app:
Ctrl+C

# Disattiva l'ambiente:
deactivate
```

---

## Opzione 2: Notebook Interattivi (Educativo)

I **Jupyter Notebooks** sono perfetti per imparare passo dopo passo. Vedi il codice, l'output, e le spiegazioni tutto insieme!

### 📦 Installa Jupyter

```bash
# Se sei nella cartella medical_agent, esci prima:
cd /home/engine/project

# Installa Jupyter
pip install jupyter
```

### 🚀 Avvia Jupyter

```bash
jupyter notebook
```

Il browser si aprirà automaticamente mostrando i file disponibili.

### 📚 Notebook da Leggere (In Ordine)

#### 1️⃣ **Day_1b_Agent_Architectures.ipynb** (START HERE!)
Impara come funzionano gli agenti:
- Cosa è una Chain vs un Agent
- Come funzionano i Tools
- ReAct Pattern (Reasoning + Acting)

#### 2️⃣ **Day_3b_Agent_Memory.ipynb**
Come gli agenti ricordano le conversazioni:
- Conversation Memory
- Buffer Memory
- Token Management

#### 3️⃣ **Day_4b_Agent_Evaluation.ipynb**
Come testare se un agente funziona bene:
- Metriche di qualità
- Benchmark
- Debugging

#### 4️⃣ **Day_5b_Agent_Deployment.ipynb**
Come mettere un agente in produzione:
- Deployment su cloud
- Monitoring
- Cost Optimization

#### 5️⃣ **Bonus_Day_Extra_API_features_to_try.ipynb**
Esplora feature avanzate e API diverse!

### 💡 Come Usare i Notebook

1. Clicca su un notebook per aprirlo
2. Leggi le spiegazioni
3. Premi **Shift+Enter** per eseguire ogni cella di codice
4. Vedi l'output immediatamente sotto
5. Modifica il codice e ri-esegui per imparare!

Esempio di cella:
```python
# Questo è codice Python
from langchain import OpenAI

llm = OpenAI()
result = llm("Tell me a joke")
print(result)
```

Premi Shift+Enter → vedrai il risultato!

---

## Opzione 3: Linea di Comando (Avanzato)

Se vuoi lavorare con il dataset BookSum e l'allineamento di testi:

### 📚 Cosa è il Dataset BookSum?

BookSum è:
- 🔬 Un dataset di **riassunti di libri** a livello paragrafo, capitolo, e libro
- 📖 Estratto da **Project Gutenberg** (libri classici gratuiti)
- 🎯 Usato per addestrare modelli di summarization

### ⚙️ Esplora il Dataset

```bash
cd /home/engine/project/alignments

# Vedi i file disponibili
ls -lh *.jsonl.gz

# Esempio: Guarda i dati
# Decomprime e leggi il primo capitolo allineato
zcat chapter_summary_aligned_train.jsonl.gz | head -1 | python -m json.tool
```

Output (esempio):
```json
{
  "book_id": "walter_scott__ivanhoe__0",
  "chapter_id": 0,
  "chapter_summary": "Chapter 0 summary text...",
  "chapter_text": "Full chapter text...",
  "alignments": [...]
}
```

### 🔍 Script Disponibili

#### `gather_data.py`
Raccogli dati grezzi e preparali per l'allineamento:
```bash
python gather_data.py \
  --matched_file chapter_summary_aligned_train.jsonl \
  --split_paragraphs
```

#### `align_data_bi_encoder_paraphrase.py`
Allinea paragrafi con le loro sentenze di sommario:
```bash
python align_data_bi_encoder_paraphrase.py \
  --data_path chapter_summary_aligned_train.jsonl.gathered \
  --stable_alignment
```

### 📊 Analizza gli Allineamenti

Uno script Python semplice per esplorare:

```python
import json
import gzip

# Apri il file compresso
with gzip.open('chapter_summary_aligned_train.jsonl.gz', 'rt') as f:
    # Leggi la prima riga
    first_record = json.loads(f.readline())
    
    print(f"Book: {first_record['book_id']}")
    print(f"Chapter: {first_record['chapter_id']}")
    print(f"\nSummary:\n{first_record['chapter_summary'][:200]}...")
    print(f"\nAlignments: {len(first_record.get('alignments', []))} found")
```

Salva questo come `explore_data.py` e esegui:
```bash
python explore_data.py
```

---

## Troubleshooting (FAQ)

### ❌ Errore: `python: command not found`

**Problema:** Python non è installato o non è nel PATH.

**Soluzione:**
```bash
# Verifica installazione
python3 --version

# Se non è installato:
# Ubuntu/Debian:
sudo apt update && sudo apt install python3 python3-pip python3-venv

# macOS (con Homebrew):
brew install python3
```

---

### ❌ Errore: `No module named 'flask'`

**Problema:** Librerie non installate o virtual environment non attivato.

**Soluzione:**
```bash
# Assicurati di essere nella cartella giusta
cd /home/engine/project/medical_agent

# Attiva venv
source venv/bin/activate  # Vedi (venv) nel prompt?

# Reinstalla
pip install -r requirements.txt
```

---

### ❌ Errore: `Address already in use` (porta 5000)

**Problema:** Un'altra app sta usando la porta 5000.

**Soluzione 1:** Fermala
```bash
# Su macOS/Linux:
lsof -ti:5000 | xargs kill -9

# Su Windows (PowerShell):
Get-Process -Id (Get-NetTCPConnection -LocalPort 5000).OwningProcess | Stop-Process -Force
```

**Soluzione 2:** Usa un'altra porta
```bash
PORT=5001 python backend/app.py
```

---

### ❌ Errore: `AuthenticationError: Invalid API key`

**Problema:** API key mancante o sbagliata in `.env`.

**Soluzione:**
```bash
# 1. Verifica il file .env esista
cat .env | grep OPENAI_API_KEY

# 2. Controlla che la chiave sia corretta
# Visita: https://platform.openai.com/api-keys

# 3. Aggiorna .env
nano .env
# Cambia: OPENAI_API_KEY=sk-...
```

---

### ❌ Errore: `ModuleNotFoundError: No module named 'langchain'`

**Problema:** LangChain non è installato.

**Soluzione:**
```bash
# Dentro il virtual environment:
pip install langchain langchain-community
```

---

### ❌ Il Notebook non si avvia

**Problema:** Jupyter non è installato o c'è un'altra issue.

**Soluzione:**
```bash
# Dalla root del progetto:
pip install --upgrade jupyter

# Quindi:
jupyter notebook
```

Se ancora non funziona, usa JupyterLab:
```bash
pip install jupyterlab
jupyter lab
```

---

## 🎓 Prossimi Step

Una volta che hai provato un'opzione:

1. **Leggi il codice sorgente:**
   ```bash
   # Per Medical Agent:
   cat backend/app.py
   cat backend/agent.py
   
   # Per capire come funzionano i tools
   ```

2. **Modifica l'agente:**
   - Cambia il prompt (istruzioni all'agente)
   - Aggiungi nuovi tools
   - Cambia il modello LLM

3. **Crea il TUO agente:**
   - Basati sul Medical Agent come template
   - Cambia il dominio (finanza, legale, tech support, ecc.)
   - Aggiungi i tuoi tools

4. **Leggi i Notebook educativi:**
   - Seguili in ordine (Day 1 → Day 5)
   - Sperimenta il codice
   - Costruisci i tuoi agenti

---

## 📚 Risorse Aggiuntive

### Documentazione Ufficiale
- **LangChain:** https://python.langchain.com/
- **Flask:** https://flask.palletsprojects.com/
- **OpenAI:** https://platform.openai.com/docs/

### Community
- **LangChain Discord:** https://discord.gg/langchain
- **Stack Overflow:** Cerca `langchain` e `llm`
- **GitHub Issues:** Se trovi un bug, segnalalo!

### Video Tutorial (in inglese)
- Cerca "LangChain agents tutorial" su YouTube
- "LangChain beginner guide"

---

## 🎯 Checklist di Completamento

Hai completato questa guida quando:

- [ ] Python 3.8+ è installato
- [ ] Hai scelto una delle 3 opzioni
- [ ] Hai installato le dipendenze
- [ ] Hai visto il tuo primo agente funzionare
- [ ] Hai modificato qualcosa nel codice
- [ ] Capisci come funzionano i tools
- [ ] Hai un'idea per il TUO agente

---

## 🤝 Aiuto Aggiuntivo

Se hai problemi o domande:

1. **Controlla il Troubleshooting** sopra
2. **Leggi il README specifico:**
   - Medical Agent: `medical_agent/README.md`
3. **Apri un Issue su GitHub** se pensi sia un bug
4. **Chiedi nella community** di LangChain

---

**Buon Divertimento! 🚀 Sei pronto a creare il tuo primo Agente AI?**
