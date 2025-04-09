import pandas as pd
import streamlit as st

def load_csv(uploaded_file):
    if uploaded_file is None:
        st.warning("No file uploaded yet.")
        return None
    try:
        df = pd.read_csv(uploaded_file)
        st.success("✅ File successfully loaded!")
        return df
    except Exception as e:
        st.error(f"❌ Failed to read file: {e}")
        return None
