# 📖 Esempi Pratici - Come Usare gli Agenti

Questa guida ti mostra esempi concreti di come usare gli agenti AI che hai installato.

## Indice

1. [Medical Research Agent - Esempi](#medical-research-agent---esempi)
2. [Creare il Tuo Agente Personalizzato](#creare-il-tuo-agente-personalizzato)
3. [Esempi Avanzati](#esempi-avanzati)

---

## Medical Research Agent - Esempi

### Prerequisito: Agente Avviato

```bash
cd medical_agent
source venv/bin/activate
python backend/app.py
```

Dovresti vedere:
```
Running on http://127.0.0.1:5000
```

---

### Esempio 1: Domanda Semplice

#### Via Browser
1. Apri http://localhost:5000
2. Digita: **"Che cos'è il diabete?"**
3. Premi Enter

#### Via Terminal (curl)
```bash
curl -X POST http://localhost:5000/api/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Che cose il diabete?"}'
```

**Risposta Attesa:**
```json
{
  "answer_text": "Il diabete è una condizione medica...",
  "bullets": ["Tipo 1", "Tipo 2", "..."],
  "source_links": ["https://pubmed.ncbi.nlm.nih.gov/..."],
  "disclaimer": "⚠️ Questo tool è solo educativo..."
}
```

---

### Esempio 2: Domanda Specifica

#### Domanda
**"Quali sono i sintomi precoci del cancro al pancreas?"**

```bash
curl -X POST http://localhost:5000/api/ask \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Quali sono i sintomi precoci del cancro al pancreas?",
    "language": "it"
  }'
```

#### Cosa Fa l'Agente Internamente

```
1. Riceve domanda: "Sintomi cancro pancreas"
2. Decide di usare il tool: "search_medical_literature"
3. Chiama PubMed API
4. Riceve 5-10 articoli scientifici
5. Estrae le informazioni rilevanti
6. Sintetizza in risposta leggibile
7. Aggiunge disclaimer medico
8. Ti risponde!
```

**Risposta Attesa:**
- Sintomi precoci (dolore addominale, ittero, ecc.)
- Link a studi scientifici
- Raccomandazione di consultare un medico

---

### Esempio 3: Follow-up / Domande Successive

Se l'agente supporta memoria (conversation memory):

```bash
# Domanda 1
curl -X POST http://localhost:5000/api/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Che cose il diabete di tipo 1?"}'

# Domanda 2 (segue dalla precedente)
curl -X POST http://localhost:5000/api/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Come si cura?"}'  # Agente capisce che è ancora di diabete tipo 1
```

---

### Esempio 4: Ricerca Comparativa

```bash
curl -X POST http://localhost:5000/api/ask \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Qual è la differenza tra aspirina e ibuprofene per il dolore?"
  }'
```

**L'agente:**
- Cerca studi su entrambi
- Compara efficacia
- Lista controindicazioni
- Suggerisce quando usare quale

---

## Creare il Tuo Agente Personalizzato

### Template: Customer Support Agent

```python
# backend/agent.py (MODIFICA QUESTO)

from langchain import OpenAI, ConversationChain
from langchain.tools import Tool

# PASSO 1: Cambia il SYSTEM PROMPT
SYSTEM_PROMPT = """
Sei un assistente al customer support per una libreria online.
Puoi:
- Cercare libri nel catalogo
- Aiutare con ordini
- Risolvere problemi di spedizione
- Rispondere a domande sul negozio

Sempre gentile e utile!
"""

# PASSO 2: Aggiungi Tools Personalizzati
def search_books(query: str) -> str:
    """Cerca libri nel catalogo"""
    # Qui farebbe una vera ricerca nel database
    return f"Risultati per '{query}': libro1, libro2, libro3"

def check_order(order_id: str) -> str:
    """Controlla lo stato di un ordine"""
    return f"Ordine {order_id}: Spedito il 2023-12-10"

# PASSO 3: Registra i Tools
tools = [
    Tool(
        name="search_books",
        func=search_books,
        description="Cerca libri nel catalogo"
    ),
    Tool(
        name="check_order",
        func=check_order,
        description="Controlla lo stato di un ordine"
    ),
]

# PASSO 4: Crea l'agente
from langchain.agents import AgentType, initialize_agent

agent = initialize_agent(
    tools,
    llm=OpenAI(),
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
)

# Usa l'agente!
# result = agent.run("Ho ordinato il libro XYZ, dove è?")
```

### Usa il Tuo Agente

```bash
# 1. Modifica backend/agent.py come sopra
# 2. Riavvia il server
python backend/app.py

# 3. Testa
curl -X POST http://localhost:5000/api/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Cerchi un libro di Asimov"}'
```

---

## Esempi Avanzati

### 1️⃣ Agente con Memory (Ricorda le Conversazioni)

```python
from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory(memory_key="chat_history")

agent = initialize_agent(
    tools,
    llm=OpenAI(),
    memory=memory,
    verbose=True,
)

# Domanda 1
agent.run("Ciao, mi piacciono i libri di fantascienza")
# Output: "Piacere! Posso aiutarti a trovare..."

# Domanda 2
agent.run("Quale mi consigli?")
# Agent ricorda che ami la fantascienza!
# Output: "Ti consiglio 'Fondazione' di Asimov..."
```

---

### 2️⃣ Agente con Tool per Web Search

```python
from langchain.tools import tool
from langchain_community.utilities import GoogleSearchAPIWrapper

search = GoogleSearchAPIWrapper()

@tool
def web_search(query: str) -> str:
    """Cerca su Google"""
    return search.run(query)

# Aggiungi a tools e usa!
tools.append(web_search)
```

---

### 3️⃣ Agente che Usa Più Tools Insieme

```python
# Un agente che:
# 1. Cerca su web
# 2. Chiama un'API
# 3. Analizza i risultati
# 4. Risponde all'utente

@tool
def get_weather(city: str) -> str:
    """Prendi il meteo di una città"""
    # Chiama API meteo
    return "Milano: 15°C, Nuvoloso"

@tool
def search_hotels(city: str, date: str) -> str:
    """Cerca hotel disponibili"""
    # Chiama API hotel
    return "Hotel A: 80€, Hotel B: 120€"

tools = [get_weather, search_hotels]

# Usa:
agent.run("""
Voglio andare a Milano il 15 dicembre.
Com'è il meteo? Quali hotel mi consigli?
""")

# Agent:
# 1. Chiama get_weather("Milano")
# 2. Chiama search_hotels("Milano", "15 dicembre")
# 3. Combina i risultati
# 4. Ti suggerisce dove andare in base al meteo
```

---

### 4️⃣ Agente ReAct (Reasoning + Acting)

ReAct significa che l'agente **pensa** prima di **agire**.

```python
# Backend della domanda "Dove nascita il presidente italiano?"
# L'agente pensa ad alta voce:

"""
Pensiero: "La domanda chiede il luogo di nascita del presidente italiano"
Azione: Cerco "presidente italia current 2024"
Osservazione: Sergio Mattarella è il presidente dal 2015
Pensiero: "Ora cerco dove è nato Sergio Mattarella"
Azione: Cerco "Sergio Mattarella nato dove"
Osservazione: "Nato a Palermo, 16 luglio 1941"
Pensiero: "Ho la risposta"
Risposta: "Il presidente italiano Sergio Mattarella è nato a Palermo"
"""
```

Questo è il modello che usa il Medical Agent!

```python
from langchain.agents import AgentType

agent = initialize_agent(
    tools,
    llm=OpenAI(),
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,  # ← ReAct
    verbose=True,  # ← Mostra il "pensiero"
)
```

---

### 5️⃣ Streaming Responses (Risposta in Tempo Reale)

```python
# Mostra la risposta mentre l'agente la genera (come ChatGPT)

from langchain.callbacks import StreamingStdOutCallbackHandler

callbacks = [StreamingStdOutCallbackHandler()]

agent = initialize_agent(
    tools,
    llm=OpenAI(callbacks=callbacks),
    verbose=True,
)

# Ora vedrai:
agent.run("Dimmi una storia")
# Output appare MENTRE viene generato, non tutto insieme!
```

---

## 🎯 Esercizi Pratici

### Esercizio 1: Crea un Finance Agent

Modificare il Medical Agent per rispondere domande di finanza:

```python
# Cambia il SYSTEM_PROMPT:
SYSTEM_PROMPT = """
Sei un esperto di finanza personale.
Puoi:
- Spiegare concetti finanziari
- Cercare quotazioni azionarie
- Consigliare strategie di investimento

Sempre con disclaimer che non è consiglio finanziario!
"""

# Aggiungi tools per:
- Cercare prezzi azioni
- Calcolare interessi
- Trovare informazioni di mercato
```

---

### Esercizio 2: Crea un Tech Support Agent

```python
SYSTEM_PROMPT = """
Sei un esperto di supporto tecnico per il software XYZ.
Puoi:
- Rispondere a domande tecniche
- Cercare nella knowledge base
- Guidare alla soluzione

Sempre cortese e paziente!
"""

# Tools:
- search_documentation()
- search_common_issues()
- generate_error_solution()
```

---

### Esercizio 3: Crea un Travel Agent

```python
SYSTEM_PROMPT = """
Sei un assistente di viaggio esperto.
Puoi:
- Cercare voli
- Trovare hotel
- Suggerire attrazioni
- Calcolare itinerari

Rendi i viaggi divertenti e senza stress!
"""

# Tools:
- search_flights(origin, destination, date)
- search_hotels(city, date_in, date_out)
- search_attractions(city)
```

---

## 🚀 Prossimi Step

1. **Scegli un dominio** che ti interessa (tech, finanza, viaggio, ecc.)
2. **Modifica il prompt** del Medical Agent
3. **Crea 2-3 tools** rilevanti
4. **Testa il tuo agente**
5. **Itera e migliora**

---

## 📚 Risorse

- **LangChain Tools:** https://python.langchain.com/en/latest/modules/tools.html
- **Tool Use Cookbook:** https://github.com/langchain-ai/langchain/discussions
- **Agents Docs:** https://python.langchain.com/en/latest/modules/agents.html

---

**Sei pronto a creare il TUO agente? 🚀**
