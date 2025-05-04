import pandas as pd
import os
import re

def clean_text(text):
    if pd.isna(text):
        return ""
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def normalize_laptop_specs(row):
    return {
        "name": clean_text(row["name"]),
        "price_usd": float(row["price_usd"]) if str(row["price_usd"]).replace('.', '', 1).isdigit() else None,
        "CPU": clean_text(row["CPU"]),
        "RAM": clean_text(row["RAM"]),
        "Storage": clean_text(row["Storage"]),
        "GPU": clean_text(row["GPU"]),
    }

def preprocess_csv(input_path="data/laptops.csv", output_path="data/clean_laptops.csv"):
    df = pd.read_csv(input_path)
    cleaned_rows = [normalize_laptop_specs(row) for _, row in df.iterrows()]
    cleaned_df = pd.DataFrame(cleaned_rows)
    cleaned_df.to_csv(output_path, index=False)
    print(f"Saved cleaned data to {output_path}")

if __name__ == "__main__":
    preprocess_csv()
