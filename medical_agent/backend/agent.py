import logging

try:
    from config import Settings
except ImportError:  # pragma: no cover
    from .config import Settings


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MedicalResearchAgent:
    """A Medical Research Agent that answers questions based on medical research.

    ⚠️ DISCLAIMER: This agent is for educational and research purposes only.
    It is NOT a substitute for professional medical advice, diagnosis, or treatment.
    Always consult with a qualified healthcare provider for medical decisions.
    """

    def __init__(self, settings: Settings):
        self.settings = settings
        logger.info(
            "Initializing MedicalResearchAgent (llm_provider=%s, memory=%s)...",
            settings.llm.provider,
            settings.agent.enable_memory,
        )

    def ask(self, question: str) -> dict:
        logger.info("Received question: %s", question)

        response = {
            "answer_text": (
                f"Processed answer for: {question}. "
                "This is a simulated response from the MedicalResearchAgent."
            ),
            "bullets": [
                "Observation 1: The input was received successfully.",
                "Observation 2: This is a placeholder for actual medical insights.",
                "Observation 3: Always consult a qualified healthcare provider for medical advice.",
            ],
            "source_links": [
                "https://pubmed.ncbi.nlm.nih.gov/",
                "https://www.who.int/",
            ],
            "disclaimer": (
                "⚠️ DISCLAIMER: This information is for educational purposes only and is NOT medical advice. "
                "Always consult with a qualified healthcare provider."
            ),
        }

        logger.info("Generated response")
        return response
