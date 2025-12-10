# Medical Agent Frontend

A minimal, mobile-friendly chat-style interface for the Medical Agent API.

## 📁 Files

- **index.html** - Main HTML structure with chat interface, disclaimer, and instructions
- **styles.css** - Mobile-first CSS with utility classes and comprehensive comments
- **app.js** - Vanilla JavaScript for form handling, API calls, and response rendering

## 🚀 Quick Start

### Option 1: Standalone (Static File Server)

The simplest way to run the frontend is to open it directly in a browser or serve it with any static file server:

```bash
# Using Python's built-in HTTP server
cd medical_agent/frontend
python3 -m http.server 8080

# Or using Node.js http-server (npm install -g http-server)
http-server -p 8080

# Then open http://localhost:8080 in your browser
```

**Note:** For API calls to work, you'll need CORS enabled on your backend or run the frontend on the same domain as the API.

### Option 2: Flask Integration

To serve the frontend as part of a Flask application:

#### Step 1: Create Flask App Structure

```
medical_agent/
├── frontend/           # This directory
│   ├── index.html
│   ├── styles.css
│   └── app.js
└── app.py             # Your Flask application
```

#### Step 2: Flask Application Code

Create `medical_agent/app.py`:

```python
from flask import Flask, send_from_directory, jsonify, request
from flask_cors import CORS  # pip install flask-cors

app = Flask(__name__, static_folder='frontend', static_url_path='')
CORS(app)  # Enable CORS for development

@app.route('/')
def index():
    """Serve the main frontend page"""
    return send_from_directory('frontend', 'index.html')

@app.route('/api/ask', methods=['POST'])
def ask():
    """Handle medical agent questions"""
    data = request.get_json()
    
    if not data or 'question' not in data:
        return jsonify({'error': 'Question is required'}), 400
    
    question = data['question'].strip()
    
    if len(question) < 3:
        return jsonify({'error': 'Question too short'}), 400
    
    # TODO: Integrate with your medical agent logic here
    # For now, return a mock response
    
    return jsonify({
        'answer': f"Received your question: {question}. Please implement the medical agent backend.",
        'sources': [
            {'title': 'Example Source', 'url': 'https://example.com'}
        ]
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

#### Step 3: Run Flask App

```bash
cd medical_agent
pip install flask flask-cors
python app.py

# Open http://localhost:5000 in your browser
```

### Option 3: Flask Blueprint (Advanced)

For larger applications, register the frontend as a blueprint:

```python
from flask import Blueprint, send_from_directory

frontend_bp = Blueprint('frontend', __name__, 
                       static_folder='frontend',
                       static_url_path='/static')

@frontend_bp.route('/')
def index():
    return send_from_directory('frontend', 'index.html')

# In your main app.py:
# app.register_blueprint(frontend_bp)
```

## 🔧 Configuration

### API Endpoint

The frontend expects the API at `/api/ask` by default. To change this, edit `app.js`:

```javascript
const API_CONFIG = {
    endpoint: '/api/ask',  // Change this to your API endpoint
    timeout: 30000,
    retryAttempts: 2
};
```

### API Request Format

The frontend sends POST requests with this structure:

```json
{
  "question": "Che cos'è l'ipertensione?"
}
```

### Expected API Response Format

The API should return JSON in this format:

```json
{
  "answer": "L'ipertensione è...",
  "sources": [
    {
      "title": "WHO - Hypertension",
      "url": "https://www.who.int/..."
    }
  ]
}
```

#### Alternative Response Fields

The frontend also accepts these alternative field names:
- `response` or `text` instead of `answer`
- `references` instead of `sources`

### Error Response Format

For errors, return:

```json
{
  "error": "Error message here"
}
```

Or:

```json
{
  "message": "Error message here"
}
```

## 🎨 Features

### User Interface
- ✅ Mobile-first responsive design
- ✅ Clean chat-style message bubbles
- ✅ Prominent disclaimer banner
- ✅ First-time user instructions
- ✅ Example questions in Italian
- ✅ Smooth animations and transitions

### Functionality
- ✅ Form validation (min/max length)
- ✅ Loading spinner during API calls
- ✅ Error handling with user-friendly messages
- ✅ Automatic retry logic (2 attempts)
- ✅ Timeout handling (30 seconds)
- ✅ Source links rendered below responses
- ✅ Auto-scroll to latest message
- ✅ Textarea auto-resize
- ✅ Submit on Enter, newline on Shift+Enter
- ✅ XSS protection (input sanitization)

### Accessibility
- ✅ ARIA labels for form inputs
- ✅ Keyboard navigation support
- ✅ Focus indicators
- ✅ Reduced motion support
- ✅ High contrast mode support

## 🧪 Demo Mode (Testing Without Backend)

For standalone testing, you can enable demo mode in `app.js`. Uncomment the demo mode section at the bottom:

```javascript
const DEMO_MODE = true;
```

This will simulate API responses for common questions without needing a backend.

## 🎯 Example Questions

The interface includes Italian example questions:
- "Che cos'è l'ipertensione?" (What is hypertension?)
- "Quali sono i sintomi del diabete?" (What are the symptoms of diabetes?)
- "Come si previene l'influenza?" (How do you prevent the flu?)
- "Cosa causa il mal di testa?" (What causes headaches?)

## 🔐 Security Considerations

1. **Input Sanitization**: All user input is sanitized to prevent XSS attacks
2. **CORS**: Configure CORS properly in production (don't use `*`)
3. **Rate Limiting**: Implement rate limiting on the backend API
4. **HTTPS**: Always use HTTPS in production
5. **Content Security Policy**: Consider adding CSP headers

## 📱 Browser Support

- Chrome/Edge (latest 2 versions)
- Firefox (latest 2 versions)
- Safari (latest 2 versions)
- Mobile browsers (iOS Safari, Chrome Mobile)

## 🛠️ Customization

### Styling

All colors and spacing are defined as CSS variables in `styles.css`:

```css
:root {
    --primary-color: #2563eb;
    --secondary-color: #10b981;
    --space-md: 1rem;
    /* ... more variables */
}
```

Simply modify these variables to match your brand.

### Utility Classes

The CSS includes utility classes for common tasks:

```html
<div class="u-text-center u-mt-lg">Centered with top margin</div>
```

Available utilities:
- `u-text-center`, `u-text-left`, `u-text-right`
- `u-mt-sm`, `u-mt-md`, `u-mt-lg` (margin-top)
- `u-mb-sm`, `u-mb-md`, `u-mb-lg` (margin-bottom)
- `u-hidden`, `u-visible`

## 📄 License

Include your license information here.

## 🤝 Contributing

Contributions welcome! Please follow the existing code style and include comments for complex logic.

## 📞 Support

For issues or questions, please open an issue in the repository.
