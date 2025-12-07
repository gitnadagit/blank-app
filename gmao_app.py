import streamlit as st
import pandas as pd
import datetime

# ========== CONFIGURATION ==========
st.set_page_config(
    page_title="GMAO Pro",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== STYLE ==========
st.markdown("""
<style>
    .main-title {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
    }
    .metric-card {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# ========== TITRE ==========
st.markdown('<h1 class="main-title">🏭 GMAO PRO - Gestion de Maintenance</h1>', unsafe_allow_html=True)
st.markdown("**Application complète • Présentation pour mardi**")

# ========== DONNÉES ==========
if 'interventions' not in st.session_state:
    interventions_data = {
        'ID': ['INT001', 'INT002', 'INT003', 'INT004', 'INT005'],
        'Équipement': ['Presse hydraulique', 'Tour CNC', 'Four industriel', 'Robot KUKA', 'Compresseur'],
        'Description': ['Panne moteur', 'Révision annuelle', 'Résistances usées', 'Calibration bras', 'Fuite huile'],
        'Technicien': ['Jean Dupont', 'Marie Martin', 'Paul Bernard', 'Sophie Laurent', 'Marc Dubois'],
        'Date': ['25/11/2024', '26/11/2024', '27/11/2024', '28/11/2024', '29/11/2024'],
        'Statut': ['En cours', 'Terminé', 'À planifier', 'En cours', 'En attente'],
        'Priorité': ['🔴 Haute', '🟢 Basse', '🟡 Moyenne', '🔴 Haute', '🔴 Haute'],
        'Durée (h)': [8, 4, 12, 6, 24],
        'Coût (€)': [850, 300, 1200, 650, 1800]
    }
    st.session_state.interventions = pd.DataFrame(interventions_data)

if 'equipements' not in st.session_state:
    equipements_data = {
        'ID': ['EQ001', 'EQ002', 'EQ003', 'EQ004', 'EQ005'],
        'Nom': ['Presse hydraulique', 'Tour CNC', 'Four industriel', 'Robot KUKA', 'Compresseur'],
        'Localisation': ['Atelier A', 'Atelier B', 'Zone chauffage', 'Ligne 2', 'Salle tech'],
        'État': ['✅ Opérationnel', '⚠️ Maintenance', '✅ Opérationnel', '✅ Opérationnel', '❌ Hors service']
    }
    st.session_state.equipements = pd.DataFrame(equipements_data)

# ========== MENU ==========
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3067/3067256.png", width=80)
    st.markdown("### 📋 **NAVIGATION**")
    st.markdown("---")
    
    menu = st.radio(
        "Menu",
        ["🏠 TABLEAU DE BORD", "🔧 INTERVENTIONS", "🏭 ÉQUIPEMENTS", "➕ NOUVELLE", "📊 STATS"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.metric("Interventions", len(st.session_state.interventions))
    st.metric("Équipements", len(st.session_state.equipements))
    st.markdown("---")
    st.caption("GMAO Pro • Présentation mardi")

# ========== DASHBOARD ==========
if menu == "🏠 TABLEAU DE BORD":
    st.header("📊 Tableau de bord")
    
    # KPI
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total interventions", len(st.session_state.interventions), "+2")
    
    with col2:
        en_cours = len(st.session_state.interventions[st.session_state.interventions['Statut'] == 'En cours'])
        st.metric("En cours", en_cours)
    
    with col3:
        urgentes = len(st.session_state.interventions[st.session_state.interventions['Priorité'] == '🔴 Haute'])
        st.metric("Urgentes", urgentes, delta="+1")
    
    with col4:
        cout_total = st.session_state.interventions['Coût (€)'].sum()
        st.metric("Coût total", f"{cout_total:,} €".replace(",", " "))
    
    # Graphiques natifs Streamlit (sans plotly)
    st.subheader("📈 Répartition par statut")
    statut_counts = st.session_state.interventions['Statut'].value_counts()
    st.bar_chart(statut_counts)
    
    st.subheader("👨‍🔧 Interventions par technicien")
    tech_counts = st.session_state.interventions['Technicien'].value_counts()
    st.bar_chart(tech_counts)
    
    # Tableau
    st.subheader("🔄 Dernières interventions")
    st.dataframe(st.session_state.interventions, use_container_width=True)

# ========== INTERVENTIONS ==========
elif menu == "🔧 INTERVENTIONS":
    st.header("🔧 Gestion des interventions")
    
    # Filtres
    col1, col2 = st.columns(2)
    with col1:
        statut_filtre = st.multiselect(
            "Statut",
            options=st.session_state.interventions['Statut'].unique(),
            default=['En cours', 'En attente']
        )
    
    with col2:
        priorite_filtre = st.multiselect(
            "Priorité",
            options=st.session_state.interventions['Priorité'].unique(),
            default=['🔴 Haute', '🟡 Moyenne']
        )
    
    # Filtrage
    df_filtre = st.session_state.interventions.copy()
    if statut_filtre:
        df_filtre = df_filtre[df_filtre['Statut'].isin(statut_filtre)]
    if priorite_filtre:
        df_filtre = df_filtre[df_filtre['Priorité'].isin(priorite_filtre)]
    
    # Affichage
    st.dataframe(df_filtre, use_container_width=True, height=400)
    
    # Actions
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Actualiser", use_container_width=True):
            st.rerun()
    
    with col2:
        csv = df_filtre.to_csv(index=False)
        st.download_button(
            "📥 Exporter CSV",
            data=csv,
            file_name="interventions.csv",
            mime="text/csv",
            use_container_width=True
        )

# ========== ÉQUIPEMENTS ==========
elif menu == "🏭 ÉQUIPEMENTS":
    st.header("🏭 Parc d'équipements")
    
    st.dataframe(st.session_state.equipements, use_container_width=True)
    
    # Ajout équipement
    with st.expander("➕ Ajouter un équipement"):
        col1, col2 = st.columns(2)
        with col1:
            nom = st.text_input("Nom")
            localisation = st.text_input("Localisation")
        with col2:
            etat = st.selectbox("État", ["✅ Opérationnel", "⚠️ Maintenance", "❌ Hors service"])
        
        if st.button("Ajouter"):
            new_eq = pd.DataFrame({
                'ID': [f'EQ{len(st.session_state.equipements)+1:03d}'],
                'Nom': [nom],
                'Localisation': [localisation],
                'État': [etat]
            })
            st.session_state.equipements = pd.concat([st.session_state.equipements, new_eq])
            st.success(f"Équipement {nom} ajouté !")

# ========== NOUVELLE INTERVENTION ==========
elif menu == "➕ NOUVELLE":
    st.header("➕ Créer une intervention")
    
    with st.form("nouvelle_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            equipement = st.selectbox("Équipement", st.session_state.equipements['Nom'].tolist())
            type_inter = st.selectbox("Type", ["Panne", "Maintenance", "Révision", "Contrôle"])
            priorite = st.select_slider("Priorité", ['🟢 Basse', '🟡 Moyenne', '🔴 Haute'])
        
        with col2:
            technicien = st.selectbox("Technicien", ["Jean Dupont", "Marie Martin", "Paul Bernard", "Sophie Laurent"])
            date_inter = st.date_input("Date", datetime.date.today())
            duree = st.slider("Durée estimée (h)", 1, 24, 4)
        
        description = st.text_area("Description", height=100)
        
        submitted = st.form_submit_button("✅ CRÉER", type="primary")
        
        if submitted and description:
            new_id = f"INT{len(st.session_state.interventions)+1:03d}"
            nouvelle = pd.DataFrame({
                'ID': [new_id],
                'Équipement': [equipement],
                'Description': [description],
                'Technicien': [technicien],
                'Date': [date_inter.strftime('%d/%m/%Y')],
                'Statut': ['À planifier'],
                'Priorité': [priorite],
                'Durée (h)': [duree],
                'Coût (€)': [duree * 75]  # Simulation
            })
            st.session_state.interventions = pd.concat([st.session_state.interventions, nouvelle])
            st.success(f"✅ Intervention {new_id} créée !")
            st.balloons()
        elif submitted:
            st.error("Veuillez remplir la description")

# ========== STATS ==========
elif menu == "📊 STATS":
    st.header("📊 Statistiques")
    
    # Calculs
    taux_termine = len(st.session_state.interventions[st.session_state.interventions['Statut'] == 'Terminé']) / len(st.session_state.interventions) * 100
    duree_moyenne = st.session_state.interventions['Durée (h)'].mean()
    cout_moyen = st.session_state.interventions['Coût (€)'].mean()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Taux d'achèvement", f"{taux_termine:.1f}%")
    with col2:
        st.metric("Durée moyenne", f"{duree_moyenne:.1f}h")
    with col3:
        st.metric("Coût moyen", f"{cout_moyen:.0f} €")
    
    # Graphiques
    st.subheader("Évolution des coûts")
    st.line_chart(st.session_state.interventions['Coût (€)'])
    
    st.subheader("Export des données")
    if st.button("📥 Exporter toutes les données"):
        csv_all = st.session_state.interventions.to_csv(index=False)
        st.download_button(
            "Télécharger CSV complet",
            data=csv_all,
            file_name="gmao_complet.csv",
            mime="text/csv"
        )

# ========== FOOTER ==========
st.markdown("---")
st.caption("© 2024 GMAO Pro • Version 1.0 • Présentation mardi • Développé avec Streamlit")
st.toast("Application prête !", icon="✅")
