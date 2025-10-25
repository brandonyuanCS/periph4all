# periph4all Backend API

FastAPI backend for the periph4all AI-driven mouse recommendation system.

## Features

- 🤖 **AI-Powered Chat**: Conversational interface to collect user preferences
- 🎯 **Smart Recommendations**: Vector embedding-based mouse matching using cosine similarity
- 📊 **Interactive Visualizations**: UMAP dimensionality reduction for 2D embedding space visualization
- 🚀 **Fast & Scalable**: Built with FastAPI for high performance
- 📦 **Caching**: Intelligent caching of embeddings for faster responses

## Project Structure

```
backend/
├── app/
│   ├── api/
│   │   ├── endpoints/        # API route handlers
│   │   │   ├── chat.py       # Chat endpoints
│   │   │   ├── recommendations.py  # Recommendation endpoints
│   │   │   └── visualizations.py   # Visualization endpoints
│   │   └── deps.py           # Dependency injection
│   ├── core/
│   │   └── config.py         # Application configuration
│   ├── models/
│   │   └── schemas.py        # Pydantic models
│   ├── services/
│   │   ├── data_loader.py    # Dataset loading
│   │   ├── embeddings.py     # Embedding generation
│   │   ├── recommender.py    # Recommendation logic
│   │   └── llm.py           # LLM chat processing
│   ├── utils/
│   │   └── similarity.py     # Similarity computations
│   └── main.py              # FastAPI app entry point
├── data/
│   ├── FINAL.csv            # Mouse dataset
│   └── cache/               # Embedding cache
└── requirements.txt         # Python dependencies
```

## Setup

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

Or use a virtual environment (recommended):

```bash
cd backend
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

Edit `.env`:
- `OPENAI_API_KEY`: (Optional) OpenAI API key for LLM-powered chat
- Without API key, the system uses rule-based fallback responses

### 3. Ensure Dataset Exists

Make sure `data/FINAL.csv` exists with your mouse dataset.

## Running the Server

### Development Mode

```bash
# From backend directory
python -m app.main
```

Or using uvicorn directly:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

### Production Mode

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Endpoints

### Health Check
- `GET /health` - Health check endpoint

### Chat
- `POST /api/v1/chat/` - Process chat messages and extract preferences
- `POST /api/v1/chat/reset` - Reset conversation

### Recommendations
- `POST /api/v1/recommendations/` - Get personalized recommendations
- `POST /api/v1/recommendations/quick` - Quick recommendations with defaults

### Visualizations
- `GET /api/v1/visualizations/embedding-space` - Get all mice in 2D space
- `POST /api/v1/visualizations/embedding-space-with-user` - Include user preferences

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
    "http://localhost:8000/api/v1/recommendations/quick",
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
    "http://localhost:8000/api/v1/chat/",
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
- **OpenAI**: Optional LLM integration

## Architecture

### Embedding Pipeline
1. Mouse specs → Descriptive text → Vector embedding
2. User preferences → Descriptive text → Vector embedding
3. Cosine similarity between user and all mice
4. Return top K matches

### Caching Strategy
- Mouse embeddings cached in `data/cache/`
- Automatically regenerated if dataset changes
- UMAP transformations cached for performance

### LLM Integration
- **With API Key**: Natural conversation with GPT
- **Without API Key**: Rule-based pattern matching
- Both modes extract structured preferences

## Development

### Adding New Endpoints

1. Create endpoint file in `app/api/endpoints/`
2. Define router and route handlers
3. Add router to `app/main.py`

### Modifying Embeddings

Edit `app/services/embeddings.py`:
- `mouse_to_text()`: Customize mouse description format
- `preferences_to_text()`: Customize preference representation

### Adjusting Recommendations

Edit `app/services/recommender.py`:
- Modify filtering logic
- Adjust similarity computation
- Customize reasoning generation

## Troubleshooting

### "Dataset not found" error
Ensure `backend/data/FINAL.csv` exists

### Slow first request
First request generates embeddings - this is cached for subsequent requests

### LLM not working
Check `OPENAI_API_KEY` in `.env` or use without (fallback mode)

## License

Part of periph4all project - AI-driven peripheral recommendation system

