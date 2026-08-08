"""
Wikipedia REST API client for medical research agent.

This module provides a wrapper around the Wikipedia REST API to fetch
medical information with proper normalization and error handling.
"""

import json
import urllib.request
import urllib.parse
import urllib.error
from typing import Dict, Optional, Any
import re


class WikipediaClient:
    """
    A client for interacting with the Wikipedia REST API.
    
    This class handles HTTP requests to Wikipedia's REST API endpoints,
    normalizes queries, and returns structured medical information.
    """
    
    def __init__(self, timeout: int = 10):
        """
        Initialize the Wikipedia client.
        
        Args:
            timeout: HTTP request timeout in seconds
        """
        self.timeout = timeout
        self.base_url = "https://en.wikipedia.org/api/rest_v1"
        
    def _make_request(self, endpoint: str) -> Dict[str, Any]:
        """
        Make a GET request to the specified Wikipedia API endpoint.
        
        Args:
            endpoint: API endpoint path (e.g., '/page/summary/diabetes')
            
        Returns:
            JSON response as dictionary
            
        Raises:
            ValueError: If the request fails or returns invalid data
        """
        url = f"{self.base_url}{endpoint}"
        
        try:
            # Create request with proper headers
            req = urllib.request.Request(url, headers={
                'User-Agent': 'MedicalResearchAgent/1.0 (Educational purposes)'
            })
            
            # Make the request with timeout
            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                if response.status == 200:
                    data = response.read().decode('utf-8')
                    return json.loads(data)
                else:
                    raise ValueError(f"HTTP {response.status}: {response.reason}")
                    
        except urllib.error.HTTPError as e:
            if e.code == 404:
                raise ValueError("Wikipedia page not found")
            else:
                raise ValueError(f"HTTP error {e.code}: {e.reason}")
                
        except urllib.error.URLError as e:
            raise ValueError(f"Network error: {e.reason}")
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON response: {e}")
            
        except Exception as e:
            raise ValueError(f"Unexpected error: {e}")
    
    def _normalize_query(self, query: str) -> str:
        """
        Normalize a medical query for Wikipedia search.
        
        This method:
        - Removes extra whitespace
        - Converts to lowercase
        - Removes special characters except spaces and hyphens
        - Handles common medical abbreviations
        
        Args:
            query: Raw medical query
            
        Returns:
            Normalized query string
        """
        if not query or not query.strip():
            raise ValueError("Query cannot be empty")
            
        # Basic cleaning
        normalized = query.strip().lower()
        
        # Remove extra whitespace
        normalized = re.sub(r'\s+', ' ', normalized)
        
        # Remove special characters but keep spaces and hyphens
        normalized = re.sub(r'[^\w\s\-]', '', normalized)
        
        # Handle common medical abbreviations
        replacements = {
            'dr ': 'doctor ',
            'md ': '',
            'symptom ': 'symptoms ',
            'condition ': '',
            'disease ': '',
            'syndrome ': '',
            'disorder ': ''
        }
        
        for abbrev, full in replacements.items():
            normalized = normalized.replace(abbrev, full)
            
        return normalized.strip()
    
    def search_pages(self, query: str, limit: int = 5) -> Dict[str, Any]:
        """
        Search for Wikipedia pages related to the query.
        
        Args:
            query: Medical query to search for
            limit: Maximum number of search results
            
        Returns:
            Dictionary containing search results
        """
        normalized_query = self._normalize_query(query)
        
        # URL encode the query
        encoded_query = urllib.parse.quote(normalized_query)
        
        # Search using Wikipedia's REST API
        endpoint = f"/page/search/{encoded_query}?limit={limit}"
        
        try:
            results = self._make_request(endpoint)
            return {
                'query': query,
                'normalized_query': normalized_query,
                'results': results.get('pages', []),
                'status': 'success'
            }
        except ValueError as e:
            return {
                'query': query,
                'normalized_query': normalized_query,
                'error': str(e),
                'status': 'error'
            }
    
    def get_page_summary(self, title: str) -> Dict[str, Any]:
        """
        Get a summary of a specific Wikipedia page.
        
        Args:
            title: Wikipedia page title
            
        Returns:
            Dictionary containing page summary information
        """
        if not title or not title.strip():
            raise ValueError("Page title cannot be empty")
            
        # URL encode the title
        encoded_title = urllib.parse.quote(title.strip())
        
        # Get page summary
        endpoint = f"/page/summary/{encoded_title}"
        
        try:
            summary_data = self._make_request(endpoint)
            
            # Extract and structure the relevant fields
            return {
                'title': summary_data.get('title', title),
                'description': summary_data.get('description', ''),
                'extract': summary_data.get('extract', ''),
                'url': summary_data.get('content_urls', {}).get('desktop', {}).get('page', ''),
                'thumbnail': summary_data.get('thumbnail', {}).get('source', ''),
                'original_image': summary_data.get('originalimage', {}).get('source', ''),
                'status': 'success'
            }
        except ValueError as e:
            return {
                'title': title,
                'error': str(e),
                'status': 'error'
            }
    
    def get_related_pages(self, title: str, limit: int = 5) -> Dict[str, Any]:
        """
        Get pages related to the specified Wikipedia page.
        
        Args:
            title: Wikipedia page title
            limit: Maximum number of related pages
            
        Returns:
            Dictionary containing related pages
        """
        if not title or not title.strip():
            raise ValueError("Page title cannot be empty")
            
        # URL encode the title
        encoded_title = urllib.parse.quote(title.strip())
        
        # Get related pages
        endpoint = f"/page/related/{encoded_title}?limit={limit}"
        
        try:
            related_data = self._make_request(endpoint)
            
            related_pages = []
            for item in related_data.get('pages', []):
                related_pages.append({
                    'title': item.get('title', ''),
                    'description': item.get('description', ''),
                    'extract': item.get('extract', ''),
                    'url': item.get('content_urls', {}).get('desktop', {}).get('page', '')
                })
            
            return {
                'title': title,
                'related_pages': related_pages,
                'status': 'success'
            }
        except ValueError as e:
            return {
                'title': title,
                'error': str(e),
                'status': 'error'
            }
    
    def get_medical_info(self, query: str) -> Dict[str, Any]:
        """
        Get comprehensive medical information for a query.
        
        This method combines search, summary, and related pages to provide
        a complete view of medical information.
        
        Args:
            query: Medical query to research
            
        Returns:
            Dictionary containing comprehensive medical information
        """
        search_results = self.search_pages(query)
        
        if search_results['status'] == 'error':
            return search_results
            
        # Get the first search result (most relevant)
        if not search_results['results']:
            return {
                'query': query,
                'error': 'No Wikipedia pages found for this query',
                'status': 'error'
            }
            
        first_result = search_results['results'][0]
        title = first_result.get('title', '')
        
        # Get detailed summary
        summary = self.get_page_summary(title)
        
        # Get related pages for additional context
        related = self.get_related_pages(title)
        
        return {
            'query': query,
            'primary_result': {
                'title': summary.get('title', title),
                'description': summary.get('description', ''),
                'extract': summary.get('extract', ''),
                'url': summary.get('url', ''),
                'thumbnail': summary.get('thumbnail', '')
            },
            'related_pages': related.get('related_pages', []),
            'status': 'success'
        }