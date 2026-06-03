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
# =========================
# NETTOYAGE NOTE INDEX
# =========================

df.columns = df.columns.str.strip()

df_plot = df.copy()

df_plot["note_index"] = pd.to_numeric(
    df_plot["note_index"],
    errors="coerce"
)

df_plot = df_plot.dropna(subset=["note_index"])

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

tab1, tab2, tab3, tab4 = st.tabs([
    "Dashboard",
    "Pre-cleaning",
    "Analyse",
    "Dataset"
])


# =========================
# TITRE
# =========================



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

with tab1:

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Nb Entreprises",
            len(df_filtre)
        )

    with col2:
        st.metric(
            "Note d'Index moyenne/100",
            round(df_filtre["Note Index"].mean(), 1)
        )

    with col3:
        st.metric(
            "Note rémunération moyenne/40",
            round(df_filtre["Note Ecart rémunération"].mean(), 1)
        )

    with col4:

        cols = [
        "Note Ecart taux d'augmentation",
        "Note Ecart taux d'augmentation (hors promotion)",
        "Note Ecart taux de promotion"
        ]

        df_filtre[cols] = df_filtre[cols].apply(
        pd.to_numeric,
        errors="coerce"
        )

        df_filtre["Note promotion harmonisée"] = np.where(
        df_filtre["Note Ecart taux d'augmentation"].notna(),
        df_filtre["Note Ecart taux d'augmentation"],
        (
            df_filtre["Note Ecart taux d'augmentation (hors promotion)"].fillna(0)
            +
            df_filtre["Note Ecart taux de promotion"].fillna(0)
        )
        )

        st.metric(
        "Note promotions moyenne /35",
        round(df_filtre["Note promotion harmonisée"].mean(), 1)
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

        promo_low = df_plot[
            [
                "Code NAF",
                "Note Ecart taux d'augmentation",
                "Note Ecart taux d'augmentation (hors promotion)",
                "Note Ecart taux de promotion"
            ]
        ].copy()

        promo_low[
            [
                "Note Ecart taux d'augmentation",
                "Note Ecart taux d'augmentation (hors promotion)",
                "Note Ecart taux de promotion"
            ]
        ] = promo_low[
            [
                "Note Ecart taux d'augmentation",
                "Note Ecart taux d'augmentation (hors promotion)",
                "Note Ecart taux de promotion"
            ]
        ].apply(
            pd.to_numeric,
            errors="coerce"
        )

        # Harmonisation sur 35 points
        promo_low["Note promotion harmonisée"] = np.where(
            promo_low["Note Ecart taux d'augmentation"].notna(),

            promo_low["Note Ecart taux d'augmentation"],

            promo_low["Note Ecart taux d'augmentation (hors promotion)"].fillna(0)
            +
            promo_low["Note Ecart taux de promotion"].fillna(0)
        )

        promo_low = promo_low.dropna(
            subset=["Note promotion harmonisée"]
        )

        promo_low["Secteur"] = (
            promo_low["Code NAF"]
            .astype(str)
            .str.split(" - ")
            .str[1]
        )

        promo_low = (
            promo_low
            .groupby("Secteur")["Note promotion harmonisée"]
            .mean()
            .reset_index()
            .sort_values(
                "Note promotion harmonisée",
                ascending=True
            )
            .head(10)
        )

        fig1 = px.bar(
            promo_low,
            x="Note promotion harmonisée",
            y="Secteur",
            orientation="h",
            color="Note promotion harmonisée",
            text="Note promotion harmonisée",
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
                'text': "Secteurs avec les plus faibles notes de promotion",
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
                'text': "Secteurs avec les plus faibles notes de rémunération",
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


with tab2:
    st.title("Pre-cleaning")

    st.markdown("""
    <div style='text-align: justify; font-size: 16px; line-height:1.8'>

    Voici les différents critères et les points attribués: Rémunération (40 pts), Taux d'augmentation (hors promotion)(20 pts set uniquement si + 250 salariés), Taux de promotion (15 pts et uniquement si + 250 salariés), Taux d'augmentation (35 pts et uniquement si < 250 salariés), Augementation au retour congé maternité (15 pts), % des femmes dans le hautes rémunérations (10pts)
    Les critères sont donc différents selon la taille de l'entreprise. Pour plus de clarté j'ai décidé de réunir les notes qui diffèrent selon la taille pour n'en attribuer qu'une seule pour calculer les promotions.
                
    
    """, unsafe_allow_html=True)



with tab3:
    st.title("Analyse")

    st.markdown("""
    <div style='text-align: justify; font-size: 16px; line-height:1.8'>

    L'index d'Egalité Professionnelle F/H permet de <b>mesurer l'égalité salariale</b> entre les femmes et les hommes dans les entreprises de plus de 50 salariés.
    Le dashboard ci-dessous a été crée dans le but de <b>trouver des tendances</b> et de mieux comprendre le fonctionnement de cet index. 
    J'ai choisi ce sujet ayant <b>déjà travaillé dessus</b> en 2025 et ayant fourni plusieurs données pour le calcul de cet Index pour l'entreprise Inditex.   
                
    
    """, unsafe_allow_html=True)

    st.markdown(
        "<h2 style='color:#A2D2FF;'>1. Performance globale de l’index</h2>",
        unsafe_allow_html=True
    )

    st.markdown("""
        <div style='text-align: justify; padding-top:25px; font-size:16px; line-height:1.8'>
            
        Le Score moyen est élevé (86.6) ce qui indique une <b>bonne conformité globale</b>, 75 étant la note minimale à avoir pour ne pas faire face à des pénalités.
        Une forte majorité d’entreprises a une note d'index comprise entre 85–94 (~48%).
        
        De plus, une part non négligeable atteint <b>95–100</b> (~19%).
        Très peu d’entreprises ont une note en-dessous de 75, la conformité est donc largement respectée          

        </div>
        """, unsafe_allow_html=True)

    st.markdown(
        "<h2 style='color:#A2D2FF;'>2. Rémunération & promotions</h2>",
        unsafe_allow_html=True
    )

    st.markdown("""
        <div style='text-align: justify; padding-top:25px; font-size:16px; line-height:1.8'>
            
        La <b>rémunération</b> est l'enjeu qui vient tout de suite en tête lorsqu'on pense aux inégalités de genre dans le milieu professionnel. On voit bien grâce à l'Index que les notes de rémunération moyenne relativement basse (35,4 sur 40) ce qui indique un <b>axe d'amélioration possible</b>. 
        
        Les notes de promotions sont encore plus faible (28,3 / 35), la promotion est donc le principal point faible contrairement à la croyance populaire.
        On peut donc dire que les <b>écarts persistent</b> sur ces points malgré un bon score global.

        </div>
        """, unsafe_allow_html=True)
    
    st.markdown(
        "<h2 style='color:#A2D2FF;'>3. Analyse par région</h2>",
        unsafe_allow_html=True
    )

    st.markdown("""
        <div style='text-align: justify; padding-top:25px; font-size:16px; line-height:1.8'>
            
        Les <b>écarts sont relativement faibles</b> entre les régions (e,tre 85,5 et 89) ce qui signifie une certaine <b>homogénéité territoriale</b>. La Corse, la Nouvelle-Aquitaine et la Bretagne sont en tête.
        
        On remarque que l'Ile-de-France qui est pourtant la région avec le plus d'entreprises est <b>en dessous de la moyenne d'un point </b> mais il ne semble pas y avoi de région en retard. 
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown(
        "<h2 style='color:#A2D2FF;'>4. Analyse par secteur</h2>",
        unsafe_allow_html=True
    )

    st.markdown("""
        <div style='text-align: justify; padding-top:25px; font-size:16px; line-height:1.8'>
                
        Certains secteurs ont une note moyenne atteignant des <b>scores très élevés</b> comme entres autres la création artistique, la fabrication d'étoffes à mailles.
        Dans le top 10 on remarque des secteurs <b>traditionnellement "fémimins"</b> comme la cultures, l'art ou les soins qui sont souvent majoritairement composés de femmes ce qui peut potentiellement expliquer ces notes hautes.      
        Les secteurs plus classiques et moins genrés semblent se situer vers la moyenne et sont légèrement en retrait.  

        En termes de promotion, certains secteurs ont des <b>notes basses allant de 0 à 15</b> comme la pêche, la réparation, l'élevage, les agences de travail temporaires. Il est possible que ces secteurs ne présentent <b>pas de grandes opportunités de promotion</b>.
        Pour la rémunération, les pires notes vont de <b>0 à 25</b>. 
        
        On y retrouve entres autres l'aquaculture, le commerce de gros, les travaux de démolition donc <b>beaucoup de secteurs "masculins"</b> et pourtant on retrouve également le commerce de textile qui est habituellement plus fréquenté par des femmes.     
        Nous pouvons donc observer des <b>tendances<b> mais parce qu'un secteur est traditionnellement associé à un genre cela n'aura pas forcément d'impact sur <b>sa note mais dépendra des politiques d'entreprises</b>.
        </div> 
        """, unsafe_allow_html=True)
    
    st.markdown(
        "<h2 style='color:#A2D2FF;'>5. Analyse par taille d’entreprise</h2>",
        unsafe_allow_html=True
    )

    st.markdown("""
        <div style='text-align: justify; padding-top:25px; font-size:16px; line-height:1.8'>
                
        On observe que les plus <b>grandes entreprises (+ de 1000 salariés) ont les meilleurs scores</b> avec une note moyenne de 88,6 alors que les PME et sont légèrement en dessous avec ~86,4.
        On peut donc théoriser une <b>corrélation entre la taille et la performance</b> du score. 
                
        Une explication possible peut être la présence dans les grandes entreprise de <b>services dédiés à améliorer l'égalité professionnelle</b> ce qui n'est pas forcément le cas dans les entreprises plus petites.
        </div> 
        """, unsafe_allow_html=True)
    
    st.markdown(
        "<h2 style='color:#A2D2FF;'>6. Entreprises outliers</h2>",
        unsafe_allow_html=True
    )

    st.markdown("""
        <div style='text-align: justify; padding-top:25px; font-size:16px; line-height:1.8'>
                
        Plusieurs entreprises atteignent <b>100/100</b> qui est la meilleure note possible mais <b>certaines sont très en retard</b> avec des notes allant entre 20 et 45. 
        En regardant l'exemple d'OVH Cloud on voit que malgré une note en 2018 faible (63), l'entreprise a augmenté son retour de congé maternité et malgré la forte variabilité des écarts elle a <b>pu atteindre une note générale de 99</b>.
        Il y a donc une forte <b>hétérogénéité individuelle</b> malgré la moyenne générale élevée. 
        </div> 
        """, unsafe_allow_html=True)
    
    st.markdown(
        "<h2 style='color:#A2D2FF;'>Conclusion globale</h2>",
        unsafe_allow_html=True
    )

    st.markdown("""
        <div style='text-align: justify; padding-top:25px; font-size:16px; line-height:1.8'>
                
        Après toutes ces analyses nous pouvons avant tout mettre en avant le <b>bon niveau global de la conformité</b> (la note minimale demandée étant 75).
        Néanmoins, des <b>inégalités sont encore présentes</b> sur la rémunération et les promotions.
        Les principales disparités remarqués sont <b>la taile de l'entreprise, le secteur et les entreprises individuelle</b>s. 
        
        Toutefois, nous avons observé que même avec une note originelle faible il est <b>possible en quelques années d'atteindre une note haute</b> en mettant en place des <b>politiques d'égalité professionnelles</b> au sein de l'entreprise.
        </div> 
        """, unsafe_allow_html=True)

with tab4:
    st.title("Exploration des données")

    # =========================
    # TABLEAU
    # =========================

    

    st.dataframe(
        df_filtre[[
            "Année",
            "Raison Sociale",
            "Région",
            "Tranche d'effectifs",
            "Note Index"
        ]].dropna(),
        use_container_width=True
    )