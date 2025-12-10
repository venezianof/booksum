import os
import logging
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from agent import MedicalResearchAgent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__, static_folder='static')
CORS(app)

# Instantiate the agent
try:
    agent = MedicalResearchAgent()
    logger.info("MedicalResearchAgent instantiated successfully.")
except Exception as e:
    logger.error(f"Failed to instantiate MedicalResearchAgent: {e}")
    agent = None


@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint.
    Returns 200 OK if the app is running and agent is initialized.
    """
    if agent:
        return jsonify({"status": "healthy", "agent": "ready"}), 200
    else:
        return jsonify({"status": "unhealthy", "agent": "not initialized"}), 503


@app.route('/api/ask', methods=['POST'])
def ask_agent():
    """
    Endpoint to ask a question to the MedicalResearchAgent.

    Expected JSON payload:
    {
        "question": "Your medical research question here"
    }

    Returns JSON with:
    {
        "answer_text": "...",
        "bullets": [...],
        "source_links": [...],
        "disclaimer": "..."
    }

    ⚠️ DISCLAIMER: This tool is for educational and research purposes only.
    It is NOT a substitute for professional medical advice.
    """
    if not agent:
        return jsonify({"error": "Agent not initialized"}), 503

    try:
        data = request.get_json(force=True, silent=True)
        if not data:
            return jsonify({"error": "Invalid JSON"}), 400

        question = data.get('question')
        if not question or not isinstance(question, str) or not question.strip():
            return jsonify({"error": "Missing or empty 'question' field"}), 400

        logger.info(f"Processing question: {question}")

        result = agent.ask(question)
        return jsonify(result), 200

    except Exception as e:
        logger.error(f"Error processing request: {e}", exc_info=True)
        return jsonify({"error": "Invalid JSON"}), 400


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_static(path):
    """
    Serve static frontend assets.
    """
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"Starting app on port {port}")
    app.run(host='0.0.0.0', port=port, debug=True)
