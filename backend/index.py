# api/index.py
# This file acts as the entry point for Vercel's serverless functions.
# It imports the Flask app instance from the backend module.

from backend.app import app

# Vercel's Python runtime will automatically detect the 'app' variable
# and use it as the WSGI application.