# Medical Agent

An AI-powered medical information assistant with a clean, mobile-friendly web interface.

## 📋 Overview

This is a complete medical agent application bundle consisting of:

1. **Frontend** (`frontend/`) - Minimal, mobile-friendly chat interface
   - Pure HTML, CSS, and vanilla JavaScript
   - No build tools or frameworks required
   - Responsive design with accessibility features
   - Italian language interface

2. **Backend** (`app.py`) - Flask API server
   - RESTful API endpoint for medical questions
   - CORS support for cross-origin requests
   - Mock responses for demonstration (ready for integration)
   - Error handling and validation

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Installation & Running

1. **Install dependencies:**
   ```bash
   cd medical_agent
   pip install -r requirements.txt
   ```

2. **Run the server:**
   ```bash
   python app.py
   ```

3. **Open in browser:**
   ```
   http://localhost:5000
   ```

That's it! The application should now be running with both the frontend and backend working together.

## 📁 Directory Structure

```
medical_agent/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── app.py                    # Flask backend server
└── frontend/                 # Frontend bundle
    ├── README.md             # Detailed frontend documentation
    ├── index.html            # Main HTML page
    ├── styles.css            # Styles with utility classes
    └── app.js                # JavaScript application logic
```

## 🎯 Features

### User Interface
- 🌍 Italian language interface
- 📱 Mobile-first responsive design
- 💬 Chat-style message bubbles (user & agent)
- ⚠️ Prominent medical disclaimer banner
- 📚 First-time user instructions
- 💡 Example questions for guidance
- 🎨 Clean, professional styling
- ♿ Accessibility features (ARIA labels, keyboard navigation)

### Functionality
- ✅ Real-time question submission
- 🔄 Loading spinner during processing
- ❌ User-friendly error handling
- 🔗 Source links with agent responses
- 📝 Input validation (length, content)
- 🔁 Automatic retry logic
- ⏱️ Request timeout handling (30s)
- 🛡️ XSS protection (input sanitization)

### API Features
- 🔌 RESTful `/api/ask` endpoint
- 📋 JSON request/response format
- 🔒 Input validation and sanitization
- 🏥 Health check endpoint (`/api/health`)
- 📊 Structured error responses
- 🔄 CORS support for development

## 🔧 Configuration

### API Endpoint

The default API endpoint is `/api/ask`. To change it, edit `frontend/app.js`:

```javascript
const API_CONFIG = {
    endpoint: '/api/ask',  // Change this
    timeout: 30000,
    retryAttempts: 2
};
```

### Port Configuration

To run on a different port, modify `app.py`:

```python
app.run(
    debug=True,
    host='0.0.0.0',
    port=5000,  # Change this
    threaded=True
)
```

### Styling Customization

All colors and spacing are CSS variables in `frontend/styles.css`:

```css
:root {
    --primary-color: #2563eb;
    --secondary-color: #10b981;
    /* ... modify as needed */
}
```

## 🔌 API Integration

### Integrating Your Medical Agent

Replace the mock responses in `app.py` with your actual agent:

```python
def generate_mock_response(question):
    # Replace with your agent integration
    # Example:
    # agent_response = your_medical_agent.ask(question)
    # return {
    #     'answer': agent_response.text,
    #     'sources': agent_response.sources
    # }
    pass
```

### API Request Format

```http
POST /api/ask
Content-Type: application/json

{
  "question": "Che cos'è l'ipertensione?"
}
```

### API Response Format

```json
{
  "answer": "L'ipertensione è una condizione...",
  "sources": [
    {
      "title": "WHO - Hypertension",
      "url": "https://www.who.int/..."
    }
  ]
}
```

### Error Response

```json
{
  "error": "Error message in Italian"
}
```

## 📝 Example Questions

The interface includes Italian example questions:

- **"Che cos'è l'ipertensione?"** - What is hypertension?
- **"Quali sono i sintomi del diabete?"** - What are diabetes symptoms?
- **"Come si previene l'influenza?"** - How to prevent flu?
- **"Cosa causa il mal di testa?"** - What causes headaches?

## 🧪 Testing

### Testing the Frontend Only

You can test the frontend without the backend using Python's HTTP server:

```bash
cd frontend
python3 -m http.server 8080
```

Then enable demo mode in `app.js` (uncomment the demo section at the bottom).

### Testing the API

Use curl to test the API endpoint:

```bash
curl -X POST http://localhost:5000/api/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Che cos'\''è l'\''ipertensione?"}'
```

### Health Check

```bash
curl http://localhost:5000/api/health
```

## 🔐 Production Considerations

Before deploying to production:

1. **Disable Debug Mode:**
   ```python
   app.run(debug=False, ...)
   ```

2. **Configure CORS Properly:**
   ```python
   CORS(app, origins=['https://yourdomain.com'])
   ```

3. **Use a Production Server:**
   - Use Gunicorn, uWSGI, or similar
   - Don't use Flask's built-in server

4. **Enable HTTPS:**
   - Use SSL certificates
   - Redirect HTTP to HTTPS

5. **Add Rate Limiting:**
   ```python
   from flask_limiter import Limiter
   limiter = Limiter(app, key_func=get_remote_address)
   ```

6. **Environment Variables:**
   - Don't hardcode sensitive values
   - Use environment variables for configuration

7. **Logging:**
   - Configure proper logging
   - Monitor errors and performance

8. **Security Headers:**
   - Add CSP, X-Frame-Options, etc.
   - Use Flask-Talisman or similar

## 📚 Further Reading

- Frontend documentation: `frontend/README.md`
- Flask documentation: https://flask.palletsprojects.com/
- CORS guide: https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS
- Accessibility: https://www.w3.org/WAI/WCAG21/quickref/

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

- Additional language support
- Enhanced medical agent integration
- More sophisticated UI components
- User authentication
- Chat history persistence
- Advanced search and filtering

## 📄 License

Include your license information here.

## ⚠️ Disclaimer

This application is for educational and informational purposes only. It is not intended to be a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.

## 📞 Support

For issues, questions, or suggestions, please open an issue in the repository.
