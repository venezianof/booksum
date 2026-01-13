#!/usr/bin/env python3
"""Quick test script for the medical agent."""

from backend.agent import MedicalResearchAgent

def test_agent():
    print("Initializing Medical Research Agent...")
    agent = MedicalResearchAgent()
    
    print("\nTesting with question: 'What is diabetes?'")
    result = agent.ask('What is diabetes?')
    
    print("\n" + "="*60)
    print("ANSWER:")
    print("="*60)
    print(result['answer_text'])
    
    print("\n" + "="*60)
    print("KEY POINTS:")
    print("="*60)
    for bullet in result['bullets']:
        print(f"  • {bullet}")
    
    print("\n" + "="*60)
    print("SOURCES:")
    print("="*60)
    for link in result['source_links']:
        print(f"  {link}")
    
    print("\n" + "="*60)
    print("Test successful!")
    print("="*60)

if __name__ == "__main__":
    test_agent()
