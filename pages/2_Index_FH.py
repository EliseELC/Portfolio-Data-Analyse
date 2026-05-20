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


df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
    .str.replace("'", "")
    .str.replace("é", "e")
)

st.markdown("""
<style>

/* Fond principal */
.stApp {
    background: linear-gradient(
        135deg,
        #880D1E 0%,
        #A4133C 35%,
        #DD2D4A 100%
    );
}

/* Sidebar -> transparente */
section[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.03);
    backdrop-filter: blur(8px);
    border-right: 1px solid rgba(255,255,255,0.08);
}

/* Texte global */
html, body, [class*="css"] {
    color: white;
}

/* Titres */
h1, h2, h3 {
    color: white !important;
    font-weight: 700 !important;
}

/* Texte markdown */
p, li {
    color: #F8F9FA !important;
}

/* KPI cards */
[data-testid="metric-container"] {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.08);
    padding: 18px;
    border-radius: 18px;
    backdrop-filter: blur(14px);
    box-shadow: 0 4px 20px rgba(0,0,0,0.15);
}

/* Valeurs KPI */
[data-testid="metric-container"] label {
    color: #F49CBB !important;
}

[data-testid="metric-container"] div {
    color: white !important;
}

/* Tabs */
button[data-baseweb="tab"] {
    background: rgba(255,255,255,0.06);
    color: white;
    border-radius: 12px;
    margin-right: 6px;
    padding: 10px 18px;
}

button[data-baseweb="tab"][aria-selected="true"] {
    background: #F26A8D !important;
    color: white !important;
}

/* Selectbox / multiselect */
[data-baseweb="select"] > div {
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    color: white !important;
}

/* Inputs */
input {
    color: white !important;
}

/* Slider */
.stSlider > div > div > div > div {
    background: linear-gradient(
        90deg,
        #880D1E,
        #DD2D4A,
        #F26A8D,
        #F49CBB,
        #CBEEF3
    ) !important;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    background: rgba(255,255,255,0.05);
    border-radius: 14px;
    overflow: hidden;
}

/* Graphiques */
[data-testid="stPlotlyChart"] {
    background: rgba(255,255,255,0.06);
    border-radius: 20px;
    padding: 10px;
    backdrop-filter: blur(12px);
    box-shadow: 0 4px 20px rgba(0,0,0,0.15);
}

/* Containers */
.block-container {
    padding-top: 2rem;
}

/* Radio buttons sidebar */
.stRadio label {
    color: white !important;
}

/* Labels */
label {
    color: white !important;
    font-weight: 600 !important;
}
/* Fond dropdown filtres */
div[data-baseweb="popover"] {
    background-color: #F49CBB !important;
}

/* Fond menu options */
ul {
    background-color: #F49CBB !important;
}
            
</style>
""", unsafe_allow_html=True)

# =========================
# COULEURS GRAPHIQUES
# =========================

PASTEL_COLORS = [
    "#CBEEF3",
    "#F49CBB",
    "#F26A8D",
    "#DD2D4A",
    "#880D1E",
    "#FFCAD4",
    "#CDB4DB",
    "#A2D2FF"
]

PASTEL_SCALE = [
    [0.0, "#CBEEF3"],
    [0.25, "#F49CBB"],
    [0.5, "#F26A8D"],
    [0.75, "#DD2D4A"],
    [1.0, "#880D1E"]
]

@st.cache_data
def load_data():
    df = pd.read_excel("data/index-egalite-fh.xlsx")
    return df

df = load_data()

# =========================
# CONVERSION DES COLONNES NUMERIQUES
# =========================

cols_num = [
    "Note Ecart rémunération",
    "Note Ecart taux d'augmentation (hors promotion)",
    "Note Ecart taux de promotion",
    "Note Ecart taux d'augmentation",
    "Note Retour congé maternité",
    "Note Hautes rémunérations",
    "Note Index"
]

df[cols_num] = df[cols_num].apply(
    pd.to_numeric,
    errors="coerce"
)

# =========================
# TITRE
# =========================

st.markdown("""
<div style='text-align: justify; font-size: 16px; line-height:1.8'>

L'index d'Egalité Professionnelle F/H permet de mesurer l'égalité salariale entre les femmes et les hommes dans les entreprises de plus de 50 salariés.
Le dashboard ci-dessous a été crée dans le but de trouver des tendances et de mieux comprendre le fonctionnement de cet index. 
J'ai choisi ce sujet ayant déjà travaillé dessus en 2025 et ayant fourni plusieurs données pour le calcul de cet Index pour l'entreprise Inditex.   
            
Voici les notes maximales pour chaque critères:<br>
Rémunération: 40<br>
Taux d'augmentation (hors promotion): 20<br>
Taux de promotion: 15<br>
Taux d'augmentation: 35<br>
Augementation au retour congé maternité: 15<br>
% des femmes dans le hautes rémunérations: 10
<br>
   
</div>
""", unsafe_allow_html=True)

# =========================
# FILTRES
# =========================

st.sidebar.header("Filtres à modifier")

annees = st.sidebar.multiselect(
    "Année",
    options=sorted(df["Année"].dropna().unique()),
    default=sorted(df["Année"].dropna().unique())
)

regions = st.sidebar.multiselect(
    "Région",
    options=sorted(df["Région"].dropna().unique()),
    default=sorted(df["Région"].dropna().unique())
)

tranches = st.sidebar.multiselect(
    "Tranche d'effectifs",
    options=sorted(df["Tranche d'effectifs"].dropna().unique()),
    default=sorted(df["Tranche d'effectifs"].dropna().unique())
)

# =========================
# DATA FILTRÉE
# =========================

df_filtre = df[
    (df["Année"].isin(annees)) &
    (df["Région"].isin(regions)) &
    (df["Tranche d'effectifs"].isin(tranches))
]

# =========================
# KPI
# =========================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Nb Entreprises",
        len(df_filtre)
    )

with col2:
    st.metric(
        "Note d'Index moyenne",
        round(df_filtre["Note Index"].mean(), 1)
    )

with col3:
    st.metric(
        "Note rémunération moyenne",
        round(df_filtre["Note Ecart rémunération"].mean(), 1)
    )

with col4:
    st.metric(
        "Note promotions moyenne",
        round(df_filtre["Note Ecart taux de promotion"].mean(), 1)
    )

# =========================
# LAYOUT
# =========================

# =========================
# STYLE DES VISUALISATIONS
# =========================

st.markdown("""
<style>

/* Fond des graphiques */
[data-testid="stPlotlyChart"] {
    background: rgba(255,255,255,0.10);
    border-radius: 22px;
    padding: 15px;
    backdrop-filter: blur(12px);
    box-shadow: 0 6px 25px rgba(0,0,0,0.18);
}

/* Titre graphiques */
.js-plotly-plot .plotly .gtitle {
    fill: white !important;
    font-size: 22px !important;
    font-weight: 700 !important;
}

</style>
""", unsafe_allow_html=True)

# =========================
# COULEURS CONTRASTÉES
# =========================

GRAPH_COLORS = [
    "#CBEEF3",
    "#FFB3C6",
    "#FF4D6D",
    "#C9184A",
    "#720026",
    "#A2D2FF",
    "#FEE440",
    "#80ED99"
]

# =========================
# LAYOUT
# =========================

col1, col2 = st.columns([0.5, 0.5])

# =========================
# PIE CHART NOTES
# =========================

with col1:

    df_plot = df.copy()

    df_plot["Note Index"] = pd.to_numeric(
        df_plot["Note Index"],
        errors="coerce"
    )

    bins = [0, 19, 34, 44, 54, 64, 74, 84, 94, 100]

    labels = [
        "0-19",
        "20-34",
        "35-44",
        "45-54",
        "55-64",
        "65-74",
        "75-84",
        "85-94",
        "95-100"
    ]

    df_plot["Tranche note"] = pd.cut(
        df_plot["Note Index"],
        bins=bins,
        labels=labels,
        include_lowest=True
    )

    repartition = (
        df_plot["Tranche note"]
        .value_counts()
        .reset_index()
    )

    repartition.columns = ["Tranche", "Nombre"]

    fig1 = px.pie(
    repartition,
    values="Nombre",
    names="Tranche",
    hole=0.60,
    color_discrete_sequence=GRAPH_COLORS
)

    fig1.update_traces(
        textinfo="percent+label",
        textfont_size=12,

        # ➜ cache les labels trop petits
        textposition="inside",
        insidetextorientation="horizontal",

        marker=dict(
            line=dict(color="rgba(0,0,0,0)", width=0)
        )
    )

    fig1.update_layout(
        title={
            'text': "Répartition des notes d'index",
            'x': 0.5,
            'xanchor': 'center'
        },

        height=520,

        # ➜ pie chart moins large
        margin=dict(l=60, r=60, t=70, b=20),

        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',

        font=dict(color="white"),

        showlegend=False
    )

    st.plotly_chart(
        fig1,
        use_container_width=True,
        key="pie_notes"
    )

# =========================
# INDEX PAR REGION
# =========================

with col2:

    region_avg = (
        df_plot
        .groupby("Région")["Note Index"]
        .mean()
        .reset_index()
        .sort_values("Note Index", ascending=True)
    )

    fig2 = px.bar(
    region_avg,
    x="Note Index",
    y="Région",
    orientation="h",
    color="Note Index",
    text="Note Index",
    color_continuous_scale=[
        "#FFB3C6",
        "#FF4D6D",
        "#C9184A",
        "#720026"
    ]
    )

    fig2.update_traces(
        texttemplate='%{text:.1f}',
        textposition='outside',
        cliponaxis=False,

        # ➜ couleur des data labels
        textfont=dict(
            color="white",
            size=14
        )
    )

    fig2.update_layout(
        title={
            'text': "Note moyenne par région",
            'x': 0.5,
            'xanchor': 'center'
        },

        height=520,

        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',

        font=dict(color="white"),

        coloraxis_showscale=False,

        xaxis_title=None,
        yaxis_title=None,

        # ➜ cacher détails axe X
        xaxis=dict(
            showticklabels=False,
            rangeslider_visible=False
        ),

        # ➜ régions couleur blanche
        yaxis=dict(
            tickfont=dict(
                size=13,
                color="white"
            )
        ),

        margin=dict(l=0, r=70, t=70, b=0)
    )

    st.plotly_chart(
        fig2,
        use_container_width=True,
        key="region_index"
    )


col1, col2 = st.columns([0.5, 0.5], gap="small")

# =========================
# NOTES PAR SECTEUR
# =========================

# =========================
# NOTES PAR SECTEUR
# =========================

with col1:

    df_plot = df.copy()

    df_plot["Note Index"] = pd.to_numeric(
        df_plot["Note Index"],
        errors="coerce"
    )

    df_plot["Secteur"] = (
        df_plot["Code NAF"]
        .astype(str)
        .str.split(" - ")
        .str[1]
    )

    secteur_avg = (
        df_plot
        .groupby("Secteur")["Note Index"]
        .mean()
        .reset_index()
        .sort_values("Note Index", ascending=False)
        .head(10)
    )

    # raccourcir les noms trop longs
    secteur_avg["Secteur"] = secteur_avg["Secteur"].apply(
        lambda x: x[:45] + "..." if len(x) > 45 else x
    )

    fig1 = px.bar(
        secteur_avg,
        x="Note Index",
        y="Secteur",
        orientation="h",
        color="Note Index",
        text="Note Index",
        color_continuous_scale=[
            "#CBEEF3",
            "#F49CBB",
            "#F26A8D",
            "#DD2D4A",
            "#880D1E"
        ]
    )

    fig1.update_traces(
        texttemplate='%{text:.1f}',
        textposition='outside',
        cliponaxis=False,
        width=0.8,
        textfont=dict(
            color="white",
            size=15
        )
    )

    fig1.update_layout(

    title={
        'text': "Note moyenne par secteur",
        'x': 0.5,
        'xanchor': 'center'
    },

    # ➜ réduire hauteur
    height=500,

    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',

    font=dict(color="white"),

    coloraxis_showscale=False,

    xaxis_title=None,
    yaxis_title=None,

    xaxis=dict(
        showticklabels=False,
        fixedrange=True
    ),

    yaxis=dict(
        autorange="reversed",
        tickfont=dict(
            size=12,
            color="white"
        )
    ),

    margin=dict(l=0, r=70, t=80, b=0)
    )

    st.plotly_chart(
        fig1,
        use_container_width=True,
        key="secteur_index",
        config={
            'displayModeBar': False,
            'scrollZoom': False
        }
    )

# =========================
# NOTES PAR EFFECTIF
# =========================

with col2:

    effectif_avg = (
        df_plot
        .groupby("Tranche d'effectifs")["Note Index"]
        .mean()
        .reset_index()
        .sort_values("Note Index", ascending=False)
    )

    fig2 = px.bar(
        effectif_avg,
        x="Note Index",
        y="Tranche d'effectifs",
        orientation="h",
        color="Note Index",
        text="Note Index",
        color_continuous_scale=[
            "#CBEEF3",
            "#F49CBB",
            "#F26A8D",
            "#DD2D4A",
            "#880D1E"
        ]
    )

    fig2.update_traces(
        texttemplate='%{text:.1f}',
        textposition='outside',
        cliponaxis=False,
        width=0.75,
        textfont=dict(
            color="white",
            size=15
        )
    )

    fig2.update_layout(

    title={
        'text': "Note moyenne par taille d'effectif",
        'x': 0.5,
        'xanchor': 'center'
    },

    # ➜ réduire hauteur
    height=500,

    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',

    font=dict(color="white"),

    coloraxis_showscale=False,

    xaxis_title=None,
    yaxis_title=None,

    xaxis=dict(
        showticklabels=False,
        showgrid=False,
        fixedrange=True
    ),

    yaxis=dict(
        tickfont=dict(
            size=13,
            color="white"
        )
    ),

    margin=dict(l=0, r=70, t=80, b=0)
    )

    st.plotly_chart(
        fig2,
        use_container_width=True,
        key="effectif_index",
        config={
            'displayModeBar': False,
            'scrollZoom': False
        }
    )


st.subheader("Meilleures et pires notes (+1000 salariés)")

col1, col2 = st.columns([0.5, 0.5], gap="small")

# =========================
# FILTRE > 1000 SALARIÉS
# =========================

df_big = df_plot[
    df_plot["Tranche d'effectifs"]
    .astype(str)
    .str.contains("1000", case=False, na=False)
]

# =========================
# MEILLEURES ENTREPRISES
# =========================

with col1:

    best_companies = (
        df_big[
            ["Raison Sociale", "Note Index"]
        ]
        .dropna()
        .sort_values("Note Index", ascending=False)
        .head(7)
    )

    fig1 = px.bar(
        best_companies,
        x="Note Index",
        y="Raison Sociale",
        orientation="h",
        color="Note Index",
        text="Note Index",
        color_continuous_scale=[
            "#CBEEF3",
            "#F49CBB",
            "#F26A8D",
            "#DD2D4A",
            "#880D1E"
        ]
    )

    fig1.update_traces(
        texttemplate='%{text:.1f}',
        textposition='outside',
        width=0.7,
        cliponaxis=False,
        textfont=dict(
            color="white",
            size=14
        )
    )

    fig1.update_layout(
        title={
            'text': "Extrait entreprises avec note maximale",
            'x': 0.5,
            'xanchor': 'center'
        },

        height=450,

        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',

        font=dict(color="white"),

        coloraxis_showscale=False,

        xaxis_title=None,
        yaxis_title=None,

        xaxis=dict(
            showticklabels=False,
            fixedrange=True
        ),

        yaxis=dict(
            autorange="reversed",
            tickfont=dict(
                size=12,
                color="white"
            )
        ),

        margin=dict(l=0, r=70, t=80, b=0)
    )

    st.plotly_chart(
        fig1,
        use_container_width=True,
        key="best_companies",
        config={
            'displayModeBar': False,
            'scrollZoom': False
        }
    )
# =========================
# PIRES ENTREPRISES
# =========================

with col2:

    worst_companies = (
        df_big[
            ["Raison Sociale", "Note Index"]
        ]
        .dropna()
        .sort_values("Note Index", ascending=True)
        .head(7)
    )

    fig2 = px.bar(
        worst_companies,
        x="Note Index",
        y="Raison Sociale",
        orientation="h",
        color="Note Index",
        text="Note Index",
        color_continuous_scale=[
            "#880D1E",
            "#DD2D4A",
            "#F26A8D",
            "#F49CBB",
            "#CBEEF3"
        ]
    )

    fig2.update_traces(
        texttemplate='%{text:.1f}',
        textposition='outside',
        width=0.7,
        cliponaxis=False,
        textfont=dict(
            color="white",
            size=14
        )
    )

    fig2.update_layout(
        title={
            'text': "Entreprises les moins bien notées",
            'x': 0.5,
            'xanchor': 'center'
        },

        height=450,

        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',

        font=dict(color="white"),

        coloraxis_showscale=False,

        xaxis_title=None,
        yaxis_title=None,

        xaxis=dict(
            showticklabels=False,
            fixedrange=True
        ),

        yaxis=dict(
            autorange="reversed",
            tickfont=dict(
                size=12,
                color="white"
            )
        ),

        margin=dict(l=0, r=70, t=80, b=0)
    )

    st.plotly_chart(
        fig2,
        use_container_width=True,
        key="worst_companies",
        config={
            'displayModeBar': False,
            'scrollZoom': False
        }
    )

st.subheader("Évolution des critères - Exemple avec OVH Cloud")

df_ditex = df_plot[
    df_plot["SIREN"]
    .astype(str)
    .str.lower()
    .str.contains("424761419", na=False)
].copy()

notes_cols = [
    "Note Ecart rémunération",
    "Note Ecart taux d'augmentation (hors promotion)",
    "Note Ecart taux de promotion",
    "Note Ecart taux d'augmentation",
    "Note Retour congé maternité",
    "Note Hautes rémunérations"
]

df_ditex[notes_cols] = df_ditex[notes_cols].apply(
    pd.to_numeric,
    errors="coerce"
)

evolution = (
    df_ditex
    .groupby("Année")[notes_cols]
    .mean()
    .reset_index()
)

evolution_melt = evolution.melt(
    id_vars="Année",
    var_name="Critère",
    value_name="Note"
)

# retirer "Note " dans les labels
evolution_melt["Critère"] = (
    evolution_melt["Critère"]
    .str.replace("Note ", "", regex=False)
)

fig = px.line(
    evolution_melt,
    x="Année",
    y="Note",
    color="Critère",
    markers=True,
    color_discrete_sequence=PASTEL_COLORS
)

fig.update_traces(
    line=dict(width=4),
    marker=dict(size=9)
)

fig.update_layout(

    title={
        'text': "Évolution des critères - OVH Cloud",
        'x': 0.5,
        'xanchor': 'center'
    },

    height=550,

    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',

    font=dict(color="white"),

    xaxis_title=None,
    yaxis_title=None,

    # ➜ texte axes en blanc
    xaxis=dict(
        tickfont=dict(
            color="white",
            size=13
        ),

        # ➜ enlever lignes verticales
        showgrid=False,

        zeroline=False
    ),

    yaxis=dict(
        tickfont=dict(
            color="white",
            size=13
        ),

        # ➜ lignes horizontales discrètes
        gridcolor='rgba(255,255,255,0.08)',

        zeroline=False
    ),

    legend=dict(
        orientation="h",
        yanchor="top",
        y=-0.25,
        xanchor="center",
        x=0.5
    )
)
st.plotly_chart(
    fig,
    use_container_width=True,
    key="ditex_evolution"
)
# =========================
col1, col2 = st.columns([0.5, 0.5], gap="small")

# =========================
# PLUS FAIBLES ECARTS DE PROMOTION
# =========================

with col1:

    promo_low = (
        df_plot[
            ["Code NAF", "Note Ecart taux de promotion"]
        ]
        .dropna()
    )

    promo_low["Secteur"] = (
        promo_low["Code NAF"]
        .astype(str)
        .str.split(" - ")
        .str[1]
    )

    promo_low = (
        promo_low
        .groupby("Secteur")["Note Ecart taux de promotion"]
        .mean()
        .reset_index()
        .sort_values(
            "Note Ecart taux de promotion",
            ascending=True
        )
        .head(10)
    )

    promo_low["Secteur"] = promo_low["Secteur"].apply(
        lambda x: x[:40] + "..."
        if len(x) > 40 else x
    )

    fig1 = px.bar(
        promo_low,
        x="Note Ecart taux de promotion",
        y="Secteur",
        orientation="h",
        color="Note Ecart taux de promotion",
        text="Note Ecart taux de promotion",
        color_continuous_scale=[
            "#CBEEF3",
            "#F49CBB",
            "#F26A8D",
            "#DD2D4A",
            "#880D1E"
        ]
    )

    fig1.update_traces(
        texttemplate='%{text:.1f}',
        textposition='outside',
        width=0.75,
        cliponaxis=False,
        textfont=dict(
            color="white",
            size=14
        )
    )

    fig1.update_layout(
        title={
            'text': "Secteurs avec les plus faibles écarts de promotion",
            'x': 0.5,
            'xanchor': 'center'
        },

        height=500,

        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',

        font=dict(color="white"),

        coloraxis_showscale=False,

        xaxis_title=None,
        yaxis_title=None,

        xaxis=dict(
            showticklabels=False,
            fixedrange=True
        ),

        yaxis=dict(
            autorange="reversed",
            tickfont=dict(
                size=12,
                color="white"
            )
        ),

        margin=dict(l=0, r=70, t=80, b=0)
    )

    st.plotly_chart(
        fig1,
        use_container_width=True,
        key="promo_low",
        config={
            'displayModeBar': False,
            'scrollZoom': False
        }
    )

# =========================
# PLUS FAIBLES ECARTS DE REMUNERATION
# =========================

with col2:

    salaire_low = (
        df_plot[
            ["Code NAF", "Note Ecart rémunération"]
        ]
        .dropna()
    )

    salaire_low["Secteur"] = (
        salaire_low["Code NAF"]
        .astype(str)
        .str.split(" - ")
        .str[1]
    )

    salaire_low = (
        salaire_low
        .groupby("Secteur")["Note Ecart rémunération"]
        .mean()
        .reset_index()
        .sort_values(
            "Note Ecart rémunération",
            ascending=True
        )
        .head(10)
    )

    salaire_low["Secteur"] = salaire_low["Secteur"].apply(
        lambda x: x[:40] + "..."
        if len(x) > 40 else x
    )

    fig2 = px.bar(
        salaire_low,
        x="Note Ecart rémunération",
        y="Secteur",
        orientation="h",
        color="Note Ecart rémunération",
        text="Note Ecart rémunération",
        color_continuous_scale=[
            "#CBEEF3",
            "#F49CBB",
            "#F26A8D",
            "#DD2D4A",
            "#880D1E"
        ]
    )

    fig2.update_traces(
        texttemplate='%{text:.1f}',
        textposition='outside',
        width=0.75,
        cliponaxis=False,
        textfont=dict(
            color="white",
            size=14
        )
    )

    fig2.update_layout(
        title={
            'text': "Secteurs avec les plus faibles écarts de rémunération",
            'x': 0.5,
            'xanchor': 'center'
        },

        height=500,

        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',

        font=dict(color="white"),

        coloraxis_showscale=False,

        xaxis_title=None,
        yaxis_title=None,

        xaxis=dict(
            showticklabels=False,
            fixedrange=True
        ),

        yaxis=dict(
            autorange="reversed",
            tickfont=dict(
                size=12,
                color="white"
            )
        ),

        margin=dict(l=0, r=70, t=80, b=0)
    )

    st.plotly_chart(
        fig2,
        use_container_width=True,
        key="salaire_low",
        config={
            'displayModeBar': False,
            'scrollZoom': False
        }
    )

# =========================
# TABLEAU
# =========================

st.subheader("📋 Détail des entreprises")

st.dataframe(
    df_filtre[[
        "Année",
        "Raison Sociale",
        "Région",
        "Tranche d'effectifs",
        "Note Index"
    ]],
    use_container_width=True
)