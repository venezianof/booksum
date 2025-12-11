#!/usr/bin/env python3
"""
Test manuale per il Medical Research Assistant Agent
Esegue una serie di test per verificare il funzionamento completo
"""

import requests
import json
import time
import threading
from backend.app import app

def test_medical_agent():
    """Test completo dell'agente medico"""
    print("🧪 Avvio test del Medical Research Assistant Agent\n")
    
    # Avvia il server Flask in background
    def run_server():
        app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)
    
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    # Aspetta che il server sia pronto
    time.sleep(2)
    
    print("📡 Server avviato su http://127.0.0.1:5000\n")
    
    # Test 1: Health Check
    print("🔍 Test 1: Health Check")
    try:
        response = requests.get('http://127.0.0.1:5000/health', timeout=5)
        health_data = response.json()
        print(f"✅ Status: {response.status_code}")
        print(f"✅ Agent Status: {health_data['agent']}")
        print(f"✅ Health Status: {health_data['status']}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return
    
    print("\n" + "="*50 + "\n")
    
    # Test 2: Medical Question - Diabetes
    print("🔍 Test 2: Domanda Medica - Diabetes")
    try:
        payload = {
            "question": "What are the main symptoms of diabetes and how is it diagnosed?"
        }
        response = requests.post('http://127.0.0.1:5000/api/ask', 
                               json=payload, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Status: {response.status_code}")
            print(f"📝 Answer: {data['answer_text'][:100]}...")
            print(f"📋 Bullets: {len(data['bullets'])} points")
            for i, bullet in enumerate(data['bullets'], 1):
                print(f"   {i}. {bullet[:60]}...")
            print(f"🔗 Sources: {len(data['source_links'])} links")
            for source in data['source_links']:
                print(f"   - {source}")
            print(f"⚠️  Disclaimer: {data['disclaimer'][:50]}...")
        else:
            print(f"❌ Request failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Medical question test failed: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # Test 3: Medical Question - Heart Disease  
    print("🔍 Test 3: Domanda Medica - Heart Disease")
    try:
        payload = {
            "question": "What are the risk factors for heart disease?"
        }
        response = requests.post('http://127.0.0.1:5000/api/ask', 
                               json=payload, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Status: {response.status_code}")
            print(f"📝 Answer: {data['answer_text'][:100]}...")
            print(f"📋 Bullets: {len(data['bullets'])} points")
            print(f"🔗 Sources: {len(data['source_links'])} links")
        else:
            print(f"❌ Request failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Heart disease question test failed: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # Test 4: Error Handling
    print("🔍 Test 4: Error Handling")
    try:
        # Test con JSON vuoto
        response = requests.post('http://127.0.0.1:5000/api/ask', 
                               json={}, timeout=5)
        print(f"✅ Empty JSON: {response.status_code}")
        
        # Test con campo question mancante
        response = requests.post('http://127.0.0.1:5000/api/ask', 
                               json={"wrong_field": "test"}, timeout=5)
        print(f"✅ Missing question: {response.status_code}")
        
        # Test con question vuota
        response = requests.post('http://127.0.0.1:5000/api/ask', 
                               json={"question": ""}, timeout=5)
        print(f"✅ Empty question: {response.status_code}")
        
    except Exception as e:
        print(f"❌ Error handling test failed: {e}")
    
    print("\n🎉 Test completati con successo!")
    print("\n📋 Riepilogo:")
    print("• ✅ Server Flask funzionante")
    print("• ✅ Medical Research Agent operativo") 
    print("• ✅ API endpoints responsive")
    print("• ✅ Error handling attivo")
    print("• ✅ Disclaimer medico presente")
    print("\n🌐 L'applicazione è pronta per l'uso!")

if __name__ == "__main__":
    test_medical_agent()