# SmartCompare - AI-Powered Product Recommender

SmartCompare is an intermediate-level Retrieval-Augmented Generation (RAG) project that allows users to find the best laptops for specific tasks and budgets by combining web scraping, semantic search (using FAISS), and OpenAI's GPT model for explanation.

---

## Features

- Scrapes laptop data from e-commerce websites.
- Extracts and stores product features such as name, price, CPU, GPU, and RAM.
- Uses `sentence-transformers` to create embeddings.
- Stores embeddings using FAISS for efficient similarity search.
- Retrieves top-N relevant laptops based on user query.
- Uses OpenAI's GPT (e.g., `text-davinci-003`) to generate a summary and comparison.


---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/SmartCompare-AI-Powered-Product-Recommender.git
cd SmartCompare-AI-Powered-Product-Recommender
```

### 2. Create a Virtual Environment (Recommended)

```bash
python -m venv .venv
.venv\Scripts\activate   # For Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up OpenAI API Key

Create a .env file in the project root:

```bash
OPENAI_API_KEY=your_openai_key_here
```

## Usage

### 1. Scrape Laptop Data

```bash
python src/data_collection.py
```

### 2. Create Embeddings and Index

```bash
python src/embed_and_index.py
```

### 3. Run the RAG Pipeline

```bash
python src/rag_pipeline.py
```

You can modify the query inside rag_pipeline.py or use this logic in a separate UI/backend integration.

### Example Query

```python
query = "Best laptop for machine learning under $1500 with good battery life"
task = "machine learning"
budget = 1500
```

### Output

```bash
Summary of top laptops:
- Laptop A: Best for performance and RAM
- Laptop B: Efficient GPU for ML tasks
- Laptop C: Longest battery life with decent specs
```

### License

MIT License - feel free to use and modify.

### Acknowledgements

- OpenAI API
- FAISS by Facebook
- Sentence-Transformers