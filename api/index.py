"""
Vercel serverless function handler for FastAPI backend.
This file wraps the FastAPI app to work with Vercel's serverless functions.
"""
import sys
import os

# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from mangum import Mangum
from Backend.main import app

# Create the handler for Vercel
# Mangum converts ASGI (FastAPI) to AWS Lambda/API Gateway format that Vercel uses
handler = Mangum(app, lifespan="off")

# Vercel expects the handler to be exported as 'handler'
__all__ = ["handler"]

