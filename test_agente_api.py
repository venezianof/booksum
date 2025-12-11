#!/usr/bin/env python3
"""
Script di test per l'API del Medical Research Assistant.
Questo script avvia il server Flask e testa gli endpoint API.
"""

import subprocess
import time
import requests
import sys
import signal
import os

print("=" * 60)
print("TEST API MEDICAL RESEARCH ASSISTANT")
print("=" * 60)
print()

# Variabili configurazione
BASE_URL = "http://localhost:5000"
server_process = None

def cleanup():
    """Termina il processo del server se attivo"""
    global server_process
    if server_process:
        print("\n\nChiusura server...")
        server_process.terminate()
        try:
            server_process.wait(timeout=3)
        except subprocess.TimeoutExpired:
            server_process.kill()
        print("✓ Server chiuso")

def signal_handler(sig, frame):
    """Gestisce Ctrl+C"""
    cleanup()
    sys.exit(0)

# Registra handler per Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

try:
    # Test 1: Avvio server
    print("Test 1: Avvio del server Flask...")
    print("(Il server verrà avviato in background)")
    print()
    
    # Cambia directory e avvia server
    backend_dir = os.path.join(os.path.dirname(__file__), 'medical_agent', 'backend')
    server_process = subprocess.Popen(
        [sys.executable, 'app.py'],
        cwd=backend_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Attendi che il server sia pronto
    print("Attendo che il server sia pronto...", end="", flush=True)
    max_attempts = 30
    for i in range(max_attempts):
        try:
            response = requests.get(f"{BASE_URL}/health", timeout=1)
            if response.status_code == 200:
                print(" OK!")
                print("✓ Server avviato con successo")
                break
        except requests.exceptions.RequestException:
            pass
        time.sleep(1)
        print(".", end="", flush=True)
    else:
        print("\n✗ Server non si è avviato entro il tempo previsto")
        cleanup()
        sys.exit(1)
    
    print()
    
    # Test 2: Health check
    print("Test 2: Health check endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status code: {response.status_code}")
        print(f"Risposta: {response.json()}")
        assert response.status_code == 200, "Health check fallito"
        data = response.json()
        assert data['status'] == 'healthy', "Agente non healthy"
        assert data['agent'] == 'ready', "Agente non pronto"
        print("✓ Health check OK")
    except Exception as e:
        print(f"✗ Errore: {e}")
        cleanup()
        sys.exit(1)
    
    print()
    
    # Test 3: Endpoint /api/ask con domanda valida
    print("Test 3: Endpoint /api/ask con domanda valida...")
    try:
        domanda = "Cos'è il diabete?"
        print(f"Invio domanda: '{domanda}'")
        response = requests.post(
            f"{BASE_URL}/api/ask",
            json={"question": domanda},
            headers={"Content-Type": "application/json"}
        )
        print(f"Status code: {response.status_code}")
        assert response.status_code == 200, f"Errore status code: {response.status_code}"
        
        data = response.json()
        print("\nRisposta ricevuta:")
        print(f"  - answer_text: {data['answer_text'][:80]}...")
        print(f"  - bullets: {len(data['bullets'])} punti")
        print(f"  - source_links: {len(data['source_links'])} fonti")
        print(f"  - disclaimer: Presente")
        
        assert 'answer_text' in data, "Campo answer_text mancante"
        assert 'bullets' in data, "Campo bullets mancante"
        assert 'source_links' in data, "Campo source_links mancante"
        assert 'disclaimer' in data, "Campo disclaimer mancante"
        
        print("✓ Test domanda valida OK")
    except Exception as e:
        print(f"✗ Errore: {e}")
        cleanup()
        sys.exit(1)
    
    print()
    
    # Test 4: Endpoint /api/ask con domanda vuota (dovrebbe fallire)
    print("Test 4: Endpoint /api/ask con domanda vuota...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/ask",
            json={"question": ""},
            headers={"Content-Type": "application/json"}
        )
        print(f"Status code: {response.status_code}")
        assert response.status_code == 400, "Dovrebbe rifiutare domanda vuota"
        print("✓ Gestione errore OK (domanda vuota correttamente rifiutata)")
    except Exception as e:
        print(f"✗ Errore: {e}")
        cleanup()
        sys.exit(1)
    
    print()
    
    # Test 5: Endpoint /api/ask senza campo question
    print("Test 5: Endpoint /api/ask senza campo 'question'...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/ask",
            json={"other_field": "test"},
            headers={"Content-Type": "application/json"}
        )
        print(f"Status code: {response.status_code}")
        assert response.status_code == 400, "Dovrebbe rifiutare richiesta senza question"
        print("✓ Gestione errore OK (campo mancante correttamente rifiutato)")
    except Exception as e:
        print(f"✗ Errore: {e}")
        cleanup()
        sys.exit(1)
    
    print()
    
    # Test 6: Domanda in italiano
    print("Test 6: Domanda in italiano...")
    try:
        domanda = "Quali sono i sintomi dell'influenza?"
        print(f"Invio domanda: '{domanda}'")
        response = requests.post(
            f"{BASE_URL}/api/ask",
            json={"question": domanda},
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 200, f"Errore status code: {response.status_code}"
        data = response.json()
        print(f"✓ Risposta ricevuta: {data['answer_text'][:60]}...")
    except Exception as e:
        print(f"✗ Errore: {e}")
        cleanup()
        sys.exit(1)
    
    print()
    print("=" * 60)
    print("TUTTI I TEST API COMPLETATI CON SUCCESSO! ✓")
    print("=" * 60)
    print()
    print("Il server è ancora attivo su http://localhost:5000")
    print("Puoi testarlo manualmente con:")
    print()
    print("  curl http://localhost:5000/health")
    print()
    print("  curl -X POST http://localhost:5000/api/ask \\")
    print("    -H 'Content-Type: application/json' \\")
    print("    -d '{\"question\": \"Cos'è il diabete?\"}'")
    print()
    print("Premi Ctrl+C per terminare il server.")
    print()
    
    # Mantieni il server attivo
    server_process.wait()
    
except KeyboardInterrupt:
    print("\nInterrotto dall'utente")
    cleanup()
except Exception as e:
    print(f"\n✗ Errore imprevisto: {e}")
    import traceback
    traceback.print_exc()
    cleanup()
    sys.exit(1)
