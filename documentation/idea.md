# periph4all — Personalized Peripheral Recommender

## Project Intent
**periph4all** is an AI-driven application designed to help users find their *perfect mouse*. By simulating a conversation with a chatbot, the app collects user preferences such as hand size, grip type, game genre, sensitivity, and budget. It then vectorizes these preferences into an embedding space and compares them against a database of gaming mice to recommend the top 3 matches.  

It's also going to use an LLM to make the conversation seem more fluid, real, and dyamic.

Additionally, **periph4all** visualizes a graph of all mice in embedding space, allowing users to explore how their preferences align with other options and discover similar alternatives. The goal is to combine personalization, technical sophistication, and interactive visualization into a fun, intuitive user experience.

---

## Tech Stack

* indicates I'm not sure yet

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend | Next.js + Plotly.js* | Interactive chat interface and embedding graph visualization |
| Backend | FastAPI | API endpoints for recommendation logic, LLM integration, and embedding similarity |
| ML / AI | OpenAI Embeddings* API or SentenceTransformers* | Convert mouse specs and user preferences into vector embeddings |
| Dimensionality Reduction | UMAP* | Project embeddings to 2D for graph visualization |
| Data Storage | JSON / CSV | Store precomputed embeddings and mouse metadata |

---

## Technologies & Concepts Applied

- **Vector Embeddings:** Represent both user preferences and mouse specifications in a high-dimensional semantic space for similarity comparison.  
- **Cosine Similarity:** Rank mice by closeness to user preference vectors to determine top recommendations.  
- **Dimensionality Reduction (UMAP/t-SNE):** Convert high-dimensional embeddings into 2D space for visualization.  
- **LLM Chatbot:** Collect user preferences in a conversational interface and generate natural-language explanations for recommendations.  
- **Graph Visualization:** Interactive embedding map showing mouse clusters and user positioning for intuitive exploration.  
- **Hybrid Embedding Strategy:** Combine numeric features (weight, dimensions, DPI) with categorical/semantic features (grip type, shape, genre suitability) to reduce bias.  
- **Frontend-Backend Integration:** Real-time interaction between React UI and Python backend for smooth recommendation flow.  
- **Data-Driven Design:** Use structured datasets of gaming mice to power accurate and meaningful recommendations.  

---

## Summary
**periph4all** demonstrates the application of modern AI/ML techniques, embedding-based search, and interactive visualization in a niche but technically rich domain. The project balances technical sophistication, user engagement, and a clear demo narrative suitable for a hackathon setting.
