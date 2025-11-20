"""
Hugging Face Spaces entry point
This file is used by Hugging Face Spaces to run the FastAPI application
"""
import os
import uvicorn
from app.main import app

if __name__ == "__main__":
    # Hugging Face Spaces uses PORT environment variable (defaults to 7860)
    port = int(os.environ.get("PORT", 7860))
    host = os.environ.get("HOST", "0.0.0.0")
    
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        log_level="info"
    )

