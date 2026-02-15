import sys
import os
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Add the parent directory to the Python path so we can import flask_app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    logger.info("Importing flask_app...")
    from flask_app import app
    logger.info("Successfully imported flask_app")
except Exception as e:
    logger.error(f"Failed to import flask_app: {e}", exc_info=True)
    raise

# This is the entry point for Vercel
if __name__ == "__main__":
    app.run()

# Export the app for Vercel
handler = app
