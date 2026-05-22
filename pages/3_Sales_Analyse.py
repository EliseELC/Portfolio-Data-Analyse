import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(
    page_title="Analyse des ventes 2023-2024",
    layout="wide"
)
st.title("Analyse des ventes 2023-2025")

@st.cache_data
def load_data():

    df = pd.read_excel(
        r"data\sales.xlsx"
    )

    df.columns = df.columns.str.strip()

    return df

df = load_data()

# =========================
# STYLE GLOBAL
# =========================

st.markdown("""
<style>

/* Fond général */
.stApp {
    background-color: #F7F8FA;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: white;
    border-right: 1px solid #E5E7EB;
}

/* Titres */
h1, h2, h3 {
    color: #1F2937 !important;
    font-weight: 700 !important;
}

/* Texte */
p, label {
    color: #4B5563 !important;
}

/* KPI */
[data-testid="metric-container"] {
    background: white;
    border-radius: 18px;
    padding: 20px;
    border: 1px solid #E5E7EB;
    box-shadow: 0 2px 10px rgba(0,0,0,0.04);
}



/* Tabs */
button[data-baseweb="tab"] {
    background: #EEF2FF;
    color: #374151;
    border-radius: 12px;
    margin-right: 6px;
    padding: 10px 18px;
}

button[data-baseweb="tab"][aria-selected="true"] {
    background: #2563EB !important;
    color: white !important;
}

/* Filtres */
[data-baseweb="select"] > div {
    background: white !important;
    border: 1px solid #D1D5DB !important;
    border-radius: 12px !important;
}

/* Texte filtres */
[data-baseweb="select"] span {
    color: #1F2937 !important;
}

/* Tableau */
[data-testid="stDataFrame"] {
    background: white;
    border-radius: 18px;
    border: 1px solid #E5E7EB;
}

</style>
""", unsafe_allow_html=True)

# =========================
# COULEURS
# =========================

DASH_COLORS = [
    "#2563EB",
    "#60A5FA",
    "#34D399",
    "#F59E0B",
    "#F87171",
    "#A78BFA"
]

DASH_SCALE = [
    [0.0, "#DBEAFE"],
    [0.25, "#93C5FD"],
    [0.5, "#60A5FA"],
    [0.75, "#2563EB"],
    [1.0, "#1D4ED8"]
]

# =========================
# DATA
# =========================

@st.cache_data
def load_data():

    df = pd.read_excel(
        "data\Product-Sales.xlsx"
    )

    df.columns = df.columns.str.strip()

    return df

df = load_data()

# =========================
# PREP DATA
# =========================

date_cols = ["Date", "OrderDate", "DeliveryDate"]

for col in date_cols:
    df[col] = pd.to_datetime(
        df[col],
        errors="coerce"
    )

num_cols = [
    "Quantity",
    "UnitPrice",
    "Discount",
    "TotalPrice",
    "ShippingCost"
]

for col in num_cols:
    df[col] = pd.to_numeric(
        df[col],
        errors="coerce"
    )

df["Returned_Flag"] = (
    df["Returned"]
    .astype(str)
    .str.strip()
    .str.lower()
    .isin(["yes", "true", "1", "returned"])
)


# =========================
# FILTRES SIDEBAR
# =========================

st.sidebar.header("🎛️ Filtres")

regions = st.sidebar.multiselect(
    "🌍 Région",
    options=sorted(df["Region"].dropna().unique()),
    default=sorted(df["Region"].dropna().unique())
)

products = st.sidebar.multiselect(
    "📦 Produit",
    options=sorted(df["Product"].dropna().unique()),
    default=sorted(df["Product"].dropna().unique())
)

store_locations = st.sidebar.multiselect(
    "🏪 Magasin",
    options=sorted(df["StoreLocation"].dropna().unique()),
    default=sorted(df["StoreLocation"].dropna().unique())
)

# =========================
# DATA FILTRÉE
# =========================

df_filtre = df[
    (df["Region"].isin(regions)) &
    (df["Product"].isin(products)) &
    (df["StoreLocation"].isin(store_locations))
]

# =========================
# TABS
# =========================

tab1, tab2, tab3, tab4 = st.tabs([
    "🧹Pre-cleaning",
    "📊Dashboard",
    "📈Analyse",
    "📖Dataset"
])



# =========================
# DASHBOARD
# =========================

with tab1:

        st.title("🧹Pre-cleaning")

    #df modifié car chiffres choisis aléatoirement donc pas cohérent niveau profit, cout, prix...#



with tab2:

    st.title("Sales Dashboard")

        # =========================
    # KPI
    # =========================

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        total_sales = df_filtre["TotalPrice"].sum()

        st.metric(
            "Chiffre d'affaires",
            f"${total_sales:,.0f}"
        )

    with col2:

        total_orders = df_filtre["OrderID"].nunique()

        st.metric(
            "Nombre de commandes",
            f"{total_orders:,}"
        )

    with col3:

        avg_order = df_filtre["TotalPrice"].mean()

        st.metric(
            "Panier moyen",
            f"${avg_order:,.2f}"
        )

    with col4:

        best_region = (
            df_filtre
            .groupby("Region")["TotalPrice"]
            .sum()
            .idxmax()
        )

        st.metric(
            "Meilleure région",
            best_region
        )

    # =========================
    # LIGNE 1
    # =========================

    col1, col2 = st.columns([0.6, 0.4], gap="small")

    # =========================
    # ÉVOLUTION DES VENTES
    # =========================

    with col1:

        sales_month = (
            df_filtre
            .groupby(df_filtre["Date"].dt.to_period("M"))
            ["TotalPrice"]
            .sum()
            .reset_index()
        )

        sales_month["Date"] = (
            sales_month["Date"]
            .astype(str)
        )

        fig1 = px.line(
            sales_month,
            x="Date",
            y="TotalPrice",
            markers=True
        )

        fig1.update_traces(
            line=dict(
                color="#2563EB",
                width=4
            ),
            marker=dict(
                size=9,
                color="#60A5FA"
            )
        )

        fig1.update_layout(
            title={
            'text': "Evolution des ventes",
            'x': 0.5,
            'xanchor': 'center'
        },

            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',

            font=dict(color="#1F2937"),

            xaxis_title=None,
            yaxis_title=None
        )

        st.plotly_chart(
            fig1,
            use_container_width=True,
            config={'displayModeBar': False}
        )

    # =========================
    # VENTES PAR RÉGION
    # =========================

    with col2:

        sales_region = (
            df_filtre
            .groupby("Region")["TotalPrice"]
            .sum()
            .reset_index()
        )

        fig2 = px.pie(
            sales_region,
            values="TotalPrice",
            names="Region",
            hole=0.55,
            color_discrete_sequence=DASH_COLORS
        )

        fig2.update_traces(
            textinfo='percent'
        )

        fig2.update_layout(
            title={
            'text': "Ventes par région",
            'x': 0.5,
            'xanchor': 'center'
        },

            paper_bgcolor='rgba(0,0,0,0)',

            font=dict(color="#1F2937")
        )

        st.plotly_chart(
            fig2,
            use_container_width=True,
            config={'displayModeBar': False}
        )
    # =========================
    # PROFIT PAR PRODUIT ET PAR RÉGION
    # =========================

    df_filtre["Profit"] = (
        (
            df_filtre["UnitPrice"]
            * df_filtre["Quantity"]
            * (1 - df_filtre["Discount"])
        )
        -
        (
            df_filtre["ShippingCost"]
            + (
                df_filtre["UnitPrice"] * 0.6
            ) * df_filtre["Quantity"]
        )
    )

    profit_region_product = (
        df_filtre
        .groupby(["Region", "Product"])["Profit"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        profit_region_product,
        x="Region",
        y="Profit",
        color="Product",
        barmode="group",
        text="Profit",
        color_discrete_sequence=DASH_COLORS
    )

    fig.update_traces(
        texttemplate='%{text:,.0f}',
        textposition='outside'
    )

    fig.update_layout(
        title={
            'text': "Chiffre d'affaires par produit et région",
            'x': 0.5,
            'xanchor': 'center'
        },

    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',

    font=dict(color="#1F2937"),

    xaxis_title=None,
    yaxis_title=None,

    legend=dict(
        orientation="h",
        yanchor="top",
        y=-0.25,
        xanchor="center",
        x=0.5,
        itemwidth=30
    )
    )
    

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={'displayModeBar': False}
    )
    # =========================
    # LIGNE 3
    # =========================

    col1, col2 = st.columns(2, gap="small")

    # =========================
    # PRODUITS LES PLUS VENDUS
    # =========================

    with col1:

        product_sales = (
            df_filtre
            .groupby("Product")["Quantity"]
            .sum()
            .reset_index()
            .sort_values("Quantity", ascending=False)
            .head(10)
        )

        fig3 = px.bar(
            product_sales,
            x="Product",
            y="Quantity",
            color="Quantity",
            text="Quantity",
            color_continuous_scale=DASH_SCALE
        )

        fig3.update_traces(
            texttemplate='%{text:,.0f}',
            textposition='outside'
        )

        fig3.update_layout(
            title={
            'text': "Produit les plus vendus",
            'x': 0.5,
            'xanchor': 'center'
        },
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',

            font=dict(color="#1F2937"),

            coloraxis_showscale=False,

            xaxis_title=None,
            yaxis_title=None
        )

        st.plotly_chart(
            fig3,
            use_container_width=True,
            config={'displayModeBar': False}
        )

    # =========================
    # VENTES PAR PAIEMENT
    # =========================

    with col2:

        payment = (
            df_filtre
            .groupby("PaymentMethod")["TotalPrice"]
            .sum()
            .reset_index()
        )

        fig4 = px.bar(
            payment,
            x="PaymentMethod",
            y="TotalPrice",
            color="PaymentMethod",
            text="TotalPrice",
            color_discrete_sequence=DASH_COLORS
        )

        fig4.update_traces(
            texttemplate='%{text:,.0f}',
            textposition='outside'
        )

        fig4.update_layout(
            title={
            'text': "Ventes par type de paiement",
            'x': 0.5,
            'xanchor': 'center'
        },

            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',

            font=dict(color="#1F2937"),

            showlegend=False,

            xaxis_title=None,
            yaxis_title=None
        )

        st.plotly_chart(
            fig4,
            use_container_width=True,
            config={'displayModeBar': False}
        )

    # =========================
    # LIGNE 3
    # =========================

    col1, col2 = st.columns(2, gap="small")

    # =========================
    # CA PAR PRODUIT
    # =========================

    with col1:

        sales_product = (
            df_filtre
            .groupby("Product")["TotalPrice"]
            .sum()
            .reset_index()
            .sort_values("TotalPrice", ascending=False)
        )

        fig7 = px.pie(
            sales_product,
            values="TotalPrice",
            names="Product",
            hole=0.55,
            color_discrete_sequence=DASH_COLORS
        )

        fig7.update_traces(
            textinfo='percent'
        )

        fig7.update_layout(
            title={
            'text': "Chiffres d'affaires par produit",
            'x': 0.5,
            'xanchor': 'center'
        },

            paper_bgcolor='rgba(0,0,0,0)',

            font=dict(color="#1F2937"),

            legend=dict(
                orientation="h",
                yanchor="top",
                y=-0.2,
                xanchor="center",
                x=0.5
            )
        )

        st.plotly_chart(
            fig7,
            use_container_width=True,
            config={'displayModeBar': False}
        )

    # =========================
    # TOP PRODUITS PAR RÉGION
    # =========================

    with col2:

        market_sales = (
            df_filtre
            .groupby(["Region", "Product"])["TotalPrice"]
            .sum()
            .reset_index()
        )

        top_products = (
            market_sales
            .groupby("Product")["TotalPrice"]
            .sum()
            .sort_values(ascending=False)
            .index
        )

        market_sales = market_sales[
            market_sales["Product"].isin(top_products)
        ]

        fig8 = px.bar(
            market_sales,
            y="Region",
            x="TotalPrice",
            color="Product",
            orientation="h",
            barmode="stack",
            color_discrete_sequence=DASH_COLORS
        )

        fig8.update_layout(
            title={
            'text': "Top produit par région",
            'x': 0.5,
            'xanchor': 'center'
        },

            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',

            font=dict(color="#1F2937"),

            xaxis_title=None,
            yaxis_title=None,

            xaxis=dict(
                gridcolor='rgba(0,0,0,0.06)'
            ),

            yaxis=dict(
                showgrid=False
            ),

            legend=dict(
                orientation="h",
                yanchor="top",
                y=-0.2,
                xanchor="center",
                x=0.5
            )
        )

        st.plotly_chart(
            fig8,
            use_container_width=True,
            config={'displayModeBar': False}
        )



    
        # =========================
    # KPI LIVRAISON
    # =========================

    # calcul temps de livraison
    df_filtre["Temps_Livraison"] = (
        df_filtre["DeliveryDate"]
        - df_filtre["OrderDate"]
    ).dt.days

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        avg_delivery = (
            df_filtre["Temps_Livraison"]
            .mean()
        )

        st.metric(
            "🚚 Livraison moyenne",
            f"{avg_delivery:.1f} jours"
        )

    with col2:

        min_delivery = (
            df_filtre["Temps_Livraison"]
            .min()
        )

        st.metric(
            "⚡ Livraison la plus rapide",
            f"{min_delivery:.0f} jour(s)"
        )

    with col3:

        max_delivery = (
            df_filtre["Temps_Livraison"]
            .max()
        )

        st.metric(
            "🐢 Livraison la plus longue",
            f"{max_delivery:.0f} jours"
        )

    with col4:

        avg_shipping = (
            df_filtre["ShippingCost"]
            .mean()
        )

        st.metric(
            "💰 Prix moyen livraison",
            f"${avg_shipping:.2f}"
        )

        # =========================
    # CA PAR SALESPERSON
    # =========================
    col1, col2 = st.columns(2, gap="small")

    with col1:

        salesperson_sales = (
            df_filtre
            .groupby("Salesperson")["TotalPrice"]
            .sum()
            .reset_index()
            .sort_values("TotalPrice", ascending=False)
        )

        fig5 = px.bar(
            salesperson_sales,
            x="Salesperson",
            y="TotalPrice",
            color="TotalPrice",
            text="TotalPrice",
            color_continuous_scale=DASH_SCALE
        )

        fig5.update_traces(
            texttemplate='%{text:,.0f}',
            textposition='outside'
        )

        fig5.update_layout(
            title={
            'text': "Chiffres d'affaires par vendeur",
            'x': 0.5,
            'xanchor': 'center'
        },

            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',

            font=dict(color="#1F2937"),

            coloraxis_showscale=False,

            xaxis_title=None,
            yaxis_title=None
        )

        st.plotly_chart(
            fig5,
            use_container_width=True,
            config={'displayModeBar': False}
        )

    # =========================
    # PRODUITS RETOURNÉS
    # =========================

    with col2:

        returns = (
            df_filtre
            .groupby("Product")["Returned_Flag"]
            .mean()
            .reset_index()
            .sort_values("Returned_Flag", ascending=False)
            .head(10)
        )

        returns["Returned_Flag"] = (
            returns["Returned_Flag"] * 100
        )

        fig6 = px.bar(
            returns,
            x="Product",
            y="Returned_Flag",
            color="Returned_Flag",
            text="Returned_Flag",
            color_continuous_scale=[
                "#FEE2E2",
                "#FCA5A5",
                "#EF4444",
                "#991B1B"
            ]
        )

        fig6.update_traces(
            texttemplate='%{text:.1f}%',
            textposition='outside'
        )

        fig6.update_layout(
            title={
            'text': "Produit avec le plus de retours",
            'x': 0.5,
            'xanchor': 'center'
        },

            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',

            font=dict(color="#1F2937"),

            coloraxis_showscale=False,

            xaxis_title=None,
            yaxis_title=None
        )

        st.plotly_chart(
            fig6,
            use_container_width=True,
            config={'displayModeBar': False}
        )

# =========================
# ANALYSE
# =========================

with tab3:

    st.title("📈Analyse")




with tab4:

    st.title("📖Dataset")

    st.dataframe(
        df_filtre,
        use_container_width=True
    )