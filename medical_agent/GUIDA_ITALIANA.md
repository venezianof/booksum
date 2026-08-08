# Guida Rapida - Agente di Ricerca Medica

## Come far funzionare l'agente

### Passo 1: Attivare l'ambiente virtuale

```bash
cd /home/engine/project/medical_agent
source venv/bin/activate
```

### Passo 2: Avviare il server

```bash
python run_server.py
```

Oppure:

```bash
python backend/app.py
```

### Passo 3: Aprire il browser

Vai su: **http://localhost:5000**

Vedrai un'interfaccia web dove puoi fare domande mediche.

## Test rapido dall'interfaccia web

1. Apri il browser su http://localhost:5000
2. Vedrai un'interfaccia elegante con esempi di domande
3. Clicca su una domanda di esempio o scrivi la tua domanda
4. Clicca su "Ask" e vedrai la risposta dell'agente

## Test rapido dalla riga di comando

```bash
# Test diretto dell'agente
python test_agent.py

# Test dell'API con curl
curl -X POST http://localhost:5000/api/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Che cos è il diabete?"}'
```

## Domande di esempio funzionanti

L'agente è già configurato per rispondere a domande su:

- **Diabete**: "What is diabetes?" o "Che cos'è il diabete?"
- **Ipertensione**: "What are the symptoms of hypertension?"
- **Aspirina**: "How does aspirin work?"
- Qualsiasi altra domanda medica (risposta generica)

## Funzionalità

✅ **Interfaccia web moderna e intuitiva**
- Design elegante con gradiente viola
- Esempi di domande cliccabili
- Visualizzazione delle fonti (PubMed, WHO, CDC)
- Disclaimer medico sempre visibile

✅ **Agente intelligente con LangChain**
- Mock LLM che funziona senza API key
- Risposte mediche strutturate con bullet points
- Collegamenti a fonti PubMed reali
- Tools per cercare su PubMed e Wikipedia

✅ **API REST funzionale**
- Endpoint `/health` per verificare lo stato
- Endpoint `/api/ask` per fare domande
- Gestione errori robusta
- CORS abilitato per sviluppo

## Struttura del progetto

```
medical_agent/
├── backend/
│   ├── app.py              # Server Flask principale
│   ├── agent.py            # Agente LangChain con mock LLM
│   └── static/
│       └── index.html      # Interfaccia web
├── venv/                   # Ambiente virtuale (già configurato)
├── requirements.txt        # Dipendenze Python
├── test_agent.py          # Script di test rapido
├── run_server.py          # Script per avviare il server
└── GUIDA_ITALIANA.md      # Questa guida
```

## Note tecniche

- L'agente usa un **Mock LLM** che non richiede API key
- Per usare OpenAI/Anthropic, configura il file `.env` con le chiavi API
- Le ricerche su PubMed funzionano realmente (API pubblica di NCBI)
- Wikipedia tool è disponibile ma opzionale

## Risoluzione problemi

### Errore: ModuleNotFoundError

```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Server non si avvia

```bash
# Verifica che la porta 5000 sia libera
lsof -i:5000

# Usa un'altra porta
PORT=5001 python run_server.py
```

### L'agente non risponde

Verifica i log del server per vedere eventuali errori. L'agente dovrebbe inizializzarsi correttamente anche senza API key grazie al Mock LLM.

## Prossimi passi

Per usare un LLM reale (OpenAI, Anthropic, ecc.):

1. Copia il file di esempio: `cp .env.example .env`
2. Aggiungi la tua API key nel file `.env`
3. Riavvia il server

L'agente rileverà automaticamente la chiave API e userà il modello reale invece del mock.

---

**⚠️ DISCLAIMER IMPORTANTE**

Questo strumento è solo per scopi educativi e di ricerca. NON è un sostituto per consulenza medica professionale. Consulta sempre un medico qualificato per decisioni mediche.
