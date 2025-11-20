---
title: periph4all API
emoji: 🖱️
colorFrom: blue
colorTo: purple
sdk: docker
sdk_version: latest
app_port: 7860
---

# periph4all Backend API

FastAPI backend for the periph4all AI-driven mouse recommendation system.

## Features

- 🤖 **AI-Powered Chat**: Conversational interface to collect user preferences
- 🎯 **Smart Recommendations**: Vector embedding-based mouse matching using cosine similarity
- 📊 **Interactive Visualizations**: UMAP dimensionality reduction for 2D embedding space visualization
- 🚀 **Fast & Scalable**: Built with FastAPI for high performance
- 📦 **Caching**: Intelligent caching of embeddings for faster responses

## API Endpoints

### Health Check
- `GET /health` - Health check endpoint
- `GET /` - Root endpoint with API info

### Chat
- `POST /api/v1/chat/` - Process chat messages and extract preferences
- `POST /api/v1/chat/reset` - Reset conversation

### Recommendations
- `POST /api/v1/recommendations/` - Get personalized recommendations
- `POST /api/v1/recommendations/quick` - Quick recommendations with defaults

### Visualizations
- `GET /api/v1/visualizations/embedding-space` - Get all mice in 2D space
- `POST /api/v1/visualizations/embedding-space-with-user` - Include user preferences

## Interactive Documentation

- **Swagger UI**: `/docs`
- **ReDoc**: `/redoc`

## Environment Variables

Set these in your Hugging Face Space settings (Settings → Repository secrets):

- `GROQ_API_KEY`: (Optional) Your Groq API key for LLM-powered chat
- `ALLOWED_ORIGINS`: (Optional) Comma-separated list of allowed CORS origins

## Usage Examples

### Get Recommendations

```python
import requests

preferences = {
    "hand_size": "medium",
    "grip_type": "claw",
    "genre": "fps",
    "budget_max": 100,
    "wireless_preference": True
}

response = requests.post(
    "https://YOUR-USERNAME-periph4all-api.hf.space/api/v1/recommendations/quick",
    json=preferences
)

recommendations = response.json()
```

### Chat Interaction

```python
import requests

messages = [
    {"role": "user", "content": "I need a gaming mouse"}
]

response = requests.post(
    "https://YOUR-USERNAME-periph4all-api.hf.space/api/v1/chat/",
    json={"messages": messages}
)

chat_response = response.json()
print(chat_response["message"]["content"])
```

## Tech Stack

- **FastAPI**: Modern web framework
- **Pydantic**: Data validation
- **SentenceTransformers**: Embedding generation
- **scikit-learn**: ML utilities
- **UMAP**: Dimensionality reduction
- **NumPy**: Numerical computing
- **Pandas**: Data manipulation
- **Groq**: LLM integration
