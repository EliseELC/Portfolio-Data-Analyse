import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import plotly.express as px
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

st.markdown("""
Les licences sont donc le type de formation le plus demandée, on retrouve ensuite les BTS, les IFSI et les BUT.
""")

st.subheader("Top 10 des formations les plus demandées")

st.code("""
top_formations = (
    df_plot
    .groupby('nom_complet_formation')['effectif_total_candidats']
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

sns.set_theme(style="whitegrid")

palette = sns.color_palette("viridis", len(top_formations)) 

plt.figure(figsize=(15,6))
ax = sns.barplot(x=top_formations.values, y=top_formations.index)

for bar in ax.patches:
    ax.annotate(
        f"{int(bar.get_width())}",
        (bar.get_width(), bar.get_y() + bar.get_height()/2),
        va='center', ha='left', xytext=(5,0), textcoords='offset points'
    )

plt.title("Top 10 des formations les plus demandées")
plt.xlabel("Nombre de candidats")
plt.tight_layout()
plt.show()
""", language="python")

top_formations = (
    df_plot
    .groupby('nom_complet_formation')['effectif_total_candidats']
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

sns.set_theme(style="whitegrid")

palette = sns.color_palette("viridis", len(top_formations)) 

fig, ax = plt.subplots(figsize=(15,6))

sns.barplot(
    x=top_formations.values,
    y=top_formations.index,
    palette=palette,
    ax=ax
)

for bar in ax.patches:
    ax.annotate(
        f"{int(bar.get_width())}",
        (bar.get_width(), bar.get_y() + bar.get_height()/2),
        va='center',
        ha='left',
        xytext=(5,0),
        textcoords='offset points'
    )

ax.set_title("Top 10 des formations les plus demandées")
ax.set_xlabel("Nombre de candidats")

st.pyplot(fig)

st.subheader("Répartition des types de formation par nombre de candidatures")

st.code("""
type_counts = df_plot['type_formation'].value_counts()

colors = sns.color_palette("tab20", len(type_counts))

fig, ax = plt.subplots(figsize=(9,9))

wedges, texts, autotexts = ax.pie(
    type_counts.values,
    labels=None,
    colors=colors,
    startangle=90,
    autopct=lambda p: f"{p:.1f}%" if p >= 2 else "",
    pctdistance=0.7,
    wedgeprops=dict(edgecolor='white', linewidth=1)
)

ax.legend(
    wedges,
    type_counts.index,
    title="Type de formation",
    loc="center left",
    bbox_to_anchor=(1, 0.5)
)

for autotext in autotexts:
    autotext.set_color("white")
    autotext.set_fontsize(10)
    autotext.set_weight("bold")

plt.title("Répartition des types de formation", fontsize=14, weight='bold')
plt.tight_layout()
plt.show()
""", language="python")

type_counts = df_plot['type_formation'].value_counts()

colors = sns.color_palette("tab20", len(type_counts))

fig, ax = plt.subplots(figsize=(9,9))

wedges, texts, autotexts = ax.pie(
    type_counts.values,
    labels=None,
    colors=colors,
    startangle=90,
    autopct=lambda p: f"{p:.1f}%" if p >= 2 else "",
    pctdistance=0.7,
    wedgeprops=dict(edgecolor='white', linewidth=1)
)

ax.legend(
    wedges,
    type_counts.index,
    title="Type de formation",
    loc="center left",
    bbox_to_anchor=(1, 0.5)
)

for autotext in autotexts:
    autotext.set_color("white")
    autotext.set_fontsize(10)
    autotext.set_weight("bold")

ax.set_title("Répartition des types de formation", fontsize=14, weight='bold')

st.pyplot(fig)

st.subheader("Étude de la sélectivité et des taux d'accès des formations")

st.code("""
plt.figure(figsize=(10,6))
sns.boxplot(data=df_plot, x='type_formation', y='taux_d’accès')

plt.xticks(rotation=45, ha='right')
plt.title("Distribution du taux d'accès par type de formation")

plt.tight_layout()
plt.show()
""", language="python")

fig, ax = plt.subplots(figsize=(10,6))

sns.boxplot(
    data=df_plot,
    x='type_formation',
    y='taux_d’accès',
    ax=ax
)

plt.xticks(rotation=45, ha='right')

ax.set_title("Distribution du taux d'accès par type de formation")

st.pyplot(fig)

st.subheader("📊 Capacité vs nombre de candidats")

st.code("""
agg = (
    df_plot
    .groupby('type_formation')
    .agg({
        'capacite_formation': 'sum',
        'effectif_total_candidats': 'sum'
    })
    .reset_index()
)

agg_melt = agg.melt(
    id_vars='type_formation',
    value_vars=['capacite_formation', 'effectif_total_candidats'],
    var_name='variable',
    value_name='valeur'
)

sns.set_theme(style="whitegrid")

plt.figure(figsize=(12,6))

sns.lineplot(
    data=agg_melt,
    x='type_formation',
    y='valeur',
    hue='variable',
    marker='o'
)

for _, row in agg_melt.iterrows():
    plt.text(
        row.name % len(agg),
        row['valeur'],
        f"{int(row['valeur'])}",
        ha='center',
        va='bottom',
        fontsize=8
    )

plt.xticks(rotation=45, ha='right')
plt.title("Capacité vs Candidats par type de formation")
plt.xlabel("Type de formation")
plt.ylabel("Nombre")

plt.tight_layout()
plt.show()
""", language="python")

agg = (
    df_plot
    .groupby('type_formation')
    .agg({
        'capacite_formation': 'sum',
        'effectif_total_candidats': 'sum'
    })
    .reset_index()
)

agg_melt = agg.melt(
    id_vars='type_formation',
    value_vars=['capacite_formation', 'effectif_total_candidats'],
    var_name='variable',
    value_name='valeur'
)

fig, ax = plt.subplots(figsize=(12,6))

sns.lineplot(
    data=agg_melt,
    x='type_formation',
    y='valeur',
    hue='variable',
    marker='o',
    ax=ax
)

for _, row in agg_melt.iterrows():
    ax.text(
        row.name % len(agg),
        row['valeur'],
        f"{int(row['valeur'])}",
        ha='center',
        va='bottom',
        fontsize=8
    )

plt.xticks(rotation=45, ha='right')

ax.set_title("Capacité vs Candidats par type de formation")
ax.set_xlabel("Type de formation")
ax.set_ylabel("Nombre")

st.pyplot(fig)

st.subheader("Corrélation capacité vs nombre de candidats")

st.code("""
plt.figure(figsize=(10,6))

sns.scatterplot(
    data=df_plot,
    x='capacite_formation',
    y='effectif_total_candidats',
    hue='type_formation',
    style='type_formation',
    palette='tab10',
    markers=['o','s','D','^','v','P','X'],
    alpha=0.8,
    s=80
)

plt.xlim(0, 1000)

plt.title("Capacité vs nombre de candidats")
plt.xlabel("Capacité")
plt.ylabel("Candidats")

plt.tight_layout()
plt.show()
""", language="python")

fig, ax = plt.subplots(figsize=(10,6))

sns.scatterplot(
    data=df_plot,
    x='capacite_formation',
    y='effectif_total_candidats',
    hue='type_formation',
    style='type_formation',
    palette='tab10',
    markers=['o','s','D','^','v','P','X'],
    alpha=0.8,
    s=80,
    ax=ax
)

plt.xlim(0, 1000)

ax.set_title("Capacité vs nombre de candidats")
ax.set_xlabel("Capacité")
ax.set_ylabel("Candidats")

st.pyplot(fig)

st.subheader("📌 Demande vs sélectivité des formations")

st.code("""
compare = (
    df_plot
    .groupby('nom_formation')
    .agg({
        'effectif_total_candidats':'sum',
        'taux_d’accès':'mean'
    })
    .dropna()
    .sort_values('effectif_total_candidats', ascending=False)
    .head(10)
)

plt.figure(figsize=(10,6))

sns.scatterplot(
    data=compare,
    x='effectif_total_candidats',
    y='taux_d’accès',
    s=100
)

for i, txt in enumerate(compare.index):
    plt.text(
        compare['effectif_total_candidats'][i],
        compare['taux_d’accès'][i],
        txt,
        fontsize=8
    )

plt.title("Demande vs sélectivité (Top 10 formations)")
plt.xlabel("Nombre de candidats")
plt.ylabel("Taux d'accès (%)")

plt.tight_layout()
plt.show()
""", language="python")

compare = (
    df_plot
    .groupby('nom_formation')
    .agg({
        'effectif_total_candidats':'sum',
        'taux_d’accès':'mean'
    })
    .dropna()
    .sort_values('effectif_total_candidats', ascending=False)
    .head(10)
)

fig = px.scatter(
    compare,
    x='effectif_total_candidats',
    y='taux_d’accès',
    text=compare.index,
    size='effectif_total_candidats',
    color='taux_d’accès',
    color_continuous_scale='Viridis',
    hover_name=compare.index,
    title="Demande vs sélectivité (Top 10 formations)"
)

fig.update_traces(
    textposition='top center',
    hovertemplate=
    "<b>%{hovertext}</b><br>" +
    "Candidats : %{x:,}<br>" +
    "Taux d'accès : %{y:.1f}%<extra></extra>"
)

st.plotly_chart(fig, use_container_width=True)