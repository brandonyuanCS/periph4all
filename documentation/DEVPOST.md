# periph4all - Devpost Submission

## Elevator Pitch

Finding the perfect gaming mouse is overwhelming with 175+ options and endless specs. **periph4all** uses conversational AI (Groq LLM) to extract your preferences through natural chat, then matches you with your top 3 mice using vector embeddings and semantic similarity search across our database. Built with Next.js, FastAPI, and Sentence Transformers, the system delivers personalized recommendations in under 2 seconds with interactive UMAP visualizations to explore the entire "mouse universe." It demonstrates how modern AI can transform product discovery by understanding meaning over keywords—matching "lightweight FPS mouse" to actual specs like weight, sensor type, and shape. **No more analysis paralysis—just chat, match, and game.**

**One-liner**: *Chat with AI, get your perfect gaming mouse—powered by LLMs and vector embeddings.*

---

## Inspiration
We've all been there—scrolling endlessly through gaming mouse reviews, drowning in specs, forum debates, and marketing jargon. With 175+ options and countless variables (hand size, grip type, DPI, weight, shape), finding the *right* mouse is paralyzing. We wanted to solve this with AI, making peripheral discovery as simple as having a conversation.

## What it does
**periph4all** is an AI-powered chatbot that finds your perfect gaming mouse through natural conversation. Chat about your preferences (hand size, grip, game genre, budget), and the system instantly recommends your top 3 matches from 175 gaming mice using vector embeddings and semantic similarity. Interactive UMAP and force-graph visualizations let you explore the entire mouse landscape in 2D space.

## How we built it
- **Frontend**: Next.js, TypeScript, React, Plotly.js for interactive visualizations
- **Backend**: FastAPI with async endpoints, dependency injection, and intelligent caching
- **AI/ML**: Groq LLM (llama-3.1-8b-instant) for conversational preference extraction, Sentence Transformers (all-MiniLM-L6-v2) for 384-dimensional embeddings, UMAP for dimensionality reduction
- **Data Pipeline**: Started with 1200+ Kaggle dataset → filtered to 450 → scraped Amazon prices with ScraperAPI → manually curated to 175 mice to reduce duplicates and brand bias
- **Architecture**: Cosine similarity ranking with hard budget filters, semantic matching for preferences, cached embeddings for <2s response times

## Challenges we ran into
**Dataset curation was brutal.** Scraping accurate pricing data for 450+ mice took hours with ScraperAPI, then we manually removed fishy prices and duplicate models. **Balancing hard filters vs. semantic parameters** was tricky—price is a hard constraint, but "lightweight" is semantic. **Groq LLM inconsistency** caused headaches (sometimes skipped questions, sometimes generated weird responses). **Embedding bias** was real—mice with "wireless" in the name would over-match "wireless" preferences, requiring careful text prompt engineering.

## Accomplishments that we're proud of
✨ Built a **fully integrated full-stack AI application** with real-time chat, vector search, and interactive visualizations  
🚀 **Sub-2-second recommendations** from 175 mice using cached embeddings and optimized similarity search  
🎨 **Beautiful, production-ready UX** with live preference tracking, smooth animations, and explainable AI reasoning  
🧠 **Semantic understanding** that matches meaning over keywords (e.g., "lightweight FPS mouse" → actual weight/sensor specs)  
📊 **Dual visualizations** (UMAP scatter + force graph) showing mouse clustering and k-nearest neighbors

## What we learned
- **Vector embeddings are powerful** for product discovery—semantic similarity beats keyword matching every time
- **Data quality > data quantity**—curating 175 good mice beats 1200 noisy entries
- **LLM prompt engineering is an art**—getting consistent JSON output from Groq required careful system prompt design
- **Caching is critical**—precomputing embeddings reduced latency from 30s to 2s
- **Hard constraints + soft matching = best UX**—budget filtering before similarity ranking gives better results than pure vector search

## What's next for periph4all
🎧 **Expand to other peripherals** (keyboards, headsets, monitors) using the same embedding architecture  
🔊 **Voice interface** for hands-free peripheral shopping  
🤝 **Community features**: user reviews, custom preference profiles, comparison tools  
⚡ **Hybrid scoring**: combine semantic embeddings with expert brand quality scores and user ratings  
🎯 **Fine-tuned model**: train a domain-specific embedding model on gaming peripheral descriptions for even better matching  
🌐 **Multi-language support**: help gamers worldwide find their perfect setup

