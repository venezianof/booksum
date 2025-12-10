import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MedicalResearchAgent:
    """
    A Medical Research Agent that answers questions based on medical research.
    
    ⚠️ DISCLAIMER: This agent is for educational and research purposes only.
    It is NOT a substitute for professional medical advice, diagnosis, or treatment.
    Always consult with a qualified healthcare provider for medical decisions.
    """

    def __init__(self):
        logger.info("Initializing MedicalResearchAgent...")

    def ask(self, question: str) -> dict:
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

        Note:
            This is a simulated response. In a real implementation, this would
            query actual medical databases like PubMed or use an LLM with
            medical knowledge.
        """
        logger.info(f"Received question: {question}")

        response = {
            "answer_text": f"Processed answer for: {question}. This is a simulated response from the MedicalResearchAgent.",
            "bullets": [
                "Observation 1: The input was received successfully.",
                "Observation 2: This is a placeholder for actual medical insights.",
                "Observation 3: Always consult a qualified healthcare provider for medical advice.",
            ],
            "source_links": [
                "https://pubmed.ncbi.nlm.nih.gov/",
                "https://www.who.int/",
            ],
            "disclaimer": "⚠️ DISCLAIMER: This information is for educational purposes only and is NOT medical advice. Always consult with a qualified healthcare provider.",
        }
        logger.info("Generated response")
        return response
