"""
Unit tests for the Medical Research Agent.

These tests use mocked HTTP responses to verify the agent's behavior
without making actual network requests to Wikipedia.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add the parent directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from medical_agent.agent.wikipedia_client import WikipediaClient
from medical_agent.agent.medical_agent import (
    MedicalResearchAgent,
    validate_health_question,
    format_medical_info_for_beginners,
    add_safety_disclaimer
)


class TestWikipediaClient(unittest.TestCase):
    """Test the Wikipedia client functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.client = WikipediaClient(timeout=5)
    
    def test_normalize_query(self):
        """Test query normalization"""
        # Test basic normalization
        result = self.client._normalize_query("  DIABETES  ")
        self.assertEqual(result, "diabetes")
        
        # Test medical abbreviation handling
        result = self.client._normalize_query("Dr. Smith diagnosed my condition")
        self.assertIn("doctor smith diagnosed", result)
        
        # Test empty query handling
        with self.assertRaises(ValueError):
            self.client._normalize_query("")
    
    @patch('urllib.request.urlopen')
    def test_get_page_summary_success(self, mock_urlopen):
        """Test successful page summary retrieval"""
        # Mock successful HTTP response
        mock_response = Mock()
        mock_response.status = 200
        mock_response.read.return_value = b'{"title": "Diabetes", "extract": "Diabetes is a disease", "content_urls": {"desktop": {"page": "https://example.com"}}}'
        mock_response.__enter__ = Mock(return_value=mock_response)
        mock_response.__exit__ = Mock(return_value=False)
        mock_urlopen.return_value = mock_response
        
        result = self.client.get_page_summary("diabetes")
        
        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['title'], 'Diabetes')
        self.assertEqual(result['extract'], 'Diabetes is a disease')
        self.assertEqual(result['url'], 'https://example.com')
    
    @patch('urllib.request.urlopen')
    def test_get_page_summary_404_error(self, mock_urlopen):
        """Test 404 error handling"""
        # Mock 404 HTTP error
        from urllib.error import HTTPError
        mock_urlopen.side_effect = HTTPError(None, 404, "Not Found", None, None)
        
        result = self.client.get_page_summary("nonexistent")
        
        self.assertEqual(result['status'], 'error')
        self.assertIn('Wikipedia page not found', result['error'])
    
    @patch('urllib.request.urlopen')
    def test_get_medical_info_success(self, mock_urlopen):
        """Test comprehensive medical info retrieval"""
        # Mock search response
        search_response = Mock()
        search_response.status = 200
        search_response.read.return_value = b'{"pages": [{"title": "Diabetes"}]}'
        search_response.__enter__ = Mock(return_value=search_response)
        search_response.__exit__ = Mock(return_value=False)
        
        # Mock summary response
        summary_response = Mock()
        summary_response.status = 200
        summary_response.read.return_value = b'{"title": "Diabetes", "description": "A metabolic disease", "extract": "Diabetes is characterized by high blood sugar", "content_urls": {"desktop": {"page": "https://en.wikipedia.org/wiki/Diabetes"}}, "thumbnail": {"source": "thumb.jpg"}}'
        summary_response.__enter__ = Mock(return_value=summary_response)
        summary_response.__exit__ = Mock(return_value=False)
        
        # Mock related response
        related_response = Mock()
        related_response.status = 200
        related_response.read.return_value = b'{"pages": [{"title": "Type 1 diabetes", "description": "A form of diabetes", "extract": "Type 1 diabetes...", "content_urls": {"desktop": {"page": "https://en.wikipedia.org/wiki/Type_1_diabetes"}}}]}'
        related_response.__enter__ = Mock(return_value=related_response)
        related_response.__exit__ = Mock(return_value=False)
        
        mock_urlopen.side_effect = [search_response, summary_response, related_response]
        
        result = self.client.get_medical_info("diabetes")
        
        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['query'], "diabetes")
        self.assertEqual(result['primary_result']['title'], 'Diabetes')
        self.assertEqual(result['primary_result']['description'], 'A metabolic disease')
        self.assertIn('Type 1 diabetes', str(result['related_pages']))


class TestValidationFunctions(unittest.TestCase):
    """Test the validation and formatting functions"""
    
    def test_validate_health_question_valid(self):
        """Test validation of valid health questions"""
        valid_questions = [
            "What are the symptoms of diabetes?",
            "What is hypertension?",
            "Tell me about heart disease symptoms",
            "What is diabetes?",
            "What causes headaches?"
        ]
        
        for question in valid_questions:
            result = validate_health_question(question)
            self.assertTrue(result['is_valid'], f"Question '{question}' should be valid but got: {result}")
            self.assertEqual(result['sanitized_question'], question)
    
    def test_validate_health_question_invalid_empty(self):
        """Test validation of empty questions"""
        result = validate_health_question("")
        self.assertFalse(result['is_valid'])
        self.assertIn('Question cannot be empty', result['error'])
    
    def test_validate_health_question_non_medical(self):
        """Test validation of non-medical questions"""
        result = validate_health_question("What is the weather like?")
        self.assertFalse(result['is_valid'])
        self.assertIn('not appear to be a health-related question', result['error'])
    
    def test_validate_health_question_inappropriate(self):
        """Test validation of inappropriate medical questions"""
        inappropriate_questions = [
            "Can you diagnose my symptoms?",  # matches 'diagnose'
            "Should I take aspirin for my headache?",  # matches 'should i take'
            "What medication should I prescribe for this?",  # matches 'prescribe'
            "I need urgent medical advice",  # matches 'medical advice'
            "I'm having suicidal thoughts, what should I do?",  # matches 'suicide'
            "Is this life-threatening?",  # matches 'life-threatening'
            "Should I overdose on medication?",  # matches 'overdose'
        ]
        
        for question in inappropriate_questions:
            result = validate_health_question(question)
            self.assertFalse(result['is_valid'], f"Question '{question}' should be invalid")
            self.assertIn('professional medical attention', result['error'])
    
    def test_format_medical_info_for_beginners(self):
        """Test formatting of medical information"""
        # Mock medical data with clearer categorization
        medical_data = {
            'status': 'success',
            'primary_result': {
                'title': 'Diabetes',
                'description': 'A metabolic disease',
                'extract': 'Diabetes is a metabolic disorder characterized by high blood sugar levels. Common symptoms include frequent urination and excessive thirst. Patients should seek immediate medical attention if symptoms worsen or if they experience severe complications.',
                'url': 'https://example.com'
            },
            'related_pages': []
        }
        
        result = format_medical_info_for_beginners(medical_data)
        
        self.assertEqual(result['status'], 'success')
        self.assertIn('Diabetes', result['title'])
        self.assertIn('Cos\'è', result['sections'])
        self.assertIn('Sintomi comuni', result['sections'])
        self.assertIn('Quando consultare un medico', result['sections'])
        
        # Check that content was actually categorized
        self.assertGreater(len(result['sections']['Cos\'è']), 0)
        self.assertGreater(len(result['sections']['Sintomi comuni']), 0)
        # The last sentence should be categorized as "when to see a doctor"
        self.assertGreater(len(result['sections']['Quando consultare un medico']), 0)
    
    def test_add_safety_disclaimer(self):
        """Test adding safety disclaimers"""
        medical_info = {
            'title': 'Test',
            'sections': {'Cos\'è': 'Test content'}
        }
        
        result = add_safety_disclaimer(medical_info)
        
        self.assertIn('disclaimer', result)
        self.assertEqual(result['disclaimer']['title'], '⚠️ Importante - Disclaimer Medico')
        self.assertIn('Le informazioni fornite', result['disclaimer']['content'])
        self.assertTrue(result['disclaimer']['is_disclaimer'])


class TestMedicalResearchAgent(unittest.TestCase):
    """Test the main MedicalResearchAgent class"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Create a mock Wikipedia client
        self.mock_wikipedia_client = Mock(spec=WikipediaClient)
        
        # Create agent with mocked dependencies
        self.agent = MedicalResearchAgent(wikipedia_client=self.mock_wikipedia_client)
    
    def test_agent_initialization(self):
        """Test agent initialization with dependency injection"""
        # Test default initialization
        agent_default = MedicalResearchAgent()
        self.assertIsInstance(agent_default, MedicalResearchAgent)
        
        # Test custom initialization
        mock_client = Mock()
        agent_custom = MedicalResearchAgent(wikipedia_client=mock_client)
        self.assertEqual(agent_custom.wikipedia_client, mock_client)
    
    def test_research_valid_question_success(self):
        """Test successful research of a valid question"""
        # Mock successful Wikipedia response
        mock_medical_info = {
            'status': 'success',
            'primary_result': {
                'title': 'Diabetes',
                'description': 'A metabolic disease',
                'extract': 'Diabetes is characterized by high blood sugar levels. Common symptoms include frequent urination and excessive thirst.',
                'url': 'https://en.wikipedia.org/wiki/Diabetes'
            },
            'related_pages': []
        }
        
        self.mock_wikipedia_client.get_medical_info.return_value = mock_medical_info
        
        result = self.agent.research("What are the symptoms of diabetes?")
        
        # Verify the pipeline processed correctly
        self.assertEqual(result['status'], 'success')
        self.assertIn('sections', result)
        self.assertIn('disclaimer', result)
        
        # Check that the original data is preserved in the formatted result
        self.assertIn('title', result)
        self.assertEqual(result['title'], 'Diabetes')
    
    def test_research_invalid_question(self):
        """Test research of an invalid question"""
        result = self.agent.research("What is the weather like?")
        
        # Should return validation error
        self.assertEqual(result['status'], 'error')
        self.assertIn('health-related question', result['error'])
    
    def test_research_inappropriate_question(self):
        """Test research of an inappropriate question"""
        result = self.agent.research("Should I take an overdose of aspirin?")
        
        # Should return validation error for inappropriate content
        self.assertEqual(result['status'], 'error')
        self.assertIn('professional medical attention', result['error'])
    
    def test_research_wikipedia_error(self):
        """Test handling of Wikipedia API errors"""
        # Mock Wikipedia client returning error
        self.mock_wikipedia_client.get_medical_info.return_value = {
            'status': 'error',
            'error': 'Wikipedia API temporarily unavailable'
        }
        
        result = self.agent.research("What is diabetes?")
        
        # Should still get formatted response with error handling
        self.assertIn('status', result)
        # The error should be propagated through the pipeline
    
    def test_get_step_results(self):
        """Test getting intermediate results for debugging"""
        # Mock successful responses
        mock_medical_info = {
            'status': 'success',
            'primary_result': {
                'title': 'Diabetes',
                'description': 'A metabolic disease',
                'extract': 'Diabetes is characterized by high blood sugar.',
                'url': 'https://example.com'
            },
            'related_pages': []
        }
        
        self.mock_wikipedia_client.get_medical_info.return_value = mock_medical_info
        
        result = self.agent.get_step_results("What is diabetes?")
        
        # Verify all pipeline steps were executed
        self.assertIn('question', result)
        self.assertIn('validation', result)
        self.assertIn('retrieval', result)
        self.assertIn('formatting', result)
        self.assertIn('final', result)
        
        # Verify validation passed
        self.assertTrue(result['validation']['is_valid'])
        self.assertEqual(result['retrieval']['primary_result']['title'], 'Diabetes')
    
    def test_dependency_injection(self):
        """Test dependency injection for easier testing"""
        # Create custom functions for testing
        def custom_validator(question):
            return {
                'is_valid': True,
                'sanitized_question': question + ' (validated)',
                'is_question': True
            }
        
        def custom_formatter(medical_data):
            return {
                **medical_data,
                'custom_formatting': True,
                'sections': {'Custom': 'Section'}
            }
        
        # Create agent with custom functions
        agent = MedicalResearchAgent(
            question_validator=custom_validator,
            content_formatter=custom_formatter
        )
        
        # Test that custom functions are used
        result = agent.research("What is diabetes?")
        
        # Should use custom formatting
        self.assertTrue(result.get('custom_formatting', False))
        self.assertIn('Custom', result['sections'])


class TestIntegration(unittest.TestCase):
    """Integration tests using mocked HTTP requests"""
    
    @patch('urllib.request.urlopen')
    def test_full_integration_with_mocks(self, mock_urlopen):
        """Test complete integration with mocked HTTP responses"""
        # Create a real agent but mock the HTTP layer
        agent = MedicalResearchAgent()
        
        # Mock search response
        search_response = Mock()
        search_response.status = 200
        search_response.read.return_value = b'{"pages": [{"title": "Diabetes mellitus"}]}'
        search_response.__enter__ = Mock(return_value=search_response)
        search_response.__exit__ = Mock(return_value=False)
        
        # Mock summary response
        summary_response = Mock()
        summary_response.status = 200
        summary_response.read.return_value = b'''{
            "title": "Diabetes mellitus",
            "description": "A metabolic disorder",
            "extract": "Diabetes mellitus is a group of metabolic disorders characterized by chronic high blood sugar levels. Symptoms include frequent urination, excessive thirst, and unexplained weight loss. Patients should consult healthcare providers for proper diagnosis and treatment.",
            "content_urls": {"desktop": {"page": "https://en.wikipedia.org/wiki/Diabetes_mellitus"}},
            "thumbnail": {"source": "thumb.jpg"}
        }'''
        summary_response.__enter__ = Mock(return_value=summary_response)
        summary_response.__exit__ = Mock(return_value=False)
        
        # Mock related response
        related_response = Mock()
        related_response.status = 200
        related_response.read.return_value = b'''{
            "pages": [
                {
                    "title": "Type 1 diabetes",
                    "description": "An autoimmune form of diabetes",
                    "extract": "Type 1 diabetes is characterized by the inability to produce insulin.",
                    "content_urls": {"desktop": {"page": "https://en.wikipedia.org/wiki/Type_1_diabetes"}}
                }
            ]
        }'''
        related_response.__enter__ = Mock(return_value=related_response)
        related_response.__exit__ = Mock(return_value=False)
        
        mock_urlopen.side_effect = [search_response, summary_response, related_response]
        
        # Test the complete pipeline
        result = agent.research("What is diabetes mellitus and what are its symptoms?")
        
        # Verify the complete flow worked
        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['title'], 'Diabetes mellitus')
        self.assertIn('Cos\'è', result['sections'])
        self.assertIn('Sintomi comuni', result['sections'])
        self.assertIn('Quando consultare un medico', result['sections'])
        self.assertIn('disclaimer', result)
        self.assertIn('Type 1 diabetes', str(result['related_pages']))


if __name__ == '__main__':
    unittest.main()