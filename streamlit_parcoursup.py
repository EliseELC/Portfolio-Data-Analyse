import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Analyse Parcoursup",
    layout="wide"
)

@st.cache_data
def load_data():
    chemin = r"\\frfs.sedes.inditex.grp\Rhome$\eliselc.SEDES\Mis Documentos\GitHub\Portfolio-Data-Analyse\fr-esr-parcoursup.csv"

    df = pd.read_csv(
        chemin,
        sep=";",
        encoding="utf-8",
        engine="python",
        on_bad_lines="skip"
    )

    return df

df = load_data()

st.title("Analyse des données de candidature Parcoursup (session 2025)")
st.markdown("""
Bienvenue dans cette analyse exploratoire des données Parcoursup.  
Cette application permet d'étudier les formations, les profils des admis et les dynamiques de sélection.
""")
st.header("Première étape: Nettoyage")
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
    .str.replace("'", "")
    .str.replace("é", "e")
)

st.subheader("Renommage des colonnes")
st.code("""#Uniformiser le nom des colonnes
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
    .str.replace("'", "")
    .str.replace("é", "e")
)
""", language="python")

st.subheader("🔤 Renommage des colonnes")

st.code("""
# Changer le nom des colonnes trop longues
df.rename(columns={
    'code_uai_de_letablissement': 'code_uai',
    'statut_de_l’etablissement_de_la_filière_de_formation_(public,_prive…)': 'statut_etablissment',
    'code_departemental_de_l’etablissement': 'code_departemental',
    'departement_de_l’etablissement': 'departement',
    'region_de_l’etablissement': 'region',
    'academie_de_l’etablissement': 'academie',
    'commune_de_l’etablissement': 'commune',
    'filière_de_formation_detaillee': 'nom_complet_formation',
    'filière_de_formation_très_agregee': 'type_formation',
    'filière_de_formation.1': 'nom_formation',
    'filière_de_formation_detaillee_bis': 'nom_formation_bis',
    'filière_de_formation_très_detaillee': 'nom_formation_detaille',
    'coordonnees_gps_de_la_formation': 'coordonnes_gps',
    'capacite_de_l’etablissement_par_formation': 'capacite_formation',
    'effectif_total_des_candidats_pour_une_formation': 'effectif_total_candidats',
    'dont_effectif_des_candidates_pour_une_formation': 'nombre_candidates'
}, inplace=True)
""", language="python")

df.rename(columns={
    'code_uai_de_letablissement': 'code_uai',
    'statut_de_l’etablissement_de_la_filière_de_formation_(public,_prive…)': 'statut_etablissment',
    'code_departemental_de_l’etablissement': 'code_departemental',
    'departement_de_l’etablissement': 'departement',
    'region_de_l’etablissement': 'region',
    'academie_de_l’etablissement': 'academie',
    'commune_de_l’etablissement': 'commune',
    'filière_de_formation_detaillee': 'nom_complet_formation',
    'filière_de_formation_très_agregee': 'type_formation',
    'filière_de_formation.1': 'nom_formation',
    'filière_de_formation_detaillee_bis': 'nom_formation_bis',
    'filière_de_formation_très_detaillee': 'nom_formation_detaille',
    'coordonnees_gps_de_la_formation': 'coordonnes_gps',
    'capacite_de_l’etablissement_par_formation': 'capacite_formation',
    'effectif_total_des_candidats_pour_une_formation': 'effectif_total_candidats',
    'dont_effectif_des_candidates_pour_une_formation': 'nombre_candidates'
}, inplace=True)

df_plot = df.copy()

ancien_nouveaux = pd.DataFrame({
    "Ancien nom": [
        'code_uai_de_letablissement',
        'statut_de_l’etablissement_de_la_filière_de_formation_(public,_prive…)',
        'code_departemental_de_l’etablissement',
        'departement_de_l’etablissement',
        'region_de_l’etablissement',
        'academie_de_l’etablissement',
        'commune_de_l’etablissement',
        'filière_de_formation_detaillee',
        'filière_de_formation_très_agregee',
        'filière_de_formation.1',
        'filière_de_formation_detaillee_bis',
        'filière_de_formation_très_detaillee',
        'coordonnees_gps_de_la_formation',
        'capacite_de_l’etablissement_par_formation',
        'effectif_total_des_candidats_pour_une_formation',
        'dont_effectif_des_candidates_pour_une_formation'
    ],
    "Nouveau nom": [
        'code_uai',
        'statut_etablissment',
        'code_departemental',
        'departement',
        'region',
        'academie',
        'commune',
        'nom_complet_formation',
        'type_formation',
        'nom_formation',
        'nom_formation_bis',
        'nom_formation_detaille',
        'coordonnes_gps',
        'capacite_formation',
        'effectif_total_candidats',
        'nombre_candidates'
    ]
})

st.dataframe(ancien_nouveaux, use_container_width=True)

st.subheader("🔎 Exploration des données")

st.code("""
print(df.head())
print(df.columns.tolist())
print(df.info())

df.dtypes
""", language="python")

st.dataframe(df.head())

st.subheader("Exploration")

st.code("""#Création d'une copie du df
df_plot = df.copy()

df_plot['taux_d’accès'] = pd.to_numeric(
    df_plot['taux_d’accès'], errors='coerce'
)

df_plot['capacite_formation'] = pd.to_numeric(
    df_plot['capacite_formation'], errors='coerce'
)

df_plot['effectif_total_candidats'] = pd.to_numeric(
    df_plot['effectif_total_candidats'], errors='coerce'
)
""", language="python")

df_plot['taux_d’accès'] = pd.to_numeric(
    df_plot['taux_d’accès'], errors='coerce'
)

df_plot['capacite_formation'] = pd.to_numeric(
    df_plot['capacite_formation'], errors='coerce'
)

df_plot['effectif_total_candidats'] = pd.to_numeric(
    df_plot['effectif_total_candidats'], errors='coerce'
)

st.subheader("Calcul du nombre total de candidats")

st.code("""
total_candidats = df_plot['effectif_total_candidats'].sum()

total_candidats
""", language="python")

total_candidats = df_plot['effectif_total_candidats'].sum()

st.metric(
    "Nombre total de candidats",
    f"{int(total_candidats):,}".replace(",", " ")
)

st.markdown("""
Il y a donc eu 13 502 385 candidatures pour les formations.  
Un candidat a la possibilité de faire au moins 10 voeux et 10 de plus pour des formations spécifiques (BTS, BUT...).  
Selon le site de l'enseignement supérieur en 2025 près de 980 000 candidats avaient confirmé au moins un voeu.
""")

st.subheader("🏫 Calcul du nombre total de formations")

st.code("""
total_formations = len(df_plot)

total_formations
""", language="python")

total_formations = len(df_plot)

st.metric(
    "Nombre total de formations",
    f"{int(total_formations):,}".replace(",", " ")
)

st.header("Deuxième étape : Visualisations")

st.subheader("1.Formations les plus demandées")

st.code("""
top_formations = (
    df_plot.groupby('type_formation')['effectif_total_candidats']
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

sns.set_theme(style="whitegrid")

palette = sns.color_palette("viridis", len(top_formations))

plt.figure(figsize=(11,6))
ax = sns.barplot(x=top_formations.values, y=top_formations.index, palette=palette)

max_val = top_formations.values.max()
plt.xlim(0, max_val * 1.15)

for bar in ax.patches:
    width = bar.get_width()
    ax.annotate(
        f"{int(width):,}".replace(",", " "),
        (width, bar.get_y() + bar.get_height()/2),
        va='center',
        ha='left',
        xytext=(8, 0),
        textcoords='offset points',
        fontsize=9,
        fontweight='bold'
    )

ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

plt.title("Top 10 du type de formation les plus demandées", fontsize=14, weight='bold')
plt.xlabel("Nombre de candidats")
plt.ylabel("")
plt.tight_layout()
plt.show()
""", language="python")

top_formations = (
    df_plot.groupby('type_formation')['effectif_total_candidats']
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

sns.set_theme(style="whitegrid")

palette = sns.color_palette("viridis", len(top_formations))

fig, ax = plt.subplots(figsize=(11,6))

sns.barplot(
    x=top_formations.values,
    y=top_formations.index,
    palette=palette,
    ax=ax
)

max_val = top_formations.values.max()
plt.xlim(0, max_val * 1.15)

for bar in ax.patches:
    width = bar.get_width()
    ax.annotate(
        f"{int(width):,}".replace(",", " "),
        (width, bar.get_y() + bar.get_height()/2),
        va='center',
        ha='left',
        xytext=(8, 0),
        textcoords='offset points',
        fontsize=9,
        fontweight='bold'
    )

ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

ax.set_title(
    "Top 10 du type de formation les plus demandées",
    fontsize=14,
    weight='bold'
)

ax.set_xlabel("Nombre de candidats")
ax.set_ylabel("")

st.pyplot(fig)
