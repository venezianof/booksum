# Medical Research Assistant Agent

A beginner-friendly AI agent that helps users research medical topics using natural language queries. This project demonstrates how to build a practical AI assistant using LangChain and Flask.

## 📋 Table of Contents

- [Project Goals](#project-goals)
- [Architecture](#architecture)
- [Medical Disclaimer](#medical-disclaimer)
- [Prerequisites](#prerequisites)
- [Step-by-Step Setup Instructions](#step-by-step-setup-instructions)
- [Running the Application](#running-the-application)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Development](#development)
  - [Running Automated Tests](#running-automated-tests)
  - [Manual Testing](#manual-testing)
- [Troubleshooting](#troubleshooting)

## 🎯 Project Goals

This project aims to:

1. **Demonstrate AI Agent Capabilities**: Show how LangChain agents can interact with external APIs and tools to gather medical research information
2. **Provide Educational Value**: Serve as a learning resource for developers new to AI agents and LangChain
3. **Enable Medical Research Exploration**: Help users discover and understand medical literature and health information from trusted sources
4. **Showcase Best Practices**: Implement proper error handling, API rate limiting, and user-friendly interfaces
5. **Maintain Isolation**: Keep the medical agent dependencies separate from the BookSum dataset tooling

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      User Interface                         │
│                    (Web Browser / CLI)                      │
└────────────────────────────┬────────────────────────────────┘
                             │
                             │ HTTP/REST
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                    Flask Backend Server                     │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              API Endpoints Layer                     │  │
│  │  • /api/query    • /api/status    • /api/health     │  │
│  └──────────────────────┬───────────────────────────────┘  │
│                         │                                   │
│  ┌──────────────────────▼───────────────────────────────┐  │
│  │            LangChain Agent Core                      │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌───────────┐ │  │
│  │  │ Conversation │  │    Memory    │  │  Prompts  │ │  │
│  │  │    Chain     │  │   Manager    │  │ Templates │ │  │
│  │  └──────────────┘  └──────────────┘  └───────────┘ │  │
│  └──────────────────────┬───────────────────────────────┘  │
│                         │                                   │
│  ┌──────────────────────▼───────────────────────────────┐  │
│  │              Tools & Integrations                    │  │
│  │  • PubMed API     • Web Search     • PDF Parser     │  │
│  │  • Citation Tool  • Summary Tool   • Validator      │  │
│  └──────────────────────┬───────────────────────────────┘  │
└─────────────────────────┼───────────────────────────────────┘
                          │
                          │ External API Calls
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                   External Data Sources                     │
│  • PubMed/NCBI    • Medical Databases    • Research APIs   │
└─────────────────────────────────────────────────────────────┘
```

### Component Details

- **Flask Backend**: Lightweight web server handling HTTP requests and serving the API
- **LangChain Agent**: Orchestrates tool usage, maintains conversation context, and generates responses
- **Tools Layer**: Modular tools for accessing medical databases, parsing documents, and validating information
- **External APIs**: PubMed, medical databases, and other trusted health information sources

## ⚠️ Medical Disclaimer

**IMPORTANT: This tool is for educational and research purposes only.**

- This AI assistant is **NOT** a substitute for professional medical advice, diagnosis, or treatment
- Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition
- Never disregard professional medical advice or delay in seeking it because of information provided by this tool
- The information provided by this agent may contain errors, be incomplete, or become outdated
- This tool should be used only for learning about medical research and literature, not for making health decisions
- In case of a medical emergency, call your local emergency services immediately

## 📦 Prerequisites

Before you begin, ensure you have the following installed on your system:

- **Python 3.8 or higher** (Python 3.9+ recommended)
- **pip** (Python package installer, usually comes with Python)
- **virtualenv** or **venv** (for creating isolated Python environments)
- **Git** (for cloning the repository)
- A modern web browser (Chrome, Firefox, Safari, or Edge)

### Optional but Recommended

- **API Keys**: Some features may require API keys (e.g., OpenAI, Anthropic, or other LLM providers)
- **curl** or **Postman**: For testing API endpoints

## 🚀 Step-by-Step Setup Instructions

### Step 1: Install Python

If you don't have Python installed:

**On macOS:**
```bash
# Using Homebrew
brew install python3
```

**On Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

**On Windows:**
1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run the installer and check "Add Python to PATH"
3. Verify installation: `python --version`

### Step 2: Navigate to the Medical Agent Directory

```bash
cd /path/to/booksum/medical_agent
```

### Step 3: Create a Virtual Environment

Creating a virtual environment keeps dependencies isolated:

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

You should see `(venv)` prefix in your terminal prompt.

### Step 4: Upgrade pip (Recommended)

```bash
pip install --upgrade pip
```

### Step 5: Install Required Packages

```bash
pip install -r requirements.txt
```

This will install all the necessary dependencies including:
- Flask and Flask-CORS for the web server
- LangChain for the AI agent framework
- Additional utilities for API interaction

### Step 6: Configure Environment Variables

Copy the example environment file and customize it:

```bash
cp .env.example .env
```

Edit `.env` with your preferred text editor:

```bash
# On macOS/Linux:
nano .env
# or
vim .env

# On Windows:
notepad .env
```

Add your API keys and configuration (see [Configuration](#configuration) section).

### Step 7: Verify Installation

Test that all dependencies are installed correctly:

```bash
python -c "import flask; import langchain; print('All dependencies installed successfully!')"
```

## 🏃 Running the Application

### Start the Backend Server

```bash
# Make sure your virtual environment is activated
# (you should see (venv) in your prompt)

python backend/app.py
```

You should see output similar to:
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

### Access the Application

1. **Health Check**: Verify server is running: `curl http://localhost:5000/health`
2. **Web UI**: Open your browser and navigate to `http://localhost:5000`
3. **API Endpoint**: Use curl or Postman to interact with the API

Example API call:
```bash
curl -X POST http://localhost:5000/api/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What are the latest treatments for diabetes?"}'
```

Expected response:
```json
{
  "answer_text": "...",
  "bullets": ["...", "..."],
  "source_links": ["https://...", "https://..."],
  "disclaimer": "⚠️ DISCLAIMER: This tool is for educational purposes only..."
}
```

### Stop the Server

Press `Ctrl+C` in the terminal where the server is running.

### Deactivate Virtual Environment

When you're done working:

```bash
deactivate
```

## 📁 Project Structure

```
medical_agent/
├── README.md                 # This file - setup, usage, and troubleshooting guide
├── requirements.txt          # Python dependencies
├── .env.example             # Example environment configuration
├── .env                     # Your local configuration (not in git)
│
├── backend/                 # Flask backend application
│   ├── __init__.py
│   ├── app.py              # Main Flask application and API endpoints
│   ├── agent.py            # Medical Research Agent implementation
│   ├── static/             # Frontend assets (CSS, JS)
│   │   └── index.html
│   └── templates/          # HTML templates (if applicable)
│
├── tests/                   # Automated test suite
│   ├── __init__.py
│   └── test_api.py         # Flask API endpoint tests (pytest)
│
└── docs/                    # Documentation and guides
    └── manual_test_plan.md  # Step-by-step manual testing guide for end-users
```

## ⚙️ Configuration

The application uses environment variables for configuration. Create a `.env` file based on `.env.example`:

### Required Configuration

```bash
# Flask Configuration
FLASK_ENV=development          # development or production
FLASK_DEBUG=1                  # 0 for production, 1 for development
PORT=5000                      # Port number for the server

# LangChain/LLM Configuration
LLM_PROVIDER=openai           # openai, anthropic, huggingface, etc.
OPENAI_API_KEY=your_key_here  # If using OpenAI
# ANTHROPIC_API_KEY=your_key  # If using Anthropic
# HUGGINGFACE_API_KEY=your_key # If using HuggingFace

# Agent Configuration
MAX_ITERATIONS=10              # Maximum agent reasoning steps
TEMPERATURE=0.7                # LLM temperature (0.0-1.0)
```

### Optional Configuration

```bash
# External API Keys (for enhanced functionality)
PUBMED_API_KEY=optional_key    # For PubMed E-utilities
SERPER_API_KEY=optional_key    # For web search capabilities

# Rate Limiting
RATE_LIMIT=100                 # Requests per hour
REQUEST_TIMEOUT=30             # Timeout in seconds

# Logging
LOG_LEVEL=INFO                 # DEBUG, INFO, WARNING, ERROR
LOG_FILE=logs/app.log          # Log file path
```

## 🛠️ Development

### Running Automated Tests

Before running tests, ensure you're in the virtual environment with all dependencies installed.

```bash
# Make sure your virtual environment is activated
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate     # On Windows

# Run all tests
pytest

# Run all tests with verbose output
pytest -v

# Run with coverage report
pytest --cov=medical_agent

# Run specific test file
pytest tests/test_api.py

# Run tests matching a pattern
pytest tests/test_api.py::TestAskEndpoint::test_ask_valid_question

# Run with detailed output and stop on first failure
pytest -vx
```

### Manual Testing

For manual testing without running automated tests, we provide a comprehensive manual test plan:

1. **Read the manual test plan**: See `docs/manual_test_plan.md` for step-by-step instructions
2. **Start the server**: `python backend/app.py`
3. **Test endpoints in browser or with curl**: Follow the test plan to verify all functionality
4. **Check the logs**: Monitor the terminal for any errors

**Quick manual test example**:
```bash
# In one terminal, start the server
python backend/app.py

# In another terminal, test the API
curl -X POST http://localhost:5000/api/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is diabetes?"}'
```

### Adding New Tools

To add a new tool to the agent:

1. Create a new tool function in `agent/tools.py`
2. Register it with the agent in `agent/medical_agent.py`
3. Add tests in `tests/test_agent.py` or `tests/test_api.py`

Example:
```python
from langchain.tools import tool

@tool
def search_clinical_trials(condition: str) -> str:
    """Search for clinical trials related to a medical condition."""
    # Implementation here
    pass
```

### Code Style

This project follows PEP 8 style guidelines. Format your code with:

```bash
# Install formatters (if not already installed)
pip install black flake8

# Format code
black .

# Check style
flake8 .
```

## 🔧 Troubleshooting

### Installation Issues

**Issue: `ModuleNotFoundError: No module named 'flask'` or similar**

- **Solution 1**: Ensure virtual environment is activated (look for `(venv)` prefix in prompt)
- **Solution 2**: Run `pip install -r requirements.txt` again
- **Solution 3**: Verify you're in the `medical_agent/` directory

```bash
# Verify installation
python -c "import flask; import langchain; print('OK')"
```

**Issue: `pip install -r requirements.txt` fails with permission errors**

- **Solution**: Use a virtual environment (recommended):
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  pip install --upgrade pip
  pip install -r requirements.txt
  ```

### Server Startup Issues

**Issue: Server won't start or crashes immediately**

- **Check dependencies**: `python -c "from flask import Flask; print('Flask OK')"`
- **Check Python version**: `python --version` (should be 3.8+)
- **Check for syntax errors**: `python -m py_compile backend/app.py`

**Issue: "Address already in use" (port 5000 is taken)**

- **Solution**: Kill the process using the port:
  ```bash
  # On macOS/Linux:
  lsof -ti:5000 | xargs kill -9
  
  # On Windows (PowerShell):
  Get-Process -Id (Get-NetTCPConnection -LocalPort 5000).OwningProcess | Stop-Process -Force
  ```

- **Alternative**: Use a different port:
  ```bash
  PORT=5001 python backend/app.py
  ```

### Runtime Issues

**Issue: API returns "Agent not initialized" (503 error)**

- **Cause**: Agent failed to initialize at startup
- **Solution**: Check terminal for error messages during startup
- **Debug**: Ensure all environment variables in `.env` are set correctly:
  ```bash
  cp .env.example .env
  # Edit .env with required values
  ```

**Issue: CORS errors when accessing from browser**

- **Cause**: Flask-CORS not installed or not configured
- **Solution**: 
  ```bash
  pip install Flask-CORS
  # Verify it's in app.py: from flask_cors import CORS; CORS(app)
  ```

**Issue: Import errors with LangChain modules**

- **Solution**: Install both langchain packages:
  ```bash
  pip install langchain langchain-community
  ```

**Issue: API key errors or authentication failures**

- **Cause**: Missing or invalid API keys in `.env`
- **Solution**: 
  ```bash
  cp .env.example .env
  # Edit .env and add your actual API keys
  ```

### Restarting the Server

If you need to restart the server after making code changes:

1. **Stop the server**: Press `Ctrl+C` in the terminal running the server
2. **Verify it stopped**: Run `curl http://localhost:5000/health` (should fail)
3. **Restart**: Run `python backend/app.py` again

**For development with auto-reload**:
```bash
# Flask automatically reloads on code changes in debug mode
# If it doesn't, restart manually as shown above
python backend/app.py
```

### Testing Issues

**Issue: Tests fail with import errors**

- **Solution**: Ensure you're running pytest from the `medical_agent/` directory:
  ```bash
  cd medical_agent
  pytest tests/test_api.py
  ```

**Issue: Tests hang or timeout**

- **Solution**: 
  ```bash
  # Run with timeout
  pytest --timeout=30 tests/test_api.py
  
  # Or increase the timeout
  pytest --timeout=60 tests/test_api.py
  ```

**Issue: "Connection refused" when running tests**

- **Cause**: Flask test client is used but app isn't properly initialized
- **Solution**: Verify app initialization in test file (it should use test client automatically)

### Getting Help

If you encounter issues not covered here:

1. **Check the manual test plan**: `docs/manual_test_plan.md` has common issues and solutions
2. **Review the main BookSum README**: `../README.md` for general guidelines
3. **Check logs**: 
   - Terminal output where server is running
   - Browser console (F12 → Console tab)
4. **Open an issue on GitHub** with:
   - Your Python version: `python --version`
   - Your OS (Windows/macOS/Linux)
   - Full error message or stack trace
   - Steps to reproduce the issue

### Health Check Endpoint

To verify the server is running correctly:

```bash
curl http://localhost:5000/health
# Should return: {"status": "healthy", "agent": "ready"}
```

If this returns an error, the server is not running or failed to start.

## 📚 Additional Resources

- [LangChain Documentation](https://python.langchain.com/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [PubMed E-utilities API](https://www.ncbi.nlm.nih.gov/books/NBK25501/)
- [OpenAI API Documentation](https://platform.openai.com/docs/)

## 📄 License

This project is part of the BookSum repository and is released under the BSD-3 License. See the [main LICENSE](../LICENSE.txt) for details.

## 🤝 Contributing

Contributions are welcome! Please ensure:

- Code follows PEP 8 style guidelines
- All tests pass (`pytest`)
- New features include tests
- Documentation is updated

See the main [BookSum README](../README.md) for contribution guidelines.
