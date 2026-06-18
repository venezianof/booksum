# 📑 Indice Completo dei Test - Medical Research Assistant Agent

Questo documento fornisce un indice completo di tutti gli script, guide e risorse disponibili per testare l'agente.

## 🎯 File di Test Disponibili

### 1. Script Python

| File | Descrizione | Comando | Tempo |
|------|-------------|---------|-------|
| `test_agente.py` | Test base senza server | `python test_agente.py` | ~2 sec |
| `test_agente_api.py` | Test completo con API | `python test_agente_api.py` | ~10 sec |
| `esempio_uso_agente.py` | Esempi d'uso interattivi | `python esempio_uso_agente.py` | ~5 sec |

### 2. Script Bash

| File | Descrizione | Comando |
|------|-------------|---------|
| `testa_agente.sh` | Script unificato per tutti i test | `./testa_agente.sh [base\|api\|manuale]` |

### 3. Guide e Documentazione

| File | Descrizione |
|------|-------------|
| `GUIDA_RAPIDA_TEST.md` | Guida rapida con esempi pratici |
| `README_TEST_AGENTE.md` | README completo sui test |
| `TESTING_INDEX.md` | Questo file - indice di tutte le risorse |
| `medical_agent/README.md` | Documentazione completa del medical agent |

## 🚀 Come Iniziare

### Opzione 1: Test Veloce (consigliato per iniziare)

```bash
# Esegui il test più semplice
python test_agente.py
```

**Output atteso:** ✓ Test completati in ~2 secondi

### Opzione 2: Test Completo

```bash
# Testa anche il server API
python test_agente_api.py
```

**Output atteso:** ✓ Server avviato e testato automaticamente

### Opzione 3: Esempio Interattivo

```bash
# Vedi esempi d'uso e prova interattivamente
python esempio_uso_agente.py
```

**Output atteso:** Esempi di codice e possibilità di fare domande

### Opzione 4: Script Bash All-in-One

```bash
# Test base
./testa_agente.sh base

# Test API
./testa_agente.sh api

# Avvia server per test manuali
./testa_agente.sh manuale
```

## 📋 Checklist Completa dei Test

Usa questa checklist per verificare che tutto funzioni:

- [ ] **Test 1: Importazione moduli**
  ```bash
  python -c "import sys; sys.path.insert(0, 'medical_agent/backend'); from agent import MedicalResearchAgent; print('✓ OK')"
  ```

- [ ] **Test 2: Inizializzazione agente**
  ```bash
  python test_agente.py
  ```

- [ ] **Test 3: Health check endpoint**
  ```bash
  # In un terminale
  cd medical_agent && python backend/app.py &
  # In un altro terminale
  curl http://localhost:5000/health
  ```

- [ ] **Test 4: Endpoint /api/ask**
  ```bash
  curl -X POST http://localhost:5000/api/ask \
    -H "Content-Type: application/json" \
    -d '{"question": "Test"}'
  ```

- [ ] **Test 5: Gestione errori**
  ```bash
  # Domanda vuota (deve dare errore 400)
  curl -X POST http://localhost:5000/api/ask \
    -H "Content-Type: application/json" \
    -d '{"question": ""}'
  ```

- [ ] **Test 6: Test automatici completi**
  ```bash
  python test_agente_api.py
  ```

## 🎓 Percorso di Apprendimento Suggerito

### Livello 1: Principiante
1. Leggi `GUIDA_RAPIDA_TEST.md`
2. Esegui `python test_agente.py`
3. Esegui `python esempio_uso_agente.py`

### Livello 2: Intermedio
1. Leggi `README_TEST_AGENTE.md`
2. Esegui `python test_agente_api.py`
3. Esplora il codice in `medical_agent/backend/`

### Livello 3: Avanzato
1. Leggi `medical_agent/README.md` completo
2. Avvia il server e prova test manuali
3. Esplora e modifica i test in `medical_agent/tests/`

## 📊 Matrice di Compatibilità

| Script | Python 3.8 | Python 3.9 | Python 3.10 | Python 3.11+ |
|--------|:----------:|:----------:|:-----------:|:------------:|
| test_agente.py | ✓ | ✓ | ✓ | ✓ |
| test_agente_api.py | ✓ | ✓ | ✓ | ✓ |
| esempio_uso_agente.py | ✓ | ✓ | ✓ | ✓ |
| testa_agente.sh | ✓ | ✓ | ✓ | ✓ |

## 🔧 Risoluzione Problemi Rapida

### Problema: ModuleNotFoundError

**Soluzione:**
```bash
cd medical_agent
pip install -r requirements.txt
```

### Problema: Porta 5000 occupata

**Soluzione:**
```bash
# Termina il processo
lsof -ti:5000 | xargs kill -9

# Oppure usa un'altra porta
PORT=5001 python backend/app.py
```

### Problema: Script non eseguibile

**Soluzione:**
```bash
chmod +x test_agente.py test_agente_api.py esempio_uso_agente.py testa_agente.sh
```

### Problema: Test API non parte

**Soluzione:**
```bash
# Verifica che Flask sia installato
python -c "import flask; print('✓ Flask OK')"

# Se manca, installa
pip install flask flask-cors
```

## 📞 Supporto e Risorse

- **Domande generali:** Apri una Issue su GitHub
- **Bug report:** Usa il template di bug report
- **Richieste di funzionalità:** Apri una feature request

## 🎯 Test Rapidi per Scenario

### Scenario 1: "Voglio solo verificare che funzioni"
```bash
./testa_agente.sh base
```

### Scenario 2: "Voglio testare l'API"
```bash
./testa_agente.sh api
```

### Scenario 3: "Voglio vedere come si usa nel codice"
```bash
python esempio_uso_agente.py
```

### Scenario 4: "Voglio fare test manuali"
```bash
./testa_agente.sh manuale
# In un altro terminale, usa curl per testare
```

### Scenario 5: "Voglio eseguire i test pytest"
```bash
cd medical_agent
pytest tests/ -v
```

## 📈 Metriche dei Test

| Test | Copertura | Tempo Medio | Affidabilità |
|------|:---------:|:-----------:|:------------:|
| test_agente.py | Base | 2 sec | ⭐⭐⭐⭐⭐ |
| test_agente_api.py | Completa | 10 sec | ⭐⭐⭐⭐⭐ |
| esempio_uso_agente.py | Esempi | 5 sec | ⭐⭐⭐⭐⭐ |
| pytest suite | Estesa | 15 sec | ⭐⭐⭐⭐⭐ |

## 🔄 Aggiornamenti e Manutenzione

Questo indice viene aggiornato regolarmente. Ultima revisione: Dicembre 2024

---

**💡 Suggerimento:** Inizia sempre con `python test_agente.py` per un test rapido!

**⚠️ Ricorda:** Questo agente è solo per scopi educativi e di ricerca.
