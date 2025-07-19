import sys
import os

# Add the parent directory to the Python path so we can import flask_app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask_app import app

# This is the entry point for Vercel
if __name__ == "__main__":
    app.run()

# Export the app for Vercel
handler = app
