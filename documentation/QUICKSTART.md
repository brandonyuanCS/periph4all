# Quick Start Guide

## 🚀 Get Started in 3 Steps

### 1️⃣ Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

> **Tip**: Use a virtual environment to avoid dependency conflicts:
> ```bash
> python -m venv venv
> venv\Scripts\activate  # Windows
> # or
> source venv/bin/activate  # Linux/Mac
> ```

### 2️⃣ Configure (Optional)

Create a `.env` file if you want to use OpenAI for chat:

```bash
# Copy the example
cp env.example .env

# Edit .env and add your OpenAI API key
OPENAI_API_KEY=sk-your-key-here
```

> **Note**: The system works without an API key using rule-based chat fallback!

### 3️⃣ Run the Server

```bash
# Simple way
python run.py

# Or with uvicorn directly
uvicorn app.main:app --reload
```

Visit:
- 🌐 **API Docs**: http://localhost:8000/docs
- 📖 **ReDoc**: http://localhost:8000/redoc
- ✅ **Health Check**: http://localhost:8000/health

## 📝 First Request

Open the interactive docs at http://localhost:8000/docs and try:

### Get Recommendations

Click on `POST /api/v1/recommendations/quick` and use this example:

```json
{
  "hand_size": "medium",
  "grip_type": "claw",
  "genre": "fps",
  "budget_max": 100
}
```

### Chat Interaction

Try `POST /api/v1/chat/` with:

```json
{
  "messages": [
    {
      "role": "user",
      "content": "I need help finding a gaming mouse"
    }
  ]
}
```

## 🔧 Common Issues

### "ModuleNotFoundError"
→ Install dependencies: `pip install -r requirements.txt`

### "Dataset not found"
→ Ensure `data/FINAL.csv` exists

### Slow first request
→ Normal! Embeddings are being generated (cached after first time)

## 📚 Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Explore the API at http://localhost:8000/docs
- Check out the code structure in `app/`
- Integrate with your Next.js frontend

## 🎯 API Endpoints Summary

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Health check |
| `/api/v1/chat/` | POST | Chat interaction |
| `/api/v1/recommendations/` | POST | Get recommendations |
| `/api/v1/recommendations/quick` | POST | Quick recommendations |
| `/api/v1/visualizations/embedding-space` | GET | Visualization data |

Happy coding! 🎉

