"""
Main entry point for the backend application
"""

from app import create_app

if __name__ == "__main__":
    app = create_app(__name__)

    app.run(debug=True)
