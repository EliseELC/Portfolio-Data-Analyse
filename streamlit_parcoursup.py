import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(
    page_title="Analyse Parcoursup",
    layout="wide"
)

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

@st.cache_data
def load_data():
    df = pd.read_csv(
        "fr-esr-parcoursup.csv",
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

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
    .str.replace("'", "")
    .str.replace("é", "e")
)

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

df_plot['taux_d’accès'] = pd.to_numeric(
    df_plot['taux_d’accès'],
    errors='coerce'
)

df_plot['capacite_formation'] = pd.to_numeric(
    df_plot['capacite_formation'],
    errors='coerce'
)

df_plot['effectif_total_candidats'] = pd.to_numeric(
    df_plot['effectif_total_candidats'],
    errors='coerce'
)

st.header("Chiffres clés")

total_candidats = df_plot['effectif_total_candidats'].sum()

st.metric(
    "Nombre total de candidats",
    f"{int(total_candidats):,}".replace(",", " ")
)

total_formations = len(df_plot)

st.metric(
    "Nombre total de formations",
    f"{int(total_formations):,}".replace(",", " ")
)

st.header("Visualisations")

# =========================
# TYPES DE FORMATIONS
# =========================

st.subheader("Types de formations les plus demandés")

top_formations = (
    df_plot.groupby('type_formation')['effectif_total_candidats']
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

fig = px.bar(
    x=top_formations.values,
    y=top_formations.index,
    orientation='h',
    color=top_formations.values,
    text=top_formations.values,
    color_continuous_scale=PASTEL_SCALE
)

fig.update_traces(
    texttemplate='%{text:,}',
    textposition='outside'
)

fig.update_layout(
    title="Top 10 des types de formation",
    yaxis={'categoryorder':'total ascending'}
)

st.plotly_chart(
    fig,
    use_container_width=True,
    key="top_types_formations"
)

# =========================
# TOP FORMATIONS
# =========================

st.subheader("Top 10 des formations les plus demandées")

top_formations = (
    df_plot
    .groupby('nom_complet_formation')['effectif_total_candidats']
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

fig = px.bar(
    x=top_formations.values,
    y=top_formations.index,
    orientation='h',
    color=top_formations.values,
    text=top_formations.values,
    color_continuous_scale=PASTEL_SCALE
)

fig.update_traces(
    texttemplate='%{text:,}',
    textposition='outside'
)

fig.update_layout(
    title="Top 10 des formations les plus demandées",
    yaxis={'categoryorder':'total ascending'}
)

st.plotly_chart(
    fig,
    use_container_width=True,
    key="top_formations"
)

# =========================
# PIE CHART
# =========================

st.subheader("Répartition des types de formation")

type_counts = df_plot['type_formation'].value_counts()

fig = px.pie(
    values=type_counts.values,
    names=type_counts.index,
    hole=0.4,
    color_discrete_sequence=PASTEL_COLORS
)

fig.update_traces(
    textinfo='percent+label'
)

st.plotly_chart(
    fig,
    use_container_width=True,
    key="pie_types"
)

# =========================
# BOXPLOT
# =========================

st.subheader("Distribution du taux d'accès")

fig = px.box(
    df_plot,
    x='type_formation',
    y='taux_d’accès',
    color='type_formation',
    color_discrete_sequence=PASTEL_COLORS
)

fig.update_layout(
    xaxis_tickangle=-45,
    showlegend=False
)

st.plotly_chart(
    fig,
    use_container_width=True,
    key="boxplot"
)

# =========================
# LINEPLOT
# =========================

st.subheader("Capacité vs nombre de candidats")

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

fig = px.line(
    agg_melt,
    x='type_formation',
    y='valeur',
    color='variable',
    markers=True,
    color_discrete_sequence=PASTEL_COLORS
)

fig.update_layout(
    xaxis_tickangle=-45
)

st.plotly_chart(
    fig,
    use_container_width=True,
    key="capacite_vs_candidats"
)

# =========================
# SCATTER
# =========================

st.subheader("Corrélation capacité vs candidats")

fig = px.scatter(
    df_plot,
    x='capacite_formation',
    y='effectif_total_candidats',
    color='type_formation',
    symbol='type_formation',
    hover_data=[
        'nom_complet_formation',
        'academie',
        'region'
    ],
    color_discrete_sequence=PASTEL_COLORS
)

fig.update_layout(
    xaxis_range=[0,1000]
)

st.plotly_chart(
    fig,
    use_container_width=True,
    key="scatter_capacite"
)

# =========================
# DEMANDE VS SELECTIVITE
# =========================

st.subheader("Demande vs sélectivité")

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
    color_continuous_scale=PASTEL_SCALE
)

fig.update_traces(
    textposition='top center'
)

st.plotly_chart(
    fig,
    use_container_width=True,
    key="demande_selectivite"
)

# =========================
# FILIERES
# =========================

st.subheader("Filières avec le plus de candidats")

df_plot['nom_formation_bis'] = (
    df_plot['nom_formation_bis']
    .astype(str)
    .str.strip()
)

top_candidats = (
    df_plot
    .groupby('nom_formation_bis')['effectif_total_candidats']
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

fig = px.bar(
    x=top_candidats.values,
    y=top_candidats.index,
    orientation='h',
    color=top_candidats.values,
    text=top_candidats.values,
    color_continuous_scale=PASTEL_SCALE
)

fig.update_traces(
    texttemplate='%{text:,}',
    textposition='outside'
)

st.plotly_chart(
    fig,
    use_container_width=True,
    key="filieres"
)

# =========================
# OUTLIERS
# =========================

st.subheader("Formations avec moins de candidats que de capacité")

df_out = df.copy()

df_out['capacite_formation'] = pd.to_numeric(
    df_out['capacite_formation'],
    errors='coerce'
)

df_out['effectif_total_candidats'] = pd.to_numeric(
    df_out['effectif_total_candidats'],
    errors='coerce'
)

outliers = df_out[
    (df_out['effectif_total_candidats'] < df_out['capacite_formation'])
]

st.dataframe(
    outliers[[
        'filière_de_formation',
        'region',
        'etablissement',
        'capacite_formation',
        'effectif_total_candidats'
        
    ]],
    use_container_width=True
)

fig = px.scatter(
    outliers,
    x='capacite_formation',
    y='effectif_total_candidats',
    color='type_formation',
    hover_data=[
        'nom_formation_detaille',
        'region',
        'etablissement'
    ],
    color_discrete_sequence=PASTEL_COLORS
)

st.plotly_chart(
    fig,
    use_container_width=True,
    key="outliers"
)

# =========================
# REGIONS
# =========================

st.subheader("Régions avec le plus de formations")

top_regions = df_plot['region'].value_counts().head(10)

fig = px.bar(
    x=top_regions.values,
    y=top_regions.index,
    orientation='h',
    color=top_regions.values,
    text=top_regions.values,
    color_continuous_scale=PASTEL_SCALE
)

fig.update_traces(
    texttemplate='%{text:,}',
    textposition='outside'
)

fig.update_layout(
    yaxis={'categoryorder':'total ascending'}
)

st.plotly_chart(
    fig,
    use_container_width=True,
    key="regions"
)

# =========================
# HEATMAP
# =========================

st.subheader("Répartition des formations par région et type")

pivot = pd.crosstab(
    df_plot['region'],
    df_plot['type_formation']
)

fig = px.imshow(
    pivot,
    text_auto=True,
    aspect="auto",
    color_continuous_scale=PASTEL_SCALE
)
fig.update_layout(
    title="Heatmap nombre de formations par région",
    xaxis_tickangle=-45
)

st.plotly_chart(
    fig,
    use_container_width=True,
    key="heatmap"
)

st.markdown("""
L'Île-de-France est presque systématiquement la région qui possède le plus de formations  
(sauf pour les PASS).
""")

st.subheader("Comparaison des admis selon l'origine académique")

cols = [
    'dont_effectif_des_admis_issus_de_la_même_academie_(paris/creteil/versailles_reunies)',
    'dont_effectif_des_admis_issus_de_la_même_academie'
]

df_plot[cols] = df_plot[cols].apply(
    pd.to_numeric,
    errors='coerce'
)

df_plot = df_plot.dropna(subset=cols)

totaux = df_plot[cols].sum()

labels = [
    "Paris / Créteil / Versailles",
    "Même académie"
]

fig = px.bar(
    x=labels,
    y=totaux.values,
    color=labels,
    text=totaux.values,
    color_discrete_sequence=PASTEL_COLORS
)

fig.update_traces(
    texttemplate='%{text:,}',
    textposition='outside'
)

fig.update_layout(
    title="Comparaison des admis selon l'origine académique",
    showlegend=False
)

st.plotly_chart(
    fig,
    use_container_width=True,
    key="origine_academique"
)

# =========================
# PCV VS AUTRES
# =========================

st.subheader("Admis PCV vs autres académies")

df_plot = df.copy()

df_plot['academie'] = (
    df_plot['academie']
    .astype(str)
    .str.strip()
    .str.lower()
)

df_plot = df_plot[
    df_plot['academie'].isin(['paris', 'creteil', 'versailles'])
]

cols = [
    'dont_effectif_des_admis_issus_de_la_même_academie_(paris/creteil/versailles_reunies)',
    'effectif_des_admis_en_phase_principale',
    'effectif_des_admis_en_phase_complementaire'
]

df_plot[cols] = df_plot[cols].apply(
    pd.to_numeric,
    errors='coerce'
)

df_plot['total_admis'] = (
    df_plot['effectif_des_admis_en_phase_principale'].fillna(0) +
    df_plot['effectif_des_admis_en_phase_complementaire'].fillna(0)
)

df_plot['admis_pcv'] = (
    df_plot['dont_effectif_des_admis_issus_de_la_même_academie_(paris/creteil/versailles_reunies)']
    .fillna(0)
)

df_plot['admis_autres'] = (
    df_plot['total_admis'] - df_plot['admis_pcv']
)

agg = (
    df_plot
    .groupby('type_formation')[['admis_pcv', 'admis_autres']]
    .sum()
    .reset_index()
)

agg_melt = agg.melt(
    id_vars='type_formation',
    value_vars=['admis_pcv', 'admis_autres'],
    var_name='origine',
    value_name='nb_admis'
)

fig = px.line(
    agg_melt,
    x='type_formation',
    y='nb_admis',
    color='origine',
    markers=True,
    color_discrete_sequence=PASTEL_COLORS
)

fig.update_layout(
    title="Admis PCV vs autres (formations Paris / Créteil / Versailles)",
    xaxis_tickangle=-45
)

st.plotly_chart(
    fig,
    use_container_width=True,
    key="pcv_vs_autres"
)

st.markdown("""
On remarque que pour les formations dans les académies de Créteil, Paris et Versailles la majorité des formations ont admis plus de candidats étant néobacheliers dans ces académies sauf pour les autres formations, les IFSI et les EFTS.

On remarque également que le nombre d'admis dans les licences est quasiment identique pour tous les néobacheliers admis.
""")

# =========================
# PCV GLOBAL
# =========================

st.subheader("Admis PCV vs autres (toutes formations)")

df_plot = df.copy()

cols = [
    'dont_effectif_des_admis_issus_de_la_même_academie_(paris/creteil/versailles_reunies)',
    'effectif_des_admis_en_phase_principale',
    'effectif_des_admis_en_phase_complementaire'
]

df_plot[cols] = df_plot[cols].apply(
    pd.to_numeric,
    errors='coerce'
)

df_plot['total_admis'] = (
    df_plot['effectif_des_admis_en_phase_principale'].fillna(0) +
    df_plot['effectif_des_admis_en_phase_complementaire'].fillna(0)
)

df_plot['admis_pcv'] = (
    df_plot['dont_effectif_des_admis_issus_de_la_même_academie_(paris/creteil/versailles_reunies)']
    .fillna(0)
)

df_plot['admis_autres'] = (
    df_plot['total_admis'] - df_plot['admis_pcv']
)

agg = (
    df_plot
    .groupby('type_formation')[['admis_pcv', 'admis_autres']]
    .sum()
    .reset_index()
)

agg_melt = agg.melt(
    id_vars='type_formation',
    value_vars=['admis_pcv', 'admis_autres'],
    var_name='origine',
    value_name='nb_admis'
)

fig = px.line(
    agg_melt,
    x='type_formation',
    y='nb_admis',
    color='origine',
    markers=True,
    color_discrete_sequence=PASTEL_COLORS
)

fig.update_layout(
    title="Admis PCV vs autres (toutes formations)",
    xaxis_tickangle=-45
)

st.plotly_chart(
    fig,
    use_container_width=True,
    key="pcv_vs_autres_all"
)

st.markdown("""
Quand on regarde pour toutes les formations indépendamment de la région on voit que les élèves issus des académies d'Île-de-France sont quand même avantagés par rapport aux autres dans la majorité des formations.

Les formations avec le plus d'égalité dans les admissions sont les écoles d'ingénieur, écoles de commerce, IFSI, EFTS et Licences.
""")

# =========================
# SELECTIVITE
# =========================

st.subheader("Répartition de la sélectivité selon le type de formation")

df_plot = df.copy()

df_plot['type_formation'] = (
    df_plot['type_formation']
    .astype(str)
    .str.strip()
)

df_plot['selectivite'] = (
    df_plot['selectivite']
    .astype(str)
    .str.strip()
    .str.lower()
)

table = (
    pd.crosstab(
        df_plot['type_formation'],
        df_plot['selectivite'],
        normalize='index'
    ) * 100
)

table = table.sort_index().reset_index()

table_melt = table.melt(
    id_vars='type_formation',
    var_name='selectivite',
    value_name='pourcentage'
)

fig = px.bar(
    table_melt,
    x='type_formation',
    y='pourcentage',
    color='selectivite',
    text='pourcentage',
    barmode='stack',
    color_discrete_sequence=PASTEL_COLORS
)

fig.update_traces(
    texttemplate='%{text:.1f}%',
    textposition='inside'
)

fig.update_layout(
    title="Répartition de la sélectivité selon le type de formation",
    xaxis_tickangle=-45
)

st.plotly_chart(
    fig,
    use_container_width=True,
    key="selectivite_types"
)

# =========================
# TYPES DE BAC
# =========================

st.subheader("Répartition des admis par type de bac")

df_plot = df.copy()

cols = [
    'effectif_des_admis_neo_bacheliers_generaux',
    'effectif_des_admis_neo_bacheliers_technologiques',
    'effectif_des_admis_neo_bacheliers_professionnels',
    'effectif_des_admis_neo_bacheliers'
]

df_plot[cols] = df_plot[cols].apply(
    pd.to_numeric,
    errors='coerce'
)

df_plot = df_plot.dropna(subset=cols)

df_plot['generaux'] = (
    df_plot['effectif_des_admis_neo_bacheliers_generaux'] /
    df_plot['effectif_des_admis_neo_bacheliers']
) * 100

df_plot['technologique'] = (
    df_plot['effectif_des_admis_neo_bacheliers_technologiques'] /
    df_plot['effectif_des_admis_neo_bacheliers']
) * 100

df_plot['professionnel'] = (
    df_plot['effectif_des_admis_neo_bacheliers_professionnels'] /
    df_plot['effectif_des_admis_neo_bacheliers']
) * 100

agg = (
    df_plot
    .groupby('type_formation')[[
        'generaux',
        'technologique',
        'professionnel'
    ]]
    .mean()
    .reset_index()
)

agg_melt = agg.melt(
    id_vars='type_formation',
    var_name='type_bac',
    value_name='pourcentage'
)

fig = px.bar(
    agg_melt,
    x='type_formation',
    y='pourcentage',
    color='type_bac',
    text='pourcentage',
    barmode='stack',
    color_discrete_sequence=PASTEL_COLORS
)

fig.update_traces(
    texttemplate='%{text:.1f}%',
    textposition='inside'
)

fig.update_layout(
    title="Répartition des admis par type de bac selon la formation",
    xaxis_tickangle=-45
)

st.plotly_chart(
    fig,
    use_container_width=True,
    key="bac_repartition"
)

# =========================
# GENRE
# =========================

st.header("Analyse des candidatures par genre")

df_plot = df.copy()

cols = [
    'effectif_total_candidats',
    'nombre_candidates'
]

df_plot[cols] = df_plot[cols].apply(
    pd.to_numeric,
    errors='coerce'
)

df_plot['candidates'] = (
    df_plot['nombre_candidates']
    .fillna(0)
)

df_plot['candidats_hommes'] = (
    df_plot['effectif_total_candidats'] -
    df_plot['candidates']
)

agg = pd.DataFrame({
    'genre': ['Femmes', 'Hommes'],
    'nb_candidats': [
        df_plot['candidates'].sum(),
        df_plot['candidats_hommes'].sum()
    ]
})

fig = px.bar(
    agg,
    x='genre',
    y='nb_candidats',
    color='genre',
    text='nb_candidats',
    color_discrete_sequence=PASTEL_COLORS
)

fig.update_traces(
    texttemplate='%{text:,}',
    textposition='outside'
)

fig.update_layout(
    title="Nombre de candidats : Hommes VS Femmes",
    showlegend=False
)

st.plotly_chart(
    fig,
    use_container_width=True,
    key="genre_candidats"
)

st.markdown("""
On remarque une grosse différence du nombre de candidats entre les femmes et les hommes.

Pour environ 7 millions de femmes candidates sur Parcoursup, il y a seulement 5 millions d'hommes.

Nous pouvons théoriser que les hommes, s'ils poursuivent leurs études, le font davantage dans des formations spécialisées hors Parcoursup (CAP, BP...).
""")

# =========================
# GENRE PAR FORMATION
# =========================

st.subheader("Répartition Hommes / Femmes par formation")

df_plot = df.copy()

cols = [
    'effectif_total_candidats',
    'nombre_candidates',
    'effectif_des_admis_en_phase_principale',
    'effectif_des_admis_en_phase_complementaire',
    'dont_effectif_des_candidates_admises'
]

df_plot[cols] = df_plot[cols].apply(
    pd.to_numeric,
    errors='coerce'
)

df_plot['total_admis'] = (
    df_plot['effectif_des_admis_en_phase_principale'].fillna(0) +
    df_plot['effectif_des_admis_en_phase_complementaire'].fillna(0)
)

df_plot['candidates'] = (
    df_plot['nombre_candidates']
    .fillna(0)
)

df_plot['candidats_hommes'] = (
    df_plot['effectif_total_candidats'] -
    df_plot['candidates']
)

df_plot['admises'] = (
    df_plot['dont_effectif_des_candidates_admises']
    .fillna(0)
)

df_plot['admis_hommes'] = (
    df_plot['total_admis'] -
    df_plot['admises']
)

agg = (
    df_plot
    .groupby('type_formation')[[
        'candidates',
        'candidats_hommes',
        'admises',
        'admis_hommes'
    ]]
    .sum()
    .reset_index()
)

agg['pct_femmes_candidats'] = (
    agg['candidates'] /
    (agg['candidates'] + agg['candidats_hommes'])
) * 100

agg['pct_hommes_candidats'] = (
    agg['candidats_hommes'] /
    (agg['candidates'] + agg['candidats_hommes'])
) * 100

agg['pct_femmes_admis'] = (
    agg['admises'] /
    (agg['admises'] + agg['admis_hommes'])
) * 100

agg['pct_hommes_admis'] = (
    agg['admis_hommes'] /
    (agg['admises'] + agg['admis_hommes'])
) * 100

agg_melt = agg.melt(
    id_vars='type_formation',
    value_vars=[
        'pct_femmes_candidats',
        'pct_hommes_candidats',
        'pct_femmes_admis',
        'pct_hommes_admis'
    ],
    var_name='categorie',
    value_name='pourcentage'
)

fig = px.bar(
    agg_melt,
    x='type_formation',
    y='pourcentage',
    color='categorie',
    text='pourcentage',
    barmode='group',
    color_discrete_sequence=PASTEL_COLORS
)

fig.update_traces(
    texttemplate='%{text:.0f}%',
    textposition='outside'
)

fig.update_layout(
    title="Répartition Hommes / Femmes par formation",
    xaxis_tickangle=-45
)

st.plotly_chart(
    fig,
    use_container_width=True,
    key="genre_formation"
)

st.markdown("""
Globalement on observe une surreprésensation des femmes dans les formations par rapport aux hommes.
Plus particulièrement dans les EFTS, IFSI, Licences, Licences LAS, PASS et les autres formations.Les EFTS et IFSI sont les formations avec le plus haut taux de candidates et admises (entre 80 et 90%).

Au contraire les hommes eux sont plus présents dans les BTS, BUT, CPGE, écoles d'ingénieur et écoles de commerce.
""")

# =========================
# BOURSIERS
# =========================

st.subheader("Part des admis néobacheliers boursiers vs non boursiers")

df_plot = df.copy()

cols = [
    'dont_effectif_des_admis_boursiers_neo_bacheliers',
    'effectif_des_admis_neo_bacheliers'
]

df_plot[cols] = df_plot[cols].apply(
    pd.to_numeric,
    errors='coerce'
)

df_plot = df_plot.dropna(subset=cols)

df_plot['non_boursiers'] = (
    df_plot['effectif_des_admis_neo_bacheliers'] -
    df_plot['dont_effectif_des_admis_boursiers_neo_bacheliers']
)

agg = (
    df_plot
    .groupby('type_formation')[[
        'dont_effectif_des_admis_boursiers_neo_bacheliers',
        'non_boursiers'
    ]]
    .sum()
)

pct = agg.div(
    agg.sum(axis=1),
    axis=0
) * 100

pct = pct.reset_index()

pct_melt = pct.melt(
    id_vars='type_formation',
    var_name='categorie',
    value_name='pourcentage'
)

fig = px.bar(
    pct_melt,
    x='type_formation',
    y='pourcentage',
    color='categorie',
    text='pourcentage',
    barmode='stack',
    color_discrete_sequence=PASTEL_COLORS
)

fig.update_traces(
    texttemplate='%{text:.0f}%',
    textposition='inside'
)

fig.update_layout(
    title="Part des admis néobacheliers boursiers vs non boursiers (%)",
    xaxis_tickangle=-45
)

st.plotly_chart(
    fig,
    use_container_width=True,
    key="boursiers_vs_non"
)

# =========================
# MENTIONS
# =========================

st.subheader("Répartition des admis par type de mention")

df_plot = df.copy()

cols = [
    'dont_effectif_des_admis_neo_bacheliers_sans_mention_au_bac',
    'dont_effectif_des_admis_neo_bacheliers_avec_mention_assez_bien_au_bac',
    'dont_effectif_des_admis_neo_bacheliers_avec_mention_bien_au_bac',
    'dont_effectif_des_admis_neo_bacheliers_avec_mention_très_bien_au_bac',
    'dont_effectif_des_admis_neo_bacheliers_avec_mention_très_bien_avec_felicitations_au_bac',
    'effectif_des_admis_neo_bacheliers'
]

df_plot[cols] = df_plot[cols].apply(
    pd.to_numeric,
    errors='coerce'
)

df_plot = df_plot.dropna(
    subset=['effectif_des_admis_neo_bacheliers']
)

agg = (
    df_plot
    .groupby('type_formation')[cols[:-1]]
    .sum()
)

pct = agg.div(
    agg.sum(axis=1),
    axis=0
) * 100

pct = pct.rename(columns={
    'dont_effectif_des_admis_neo_bacheliers_sans_mention_au_bac': 'Sans mention',
    'dont_effectif_des_admis_neo_bacheliers_avec_mention_assez_bien_au_bac': 'Mention assez bien',
    'dont_effectif_des_admis_neo_bacheliers_avec_mention_bien_au_bac': 'Mention bien',
    'dont_effectif_des_admis_neo_bacheliers_avec_mention_très_bien_au_bac': 'Mention très bien',
    'dont_effectif_des_admis_neo_bacheliers_avec_mention_très_bien_avec_felicitations_au_bac': 'Très bien (félicitations)'
})

pct = pct.reset_index()

pct_melt = pct.melt(
    id_vars='type_formation',
    var_name='mention',
    value_name='pourcentage'
)

fig = px.bar(
    pct_melt,
    x='type_formation',
    y='pourcentage',
    color='mention',
    text='pourcentage',
    barmode='stack',
    color_discrete_sequence=PASTEL_COLORS
)

fig.update_traces(
    texttemplate='%{text:.0f}%',
    textposition='inside'
)

fig.update_layout(
    title="Répartition des admis par type de mention (%)",
    xaxis_tickangle=-45
)

st.plotly_chart(
    fig,
    use_container_width=True,
    key="mentions_bac"
)