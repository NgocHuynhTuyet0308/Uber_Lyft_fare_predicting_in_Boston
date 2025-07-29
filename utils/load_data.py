import streamlit as st
import pandas as pd

@st.cache_data
def load_csv(csv_path):
    df = pd.read_csv(csv_path)
    return df