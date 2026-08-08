import logging
import os

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

try:
    from config import get_settings
except ImportError:  # pragma: no cover
    from .config import get_settings

try:
    from agent import MedicalResearchAgent
except ImportError:  # pragma: no cover
    from .agent import MedicalResearchAgent


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


try:
    settings = get_settings()
    logger.info(
        "Configuration loaded successfully (llm_provider=%s, web_search=%s).",
        settings.llm.provider,
        settings.features.enable_web_search,
    )
except Exception as e:
    logger.error(
        "Configuration error: %s\n\n"
        "Fix: run 'python medical_agent/scripts/bootstrap_agent.py' to create/update your .env.",
        e,
    )
    raise SystemExit(1)


app = Flask(__name__, static_folder="static")
app.secret_key = settings.server.secret_key

CORS(app, origins=settings.server.cors_origins)


try:
    agent = MedicalResearchAgent(settings)
    logger.info("MedicalResearchAgent instantiated successfully.")
except Exception as e:
    logger.error(
        "Failed to instantiate MedicalResearchAgent: %s\n\n"
        "This usually indicates missing configuration or a missing dependency.",
        e,
        exc_info=True,
    )
    raise SystemExit(1)


@app.route("/health", methods=["GET"])
def health_check():
    if agent:
        return jsonify({"status": "healthy", "agent": "ready"}), 200
    return jsonify({"status": "unhealthy", "agent": "not initialized"}), 503


@app.route("/api/ask", methods=["POST"])
def ask_agent():
    if not agent:
        return jsonify({"error": "Agent not initialized"}), 503

    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    question = data.get("question")
    if not question or not isinstance(question, str) or not question.strip():
        return jsonify({"error": "Missing or empty 'question' field"}), 400

    try:
        logger.info("Processing question: %s", question)
        result = agent.ask(question)
        return jsonify(result), 200
    except Exception as e:
        logger.error("Error processing request: %s", e, exc_info=True)
        return jsonify({"error": "Agent processing error"}), 500


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_static(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, "index.html")


if __name__ == "__main__":
    logger.info("Starting app on port %s", settings.server.port)
    app.run(host="0.0.0.0", port=settings.server.port, debug=settings.server.flask_debug)
