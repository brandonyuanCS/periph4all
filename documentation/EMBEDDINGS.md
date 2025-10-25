# Data Processing Scripts

This directory contains scripts for processing the mouse dataset and generating embeddings.

## Scripts

### 1. `generate_embeddings.py` 🧠

Generates vector embeddings for all mice in the dataset using SentenceTransformers.

**Usage:**
```bash
# Generate embeddings with default model
python generate_embeddings.py

# Use a specific model
python generate_embeddings.py --model sentence-transformers/all-mpnet-base-v2

# Force regeneration (skip cache check)
python generate_embeddings.py --force

# Custom batch size
python generate_embeddings.py --batch-size 64
```

**What it does:**
1. Loads `FINAL.csv` dataset
2. Converts each mouse to descriptive text (name, specs, shape, etc.)
3. Generates embeddings using SentenceTransformers
4. Saves to `data/cache/`:
   - `mouse_embeddings.npy` - Numpy array of embeddings
   - `mouse_embeddings_meta.json` - Metadata (model, count, dimension)
   - `mouse_texts.json` - Text representations (for debugging)

**Output:**
```
data/cache/
├── mouse_embeddings.npy          # 177 x 384 array (for all-MiniLM-L6-v2)
├── mouse_embeddings_meta.json    # Metadata
└── mouse_texts.json              # Text descriptions
```

---

### 2. `test_embeddings.py` ✅

Tests and validates the generated embeddings.

**Usage:**
```bash
python test_embeddings.py
```

**Tests:**
- ✓ Basic properties (shape, dimensions, NaN check)
- ✓ Similarity search with example queries
- ✓ Mouse-to-mouse similarity
- ✓ Diversity analysis

**Example output:**
```
✓ Shape: (177, 384)
✓ Number of mice: 177
✓ Embedding dimension: 384
✓ Model used: sentence-transformers/all-MiniLM-L6-v2

🔍 Query: 'lightweight wireless mouse for FPS gaming'
Top 3 matches:
  1. Corsair Sabre v2 Pro (Similarity: 0.8234)
  2. Logitech G Pro X Superlight 2c (Similarity: 0.8102)
  3. Pulsar X2 CrazyLight Medium (Similarity: 0.7956)
```

---

### 3. `filter_dataset.py` 📊

(Existing script) Filters and cleans the raw dataset.

---

### 4. `price_scraper_v2.py` 💰

(Existing script) Scrapes mouse prices from various sources.

---

## Workflow

### Initial Setup

1. **Generate embeddings:**
   ```bash
   cd backend/data/scripts
   python generate_embeddings.py
   ```

2. **Test embeddings:**
   ```bash
   python test_embeddings.py
   ```

3. **Start the API:**
   ```bash
   cd ../../
   python run.py
   ```

The API will automatically load cached embeddings on first request!

---

## Embedding Models

### Default Model
- **Name:** `sentence-transformers/all-MiniLM-L6-v2`
- **Dimension:** 384
- **Speed:** Fast (~1-2 seconds for 177 mice)
- **Quality:** Good for general similarity

### Alternative Models

**Higher Quality:**
```bash
# Better semantic understanding, slower
python generate_embeddings.py --model sentence-transformers/all-mpnet-base-v2
# Dimension: 768
```

**Faster:**
```bash
# Smaller, faster, slightly lower quality
python generate_embeddings.py --model sentence-transformers/paraphrase-MiniLM-L3-v2
# Dimension: 384
```

**Domain-Specific:**
```bash
# If you have product-specific training data
python generate_embeddings.py --model sentence-transformers/msmarco-distilbert-base-v4
```

---

## Text Representation

Each mouse is converted to descriptive text like:

```
Mouse: Logitech G Pro X Superlight 2c. Brand: Logitech. 
Weight: 51g (lightweight). Length: 118.4mm. Width: 61.2mm. 
Height: 38.6mm. Shape: Symmetrical. Hand compatibility: Right. 
Hump: Center. Sensor: HERO 2. Sensor type: Optical. 
Max DPI: 44000. Polling rate: 8000Hz. Connection: Wireless. 
Side buttons: 2. Switches: LIGHTFORCE. Material: Plastic. 
Price: $159.99 (premium)
```

This rich semantic representation allows the model to understand:
- Physical properties (weight, dimensions)
- Shape characteristics
- Performance specs
- Price range
- Connectivity

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'sentence_transformers'"
```bash
pip install sentence-transformers
```

### "Dataset not found"
Make sure `backend/data/FINAL.csv` exists

### "Out of memory"
Reduce batch size:
```bash
python generate_embeddings.py --batch-size 16
```

### Regenerate embeddings
```bash
python generate_embeddings.py --force
```

---

## Performance

**Generation time** (on typical laptop):
- All-MiniLM-L6-v2: ~1-2 seconds for 177 mice
- All-mpnet-base-v2: ~3-5 seconds for 177 mice

**Cache size:**
- Embeddings: ~270 KB (for 384-dim)
- Metadata: ~5 KB
- Total: <1 MB

**First API request:**
- Loads from cache: <100ms
- No regeneration needed!

---

## Tips

1. **Regenerate when dataset changes:**
   ```bash
   python generate_embeddings.py --force
   ```

2. **Test different models:**
   Try different models and run `test_embeddings.py` to compare

3. **Version control:**
   Add `data/cache/*.npy` to `.gitignore` (already done)
   Commit the generation script for reproducibility

4. **Production:**
   Pre-generate embeddings before deployment
   No need to generate at runtime!




# Embedding Generation Quick Start

## 🚀 Get Started in 2 Steps

### Step 1: Generate Embeddings

```bash
cd backend/data/scripts
python generate_embeddings.py
```

**First time:** Downloads the model (~80MB) and generates embeddings (~1-2 seconds)  
**Next times:** Loads from cache instantly!

---

### Step 2: Test Your Embeddings

```bash
python test_embeddings.py
```

This will verify everything works and show you example similarity searches.

---

## 📋 Quick Commands

### Preview Text Representations
See how mice are converted to text:
```bash
python preview_texts.py --count 3
```

Search for specific mouse:
```bash
python preview_texts.py --search "Logitech"
```

---

### Force Regeneration
If you update FINAL.csv:
```bash
python generate_embeddings.py --force
```

---

### Try Different Models

**Faster (smaller):**
```bash
python generate_embeddings.py --model sentence-transformers/paraphrase-MiniLM-L3-v2
```

**Higher quality (larger):**
```bash
python generate_embeddings.py --model sentence-transformers/all-mpnet-base-v2
```

---

## 📂 What Gets Created

After running `generate_embeddings.py`:

```
backend/data/cache/
├── mouse_embeddings.npy       # Vector embeddings (177 x 384)
├── mouse_embeddings_meta.json # Metadata (model, count, etc.)
└── mouse_texts.json          # Text descriptions (for reference)
```

---

## ✅ Verification

After generating embeddings, you should see:

```
✅ Embedding generation complete!
==========================================
Generated 177 embeddings
Embedding dimension: 384
Model used: sentence-transformers/all-MiniLM-L6-v2
```

Test with:
```bash
python test_embeddings.py
```

Expected output:
```
✓ Shape: (177, 384)
✓ No NaN values
✓ No Inf values
✓ Good diversity in embeddings

🔍 Query: 'lightweight wireless mouse for FPS gaming'
Top 3 matches:
  1. Corsair Sabre v2 Pro (Similarity: 0.82xx)
  2. Logitech G Pro X Superlight 2c (Similarity: 0.81xx)
  ...
```

---

## 🔧 Troubleshooting

**"ModuleNotFoundError"**
```bash
pip install sentence-transformers
```

**"Dataset not found"**
Make sure you're in `backend/data/scripts/` and `FINAL.csv` exists in `backend/data/`

**Out of memory**
```bash
python generate_embeddings.py --batch-size 16
```

---

## 🎯 Next Steps

Once embeddings are generated:

1. Start the FastAPI server:
   ```bash
   cd ../../
   python run.py
   ```

2. Test the recommendation API:
   - Visit http://localhost:8000/docs
   - Try the `/api/v1/recommendations/quick` endpoint

3. Integrate with your Next.js frontend!

---

That's it! 🎉 Your embeddings are ready to power the recommendation system.

