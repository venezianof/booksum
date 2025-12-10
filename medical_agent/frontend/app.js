/**
 * MEDICAL AGENT - Frontend Application
 * Vanilla JavaScript chat interface with API integration
 */

// ============================================
// DOM ELEMENTS & STATE
// ============================================
const chatForm = document.getElementById('chatForm');
const questionInput = document.getElementById('questionInput');
const submitButton = document.getElementById('submitButton');
const chatMessages = document.getElementById('chatMessages');
const spinnerContainer = document.getElementById('spinnerContainer');
const errorMessage = document.getElementById('errorMessage');
const errorContent = document.getElementById('errorContent');

// Configuration - adjust API endpoint as needed
const API_CONFIG = {
    endpoint: '/api/ask',
    timeout: 30000, // 30 seconds
    retryAttempts: 2
};

// ============================================
// UTILITY FUNCTIONS
// ============================================

/**
 * Scrolls chat messages to bottom (latest message)
 */
function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

/**
 * Shows the loading spinner
 */
function showSpinner() {
    spinnerContainer.style.display = 'block';
    submitButton.disabled = true;
    questionInput.disabled = true;
}

/**
 * Hides the loading spinner
 */
function hideSpinner() {
    spinnerContainer.style.display = 'none';
    submitButton.disabled = false;
    questionInput.disabled = false;
}

/**
 * Shows error message with given text
 * @param {string} message - Error message to display
 */
function showError(message) {
    errorContent.textContent = message;
    errorMessage.style.display = 'flex';
    
    // Auto-hide error after 5 seconds
    setTimeout(() => {
        hideError();
    }, 5000);
}

/**
 * Hides error message
 */
function hideError() {
    errorMessage.style.display = 'none';
}

/**
 * Sanitizes HTML to prevent XSS attacks
 * @param {string} text - Text to sanitize
 * @returns {string} - Sanitized text
 */
function sanitizeHTML(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Formats text with basic markdown-like support
 * Converts line breaks and preserves spacing
 * @param {string} text - Text to format
 * @returns {string} - Formatted HTML string
 */
function formatText(text) {
    // Sanitize first
    const sanitized = sanitizeHTML(text);
    
    // Convert line breaks to <br>
    let formatted = sanitized.replace(/\n/g, '<br>');
    
    // Convert URLs to clickable links
    formatted = formatted.replace(
        /(https?:\/\/[^\s<]+)/g,
        '<a href="$1" target="_blank" rel="noopener noreferrer" class="message__link">$1</a>'
    );
    
    return formatted;
}

/**
 * Validates user input
 * @param {string} question - Question text to validate
 * @returns {Object} - {valid: boolean, error: string}
 */
function validateInput(question) {
    if (!question || question.trim().length === 0) {
        return {
            valid: false,
            error: 'Per favore, inserisci una domanda.'
        };
    }
    
    if (question.trim().length < 3) {
        return {
            valid: false,
            error: 'La domanda deve contenere almeno 3 caratteri.'
        };
    }
    
    if (question.trim().length > 1000) {
        return {
            valid: false,
            error: 'La domanda è troppo lunga. Limite: 1000 caratteri.'
        };
    }
    
    return { valid: true, error: null };
}

// ============================================
// MESSAGE RENDERING
// ============================================

/**
 * Creates and appends a user message bubble
 * @param {string} text - User's question
 */
function addUserMessage(text) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message message--user';
    
    messageDiv.innerHTML = `
        <div class="message__avatar">👤</div>
        <div class="message__content">
            <div class="message__bubble">${formatText(text)}</div>
        </div>
    `;
    
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

/**
 * Creates and appends an agent message bubble with optional sources
 * @param {string} text - Agent's response
 * @param {Array} sources - Optional array of source objects {title, url}
 */
function addAgentMessage(text, sources = []) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message message--agent';
    
    // Build sources HTML if provided
    let sourcesHTML = '';
    if (sources && sources.length > 0) {
        const sourceLinks = sources
            .map(source => {
                const title = sanitizeHTML(source.title || source.url || 'Fonte');
                const url = sanitizeHTML(source.url || '#');
                return `<a href="${url}" target="_blank" rel="noopener noreferrer" class="message__source-link">📎 ${title}</a>`;
            })
            .join('');
        
        sourcesHTML = `
            <div class="message__sources">
                <div class="message__sources-title">📚 Fonti:</div>
                ${sourceLinks}
            </div>
        `;
    }
    
    messageDiv.innerHTML = `
        <div class="message__avatar">🤖</div>
        <div class="message__content">
            <div class="message__bubble">
                ${formatText(text)}
                ${sourcesHTML}
            </div>
        </div>
    `;
    
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

// ============================================
// API COMMUNICATION
// ============================================

/**
 * Makes API call to the medical agent backend
 * @param {string} question - User's question
 * @returns {Promise<Object>} - Response data
 */
async function askMedicalAgent(question) {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), API_CONFIG.timeout);
    
    try {
        const response = await fetch(API_CONFIG.endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify({ question: question.trim() }),
            signal: controller.signal
        });
        
        clearTimeout(timeoutId);
        
        // Handle HTTP errors
        if (!response.ok) {
            let errorMsg = 'Si è verificato un errore durante la richiesta.';
            
            try {
                const errorData = await response.json();
                errorMsg = errorData.error || errorData.message || errorMsg;
            } catch (e) {
                // If response is not JSON, use status text
                errorMsg = `Errore ${response.status}: ${response.statusText}`;
            }
            
            throw new Error(errorMsg);
        }
        
        // Parse successful response
        const data = await response.json();
        return data;
        
    } catch (error) {
        clearTimeout(timeoutId);
        
        // Handle specific error types
        if (error.name === 'AbortError') {
            throw new Error('La richiesta è scaduta. Per favore riprova.');
        }
        
        if (error.message.includes('Failed to fetch') || error.message.includes('NetworkError')) {
            throw new Error('Impossibile connettersi al server. Verifica la tua connessione e riprova.');
        }
        
        throw error;
    }
}

/**
 * Handles API call with retry logic
 * @param {string} question - User's question
 * @param {number} attempt - Current attempt number
 * @returns {Promise<Object>} - Response data
 */
async function askWithRetry(question, attempt = 1) {
    try {
        return await askMedicalAgent(question);
    } catch (error) {
        if (attempt < API_CONFIG.retryAttempts) {
            console.warn(`Attempt ${attempt} failed, retrying...`, error);
            // Wait before retrying (exponential backoff)
            await new Promise(resolve => setTimeout(resolve, 1000 * attempt));
            return askWithRetry(question, attempt + 1);
        }
        throw error;
    }
}

// ============================================
// FORM HANDLING
// ============================================

/**
 * Handles form submission
 * @param {Event} event - Form submit event
 */
async function handleFormSubmit(event) {
    event.preventDefault();
    hideError();
    
    const question = questionInput.value;
    
    // Validate input
    const validation = validateInput(question);
    if (!validation.valid) {
        showError(validation.error);
        return;
    }
    
    // Add user message to chat
    addUserMessage(question);
    
    // Clear input
    questionInput.value = '';
    questionInput.style.height = 'auto';
    
    // Show loading state
    showSpinner();
    
    try {
        // Make API call
        const response = await askWithRetry(question);
        
        // Extract response data
        const answerText = response.answer || response.response || response.text || 
                          'Mi dispiace, non ho potuto generare una risposta.';
        const sources = response.sources || response.references || [];
        
        // Add agent response to chat
        addAgentMessage(answerText, sources);
        
    } catch (error) {
        console.error('Error calling medical agent:', error);
        showError(error.message || 'Si è verificato un errore. Riprova più tardi.');
        
        // Add error message to chat
        addAgentMessage(
            '❌ Mi dispiace, si è verificato un errore durante l\'elaborazione della tua domanda. ' +
            'Verifica che il server sia avviato e riprova.'
        );
        
    } finally {
        hideSpinner();
    }
}

// ============================================
// INPUT ENHANCEMENTS
// ============================================

/**
 * Handles textarea auto-resize
 */
function handleTextareaResize() {
    questionInput.style.height = 'auto';
    questionInput.style.height = questionInput.scrollHeight + 'px';
}

/**
 * Handles Enter key behavior (submit on Enter, newline on Shift+Enter)
 * @param {KeyboardEvent} event - Keyboard event
 */
function handleKeyPress(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        chatForm.dispatchEvent(new Event('submit', { cancelable: true }));
    }
}

// ============================================
// EVENT LISTENERS
// ============================================

// Form submission
chatForm.addEventListener('submit', handleFormSubmit);

// Textarea auto-resize
questionInput.addEventListener('input', handleTextareaResize);

// Enter key handling
questionInput.addEventListener('keypress', handleKeyPress);

// ============================================
// INITIALIZATION
// ============================================

/**
 * Initializes the application
 */
function init() {
    console.log('Medical Agent Frontend initialized');
    console.log('API Endpoint:', API_CONFIG.endpoint);
    
    // Focus on input
    questionInput.focus();
    
    // Check if API is available (optional health check)
    checkAPIHealth();
}

/**
 * Optional: Check if API endpoint is available
 */
async function checkAPIHealth() {
    try {
        // Try a HEAD request to check if endpoint exists
        const response = await fetch(API_CONFIG.endpoint, { 
            method: 'OPTIONS',
            signal: AbortSignal.timeout(3000)
        });
        
        if (!response.ok && response.status !== 404) {
            console.warn('API health check failed:', response.status);
        }
    } catch (error) {
        console.warn('Could not reach API endpoint. Make sure the backend is running.');
        console.warn('You can still use this interface - it will show connection errors when you submit questions.');
    }
}

// Start the application when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}

// ============================================
// DEMO MODE (for standalone testing)
// ============================================

/**
 * Demo mode: Simulates API responses when backend is not available
 * Uncomment the code below to enable demo mode
 */
/*
const DEMO_MODE = true;

if (DEMO_MODE) {
    console.log('🎭 DEMO MODE ENABLED - Using simulated responses');
    
    // Override askMedicalAgent with demo implementation
    window.askMedicalAgent = async function(question) {
        // Simulate network delay
        await new Promise(resolve => setTimeout(resolve, 1500));
        
        // Simulate response based on question
        const lowerQuestion = question.toLowerCase();
        
        if (lowerQuestion.includes('ipertensione')) {
            return {
                answer: "L'ipertensione, o pressione alta, è una condizione in cui la pressione del sangue nelle arterie è costantemente elevata. " +
                       "È spesso chiamata 'killer silenzioso' perché raramente causa sintomi ma può portare a gravi problemi di salute come " +
                       "malattie cardiache, ictus e problemi renali. La pressione normale è inferiore a 120/80 mmHg.",
                sources: [
                    { title: "WHO - Hypertension", url: "https://www.who.int/news-room/fact-sheets/detail/hypertension" },
                    { title: "Mayo Clinic - High blood pressure", url: "https://www.mayoclinic.org/diseases-conditions/high-blood-pressure/symptoms-causes/syc-20373410" }
                ]
            };
        } else if (lowerQuestion.includes('diabete')) {
            return {
                answer: "Il diabete è una malattia cronica caratterizzata da livelli elevati di glucosio nel sangue. I sintomi comuni includono: " +
                       "aumento della sete, minzione frequente, fame eccessiva, perdita di peso inspiegabile, affaticamento, visione offuscata, " +
                       "lenta guarigione delle ferite e infezioni frequenti. Esistono principalmente due tipi: diabete di tipo 1 e di tipo 2.",
                sources: [
                    { title: "CDC - Diabetes Symptoms", url: "https://www.cdc.gov/diabetes/basics/symptoms.html" }
                ]
            };
        } else {
            return {
                answer: "Ho ricevuto la tua domanda: '" + question + "'. In modalità demo, posso rispondere a domande su ipertensione e diabete. " +
                       "Per risposte complete, assicurati che il backend sia in esecuzione.",
                sources: []
            };
        }
    };
}
*/
