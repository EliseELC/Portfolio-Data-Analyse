import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px



@st.cache_data
def load_data():
    df = pd.read_csv(
        r"data\sales_data.csv",
        sep=";",
        encoding="utf-8",
        engine="python",
        on_bad_lines="skip"
    )
    return df

df = load_data()

st.set_page_config(
    page_title="Analyse des ventes 2023-2024",
    layout="wide"
)
st.title("Analyse des ventes 2023-2024")
