import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
import os
import pickle

def generate_text_repr(row):
    return f"""
    Laptop Name: {row['name']}
    CPU: {row['CPU']}
    RAM: {row['RAM']}
    Storage: {row['Storage']}
    GPU: {row['GPU']}
    Price (USD): {row['price_usd']}
    """

def embed_and_store(csv_path="data/clean_laptops.csv", index_dir="vector_store/faiss_index"):
    df = pd.read_csv(csv_path)
    model = SentenceTransformer('all-MiniLM-L6-v2')
    texts = [generate_text_repr(row) for _, row in df.iterrows()]
    embeddings = model.encode(texts, show_progress_bar=True)

    dim = embeddings[0].shape[0]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    os.makedirs(index_dir, exist_ok=True)
    faiss.write_index(index, os.path.join(index_dir, "laptop.index"))

    with open(os.path.join(index_dir, "metadata.pkl"), "wb") as f:
        pickle.dump(df.to_dict(orient="records"), f)

    print(f"Saved FAISS index and metadata to {index_dir}")

if __name__ == "__main__":
    embed_and_store()
