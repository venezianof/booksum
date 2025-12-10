"""
Medical Agent Flask Application
Simple backend server for the medical agent frontend
"""

from flask import Flask, send_from_directory, jsonify, request
from flask_cors import CORS
import os

# Initialize Flask app
app = Flask(__name__, static_folder='frontend', static_url_path='')

# Enable CORS for development (configure properly for production)
CORS(app)

# Get the frontend directory path
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), 'frontend')


@app.route('/')
def index():
    """
    Serve the main frontend page
    """
    return send_from_directory(FRONTEND_DIR, 'index.html')


@app.route('/api/ask', methods=['POST'])
def ask():
    """
    Handle medical agent questions
    
    Expected request body:
    {
        "question": "Che cos'è l'ipertensione?"
    }
    
    Returns:
    {
        "answer": "Response text...",
        "sources": [
            {"title": "Source Title", "url": "https://..."}
        ]
    }
    """
    try:
        # Get JSON data from request
        data = request.get_json()
        
        # Validate request
        if not data:
            return jsonify({'error': 'Request body is required'}), 400
        
        if 'question' not in data:
            return jsonify({'error': 'Question field is required'}), 400
        
        question = data['question'].strip()
        
        # Validate question
        if len(question) < 3:
            return jsonify({'error': 'La domanda deve contenere almeno 3 caratteri'}), 400
        
        if len(question) > 1000:
            return jsonify({'error': 'La domanda è troppo lunga. Limite: 1000 caratteri'}), 400
        
        # ============================================
        # TODO: Integrate with your medical agent here
        # ============================================
        # Example integration points:
        # 1. Call your LLM/agent with the question
        # 2. Retrieve relevant medical information
        # 3. Generate a response with sources
        # 4. Return formatted response
        
        # For now, return a mock response with examples
        response_data = generate_mock_response(question)
        
        return jsonify(response_data), 200
        
    except Exception as e:
        app.logger.error(f"Error processing request: {str(e)}")
        return jsonify({'error': 'Si è verificato un errore interno del server'}), 500


def generate_mock_response(question):
    """
    Generate a mock response for demonstration
    Replace this with your actual medical agent logic
    
    Args:
        question (str): User's question
        
    Returns:
        dict: Response with answer and sources
    """
    question_lower = question.lower()
    
    # Mock responses for common medical questions
    if 'ipertensione' in question_lower or 'pressione alta' in question_lower:
        return {
            'answer': (
                "L'ipertensione, nota anche come pressione alta, è una condizione medica in cui "
                "la pressione del sangue nelle arterie è persistentemente elevata. "
                "Una pressione normale è inferiore a 120/80 mmHg. L'ipertensione è considerata "
                "quando i valori sono costantemente pari o superiori a 140/90 mmHg.\n\n"
                "Le cause possono includere:\n"
                "• Fattori genetici\n"
                "• Dieta ricca di sale\n"
                "• Mancanza di attività fisica\n"
                "• Obesità\n"
                "• Consumo eccessivo di alcol\n"
                "• Stress cronico\n\n"
                "È importante consultare un medico per diagnosi e trattamento appropriati."
            ),
            'sources': [
                {
                    'title': 'WHO - Hypertension Fact Sheet',
                    'url': 'https://www.who.int/news-room/fact-sheets/detail/hypertension'
                },
                {
                    'title': 'Mayo Clinic - High Blood Pressure',
                    'url': 'https://www.mayoclinic.org/diseases-conditions/high-blood-pressure/symptoms-causes/syc-20373410'
                }
            ]
        }
    
    elif 'diabete' in question_lower:
        return {
            'answer': (
                "Il diabete è una malattia cronica caratterizzata da livelli elevati di glucosio nel sangue. "
                "I sintomi comuni includono:\n\n"
                "• Aumento della sete\n"
                "• Minzione frequente\n"
                "• Fame eccessiva\n"
                "• Perdita di peso inspiegabile\n"
                "• Affaticamento e debolezza\n"
                "• Visione offuscata\n"
                "• Lenta guarigione delle ferite\n"
                "• Infezioni frequenti\n\n"
                "Esistono principalmente due tipi di diabete:\n"
                "• Tipo 1: Il corpo non produce insulina\n"
                "• Tipo 2: Il corpo non usa l'insulina in modo efficace\n\n"
                "Se si sospetta il diabete, è fondamentale consultare un medico per test e diagnosi."
            ),
            'sources': [
                {
                    'title': 'CDC - Diabetes Symptoms',
                    'url': 'https://www.cdc.gov/diabetes/basics/symptoms.html'
                },
                {
                    'title': 'American Diabetes Association',
                    'url': 'https://diabetes.org/about-diabetes/symptoms'
                }
            ]
        }
    
    elif 'influenza' in question_lower or 'prevenzione' in question_lower:
        return {
            'answer': (
                "La prevenzione dell'influenza include diverse misure efficaci:\n\n"
                "1. **Vaccinazione annuale**: Il modo più efficace per prevenire l'influenza\n"
                "2. **Igiene delle mani**: Lavarsi frequentemente con acqua e sapone\n"
                "3. **Evitare il contatto ravvicinato**: Con persone malate\n"
                "4. **Coprire naso e bocca**: Quando si tossisce o starnutisce\n"
                "5. **Non toccare occhi, naso e bocca**: Con mani non lavate\n"
                "6. **Pulire superfici**: Disinfettare oggetti e superfici toccati frequentemente\n"
                "7. **Stile di vita sano**: Dormire a sufficienza, fare esercizio, gestire lo stress\n\n"
                "Il vaccino antinfluenzale è raccomandato annualmente, specialmente per bambini, "
                "anziani e persone con condizioni mediche croniche."
            ),
            'sources': [
                {
                    'title': 'CDC - Preventing the Flu',
                    'url': 'https://www.cdc.gov/flu/prevent/index.html'
                }
            ]
        }
    
    elif 'mal di testa' in question_lower or 'cefalea' in question_lower:
        return {
            'answer': (
                "Il mal di testa può avere molte cause diverse:\n\n"
                "**Cause comuni:**\n"
                "• Tensione e stress\n"
                "• Disidratazione\n"
                "• Mancanza di sonno\n"
                "• Fame o basso livello di zucchero nel sangue\n"
                "• Postura scorretta\n"
                "• Affaticamento degli occhi (schermi)\n"
                "• Consumo eccessivo di caffeina\n\n"
                "**Tipi di mal di testa:**\n"
                "• Cefalea tensiva: Il tipo più comune\n"
                "• Emicrania: Dolore pulsante, spesso da un lato\n"
                "• Cefalea a grappolo: Dolore intenso intorno a un occhio\n\n"
                "Se i mal di testa sono frequenti, severi o accompagnati da altri sintomi, "
                "è importante consultare un medico."
            ),
            'sources': [
                {
                    'title': 'Mayo Clinic - Headache Causes',
                    'url': 'https://www.mayoclinic.org/symptoms/headache/basics/causes/sym-20050800'
                },
                {
                    'title': 'NHS - Headaches',
                    'url': 'https://www.nhs.uk/conditions/headaches/'
                }
            ]
        }
    
    else:
        # Generic response for other questions
        return {
            'answer': (
                f'Ho ricevuto la tua domanda: "{question}"\n\n'
                "Questa è un'applicazione dimostrativa. Per informazioni mediche accurate, "
                "integra questo endpoint con un vero agente medico che utilizza fonti affidabili "
                "e modelli di linguaggio specializzati.\n\n"
                "Per ora, ho risposte predefinite per domande su:\n"
                "• Ipertensione\n"
                "• Diabete\n"
                "• Prevenzione dell'influenza\n"
                "• Mal di testa\n\n"
                "⚠️ Ricorda: Consulta sempre un professionista sanitario qualificato per "
                "consigli medici personalizzati."
            ),
            'sources': [
                {
                    'title': 'WHO - Health Topics',
                    'url': 'https://www.who.int/health-topics'
                }
            ]
        }


@app.route('/api/health', methods=['GET'])
def health():
    """
    Health check endpoint
    """
    return jsonify({
        'status': 'healthy',
        'service': 'medical-agent-api',
        'version': '1.0.0'
    }), 200


@app.errorhandler(404)
def not_found(error):
    """
    Handle 404 errors
    """
    return jsonify({'error': 'Endpoint non trovato'}), 404


@app.errorhandler(500)
def internal_error(error):
    """
    Handle 500 errors
    """
    return jsonify({'error': 'Errore interno del server'}), 500


if __name__ == '__main__':
    # Run the Flask app
    print("=" * 50)
    print("🏥 Medical Agent Server Starting...")
    print("=" * 50)
    print(f"Frontend: http://localhost:5000")
    print(f"API: http://localhost:5000/api/ask")
    print(f"Health: http://localhost:5000/api/health")
    print("=" * 50)
    
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000,
        threaded=True
    )
