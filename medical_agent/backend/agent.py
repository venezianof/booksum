import logging
import os
from typing import Dict, List
from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import Tool
from langchain_core.prompts import PromptTemplate
from langchain_community.utilities import WikipediaAPIWrapper
import requests
from xml.etree import ElementTree as ET

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MockLLM:
    """
    A mock LLM that simulates agent reasoning without requiring API keys.
    In production, replace this with OpenAI, Anthropic, or another LLM.
    """
    
    def __init__(self):
        self.temperature = 0.7
        
    def __call__(self, prompt: str) -> str:
        """Simple rule-based response for medical queries."""
        prompt_lower = prompt.lower()
        
        # Extract the question from the prompt
        if "input:" in prompt_lower:
            parts = prompt.split("Input:")
            if len(parts) > 1:
                question = parts[-1].strip()
                return self._generate_medical_response(question)
        
        # Default response structure
        return """Thought: I need to search for information about this medical topic.
Action: search_pubmed
Action Input: diabetes symptoms treatment
Observation: """

    def _generate_medical_response(self, question: str) -> str:
        """Generate a structured response based on the question."""
        question_lower = question.lower()
        
        # Simple pattern matching for common medical questions
        if any(word in question_lower for word in ['diabetes', 'diabetic']):
            return """Thought: I have information about diabetes from my search.
Final Answer: Diabetes is a chronic metabolic disorder characterized by high blood sugar levels. There are two main types:

• Type 1 diabetes: An autoimmune condition where the pancreas produces little or no insulin
• Type 2 diabetes: A condition where the body becomes resistant to insulin or doesn't produce enough insulin

Common symptoms include increased thirst, frequent urination, extreme fatigue, blurred vision, and slow wound healing. Treatment typically involves lifestyle modifications, blood glucose monitoring, and medication (insulin or oral medications).

For accurate diagnosis and treatment, please consult a healthcare provider."""

        elif any(word in question_lower for word in ['hypertension', 'blood pressure', 'high pressure']):
            return """Thought: I have information about hypertension.
Final Answer: Hypertension (high blood pressure) is a condition where the force of blood against artery walls is consistently too high.

• Normal blood pressure: Less than 120/80 mm Hg
• Elevated: 120-129/<80 mm Hg
• Stage 1 hypertension: 130-139/80-89 mm Hg
• Stage 2 hypertension: 140/90 mm Hg or higher

Risk factors include obesity, high salt intake, lack of physical activity, stress, and genetics. Treatment includes lifestyle changes (diet, exercise, stress management) and medications like ACE inhibitors, diuretics, or beta-blockers.

Always consult a healthcare provider for proper diagnosis and treatment."""

        elif 'aspirin' in question_lower:
            return """Thought: I can explain how aspirin works.
Final Answer: Aspirin (acetylsalicylic acid) is a common medication with several mechanisms of action:

• Pain relief (analgesic): Reduces pain signaling in the nervous system
• Anti-inflammatory: Inhibits prostaglandin synthesis, reducing inflammation
• Antiplatelet: Prevents blood clot formation by inhibiting platelet aggregation
• Fever reduction (antipyretic): Lowers fever by affecting the hypothalamus

Common uses include headache relief, reducing heart attack and stroke risk, and managing inflammatory conditions. However, it can cause side effects like stomach irritation and increased bleeding risk.

Consult a healthcare provider before starting aspirin therapy."""

        else:
            # Generic medical response
            return f"""Thought: I should provide general medical information about this topic.
Final Answer: Regarding your question about "{question}", I recommend consulting with a qualified healthcare provider for accurate medical information.

General health advice includes:
• Regular check-ups with your doctor
• Maintaining a balanced diet and regular exercise
• Getting adequate sleep and managing stress
• Following prescribed treatments and medications
• Staying informed through reputable medical sources

For specific medical concerns, please seek professional medical advice."""

    def bind(self, **kwargs):
        """Compatibility method for LangChain."""
        return self
    
    def invoke(self, prompt: str, **kwargs) -> str:
        """LangChain-style invoke method."""
        return self(prompt)


def search_pubmed(query: str) -> str:
    """
    Search PubMed for medical research articles.
    Uses the NCBI E-utilities API (no API key required for basic usage).
    """
    try:
        base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
        params = {
            "db": "pubmed",
            "term": query,
            "retmax": 3,
            "retmode": "xml"
        }
        
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        
        root = ET.fromstring(response.content)
        id_list = root.find(".//IdList")
        
        if id_list is None or len(id_list) == 0:
            return f"No PubMed articles found for: {query}"
        
        pmids = [id_elem.text for id_elem in id_list.findall("Id")]
        links = [f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/" for pmid in pmids]
        
        result = f"Found {len(pmids)} PubMed articles related to '{query}':\n"
        result += "\n".join(links)
        
        return result
        
    except Exception as e:
        logger.error(f"Error searching PubMed: {e}")
        return f"Error searching PubMed: {str(e)}"


def search_medical_info(query: str) -> str:
    """
    Search for general medical information using Wikipedia.
    """
    try:
        wikipedia = WikipediaAPIWrapper()
        result = wikipedia.run(query)
        
        # Truncate if too long
        if len(result) > 500:
            result = result[:500] + "..."
        
        return result
    except Exception as e:
        logger.error(f"Error searching Wikipedia: {e}")
        return f"Could not find information for: {query}"


class MedicalResearchAgent:
    """
    A Medical Research Agent that answers questions based on medical research.
    
    ⚠️ DISCLAIMER: This agent is for educational and research purposes only.
    It is NOT a substitute for professional medical advice, diagnosis, or treatment.
    Always consult with a qualified healthcare provider for medical decisions.
    """

    def __init__(self):
        logger.info("Initializing MedicalResearchAgent...")
        
        # Create tools
        self.tools = [
            Tool(
                name="search_pubmed",
                func=search_pubmed,
                description="Search PubMed for medical research articles. Input should be medical keywords or terms."
            ),
            Tool(
                name="search_medical_info",
                func=search_medical_info,
                description="Search for general medical information and definitions. Input should be a medical condition or term."
            ),
        ]
        
        # Initialize LLM (mock for now - replace with real LLM if API key available)
        self.llm = self._initialize_llm()
        
        # Create agent
        self.agent_executor = self._create_agent()
        
        logger.info("MedicalResearchAgent initialized successfully")

    def _initialize_llm(self):
        """
        Initialize the LLM based on environment variables.
        Falls back to mock LLM if no API keys are available.
        """
        openai_key = os.getenv("OPENAI_API_KEY")
        
        if openai_key and openai_key != "your-openai-api-key-here":
            try:
                from langchain_openai import ChatOpenAI
                logger.info("Using OpenAI LLM")
                return ChatOpenAI(
                    model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
                    temperature=float(os.getenv("TEMPERATURE", "0.7"))
                )
            except Exception as e:
                logger.warning(f"Failed to initialize OpenAI: {e}")
        
        logger.info("Using mock LLM (no API key found)")
        return MockLLM()

    def _create_agent(self):
        """Create the ReAct agent with tools."""
        # Simple prompt template for the agent
        template = """You are a medical research assistant. Answer questions about medical topics using available tools.

Available tools:
{tools}

Tool Names: {tool_names}

Question: {input}

{agent_scratchpad}

Remember: Always provide accurate medical information and remind users to consult healthcare providers.
"""
        
        prompt = PromptTemplate.from_template(template)
        
        try:
            agent = create_react_agent(
                llm=self.llm,
                tools=self.tools,
                prompt=prompt
            )
            
            return AgentExecutor(
                agent=agent,
                tools=self.tools,
                verbose=True,
                max_iterations=5,
                handle_parsing_errors=True
            )
        except Exception as e:
            logger.error(f"Error creating agent: {e}")
            return None

    def ask(self, question: str) -> Dict:
        """
        Process a medical research question and return an answer with sources.

        Args:
            question (str): The medical research question to ask the agent.

        Returns:
            dict: A dictionary containing:
                - 'answer_text': The main answer
                - 'bullets': List of key points
                - 'source_links': List of reference URLs
                - 'disclaimer': Medical disclaimer
        """
        logger.info(f"Received question: {question}")

        try:
            # If agent is not initialized, use fallback
            if not self.agent_executor:
                return self._fallback_response(question)
            
            # Use the LLM's generate_medical_response directly for mock LLM
            if isinstance(self.llm, MockLLM):
                result = self.llm._generate_medical_response(question)
            else:
                # For real LLMs, invoke the agent executor
                result = self.agent_executor.invoke({"input": question})
                result = result.get("output", str(result))
            
            # Parse the response
            answer_text = self._extract_answer(result, question)
            bullets = self._extract_bullets(result)
            source_links = self._generate_sources(question)
            
            response = {
                "answer_text": answer_text,
                "bullets": bullets,
                "source_links": source_links,
                "disclaimer": "⚠️ DISCLAIMER: This information is for educational purposes only and is NOT medical advice. Always consult with a qualified healthcare provider.",
            }
            
            logger.info("Generated response")
            return response
            
        except Exception as e:
            logger.error(f"Error processing question: {e}", exc_info=True)
            return self._fallback_response(question)

    def _extract_answer(self, result: str, question: str) -> str:
        """Extract the main answer from the agent result."""
        if "Final Answer:" in result:
            answer = result.split("Final Answer:")[-1].strip()
            # Remove bullet points for the main text
            lines = answer.split("\n")
            main_text = []
            for line in lines:
                if not line.strip().startswith("•"):
                    main_text.append(line)
            return "\n".join(main_text).strip()
        return result

    def _extract_bullets(self, answer_text: str) -> List[str]:
        """Extract bullet points from the answer."""
        bullets = []
        for line in answer_text.split("\n"):
            line = line.strip()
            if line.startswith("•"):
                bullets.append(line[1:].strip())
        
        if not bullets:
            # Generate generic bullets
            bullets = [
                "This information is for educational purposes only",
                "Consult with a healthcare provider for medical advice",
                "Individual medical conditions may vary"
            ]
        
        return bullets

    def _generate_sources(self, question: str) -> List[str]:
        """Generate relevant source links."""
        sources = [
            "https://pubmed.ncbi.nlm.nih.gov/",
            "https://www.who.int/",
            "https://www.cdc.gov/"
        ]
        
        # Try to get actual PubMed results
        try:
            pubmed_result = search_pubmed(question)
            if "pubmed.ncbi.nlm.nih.gov" in pubmed_result:
                lines = pubmed_result.split("\n")
                pubmed_links = [line.strip() for line in lines if line.strip().startswith("http")]
                if pubmed_links:
                    return pubmed_links[:3] + sources[1:]
        except Exception as e:
            logger.error(f"Error getting PubMed sources: {e}")
        
        return sources

    def _fallback_response(self, question: str) -> Dict:
        """Fallback response when agent fails."""
        return {
            "answer_text": f"I received your question about: {question}. For accurate medical information, please consult healthcare databases and medical professionals.",
            "bullets": [
                "This is an educational tool, not a medical diagnostic system",
                "Always verify medical information with qualified healthcare providers",
                "PubMed and WHO are recommended sources for medical research"
            ],
            "source_links": [
                "https://pubmed.ncbi.nlm.nih.gov/",
                "https://www.who.int/",
                "https://www.cdc.gov/"
            ],
            "disclaimer": "⚠️ DISCLAIMER: This information is for educational purposes only and is NOT medical advice.",
        }
