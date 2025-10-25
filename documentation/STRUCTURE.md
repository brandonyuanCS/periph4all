# Backend Directory Structure

```
backend/
│
├── app/                           # Main application package
│   ├── __init__.py
│   ├── main.py                   # ⭐ FastAPI app entry point
│   │
│   ├── api/                      # API layer
│   │   ├── __init__.py
│   │   ├── deps.py              # Dependency injection (service singletons)
│   │   └── endpoints/           # Route handlers
│   │       ├── __init__.py
│   │       ├── chat.py          # 💬 Chat endpoints
│   │       ├── recommendations.py # 🎯 Recommendation endpoints
│   │       └── visualizations.py  # 📊 Visualization endpoints
│   │
│   ├── core/                    # Core configuration
│   │   ├── __init__.py
│   │   └── config.py           # ⚙️ Settings and configuration
│   │
│   ├── models/                  # Data models
│   │   ├── __init__.py
│   │   └── schemas.py          # 📋 Pydantic models for API
│   │
│   ├── services/                # Business logic layer
│   │   ├── __init__.py
│   │   ├── data_loader.py      # 📂 Dataset loading and caching
│   │   ├── embeddings.py       # 🧠 Embedding generation
│   │   ├── recommender.py      # 🎯 Recommendation engine
│   │   └── llm.py             # 🤖 LLM chat processing
│   │
│   └── utils/                   # Utility functions
│       ├── __init__.py
│       └── similarity.py        # 📐 Similarity computations
│
├── data/                        # Data storage
│   ├── FINAL.csv               # 🐭 Mouse dataset
│   ├── cache/                  # Embedding cache
│   │   ├── mouse_embeddings.npy
│   │   └── mouse_embeddings_meta.json
│   └── scripts/                # Data processing scripts
│
├── requirements.txt            # 📦 Python dependencies
├── run.py                      # 🚀 Convenience startup script
├── env.example                 # 🔐 Environment variable template
├── .gitignore                  # Git ignore rules
│
└── Documentation
    ├── README.md               # 📖 Full documentation
    ├── QUICKSTART.md          # ⚡ Quick start guide
    └── STRUCTURE.md           # 📁 This file
```

## Key Components

### Entry Point
- **`main.py`**: Initializes FastAPI app, configures CORS, includes routers

### API Endpoints

#### Chat (`/api/v1/chat/`)
- Process conversational messages
- Extract user preferences
- Determine when ready for recommendations

#### Recommendations (`/api/v1/recommendations/`)
- Generate personalized mouse recommendations
- Apply budget filtering
- Return top K matches with similarity scores

#### Visualizations (`/api/v1/visualizations/`)
- Generate 2D embedding space visualization
- Include user preference point
- Highlight recommended mice

### Services (Business Logic)

#### DataLoader
- Loads mouse dataset from CSV
- Caches data in memory
- Provides filtering capabilities

#### EmbeddingService
- Generates vector embeddings using SentenceTransformers
- Converts mice and preferences to text
- Caches embeddings for performance

#### RecommenderService
- Core recommendation engine
- Uses cosine similarity for matching
- Applies UMAP for visualization
- Generates reasoning for recommendations

#### LLMService
- Processes chat conversations
- Extracts structured preferences
- Falls back to rule-based if no API key

### Models (Pydantic Schemas)

Defines request/response structures:
- `UserPreferences`: User's mouse preferences
- `MouseInfo`: Mouse product information
- `MouseRecommendation`: Recommendation with score
- `ChatMessage`, `ChatRequest`, `ChatResponse`: Chat models
- `EmbeddingPoint`, `VisualizationResponse`: Visualization models

### Configuration

- **`config.py`**: Centralized settings using Pydantic
- **`.env`**: Environment variables (API keys, etc.)

## Data Flow

### Recommendation Flow
```
User Preferences
    ↓
preferences_to_text()
    ↓
Generate Embedding (SentenceTransformer)
    ↓
Cosine Similarity with All Mice
    ↓
Apply Budget Filter
    ↓
Top K Similar Mice
    ↓
Return Recommendations
```

### Chat Flow
```
User Message
    ↓
LLM or Rule-Based Processing
    ↓
Extract Preferences
    ↓
Update UserPreferences
    ↓
Check if Ready for Recommendations
    ↓
Return Response + Updated Preferences
```

### Visualization Flow
```
Load Mouse Embeddings
    ↓
UMAP Dimensionality Reduction
    ↓
Project to 2D Space
    ↓
(Optional) Add User Point
    ↓
(Optional) Highlight Recommendations
    ↓
Return Visualization Data
```

## Design Patterns

- **Dependency Injection**: Services injected via `deps.py`
- **Singleton Pattern**: Services cached with `@lru_cache()`
- **Separation of Concerns**: Clear layers (API → Service → Data)
- **Caching**: Embeddings and data cached for performance
- **Async/Await**: Async endpoints for scalability

## Adding Features

### New Endpoint
1. Create file in `app/api/endpoints/`
2. Define router and handlers
3. Add router to `main.py`

### New Service
1. Create file in `app/services/`
2. Implement business logic
3. Add dependency in `deps.py`
4. Inject in endpoints

### New Model
1. Add Pydantic model to `schemas.py`
2. Use in endpoint type hints
3. Auto-generates API docs!

## Performance Optimizations

- ✅ Mouse embeddings cached on disk
- ✅ Data loaded once and kept in memory
- ✅ UMAP transformation cached
- ✅ Singleton services prevent reinitialization
- ✅ Batch embedding generation

