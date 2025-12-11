#!/usr/bin/env python3
"""
Esempio semplice di come usare l'agente Medical Research Assistant.
Questo script mostra come integrare l'agente nel tuo codice Python.
"""

import sys
import os

# Aggiungi il percorso del backend al path Python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'medical_agent', 'backend'))

# Importa l'agente
from agent import MedicalResearchAgent

def main():
    """
    Esempio principale di utilizzo dell'agente.
    """
    print("=" * 70)
    print(" ESEMPIO DI UTILIZZO - Medical Research Assistant Agent")
    print("=" * 70)
    print()
    
    # Passo 1: Inizializza l'agente
    print("📋 Inizializzazione agente...")
    agente = MedicalResearchAgent()
    print("✓ Agente pronto!\n")
    
    # Passo 2: Prepara alcune domande di esempio
    domande = [
        "Cos'è il diabete di tipo 2?",
        "Quali sono i sintomi dell'ipertensione?",
        "Come si previene l'influenza?",
    ]
    
    # Passo 3: Fai domande all'agente
    print("💬 Facciamo alcune domande all'agente:\n")
    
    for i, domanda in enumerate(domande, 1):
        print(f"{'─' * 70}")
        print(f"Domanda {i}: {domanda}")
        print(f"{'─' * 70}")
        
        # Chiama il metodo ask() dell'agente
        risposta = agente.ask(domanda)
        
        # Mostra la risposta
        print(f"\n📝 Risposta:")
        print(f"   {risposta['answer_text']}\n")
        
        print("🔑 Punti chiave:")
        for j, punto in enumerate(risposta['bullets'], 1):
            print(f"   {j}. {punto}")
        
        print(f"\n📚 Fonti:")
        for j, fonte in enumerate(risposta['source_links'], 1):
            print(f"   {j}. {fonte}")
        
        print(f"\n⚠️  {risposta['disclaimer']}")
        print()
    
    # Passo 4: Esempio di uso programmatico
    print("=" * 70)
    print(" ESEMPIO DI USO PROGRAMMATICO")
    print("=" * 70)
    print()
    print("Puoi usare l'agente nel tuo codice in questo modo:\n")
    print("```python")
    print("from agent import MedicalResearchAgent")
    print("")
    print("# Inizializza")
    print("agente = MedicalResearchAgent()")
    print("")
    print("# Fai una domanda")
    print('risposta = agente.ask("La tua domanda qui")')
    print("")
    print("# Usa la risposta")
    print("print(risposta['answer_text'])")
    print("for punto in risposta['bullets']:")
    print("    print(punto)")
    print("```")
    print()
    
    # Passo 5: Esempio interattivo
    print("=" * 70)
    print(" MODALITÀ INTERATTIVA")
    print("=" * 70)
    print()
    print("Vuoi fare una domanda personalizzata? (s/n): ", end="")
    
    try:
        risposta_utente = input().strip().lower()
        
        if risposta_utente in ['s', 'si', 'sì', 'yes', 'y']:
            print()
            print("Inserisci la tua domanda: ", end="")
            domanda_utente = input().strip()
            
            if domanda_utente:
                print()
                print(f"{'─' * 70}")
                print(f"La tua domanda: {domanda_utente}")
                print(f"{'─' * 70}")
                
                risposta = agente.ask(domanda_utente)
                
                print(f"\n📝 Risposta:")
                print(f"   {risposta['answer_text']}\n")
                
                print("🔑 Punti chiave:")
                for j, punto in enumerate(risposta['bullets'], 1):
                    print(f"   {j}. {punto}")
                
                print(f"\n📚 Fonti:")
                for j, fonte in enumerate(risposta['source_links'], 1):
                    print(f"   {j}. {fonte}")
                
                print(f"\n⚠️  {risposta['disclaimer']}")
            else:
                print("\nNessuna domanda inserita.")
    except (EOFError, KeyboardInterrupt):
        print("\n\nInterrotto dall'utente.")
    
    print()
    print("=" * 70)
    print(" GRAZIE PER AVER USATO IL MEDICAL RESEARCH ASSISTANT!")
    print("=" * 70)
    print()
    print("📚 Per maggiori informazioni, consulta:")
    print("   - README_TEST_AGENTE.md")
    print("   - GUIDA_RAPIDA_TEST.md")
    print("   - medical_agent/README.md")
    print()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Errore: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
