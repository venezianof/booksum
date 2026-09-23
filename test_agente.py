#!/usr/bin/env python3
"""
Script di test per l'agente Medical Research Assistant.
Questo script verifica che l'agente funzioni correttamente.
"""

import sys
import os

# Aggiungi il percorso del backend al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'medical_agent', 'backend'))

print("=" * 60)
print("TEST AGENTE MEDICAL RESEARCH ASSISTANT")
print("=" * 60)
print()

# Test 1: Importazione moduli
print("Test 1: Verifica importazione moduli...")
try:
    from agent import MedicalResearchAgent
    print("✓ Modulo agent importato con successo")
except Exception as e:
    print(f"✗ Errore nell'importazione: {e}")
    sys.exit(1)

print()

# Test 2: Inizializzazione agente
print("Test 2: Inizializzazione agente...")
try:
    agente = MedicalResearchAgent()
    print("✓ Agente inizializzato con successo")
except Exception as e:
    print(f"✗ Errore nell'inizializzazione: {e}")
    sys.exit(1)

print()

# Test 3: Domanda semplice
print("Test 3: Invio domanda all'agente...")
domanda = "Cos'è il diabete?"
print(f"Domanda: '{domanda}'")
print()

try:
    risposta = agente.ask(domanda)
    print("✓ Risposta ricevuta con successo")
    print()
    print("-" * 60)
    print("RISPOSTA:")
    print("-" * 60)
    print(f"\nTesto risposta:\n{risposta['answer_text']}")
    print(f"\nPunti chiave:")
    for i, bullet in enumerate(risposta['bullets'], 1):
        print(f"  {i}. {bullet}")
    print(f"\nFonti:")
    for i, link in enumerate(risposta['source_links'], 1):
        print(f"  {i}. {link}")
    print(f"\n{risposta['disclaimer']}")
    print("-" * 60)
except Exception as e:
    print(f"✗ Errore nell'invio della domanda: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()

# Test 4: Domanda complessa
print("Test 4: Test con domanda più complessa...")
domanda_complessa = "Quali sono i trattamenti per l'ipertensione?"
print(f"Domanda: '{domanda_complessa}'")
print()

try:
    risposta2 = agente.ask(domanda_complessa)
    print("✓ Risposta ricevuta con successo")
    print(f"\nRisposta: {risposta2['answer_text'][:100]}...")
except Exception as e:
    print(f"✗ Errore: {e}")
    sys.exit(1)

print()

# Test 5: Verifica struttura risposta
print("Test 5: Verifica struttura della risposta...")
try:
    assert 'answer_text' in risposta2, "Campo 'answer_text' mancante"
    assert 'bullets' in risposta2, "Campo 'bullets' mancante"
    assert 'source_links' in risposta2, "Campo 'source_links' mancante"
    assert 'disclaimer' in risposta2, "Campo 'disclaimer' mancante"
    assert isinstance(risposta2['bullets'], list), "'bullets' deve essere una lista"
    assert isinstance(risposta2['source_links'], list), "'source_links' deve essere una lista"
    print("✓ Struttura della risposta corretta")
except AssertionError as e:
    print(f"✗ Errore nella struttura: {e}")
    sys.exit(1)

print()
print("=" * 60)
print("TUTTI I TEST COMPLETATI CON SUCCESSO! ✓")
print("=" * 60)
print()
print("L'agente funziona correttamente!")
print("Per avviare il server web, esegui:")
print("  cd medical_agent")
print("  python backend/app.py")
print()
