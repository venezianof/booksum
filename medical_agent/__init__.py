"""
Medical Agent Package

This package contains a medical research agent that uses Wikipedia
and LangChain-style processing to provide reliable medical information
with proper safety disclaimers.
"""

from .agent import WikipediaClient, MedicalResearchAgent

__all__ = ['WikipediaClient', 'MedicalResearchAgent']