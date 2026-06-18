#!/usr/bin/env python3
"""
Demonstration script for the Medical Research Agent.

This script shows how to use the MedicalResearchAgent to research
medical questions and format the results for beginners.
"""

import sys
import os

# Add the parent directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from medical_agent.agent.medical_agent import MedicalResearchAgent
from medical_agent.agent.wikipedia_client import WikipediaClient


def demonstrate_agent():
    """Demonstrate the medical research agent capabilities"""
    
    print("🏥 Medical Research Agent Demonstration")
    print("=" * 50)
    
    # Create the agent
    agent = MedicalResearchAgent()
    
    # Test questions
    test_questions = [
        "What are the symptoms of diabetes?",
        "Can you explain what hypertension means?", 
        "What causes headaches?",
        "What is the weather like?",  # Invalid question
        "Should I overdose on aspirin?"  # Inappropriate question
    ]
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n📝 Question {i}: {question}")
        print("-" * 30)
        
        try:
            result = agent.research(question)
            
            if result.get('status') == 'success':
                print(f"✅ Research successful!")
                print(f"📋 Title: {result.get('title', 'N/A')}")
                print(f"📄 Description: {result.get('description', 'N/A')}")
                
                # Show sections
                sections = result.get('sections', {})
                for section_name, content in sections.items():
                    if content.strip():
                        print(f"\n🔍 {section_name}:")
                        print(f"   {content.strip()}")
                
                # Show source
                url = result.get('url', '')
                if url:
                    print(f"\n🔗 Source: {url}")
                
                # Show disclaimer
                disclaimer = result.get('disclaimer', {})
                if disclaimer:
                    print(f"\n⚠️  {disclaimer.get('title', 'Disclaimer')}")
                    print(f"   {disclaimer.get('content', '')}")
                    
            else:
                print(f"❌ Research failed: {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            print(f"💥 Exception occurred: {str(e)}")
        
        print("\n" + "=" * 50)


def demonstrate_wikipedia_client():
    """Demonstrate the Wikipedia client capabilities"""
    
    print("\n🔍 Wikipedia Client Demonstration")
    print("=" * 50)
    
    # Create the client
    client = WikipediaClient(timeout=10)
    
    # Test query normalization
    test_queries = [
        "  DIABETES  ",
        "Dr. Smith's condition",
        "Hypertension symptoms",
        ""  # Empty query
    ]
    
    print("\n🧹 Query Normalization Tests:")
    for query in test_queries:
        try:
            normalized = client._normalize_query(query)
            print(f"  '{query}' → '{normalized}'")
        except ValueError as e:
            print(f"  '{query}' → ERROR: {e}")
    
    print("\n🌐 API Tests (requires internet connection):")
    
    # Test search functionality
    test_search = "diabetes"
    print(f"\n🔍 Searching for: {test_search}")
    try:
        search_results = client.search_pages(test_search, limit=3)
        print(f"  Status: {search_results.get('status')}")
        if search_results.get('status') == 'success':
            print(f"  Found {len(search_results.get('results', []))} results")
            for result in search_results.get('results', [])[:2]:
                print(f"    - {result.get('title', 'Unknown')}")
    except Exception as e:
        print(f"  Error: {e}")


def demonstrate_step_by_step():
    """Demonstrate step-by-step processing"""
    
    print("\n🔬 Step-by-Step Processing Demonstration")
    print("=" * 50)
    
    agent = MedicalResearchAgent()
    
    question = "What are the symptoms of diabetes?"
    print(f"🔍 Processing: {question}")
    
    try:
        step_results = agent.get_step_results(question)
        
        print("\n📊 Step Results:")
        
        # Validation step
        validation = step_results.get('validation', {})
        print(f"\n1️⃣  Validation:")
        print(f"   Valid: {validation.get('is_valid', False)}")
        print(f"   Question: {validation.get('sanitized_question', 'N/A')}")
        
        # Retrieval step
        retrieval = step_results.get('retrieval', {})
        print(f"\n2️⃣  Wikipedia Retrieval:")
        print(f"   Status: {retrieval.get('status', 'N/A')}")
        if retrieval.get('primary_result'):
            primary = retrieval['primary_result']
            print(f"   Title: {primary.get('title', 'N/A')}")
            print(f"   Extract length: {len(primary.get('extract', ''))} characters")
        
        # Formatting step
        formatting = step_results.get('formatting', {})
        print(f"\n3️⃣  Content Formatting:")
        print(f"   Status: {formatting.get('status', 'N/A')}")
        sections = formatting.get('sections', {})
        print(f"   Sections created: {len(sections)}")
        for section_name in sections.keys():
            print(f"     - {section_name}")
        
        # Final step
        final = step_results.get('final', {})
        print(f"\n4️⃣  Final Result:")
        print(f"   Has disclaimer: {'disclaimer' in final}")
        print(f"   Has sections: {'sections' in final}")
        
    except Exception as e:
        print(f"💥 Exception: {str(e)}")


def main():
    """Main demonstration function"""
    
    print("Starting Medical Research Agent demonstrations...")
    
    # Check if we have internet connectivity (basic check)
    try:
        import urllib.request
        req = urllib.request.Request("https://www.wikipedia.org", 
                                   headers={'User-Agent': 'MedicalAgentDemo/1.0'})
        urllib.request.urlopen(req, timeout=5)
        internet_available = True
    except:
        internet_available = False
    
    if internet_available:
        print("✅ Internet connection detected - full tests will run")
    else:
        print("❌ No internet connection - some tests will be skipped")
    
    # Run demonstrations
    demonstrate_agent()
    demonstrate_wikipedia_client()
    demonstrate_step_by_step()
    
    print("\n🎉 Demonstration complete!")
    print("\nTo run the unit tests:")
    print("  python -m pytest tests/test_medical_agent.py -v")
    print("  python tests/test_medical_agent.py")


if __name__ == "__main__":
    main()