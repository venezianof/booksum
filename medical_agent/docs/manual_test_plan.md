# Manual Test Plan for Medical Research Agent

**Purpose**: Guide users through manual end-to-end testing of the Medical Research Agent in a browser without running automated tests.

**Prerequisites**:
- Python 3.8+ installed
- Virtual environment set up and activated
- All dependencies installed (`pip install -r requirements.txt`)
- Server is running (`python backend/app.py`)

---

## ⚠️ Important Medical Disclaimer

Before using this tool, please be aware:
- **This tool is for educational and research purposes only**
- It is **NOT** a substitute for professional medical advice, diagnosis, or treatment
- Always consult with a qualified healthcare provider
- Information may be incomplete, contain errors, or be outdated
- In case of medical emergency, call emergency services immediately

---

## Test Checklist

### 1. Server Startup Verification

- [ ] **Start the server**: Open a terminal, navigate to `medical_agent/` and run:
  ```bash
  python backend/app.py
  ```
  
- [ ] **Expected output**: You should see output similar to:
  ```
   * Serving Flask app 'app'
   * Debug mode: on
   * Running on http://127.0.0.1:5000
   ```

- [ ] **Server is running**: Server runs without errors and shows the Flask development server message

### 2. Health Check Endpoint

- [ ] **Open a browser**: Navigate to `http://localhost:5000/health`

- [ ] **Expected response**: You should see JSON displayed in your browser:
  ```json
  {
    "status": "healthy",
    "agent": "ready"
  }
  ```

- [ ] **HTTP Status**: Browser tab shows the page loaded (no error page)

### 3. Web Interface Access

- [ ] **Navigate to main page**: Go to `http://localhost:5000/`

- [ ] **Page loads**: The page loads without browser console errors

- [ ] **Note**: If you haven't built a frontend yet, you may see a 404 error. This is expected until the frontend is implemented.

### 4. API Endpoint Testing (Using Browser Developer Tools or curl)

#### 4.1 Success Case: Valid Question

- [ ] **Open terminal** and run this curl command:
  ```bash
  curl -X POST http://localhost:5000/api/ask \
    -H "Content-Type: application/json" \
    -d '{"question": "What are the symptoms of hypertension?"}'
  ```

- [ ] **Expected response**: JSON with the structure:
  ```json
  {
    "answer_text": "...",
    "bullets": ["...", "...", "..."],
    "source_links": ["https://...", "https://..."],
    "disclaimer": "⚠️ DISCLAIMER: ..."
  }
  ```

- [ ] **All fields present**: Response includes `answer_text`, `bullets`, `source_links`, and `disclaimer`

- [ ] **Disclaimer visible**: Disclaimer field contains the medical disclaimer text

#### 4.2 Test Multiple Valid Questions

Try these different questions and verify each returns a valid response:

- [ ] **Simple question**: 
  ```bash
  curl -X POST http://localhost:5000/api/ask \
    -H "Content-Type: application/json" \
    -d '{"question": "What is diabetes?"}'
  ```

- [ ] **Complex question**:
  ```bash
  curl -X POST http://localhost:5000/api/ask \
    -H "Content-Type: application/json" \
    -d '{"question": "What are the latest evidence-based treatments for depression?"}'
  ```

- [ ] **Medical terminology**:
  ```bash
  curl -X POST http://localhost:5000/api/ask \
    -H "Content-Type: application/json" \
    -d '{"question": "Explain pathophysiology of type 2 diabetes mellitus"}'
  ```

- [ ] **All return success**: Each request returns HTTP 200 with valid JSON response

#### 4.3 Error Case: Empty Question

- [ ] **Test empty string**:
  ```bash
  curl -X POST http://localhost:5000/api/ask \
    -H "Content-Type: application/json" \
    -d '{"question": ""}'
  ```

- [ ] **Expected response**: HTTP 400 error with JSON:
  ```json
  {"error": "Missing or empty 'question' field"}
  ```

#### 4.4 Error Case: Missing Question Field

- [ ] **Test missing field**:
  ```bash
  curl -X POST http://localhost:5000/api/ask \
    -H "Content-Type: application/json" \
    -d '{"some_other_field": "value"}'
  ```

- [ ] **Expected response**: HTTP 400 error with JSON containing `error` field

#### 4.5 Error Case: Whitespace-Only Question

- [ ] **Test whitespace**:
  ```bash
  curl -X POST http://localhost:5000/api/ask \
    -H "Content-Type: application/json" \
    -d '{"question": "   \t\n   "}'
  ```

- [ ] **Expected response**: HTTP 400 error

#### 4.6 Error Case: Invalid JSON

- [ ] **Test invalid JSON**:
  ```bash
  curl -X POST http://localhost:5000/api/ask \
    -H "Content-Type: application/json" \
    -d 'this is not json'
  ```

- [ ] **Expected response**: HTTP 400 error

#### 4.7 Error Case: Wrong HTTP Method

- [ ] **Test GET instead of POST**:
  ```bash
  curl -X GET http://localhost:5000/api/ask
  ```

- [ ] **Expected response**: HTTP 405 (Method Not Allowed)

### 5. Response Content Validation

For each successful response from `/api/ask`:

- [ ] **Response is valid JSON**: Can be parsed without JSON errors

- [ ] **`answer_text` is string**: Contains the main response text

- [ ] **`bullets` is array**: Contains at least 1 item, all items are strings

- [ ] **`source_links` is array**: Contains at least 1 URL (string), all items are strings

- [ ] **`disclaimer` contains medical notice**: Text mentions:
  - This is for educational purposes, OR
  - This is NOT medical advice, OR
  - Consult a healthcare provider

### 6. Server Restart Test

- [ ] **Stop the server**: Press `Ctrl+C` in the terminal running the server

- [ ] **Server stops**: Terminal shows shutdown messages or returns to prompt

- [ ] **Verify stopped**: Try `curl http://localhost:5000/health` - should fail with connection error

- [ ] **Start server again**: Run `python backend/app.py` again

- [ ] **Verify restarted**: Navigate to `http://localhost:5000/health` - should show healthy status again

### 7. Deactivate Virtual Environment

- [ ] **Deactivate venv**: Run:
  ```bash
  deactivate
  ```

- [ ] **Prompt changed**: The `(venv)` prefix should disappear from your terminal prompt

### 8. Cleanup

- [ ] **Stop server** if it's still running

- [ ] **Verify no leftover processes**: Run:
  ```bash
  # On macOS/Linux
  lsof -i :5000
  
  # On Windows (if using git bash)
  netstat -ano | findstr :5000
  ```
  Should show nothing or only your browser connections

---

## Test Results Summary

Create a simple checklist like this in a text file:

```
Test Date: _______________
Tester: ___________________

✓ All server startup tests passed
✓ Health check returns correct JSON
✓ Valid questions return 200 responses
✓ Empty question returns 400 error
✓ Missing field returns 400 error
✓ Invalid JSON returns 400 error
✓ Wrong HTTP method returns 405 error
✓ All responses contain required fields
✓ Disclaimer text is present in all responses
✓ Server restart works correctly

Overall Result: PASS / FAIL
```

---

## Common Issues & Solutions

### Server won't start on port 5000

**Problem**: "Address already in use" error

**Solution**:
```bash
# Find and kill the process using port 5000
# On macOS/Linux:
lsof -ti:5000 | xargs kill -9

# On Windows (PowerShell):
Get-Process -Id (Get-NetTCPConnection -LocalPort 5000).OwningProcess | Stop-Process -Force

# Or change PORT in .env file and run:
PORT=5001 python backend/app.py
```

### curl command not working

**Problem**: "curl: command not found"

**Solutions**:
- Install curl (`brew install curl` on macOS, `apt install curl` on Ubuntu)
- **OR** use Python instead:
  ```bash
  python -c "import requests; r = requests.post('http://localhost:5000/api/ask', json={'question': 'What is diabetes?'}); print(r.json())"
  ```

### Getting "ModuleNotFoundError" when starting server

**Problem**: Can't find `app` or other imports

**Solutions**:
1. Make sure virtual environment is activated (see `(venv)` in prompt)
2. Run `pip install -r requirements.txt` again
3. Navigate from the `medical_agent/` directory

### API returns "Agent not initialized" (503 error)

**Problem**: Response says agent is not ready

**Solution**: Check server logs in the terminal - there may be a startup error. Check that all required environment variables are set in `.env` file.

---

## Extending the Tests

Once you're comfortable with the basic manual tests, try:

1. **Test with special characters**:
   ```bash
   curl -X POST http://localhost:5000/api/ask \
     -H "Content-Type: application/json" \
     -d '{"question": "What about COVID-19 & immune systems? #health"}'
   ```

2. **Test with very long questions**: Copy-paste a long medical question

3. **Test rapid requests**: Send multiple requests in quick succession

4. **Test from different machines**: If on a network, try accessing from another computer using `http://<your-ip>:5000`

---

## When You're Done

✓ All tests passed  
✓ No errors in browser console or terminal  
✓ All API endpoints respond correctly  
✓ Medical disclaimer is visible in all responses  

**You're ready to use the Medical Research Agent!**

Remember: Always consult with a qualified healthcare provider for actual medical decisions. This tool is for educational purposes only.
