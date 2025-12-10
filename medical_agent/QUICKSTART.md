# Medical Agent - Quick Start Guide

Get the medical agent up and running in 3 minutes!

## 🚀 Method 1: Full Stack (Recommended)

Run both frontend and backend together:

```bash
# 1. Navigate to the medical_agent directory
cd medical_agent

# 2. Install dependencies (one-time setup)
pip install -r requirements.txt

# 3. Start the server
python app.py

# 4. Open your browser to:
http://localhost:5000
```

That's it! The frontend will be served and ready to use.

## 🎨 Method 2: Frontend Only (Testing)

Test just the frontend without the backend:

```bash
# 1. Navigate to the frontend directory
cd medical_agent/frontend

# 2. Start a simple HTTP server
python3 -m http.server 8080

# 3. Open your browser to:
http://localhost:8080

# 4. (Optional) Enable demo mode
# Edit app.js and uncomment the DEMO MODE section at the bottom
```

## 📝 Try These Example Questions

Once the app is running, try asking:

- **Che cos'è l'ipertensione?**
  _(What is hypertension?)_

- **Quali sono i sintomi del diabete?**
  _(What are the symptoms of diabetes?)_

- **Come si previene l'influenza?**
  _(How do you prevent the flu?)_

- **Cosa causa il mal di testa?**
  _(What causes headaches?)_

## 🔧 Troubleshooting

### Flask not installed?

```bash
pip install flask flask-cors
```

### Port already in use?

Edit `app.py` and change the port:

```python
app.run(port=5001)  # Change from 5000 to 5001
```

### CORS errors?

Make sure you're accessing the frontend through Flask (http://localhost:5000) and not directly opening the HTML file in your browser.

### Frontend not loading?

1. Check that all files are in place:
   ```bash
   ls -la medical_agent/frontend/
   # Should show: index.html, styles.css, app.js, README.md
   ```

2. Check Flask is serving the frontend:
   ```bash
   curl http://localhost:5000/
   # Should return HTML content
   ```

## 📚 Next Steps

- **Customize the styling**: Edit `frontend/styles.css` CSS variables
- **Add your agent**: Replace mock responses in `app.py`
- **Read the docs**: Check `README.md` for detailed documentation
- **Configure CORS**: Update CORS settings for production

## 🎯 Key Features at a Glance

| Feature | Status |
|---------|--------|
| Mobile-friendly | ✅ |
| Italian interface | ✅ |
| Loading spinner | ✅ |
| Error handling | ✅ |
| Source citations | ✅ |
| Input validation | ✅ |
| Accessibility | ✅ |
| Demo mode | ✅ |

## 💡 Tips

1. **Development**: Keep Flask debug mode enabled for auto-reload
2. **Testing**: Use the `/api/health` endpoint to check server status
3. **Customization**: All colors are CSS variables - easy to theme!
4. **Integration**: Replace `generate_mock_response()` with your agent
5. **Mobile**: Test on actual mobile devices for best experience

---

**Happy coding! 🏥**

For detailed documentation, see the main [README.md](README.md).
