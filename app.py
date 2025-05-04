import streamlit as st
from src.rag_pipeline import rag_pipeline

# Set up Streamlit UI
st.title("AI-Powered Product Recommender")

# Input fields for user preferences
query = st.text_input("Enter your product preferences", "Best laptop for machine learning under $1500 with good battery")
task = st.text_input("What task will you be using the laptop for?", "machine learning")
budget = st.number_input("Enter your budget", min_value=100, max_value=5000, value=1500)

if st.button("Get Recommendations"):
    if query and task:
        # Get recommendation summary from RAG pipeline
        summary = rag_pipeline(query, task, budget)
        st.subheader("Top Laptop Recommendations")
        st.write(summary)
    else:
        st.error("Please enter a valid query and task.")
