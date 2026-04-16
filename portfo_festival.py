# Importation des librairies
import streamlit as st
import pandas as pd
import altair as alt

# Configuration de la page
st.set_page_config(page_title="Festivals en France", layout="wide")

# Chargement des données
DATA_PATH = r"\\frfs.sedes.inditex.grp\Rhome$\eliselc.SEDES\Mis Documentos\dataset-festival.csv"
df = pd.read_csv(DATA_PATH, sep=";", engine="python", on_bad_lines="skip")

# Vérification des données
st.write(df.head())
st.write(df.columns)

# Nettoyage des données
df = df.dropna()

# Définition des colonnes (à adapter selon ton dataset)
X_COL = df.columns[0]
Y_COL = df.columns[1]
COLOR_COL = df.columns[2]

# Création du graphique principal
chart = alt.Chart(df).mark_point(size=100, filled=True).encode(
    x=alt.X(X_COL),
    y=alt.Y(Y_COL, sort="-x"),
    color=alt.Color(COLOR_COL),
    tooltip=list(df.columns)
).properties(
    width=900,
    height=500
)

# Ajout d'une ligne verticale (moyenne)
mean_value = df[X_COL].mean()

rule = alt.Chart(pd.DataFrame({X_COL: [mean_value]})).mark_rule(color='red').encode(
    x=X_COL
)

# Affichage du graphique
st.altair_chart(chart + rule, use_container_width=True)

# Lancer streamlit 
streamlit run portfo-festival.py


