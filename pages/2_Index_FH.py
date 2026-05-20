import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(
    page_title="Index égalité pro",
    layout="wide"
)

st.title("Index Egalité professionnelle (2018- 2025)")


@st.cache_data
def load_data():
    df = pd.read_excel(
        r"data\index-egalite-fh.xlsx"
    )
    return df

df = load_data()

st.dataframe(df.head())



PASTEL_SCALE = [
    [0.0, "#FADADD"],
    [0.2, "#F8C8DC"],
    [0.4, "#CDB4DB"],
    [0.6, "#A2D2FF"],
    [0.8, "#BDE0FE"],
    [1.0, "#CFFFE5"]
]

PASTEL_COLORS = [
    "#A2D2FF",
    "#F8C8DC",
    "#CDB4DB",
    "#FFD6A5",
    "#BDE0FE",
    "#CFFFE5",
    "#FADADD",
    "#FDFFB6",
    "#CAFFBF",
    "#FFC6FF"
]



df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
    .str.replace("'", "")
    .str.replace("é", "e")
)