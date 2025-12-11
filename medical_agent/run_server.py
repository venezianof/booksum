#!/usr/bin/env python3
"""Script to run the medical agent server."""

import os
import sys

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set Flask to not reload (simpler for testing)
os.environ['FLASK_DEBUG'] = '0'

# Import and run the app
from backend.app import app

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting Medical Research Agent server on http://localhost:{port}")
    print("Press CTRL+C to stop the server")
    print("-" * 60)
    app.run(host='0.0.0.0', port=port, debug=False)
