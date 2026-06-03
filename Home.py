import streamlit as st


st.set_page_config(
    page_title="Portfolio Data Analyse",
    layout="wide"
)

st.set_page_config(page_title="Portfolio Data Analyse", layout="wide")

st.markdown("""
<style>
section[data-testid="stSidebar"] {
    background: #F7F8FA;
    border-right: 1px solid #E5E7EB;
}

.sidebar-title {
    font-size: 30px;
    font-weight: 800;
    color: #1F2937;
    margin: 8px 0 18px 8px;
}

.sidebar-section {
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 1px;
    text-transform: uppercase;
    color: #6B7280;
    margin: 18px 0 8px 8px;
}

.sidebar-footer {
    position: fixed;
    bottom: 16px;
    left: 16px;
    font-size: 12px;
    color: #9CA3AF;
    line-height: 1.4;
}
</style>
""", unsafe_allow_html=True)


def home():
    st.title("Portfolio Data Analyse")
    st.markdown("""
    Bienvenue sur mon portfolio de projets Data Analyse !
    Cliquez sur un des projets sur le menu à gauche pour accéder à la page. 
    
    <i>
    *Certaines des données peuvent mettre quelques temps à s'afficher.
    </i>
    <br><br>
    </div>
    """, unsafe_allow_html=True)

    

    tab1, tab2, tab3, tab4 = st.tabs([
    "📖Présentation générale",
    "👩‍🎓Parcours académique",
    "💻Expérience professionnelle",
    "🔎Compétences",
    
])

    with tab1:
        st.markdown("""
        <div style='text-align: justify; font-size: 16px; line-height:1.8'>

        Après avoir obtenu mon deuxième Master en Data Analyse, je recherche actuellement un CDI en tant que Data Analyste ou en tant que Chef de projet marketing. Mes deux master me permettent de combiner une vision business et un esprit analytique fort. 
        Je suis capable de m'adresser aux équipes techniques, de vulgariser et de présenter différents insights et KPIs. 
                    
        J'ai créé ce portfolio afin de démontrer mes compétences en nettoyage, analyse de données et de présentation. 
        Il a été réalisé sur Streamlit, une bibliothèque Python qui permet de créer des applications web. 
        Pour chaque projet j'ai également utilisé Numpy et Pandas pour les calculs et Matplotlib et Plotly Express pour les visualisations. 
        
        <br>
        
        </div>
        """, unsafe_allow_html=True)


    with tab2:
        st.markdown(
        """
        <h3 style='color:#A2D2FF; text-align:justify;'>
        Master Business Data Analyst : Mines Paris / Liora
        </h3>
        """,
        unsafe_allow_html=True
        )

        st.markdown("""
        <div style='text-align: justify; font-size: 16px; line-height:1.8'>
        <i>
        sept. 2025 - sept. 2026
        </i>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style='text-align: justify; padding-top:25px; font-size: 16px; line-height:1.8'>
        
        Après avoir décidé de poursuivre une reconversion j'ai choisi ce master en un an délivré par <b>l'École des mines de Paris et l'école Liora</b>. Cette formation m'a permis de renforcer mes connaissances en data analyse, notamment par des <b>cours poussés sur Python, SQL et PowerBI</b>.
        
        La formation a également plusieurs <b>projets d'analyse de données, de data product management mais aussi d'expérience utilisateur</b>. Les formations comprenaient aussi bien des cours sur des outils plus marketing comme </b>Google Analytics, Google Ads<b> que des introductions à l'IA comme le <b>scraping ou l'automatisation de scénarios</b>.
                
        """, unsafe_allow_html=True)


        st.markdown(
        """
        <h3 style='color:#A2D2FF; text-align:justify;'>
        Master Humanités Management business development et marketing interculturel: Université Paris Nanterre
        </h3>
        """,
        unsafe_allow_html=True
        )

        st.markdown("""
        <div style='text-align: justify; font-size: 16px; line-height:1.8'>
        <i>
        sept 2022 - sept 2024
        </i>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style='text-align: justify; padding-top:25px; font-size: 16px; line-height:1.8'>
        Ce Master est aussi un <b>diplôme pluridisciplinaire</b> qui en plus des humanités avait plusieurs cours de <b>marketing, de ressources humaines ou de gestion de projets</b>. J'ai choisi la spécialité Business development et marketing interculturel qui m'a permis de gérer plusieurs projets marketing.
        
        Le master m'a permis d'avoir des connaissances techniques en marketing et de pouvoir les développer encore plus pendant mon <b>alternance</b>. 
        """, unsafe_allow_html=True)
    
        
        st.markdown(
        """
        <h3 style='color:#A2D2FF; text-align:justify;'>
        Licence Humanités droit, économie, gestion: Université Paris Nanterre
        </h3>
        """,
        unsafe_allow_html=True
        )

        st.markdown("""
        <div style='text-align: justify; font-size: 16px; line-height:1.8'>
        <i>
        sept 2019- sept 2022
        </i>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style='text-align: justify; padding-top:25px; font-size: 16px; line-height:1.8'>
        La licence Humanités est une formation sélective comparable à une classe préparatoire. Elle se compose d'un tronc <b>"humanités" (histoire, littéraire, philosophie)</b> tout en intégrant des cours plus analytiques comme de <b>l'économie, du droit et de la gestion</b>. 
        
        Cette formation m'a permis de développper ma <b>culture générale</b> tout en approfondissant mes connaissances dans des domaines plus spécialisés. L'aspect <b>pluridisciplinaire</b> m'a particulièrement plu.   
                        
        """, unsafe_allow_html=True)
        
        
        
        st.markdown(
        """
        <h3 style='color:#A2D2FF; text-align:justify;'>
        Diplôme universitaire Cultures, langues et rhétorique 
        </h3>
        """,
        unsafe_allow_html=True
        )

        st.markdown("""
        <div style='text-align: justify; font-size: 16px; line-height:1.8'>
        <i>
        sept 2019- sept 2022
        </i>
        </div>
        """, unsafe_allow_html=True)

        
        st.markdown("""
        <div style='text-align: justify; padding-top:25px; font-size: 16px; line-height:1.8'>
        Ce diplôme universitaire était complémentaire à la licence Humanités et s'est concentrée sur trois pilliers: l'approfondissement de la <b>littérature et de la civilisation en langues étrangères</b>, un renforcement des langues ancienne et l'apprentissage de la <b>rhétorique</b> pour maîtriser l'art oratoire, les procédés stylistiques et l'analyse de textes complexes.          
                        
        """, unsafe_allow_html=True)



    with tab3:
        st.markdown(
            "<h2 style='color:#A2D2FF;'>Data Analyst - Inditex</h2>",
            unsafe_allow_html=True
        )
        st.markdown("""
        <div style='text-align: justify; font-size: 16px; line-height:1.8'>
        <i>
        Alternance Sept 2025- Sept 2026
        </i>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style='text-align: justify; ; padding-top:25px; font-size: 16px; line-height:1.8'>
        J'ai rejoint Inditex (maison-mère de Zara) en tant que <b>Data Analyst</b> au sein du département Diversité et Inclusion qui s'occupe de gérer plusieurs projets et de mettre en avant les valeurs du groupe. Mon alternance étant une <b>création de poste</b> j'ai pu travailler avec une grande autonomie, proposer des process et gérer plusieurs projets importants. 
        
        J'ai travaillé en étroite collaboration avec le service RH et développement durable. Toutes les analyses que j'ai pu fournir se basaient sur des données issues de la <b>base de données SQL interne</b> qui contient toutes les informations des salariés. Bien comprendre cet outil a été capital afin de faire des extractions afin de <b>calculer et de fournir des KPI justes pour des audits</b>.       
                        
                
        """, unsafe_allow_html=True)

        st.markdown("""
            <div style='text-align: justify; padding-top:25px; font-size:16px; line-height:1.8'>

            <ul>
                <li>Création de <b>dashboard PowerBI</b> de suivi de l'effectif salarial(suivi pour les DRH, pour l'audit GEEIS)</li>
                <li>Extraction et analyse de données RH <b>via SQL</b> dans le cadre d’audits (GEEIS, Index Égalité, etc.)</li>
                <li>Définition et suivi des <b>KPI</b> pour des audits et obligations règlementaires (Index Egalité H/F, Commission handicap, obligation d'emploi des travailleurs handicapés...)</li>
                <li><b>Reporting décisionnel</b> pour la direction (au siège et pour les enseignes)</li>
                <li>Identification des <b>points de vigilance</b> pour les différentes projets du département</li>
                <li>Réponse aux <b>besoins métiers</b> via des analyses ponctuelles sur les données salariés</li>
                <li>Réalisation d’analyses de <b>contrôle de gestion sociale</b> (effectifs, types de contrats, temps de travail)</li>
                <li>Mise en place des <b>process d'analyse<b> de data au sein du département (arrivée dans une création de poste)</li>
                
            </ul>

            </div>
            """, unsafe_allow_html=True)

        st.markdown(
            "<h2 style='color:#A2D2FF;'>Chef de projet marketing - Orsenna (groupe Bechtle)</h2>",
            unsafe_allow_html=True
        )
        st.markdown("""
        <div style='text-align: justify; font-size: 16px; line-height:1.8'>
        <i>
        Alternance Sept 2022 - Sept 2024
        </i>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style='text-align: justify; ; padding-top:25px; font-size: 16px; line-height:1.8'>
        Orsenna est une <b>ESN</b> spécialisée dans le monitoring de parcs informatiques. Durant cette alternance j'avais la charge de tout l'aspect numérique comme le site web, le SEO, les publicités mais également tout l'aspect évènementiel. 
        Pendant ces deux années j'ai pu découvrir le B2B et découvrir le monde de l'informatique. 
        
        J'ai eu l'opportunité d'effectuer une <b>montée en compétence</b> lors du départ de mon responsable et j'ai repris ses sujets comme la <b>gestion des partenariats et l'affectation du budget</b> marketing avec ceux-ci. Cette expérience a été très enrichissante car je ne connaissais pas du tout le B2B et les ESN et la <b>technicité</b> requise pour le marketing et la communication auprès d'experts dans le métier (DSI). L'aspect qui m'a le plus plu était <b>l'analyse des données du site et des performances</b> des évènements et c'est ce qui m'a poussé à effectuer une <b>reconversion</b> dans la data.
                    
        """, unsafe_allow_html=True)

        st.markdown("""
            <div style='text-align: justify; padding-top:25px; font-size:16px; line-height:1.8'>

            <ul>
                <li>Définition du <b>plan marketing</b> (allocation du budget aux partenaires)</li>
                <li>Gestion des sites web, <b>suivi et amélioration du SEO et SEA</b></li>
                <li>Gestion et organisation des évènements (salons, workshop, webinar)</li>
                <li>Gestion des <b>relations partenariales</b> (reporting des actions, mise en place d'actions communes)</li>
                <li>Mise en place du plan de communication externe (newsletter, mailing et réseaux sociaux)</li>
                <li>Rédaction d'articles spécialisés et de success stories</li>
                <li>Collaboration avec les équipes commerciales et techniques</li>
                
            </ul>

            </div>
            """, unsafe_allow_html=True)


    with tab4:

        col1, col2 = st.columns([0.5, 0.5], gap="large")

        with col1:
            st.markdown(
            "<h3 style='color:#A2D2FF;'>Data</h2>",
            unsafe_allow_html=True
            )

            st.markdown("""
            <div style='text-align: justify; font-size:16px; line-height:1.8'>
            <ul>
            <b>Outils</b>
                <li>SGBD: SQL</li>
                <li>Programmation: Python (Pandas, NumPy, Matplotlib, Plotly, Streamlit), R</li>
                <li>Dashboarding: Power BI / Tableau</li>
                <li>Prototypage: Excel avancé, Google Sheets</li>
                <li>Collaboration: Git / GitHub</li>
                        
            <b>Data analyse</b>
                <li>Analyse de données, exploration et interprétation</li>
                <li>Définition et suivi de KPI</li>
                <li>Analyse de performance & détection d’anomalies</li>
                        
            <b>Data Processing & Management</b>
                <li>Nettoyage et préparation de données (data cleaning)</li>
                <li>Fiabilisation des données (data quality)</li>
                <li>Manipulation et structuration de datasets</li>
                        
            <b>Business Intelligence</b>
                <li>Création de dashboards interactifs</li>
                <li>Data visualisation & reporting</li>
                <li>Transformation des données en insights</li>
                        
            <b>Audit & Performance</b>
                <li>Analyse de données en contexte d’audit et conformité</li>
                <li>Suivi d’indicateurs RH (Index égalité, diversité)</li>
                <li>Contrôle et cohérence des indicateurs</li>
            
            </ul>

            </div>
            """, unsafe_allow_html=True)

        with col2:

            st.markdown(
            "<h3 style='color:#A2D2FF;'>Marketing</h2>",
            unsafe_allow_html=True
            )

            st.markdown("""
            <div style='text-align: justify; font-size:16px; line-height:1.8'>
            <ul>
            <b>Outils</b>
                <li>Analyse: Google Analytics, Google tag manager, SemRush</li>
                <li>CMS : Wordpress</li>
                <li>Dashboarding: Power BI / Tableau</li>
                <li>CRM : Salesforce, HubSpot</li>
                <li>Emailing : Mailjet, HubSpot</li>
                        
                        
            <b>Performance Marketing</b>
                <li>Analyse de performance digitale (SEO et SEA)</li>
                <li>Suivi des KPI marketing (acquisition, conversion)</li>
                <li>Optimisation des campagnes</li>
                        
            <b>Web & Acquisition</b>
                <li>Gestion de site web</li>
                <li>Analyse du trafic et comportement utilisateur</li>
                <li>Suivi des leviers d’acquisition</li>
                        
            <b>Data-driven Marketing</b>
                <li>Reporting marketing pour la direction</li>
                <li>Analyse des données clients</li>
                <li>Génération d’insights pour la prise de décision</li>
                        
            <b>Partenariats & Événementiel</b>
                <li>Suivi de performance des partenariats</li>
                <li>Créations d'évènements pour la génération de leads (webinar, salons, workshop)</li>
                <li>Analyse des retombées événements (leads, visibilité)</li>
            
            </ul>

            </div>
            """, unsafe_allow_html=True)

home_page = st.Page(home, title="Home", icon="🏠")
parcoursup_page = st.Page("pages/1_Parcoursup.py", title="Parcoursup", icon="🎓")
index_fh_page = st.Page("pages/2_Index_FH.py", title="Index FH", icon="⚖️")
sales_page = st.Page("pages/3_Sales_Analyse.py", title="Sales Analyse", icon="📈")


pg = st.navigation({
    "Accueil": [home_page],
    "Projets data": [parcoursup_page, index_fh_page, sales_page]
})

st.sidebar.markdown(
    "<div class='sidebar-footer'>Créé par Elise Le Chevillier<br>Business Data Analyst</div>",
    unsafe_allow_html=True
)

pg.run()



