"""
Medical Research Agent using LangChain primitives.

This module implements a research agent that validates health questions,
fetches information from Wikipedia, and formats it for beginners with
proper safety disclaimers.
"""

from typing import Dict, Any, Optional, List, Callable
import re
from abc import ABC, abstractmethod


# Mock LangChain interfaces for demonstration purposes
# In a real implementation, these would be from langchain_core
class Runnable(ABC):
    """Base interface for Runnable components (mock of LangChain's Runnable)"""
    
    @abstractmethod
    def invoke(self, input: Any) -> Any:
        """Invoke the runnable with input"""
        pass


class RunnableSequence(Runnable):
    """A sequence of runnable components (mock of LangChain's RunnableSequence)"""
    
    def __init__(self, steps: List[Runnable]):
        """
        Initialize a sequence of processing steps.
        
        Args:
            steps: List of Runnable components to execute in sequence
        """
        self.steps = steps
        
    def invoke(self, input: Any) -> Any:
        """
        Execute the sequence of steps.
        
        Each step receives the output of the previous step as input.
        
        Args:
            input: Initial input to the sequence
            
        Returns:
            Final processed output
        """
        current_input = input
        
        for step in self.steps:
            current_input = step.invoke(current_input)
            
        return current_input


# Helper functions for LangChain-style processing
def validate_health_question(question: str) -> Dict[str, Any]:
    """
    Validate if the input is a legitimate health question.
    
    This function checks:
    - Question is not empty
    - Contains medical-related keywords
    - Is not asking for specific medical diagnosis
    - Is phrased as a question
    
    Args:
        question: The user question to validate
        
    Returns:
        Dictionary with validation results
    """
    if not question or not question.strip():
        return {
            'is_valid': False,
            'error': 'Question cannot be empty',
            'sanitized_question': ''
        }
    
    sanitized = question.strip()
    
    # Check for inappropriate requests FIRST (we can't provide specific medical advice)
    inappropriate_patterns = [
        r'(diagnose|diagnosis)\b',
        r'\bshould i take\b',
        r'\bprescribe\b',
        r'\bmedical advice\b',
        r'\bourge\b',
        r'\bemergency\b',
        r'\blife-threatening\b',
        r'\boverdose\b',
        r'\bsuicide\b',
        r'\bsuicidal\b',
        r'\bself-harm\b',
        r'\bself harm\b',
        r'\bwhat should i do\?'  # This will catch "what should I do" questions
    ]
    
    is_inappropriate = any(re.search(pattern, sanitized.lower()) for pattern in inappropriate_patterns)
    
    if is_inappropriate:
        return {
            'is_valid': False,
            'error': 'This type of medical question requires professional medical attention. Please consult a healthcare provider.',
            'sanitized_question': sanitized
        }
    
    # Medical-related keywords that make this a health question
    medical_keywords = [
        'health', 'medical', 'medicine', 'doctor', 'physician', 'symptom', 'symptoms',
        'disease', 'disorder', 'condition', 'treatment', 'medication', 'drug',
        'pain', 'fever', 'cough', 'headache', 'diabetes', 'cancer', 'heart',
        'brain', 'lung', 'liver', 'kidney', 'stomach', 'back', 'neck',
        'infection', 'virus', 'bacteria', 'allergy', 'anxiety', 'depression',
        'mental health', 'physical therapy', 'surgery', 'diagnosis', 'prognosis',
        'blood pressure', 'cholesterol', 'asthma', 'bronchitis', 'pneumonia',
        'migraine', 'arthritis', 'osteoporosis', 'stroke', 'heart attack',
        'hypertension', 'hypotension', 'appendicitis', 'bronchitis', 'hepatitis',
        'thoughts', 'mental'
    ]
    
    has_medical_content = any(keyword in sanitized.lower() for keyword in medical_keywords)
    
    if not has_medical_content:
        return {
            'is_valid': False,
            'error': 'This does not appear to be a health-related question. Please ask about medical topics, symptoms, or health conditions.',
            'sanitized_question': sanitized
        }
    
    # Check if it's a question (ends with ? or contains question words)
    question_patterns = [
        r'.*\?$',  # Ends with ?
        r'^(what|when|where|who|why|how|can|should|do|does|did|is|are|will|would|could)\s+.*',
        r'^(tell me about|explain|describe|what is|what are)\s+.*'
    ]
    
    is_question = any(re.match(pattern, sanitized.lower()) for pattern in question_patterns)
    
    return {
        'is_valid': True,
        'sanitized_question': sanitized,
        'is_question': is_question
    }


def format_medical_info_for_beginners(medical_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Format medical information into beginner-friendly sections.
    
    Args:
        medical_data: Raw medical information from Wikipedia
        
    Returns:
        Formatted medical information with beginner sections
    """
    if medical_data.get('status') != 'success':
        return medical_data
    
    primary = medical_data.get('primary_result', {})
    extract = primary.get('extract', '')
    
    # Split extract into sentences for processing
    sentences = re.split(r'[.!?]+', extract)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    # Organize information into beginner-friendly sections
    sections = {
        "Cos'è": "",  # "What is it" in Italian
        "Sintomi comuni": "",  # "Common symptoms"
        "Quando consultare un medico": ""  # "When to consult a doctor"
    }
    
    # Try to categorize sentences into sections
    what_section_keywords = [
        'is a', 'are', 'refers to', 'characterized by', 'involves',
        'una malattia', 'una condizione', 'un disturbo', 'una sindrome'
    ]
    
    symptom_keywords = [
        'symptom', 'symptoms', 'sign', 'signs', 'manifestation', 'manifestations',
        'include', 'includes', 'may cause', 'can cause', 'causes',
        'dolore', 'febbre', 'tosse', 'mal di testa', 'nausea'
    ]
    
    when_to_see_doctor_keywords = [
        'consult', 'see a doctor', 'medical attention', 'seek help',
        'emergency', 'immediately', 'severe', 'worsening',
        'consultare un medico', 'ricorrere al medico', 'attenzione medica',
        'should consult', 'doctor if', 'seek medical', 'get medical'
    ]
    
    for sentence in sentences:
        sentence_lower = sentence.lower()
        
        # Check for when to see a doctor FIRST (higher priority)
        if any(keyword in sentence_lower for keyword in when_to_see_doctor_keywords):
            sections["Quando consultare un medico"] += sentence + ". "
        
        # Check for "what is" content
        elif any(keyword in sentence_lower for keyword in what_section_keywords):
            sections["Cos'è"] += sentence + ". "
        
        # Check for symptoms (lowest priority)
        elif any(keyword in sentence_lower for keyword in symptom_keywords):
            sections["Sintomi comuni"] += sentence + ". "
    
    # If no specific categorization worked, put everything in "Cos'è"
    if not any(sections.values()):
        sections["Cos'è"] = extract
    
    return {
        'query': medical_data.get('query', ''),
        'title': primary.get('title', ''),
        'description': primary.get('description', ''),
        'sections': sections,
        'url': primary.get('url', ''),
        'thumbnail': primary.get('thumbnail', ''),
        'related_pages': medical_data.get('related_pages', []),
        'status': 'success'
    }


def add_safety_disclaimer(medical_info: Dict[str, Any]) -> Dict[str, Any]:
    """
    Add appropriate safety disclaimers to medical information.
    
    Args:
        medical_info: Formatted medical information
        
    Returns:
        Medical information with safety disclaimers
    """
    disclaimer = {
        'title': '⚠️ Importante - Disclaimer Medico',
        'content': (
            'Le informazioni fornite sono solo a scopo educativo e non sostituiscono '
            'il consiglio medico professionale. Non utilizzare queste informazioni '
            'per autodiagnosi o automedicazione. Sempre consultare un medico qualificato '
            'per diagnosi e trattamenti. In caso di emergenza medica, contattare '
            'immediatamente i servizi di emergenza.'
        ),
        'is_disclaimer': True
    }
    
    return {
        **medical_info,
        'disclaimer': disclaimer
    }


# Individual processing steps that can be used in a LangChain-style pipeline
class QuestionValidator(Runnable):
    """Validate incoming health questions"""
    
    def __init__(self, validation_function: Callable = None):
        """
        Initialize the validator.
        
        Args:
            validation_function: Function to use for validation (allows dependency injection)
        """
        self.validate = validation_function or validate_health_question
    
    def invoke(self, question: str) -> Dict[str, Any]:
        """Validate the health question"""
        return self.validate(question)


class WikipediaRetriever(Runnable):
    """Retrieve medical information from Wikipedia"""
    
    def __init__(self, wikipedia_client):
        """
        Initialize the retriever.
        
        Args:
            wikipedia_client: WikipediaClient instance (dependency injection for testing)
        """
        self.wikipedia_client = wikipedia_client
    
    def invoke(self, validation_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Retrieve information based on validation result.
        
        Args:
            validation_result: Result from question validation
            
        Returns:
            Medical information from Wikipedia
        """
        if not validation_result.get('is_valid', False):
            return {
                'status': 'error',
                'error': validation_result.get('error', 'Invalid question'),
                'query': validation_result.get('sanitized_question', '')
            }
        
        query = validation_result.get('sanitized_question', '')
        
        # Use the injected Wikipedia client to get medical information
        medical_info = self.wikipedia_client.get_medical_info(query)
        
        return medical_info


class ContentFormatter(Runnable):
    """Format medical content for beginners"""
    
    def __init__(self, formatter_function: Callable = None):
        """
        Initialize the formatter.
        
        Args:
            formatter_function: Function to use for formatting (allows dependency injection)
        """
        self.format = formatter_function or format_medical_info_for_beginners
    
    def invoke(self, medical_data: Dict[str, Any]) -> Dict[str, Any]:
        """Format the medical information for beginners"""
        return self.format(medical_data)


class SafetyDisclaimer(Runnable):
    """Add safety disclaimers to medical information"""
    
    def __init__(self, disclaimer_function: Callable = None):
        """
        Initialize the disclaimer adder.
        
        Args:
            disclaimer_function: Function to use for adding disclaimers (allows dependency injection)
        """
        self.add_disclaimer = disclaimer_function or add_safety_disclaimer
    
    def invoke(self, medical_info: Dict[str, Any]) -> Dict[str, Any]:
        """Add safety disclaimers to the medical information"""
        return self.add_disclaimer(medical_info)


class MedicalResearchAgent:
    """
    A medical research agent that uses LangChain-style processing pipeline.
    
    This agent:
    1. Validates incoming health questions
    2. Retrieves information from Wikipedia
    3. Formats information for beginners
    4. Adds safety disclaimers
    
    The agent supports dependency injection for easier testing and flexibility.
    """
    
    def __init__(self, 
                 wikipedia_client=None,
                 question_validator=None,
                 wikipedia_retriever=None,
                 content_formatter=None,
                 safety_disclaimer_adder=None):
        """
        Initialize the medical research agent.
        
        Args:
            wikipedia_client: WikipediaClient instance (injected for testing)
            question_validator: Validation function (injected for testing)
            wikipedia_retriever: Retrieval function (injected for testing)
            content_formatter: Formatting function (injected for testing)
            safety_disclaimer_adder: Disclaimer function (injected for testing)
        """
        # Set up components with dependency injection support
        self.wikipedia_client = wikipedia_client or WikipediaClient()
        self.question_validator = QuestionValidator(question_validator)
        self.wikipedia_retriever = WikipediaRetriever(self.wikipedia_client)
        self.content_formatter = ContentFormatter(content_formatter)
        self.safety_disclaimer_adder = SafetyDisclaimer(safety_disclaimer_adder)
        
        # Build the processing pipeline using LangChain-style RunnableSequence
        self.pipeline = RunnableSequence([
            self.question_validator,
            self.wikipedia_retriever,
            self.content_formatter,
            self.safety_disclaimer_adder
        ])
    
    def research(self, question: str) -> Dict[str, Any]:
        """
        Research a medical question using the complete pipeline.
        
        Args:
            question: The health question to research
            
        Returns:
            Complete research results with safety information
        """
        try:
            # Execute the full pipeline
            result = self.pipeline.invoke(question)
            return result
            
        except Exception as e:
            # Handle any unexpected errors gracefully
            return {
                'status': 'error',
                'error': f'Research failed: {str(e)}',
                'query': question,
                'disclaimer': {
                    'title': '⚠️ Errore - Disclaimer Medico',
                    'content': 'Si è verificato un errore durante la ricerca. Si prega di consultare un medico qualificato per informazioni mediche accurate.',
                    'is_disclaimer': True
                }
            }
    
    def get_step_results(self, question: str) -> Dict[str, Any]:
        """
        Get intermediate results from each processing step for debugging.
        
        Args:
            question: The health question to research
            
        Returns:
            Dictionary containing results from each step
        """
        try:
            # Step 1: Validate question
            validation_result = self.question_validator.invoke(question)
            
            # Step 2: Retrieve from Wikipedia
            retrieval_result = self.wikipedia_retriever.invoke(validation_result)
            
            # Step 3: Format content
            formatting_result = self.content_formatter.invoke(retrieval_result)
            
            # Step 4: Add disclaimer
            final_result = self.safety_disclaimer_adder.invoke(formatting_result)
            
            return {
                'question': question,
                'validation': validation_result,
                'retrieval': retrieval_result,
                'formatting': formatting_result,
                'final': final_result
            }
            
        except Exception as e:
            return {
                'question': question,
                'error': f'Pipeline execution failed: {str(e)}'
            }


# Import the WikipediaClient for the agent
from .wikipedia_client import WikipediaClient