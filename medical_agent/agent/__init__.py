"""
Medical Agent Package

This package contains the core components for a medical research agent
that uses LangChain primitives to provide reliable medical information
from Wikipedia and other sources.
"""

from .wikipedia_client import WikipediaClient
from .medical_agent import MedicalResearchAgent

__all__ = ['WikipediaClient', 'MedicalResearchAgent']