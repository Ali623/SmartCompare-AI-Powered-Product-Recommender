import faiss
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("❌ OPENAI_API_KEY not found in .env")

# New client-based API usage
client = OpenAI(api_key=api_key)

# Load FAISS index and metadata
def load_index_and_metadata(index_dir="vector_store/faiss_index"):
    index = faiss.read_index(os.path.join(index_dir, "laptop.index"))
    with open(os.path.join(index_dir, "metadata.pkl"), "rb") as f:
        metadata = pickle.load(f)
    return index, metadata

# Generate query embedding
def embed_query(query, model):
    return model.encode([query])[0]

# Retrieve top-N similar products from FAISS index
def retrieve_top_n(query, index, metadata, n=3):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    query_embedding = embed_query(query, model)
    distances, indices = index.search(np.array([query_embedding]), n)
    results = [metadata[idx] for idx in indices[0]]
    return results

# Generate GPT summary
def generate_summary(products, task, budget):
    product_info = "\n".join([f"Laptop: {p['name']}, Price: ${p['price_usd']}, CPU: {p['CPU']}, GPU: {p['GPU']}" for p in products])
    
    prompt = f"""
    Given the following product specs for laptops under ${budget} for {task}, suggest the top 3 laptops and explain why:

    {product_info}
    """

    response = client.chat.completions.create(
        model="gpt-4-turbo",  # or "gpt-3.5-turbo"
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    return response.choices[0].message.content

# Main function to run RAG pipeline
def rag_pipeline(query, task, budget, index_dir="vector_store/faiss_index"):
    # Load index and metadata
    index, metadata = load_index_and_metadata(index_dir)

    # Retrieve top-N similar products
    top_n_products = retrieve_top_n(query, index, metadata)

    # Generate a summary using GPT
    summary = generate_summary(top_n_products, task, budget)
    
    return summary

if __name__ == "__main__":
    # Example query
    query = "Best laptop for machine learning under $1500 with good battery"
    task = "machine learning"
    budget = 1500
    
    summary = rag_pipeline(query, task, budget)
    print("Summary of top laptops:", summary)
