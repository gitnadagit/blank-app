import streamlit as st
import pandas as pd
import datetime
# Supprime les imports plotly

# ========== CONFIGURATION ==========
st.set_page_config(
    page_title="GMAO Pro",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== STYLE CSS ==========
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main-title {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.8rem !important;
        font-weight: 800 !important;
        text-align: center;
        padding: 1rem;
        margin-bottom: 0.5rem;
    }
    
    .subtitle {
        text-align: center;
        color: #6b7280;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    
    .kpi-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        border-left: 5px solid;
        transition: transform 0.3s ease;
    }
    
    .kpi-card:hover {
        transform: translateY(-5px);
    }
    
    .urgent-badge {
        background: linear-gradient(135deg, #fecaca 0%, #fca5a5 100%);
        color: #dc2626;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.875rem;
        font-weight: 600;
    }
    
    .normal-badge {
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
        color: #059669;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.875rem;
        font-weight: 600;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
    
    .stSelectbox, .stTextInput, .stTextArea, .stDateInput {
        border-radius: 10px !important;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);
    }
</style>
""", unsafe_allow_html=True)

# ========== TITRE ==========
st.markdown('<h1 class="main-title">🏭 GMAO PRO - Gestion de Maintenance</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Application complète de gestion de maintenance industrielle • Présentation pour mardi</p>', unsafe_allow_html=True)

# ========== DONNÉES SIMULÉES ==========
if 'interventions' not in st.session_state:
    interventions_data = {
        'ID': ['INT001', 'INT002', 'INT003', 'INT004', 'INT005', 'INT006', 'INT007'],
        'Équipement': ['Presse hydraulique 100T', 'Tour CNC 5 axes', 'Four industriel 800°C', 
                      'Robot soudeur KUKA', 'Compresseur Atlas', 'Système convoyeur', 'Pompe centrifuge'],
        'Description': ['Panne moteur principal', 'Révision annuelle programmée', 'Changement résistances',
                       'Calibration bras robotique', 'Fuite d\'huile détectée', 'Changement rouleaux', 'Bruit anormal'],
        'Technicien': ['Jean DUPONT', 'Marie MARTIN', 'Paul BERNARD', 'Sophie LAURENT', 
                      'Marc DUBOIS', 'Léa PETIT', 'Thomas MOREAU'],
        'Date': ['25/11/2024', '26/11/2024', '27/11/2024', '28/11/2024', 
                '29/11/2024', '30/11/2024', '01/12/2024'],
        'Statut': ['En cours', 'Terminé', 'À planifier', 'En cours', 'En attente pièce', 'Terminé', 'À planifier'],
        'Priorité': ['🔴 Haute', '🟢 Basse', '🟡 Moyenne', '🔴 Haute', '🔴 Haute', '🟢 Basse', '🟡 Moyenne'],
        'Durée (h)': [8, 4, 12, 6, 24, 3, 5],
        'Coût estimé (€)': [850, 300, 1200, 650, 1800, 250, 480]
    }
    st.session_state.interventions = pd.DataFrame(interventions_data)

if 'equipements' not in st.session_state:
    equipements_data = {
        'ID': ['EQ001', 'EQ002', 'EQ003', 'EQ004', 'EQ005', 'EQ006', 'EQ007', 'EQ008'],
        'Nom': ['Presse hydraulique 100T', 'Tour CNC 5 axes', 'Four industriel 800°C', 
               'Robot soudeur KUKA', 'Compresseur Atlas', 'Système convoyeur', 
               'Pompe centrifuge', 'Générateur 500kVA'],
        'Localisation': ['Atelier A - Zone 1', 'Atelier B - Zone 3', 'Zone traitement thermique',
                        'Ligne assemblage 2', 'Salle technique Nord', 'Ligne production 1',
                        'Salle des utilités', 'Local électrique'],
        'Type': ['Formage', 'Usinage', 'Traitement thermique', 'Assemblage', 
                'Utilitaire', 'Manutention', 'Fluidique', 'Énergie'],
        'État': ['✅ Opérationnel', '⚠️ Maintenance', '✅ Opérationnel', '✅ Opérationnel',
                '❌ Hors service', '✅ Opérationnel', '⚠️ Surveillance', '✅ Opérationnel'],
        'Date installation': ['15/03/2020', '22/07/2021', '10/11/2019', '05/09/2022',
                             '18/12/2018', '30/04/2021', '14/08/2020', '25/01/2023'],
        'Prochaine maintenance': ['15/01/2025', '22/01/2025', '10/02/2025', '05/02/2025',
                                 'À déterminer', '30/01/2025', '14/02/2025', '25/03/2025']
    }
    st.session_state.equipements = pd.DataFrame(equipements_data)

if 'stocks' not in st.session_state:
    stocks_data = {
        'Référence': ['R001-2024', 'R002-2024', 'R003-2024', 'R004-2024', 'R005-2024',
                     'R006-2024', 'R007-2024', 'R008-2024', 'R009-2024'],
        'Désignation': ['Roulement 6205-2RS', 'Courroie synchronisée B85', 'Filtre à air industriel',
                       'Joint d\'étanchéité Ø150mm', 'Capteur température PT100', 'Moteur 5.5kW 400V',
                       'Variateur de fréquence', 'Contacteur 25A', 'Câble blindé 4x2.5mm²'],
        'Quantité': [15, 8, 22, 45, 12, 3, 7, 18, 55],
        'Seuil minimum': [5, 3, 10, 20, 5, 2, 4, 10, 30],
        'Unité': ['pièce', 'pièce', 'pièce', 'pièce', 'pièce', 'pièce', 'pièce', 'pièce', 'mètre'],
        'Localisation': ['Rack A1-3', 'Rack B3-2', 'Rack C2-1', 'Rack D4-4', 'Rack E5-1',
                        'Zone stock lourd', 'Armoire électrique', 'Rack F6-2', 'Bobines Zone'],
        'Fournisseur': ['SKF France', 'Gates Europe', 'Donaldson', 'Freudenberg', 'Endress+Hauser',
                       'Siemens', 'ABB', 'Schneider', 'Nexans'],
        'Prix unitaire (€)': [45.50, 32.80, 120.00, 8.75, 89.99, 1250.00, 420.50, 67.30, 4.25]
    }
    st.session_state.stocks = pd.DataFrame(stocks_data)
    st.session_state.stocks['Valeur stock'] = st.session_state.stocks['Quantité'] * st.session_state.stocks['Prix unitaire (€)']

# ========== SIDEBAR ==========
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3067/3067256.png", width=100)
    st.markdown("### 📋 **MENU PRINCIPAL**")
    st.markdown("---")
    
    menu = st.radio(
        "Navigation",
        ["🏠 TABLEAU DE BORD", 
         "🔧 INTERVENTIONS", 
         "🏭 PARC ÉQUIPEMENTS", 
         "📦 GESTION STOCKS", 
         "➕ NOUVELLE INTERVENTION", 
         "📊 ANALYTICS & RAPPORTS"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Stats rapides
    interventions_en_cours = len(st.session_state.interventions[st.session_state.interventions['Statut'].isin(['En cours', 'En attente pièce'])])
    st.metric("🔄 Interventions en cours", interventions_en_cours)
    
    equipements_hors_service = len(st.session_state.equipements[st.session_state.equipements['État'] == '❌ Hors service'])
    st.metric("⚠️ Équipements HS", equipements_hors_service)
    
    st.markdown("---")
    
    # Mode présentation
    presentation_mode = st.checkbox("🎤 Mode présentation", value=True)
    if presentation_mode:
        st.info("**Présentation active**\\n\\nToutes les données sont simulées pour la démonstration.")
    
    st.markdown("---")
    st.caption("**GMAO Pro v1.0** • Présentation mardi")
    st.caption("Développé avec Streamlit")

# ========== PAGE : TABLEAU DE BORD ==========
if menu == "🏠 TABLEAU DE BORD":
    st.header("📊 Tableau de bord de maintenance")
    
    # ===== KPI CARDS =====
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="kpi-card" style="border-left-color: #3b82f6;">', unsafe_allow_html=True)
        st.metric("Total interventions", len(st.session_state.interventions), "+12% vs mois dernier")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="kpi-card" style="border-left-color: #10b981;">', unsafe_allow_html=True)
        taux_termine = (len(st.session_state.interventions[st.session_state.interventions['Statut'] == 'Terminé']) / 
                       len(st.session_state.interventions) * 100)
        st.metric("Taux d'achèvement", f"{taux_termine:.1f}%", "+5.2%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="kpi-card" style="border-left-color: #f59e0b;">', unsafe_allow_html=True)
        cout_total = st.session_state.interventions['Coût estimé (€)'].sum()
        st.metric("Coût total estimé", f"{cout_total:,} €".replace(",", " "))
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="kpi-card" style="border-left-color: #ef4444;">', unsafe_allow_html=True)
        valeur_stock = st.session_state.stocks['Valeur stock'].sum()
        st.metric("Valeur du stock", f"{valeur_stock:,.0f} €".replace(",", " "))
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ===== GRAPHIQUES =====
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Répartition par priorité")
        priorite_data = st.session_state.interventions['Priorité'].value_counts()
        
        fig1 = go.Figure(data=[
            go.Pie(
                labels=priorite_data.index,
                values=priorite_data.values,
                hole=.4,
                marker_colors=['#ef4444', '#f59e0b', '#10b981']
            )
        ])
        
        fig1.update_layout(
            height=400,
            showlegend=True,
            margin=dict(t=0, b=0, l=0, r=0)
        )
        
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        st.subheader("👨‍🔧 Charge par technicien")
        
        tech_work = st.session_state.interventions.groupby('Technicien')['Durée (h)'].sum().reset_index()
        tech_work = tech_work.sort_values('Durée (h)', ascending=True)
        
        fig2 = go.Figure(data=[
            go.Bar(
                y=tech_work['Technicien'],
                x=tech_work['Durée (h)'],
                orientation='h',
                marker_color='#3b82f6',
                text=tech_work['Durée (h)'],
                textposition='auto'
            )
        ])
        
        fig2.update_layout(
            height=400,
            xaxis_title="Heures de travail",
            margin=dict(t=0, b=0, l=0, r=0)
        )
        
        st.plotly_chart(fig2, use_container_width=True)
    
    # ===== INTERVENTIONS RÉCENTES =====
    st.subheader("🕐 Interventions récentes")
    
    # Style conditionnel pour le dataframe
    def color_priority(val):
        if '🔴' in str(val):
            return 'background-color: #fecaca; color: #dc2626; font-weight: bold;'
        elif '🟡' in str(val):
            return 'background-color: #fef3c7; color: #d97706;'
        elif '🟢' in str(val):
            return 'background-color: #d1fae5; color: #059669;'
        return ''
    
    styled_df = st.session_state.interventions.style.applymap(color_priority, subset=['Priorité'])
    
    st.dataframe(
        styled_df,
        use_container_width=True,
        height=300,
        column_config={
            "ID": st.column_config.TextColumn("ID", width="small"),
            "Équipement": st.column_config.TextColumn("Équipement", width="medium"),
            "Priorité": st.column_config.TextColumn("Priorité", width="small"),
            "Statut": st.column_config.TextColumn("Statut", width="small"),
            "Coût estimé (€)": st.column_config.NumberColumn("Coût (€)", format="%d €")
        }
    )
    
    # ===== ALERTES =====
    with st.expander("🚨 Alertes & Actions requises", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.warning("**Équipements critiques**")
            equipements_critiques = st.session_state.equipements[
                st.session_state.equipements['État'] == '❌ Hors service'
            ]
            if len(equipements_critiques) > 0:
                for _, eq in equipements_critiques.iterrows():
                    st.write(f"• **{eq['Nom']}** - {eq['Localisation']}")
            else:
                st.success("Aucun équipement hors service")
        
        with col2:
            st.error("**Stocks critiques**")
            stocks_critiques = st.session_state.stocks[
                st.session_state.stocks['Quantité'] <= st.session_state.stocks['Seuil minimum']
            ]
            if len(stocks_critiques) > 0:
                for _, stock in stocks_critiques.iterrows():
                    st.write(f"• **{stock['Désignation']}** : {stock['Quantité']} restants")
            else:
                st.success("Tous les stocks sont suffisants")

# ========== PAGE : INTERVENTIONS ==========
elif menu == "🔧 INTERVENTIONS":
    st.header("🔧 Gestion des interventions")
    
    tab1, tab2, tab3 = st.tabs(["📋 Liste", "🔍 Filtres avancés", "📝 Historique"])
    
    with tab1:
        # Actions rapides
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col2:
            if st.button("🔄 Actualiser", use_container_width=True):
                st.rerun()
        
        with col3:
            csv = st.session_state.interventions.to_csv(index=False)
            st.download_button(
                label="📥 Exporter CSV",
                data=csv,
                file_name="interventions_export.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        # Affichage avec filtres simples
        col1, col2, col3 = st.columns(3)
        
        with col1:
            statut_filter = st.multiselect(
                "Filtrer par statut",
                options=st.session_state.interventions['Statut'].unique(),
                default=['En cours', 'En attente pièce']
            )
        
        with col2:
            priorite_filter = st.multiselect(
                "Filtrer par priorité",
                options=st.session_state.interventions['Priorité'].unique(),
                default=['🔴 Haute', '🟡 Moyenne']
            )
        
        with col3:
            technicien_filter = st.multiselect(
                "Filtrer par technicien",
                options=st.session_state.interventions['Technicien'].unique(),
                default=st.session_state.interventions['Technicien'].unique()
            )
        
        # Application des filtres
        filtered_df = st.session_state.interventions.copy()
        
        if statut_filter:
            filtered_df = filtered_df[filtered_df['Statut'].isin(statut_filter)]
        
        if priorite_filter:
            filtered_df = filtered_df[filtered_df['Priorité'].isin(priorite_filter)]
        
        if technicien_filter:
            filtered_df = filtered_df[filtered_df['Technicien'].isin(technicien_filter)]
        
        # Affichage
        st.dataframe(
            filtered_df,
            use_container_width=True,
            height=500,
            column_order=["ID", "Équipement", "Description", "Technicien", "Date", "Statut", "Priorité", "Durée (h)", "Coût estimé (€)"]
        )
        
        # Résumé
        st.info(f"**{len(filtered_df)} interventions** correspondant aux critères • "
               f"**Durée totale : {filtered_df['Durée (h)'].sum()}h** • "
               f"**Coût estimé : {filtered_df['Coût estimé (€)'].sum():,.0f} €**")
    
    with tab2:
        st.subheader("🔍 Recherche avancée")
        
        col1, col2 = st.columns(2)
        
        with col1:
            search_text = st.text_input("Rechercher dans les descriptions")
            date_range = st.date_input(
                "Période",
                [datetime.date(2024, 11, 1), datetime.date(2024, 12, 31)]
            )
        
        with col2:
            min_duration = st.slider("Durée minimum (h)", 0, 48, 0)
            max_cost = st.slider("Coût maximum (€)", 0, 5000, 5000)
        
        if search_text:
            filtered_df = st.session_state.interventions[
                st.session_state.interventions['Description'].str.contains(search_text, case=False)
            ]
        else:
            filtered_df = st.session_state.interventions.copy()
        
        filtered_df = filtered_df[
            (filtered_df['Durée (h)'] >= min_duration) &
            (filtered_df['Coût estimé (€)'] <= max_cost)
        ]
        
        if len(filtered_df) > 0:
            st.dataframe(filtered_df, use_container_width=True)
        else:
            st.warning("Aucune intervention ne correspond aux critères")

# ========== PAGE : PARC ÉQUIPEMENTS ==========
elif menu == "🏭 PARC ÉQUIPEMENTS":
    st.header("🏭 Parc d'équipements")
    
    # Vue d'ensemble
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Carte des équipements")
        
        # Création d'une carte visuelle
        for _, equip in st.session_state.equipements.iterrows():
            with st.expander(f"{equip['État']} {equip['Nom']} - {equip['Localisation']}", expanded=False):
                col_a, col_b, col_c = st.columns(3)
                
                with col_a:
                    st.metric("Type", equip['Type'])
                
                with col_b:
                    st.metric("Installé le", equip['Date installation'])
                
                with col_c:
                    st.metric("Prochaine maintenance", equip['Prochaine maintenance'])
                
                # Actions
                col_x, col_y = st.columns(2)
                with col_x:
                    if st.button(f"📋 Créer intervention", key=f"btn_{equip['ID']}"):
                        st.success(f"Intervention créée pour {equip['Nom']}")
                
                with col_y:
                    if st.button(f"📊 Historique", key=f"hist_{equip['ID']}"):
                        st.info(f"Historique de {equip['Nom']} affiché")
    
    with col2:
        st.subheader("📊 Statistiques")
        
        # Graphique types d'équipements
        type_counts = st.session_state.equipements['Type'].value_counts()
        
        fig = go.Figure(data=[
            go.Bar(
                x=type_counts.values,
                y=type_counts.index,
                orientation='h',
                marker_color='#8b5cf6'
            )
        ])
        
        fig.update_layout(
            height=300,
            margin=dict(t=0, b=0, l=0, r=0),
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Stats rapides
        st.metric("Total équipements", len(st.session_state.equipements))
        
        etat_counts = st.session_state.equipements['État'].value_counts()
        for etat, count in etat_counts.items():
            if '✅' in etat:
                color = "🟢"
            elif '⚠️' in etat:
                color = "🟡"
            else:
                color = "🔴"
            st.write(f"{color} {etat.replace('✅', '').replace('⚠️', '').replace('❌', '')} : {count}")

# ========== PAGE : GESTION STOCKS ==========
elif menu == "📦 GESTION STOCKS":
    st.header("📦 Gestion des stocks")
    
    # Vue d'ensemble
    col1, col2, col3 = st.columns(3)
    
    with col1:
        valeur_totale = st.session_state.stocks['Valeur stock'].sum()
        st.metric("💰 Valeur totale du stock", f"{valeur_totale:,.0f} €".replace(",", " "))
    
    with col2:
        total_pieces = st.session_state.stocks['Quantité'].sum()
        st.metric("📦 Nombre total de pièces", total_pieces)
    
    with col3:
        pieces_critiques = len(st.session_state.stocks[
            st.session_state.stocks['Quantité'] <= st.session_state.stocks['Seuil minimum']
        ])
        st.metric("🚨 Pièces critiques", pieces_critiques, delta=f"+{pieces_critiques}")
    
    # Tableau des stocks
    st.subheader("Inventaire complet")
    
    # Ajouter une colonne de statut
    stocks_df = st.session_state.stocks.copy()
    stocks_df['Statut'] = stocks_df.apply(
        lambda row: '🔴 Critique' if row['Quantité'] <= row['Seuil minimum'] 
                    else '🟡 Attention' if row['Quantité'] <= row['Seuil minimum'] * 1.5 
                    else '🟢 Normal',
        axis=1
    )
    
    # Afficher avec style conditionnel
    def highlight_critical(row):
        if row['Statut'] == '🔴 Critique':
            return ['background-color: #fecaca'] * len(row)
        elif row['Statut'] == '🟡 Attention':
            return ['background-color: #fef3c7'] * len(row)
        return [''] * len(row)
    
    styled_stocks = stocks_df.style.apply(highlight_critical, axis=1)
    
    st.dataframe(
        styled_stocks,
        use_container_width=True,
        height=400,
        column_order=["Référence", "Désignation", "Quantité", "Seuil minimum", "Statut", 
                     "Localisation", "Fournisseur", "Prix unitaire (€)", "Valeur stock"]
    )
    
    # Commandes à passer
    with st.expander("📋 Suggestions de commandes", expanded=True):
        commandes = stocks_df[stocks_df['Statut'].isin(['🔴 Critique', '🟡 Attention'])]
        
        if len(commandes) > 0:
            st.write("**Pièces à réapprovisionner en priorité :**")
            
            for _, piece in commandes.iterrows():
                quantite_commande = max(piece['Seuil minimum'] * 3 - piece['Quantité'], 10)
                cout_commande = quantite_commande * piece['Prix unitaire (€)']
                
                col1, col2, col3 = st.columns([3, 1, 2])
                
                with col1:
                    st.write(f"**{piece['Désignation']}**")
                    st.caption(f"Stock actuel: {piece['Quantité']} | Seuil: {piece['Seuil minimum']}")
                
                with col2:
                    st.metric("Commander", f"{quantite_commande}")
                
                with col3:
                    st.write(f"**{cout_commande:.2f} €**")
                    st.caption(f"Fournisseur: {piece['Fournisseur']}")
                
                st.divider()
        else:
            st.success("✅ Tous les stocks sont suffisants !")

# ========== PAGE : NOUVELLE INTERVENTION ==========
elif menu == "➕ NOUVELLE INTERVENTION":
    st.header("➕ Créer une nouvelle intervention")
    
    with st.form("nouvelle_intervention_form", clear_on_submit=True):
        # En-tête
        st.markdown("### 📝 Remplissez tous les champs pour créer une intervention")
        
        # Colonnes principales
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📋 Informations générales")
            
            equipement = st.selectbox(
                "Équipement concerné *",
                st.session_state.equipements['Nom'].tolist(),
                help="Sélectionnez l'équipement nécessitant une intervention"
            )
            
            type_intervention = st.selectbox(
                "Type d'intervention *",
                ['Maintenance préventive', 'Réparation corrective', 'Contrôle réglementaire',
                 'Révision annuelle', 'Amélioration continue', 'Dépannage urgent', 'Autre']
            )
            
            priorite = st.select_slider(
                "Niveau de priorité *",
                options=['🟢 Basse', '🟡 Moyenne', '🔴 Haute', '⚫ Critique'],
                value='🟡 Moyenne'
            )
        
        with col2:
            st.subheader("👨‍🔧 Ressources & Planning")
            
            technicien = st.selectbox(
                "Technicien assigné *",
                ['Jean DUPONT', 'Marie MARTIN', 'Paul BERNARD', 
                 'Sophie LAURENT', 'Marc DUBOIS', 'Léa PETIT', 'Thomas MOREAU',
                 'Équipe externe', 'À affecter']
            )
            
            col_a, col_b = st.columns(2)
            with col_a:
                date_debut = st.date_input(
                    "Date de début *",
                    datetime.date.today()
                )
            
            with col_b:
                date_fin = st.date_input(
                    "Date de fin estimée *",
                    datetime.date.today() + datetime.timedelta(days=3)
                )
            
            duree_estimee = st.number_input(
                "Durée estimée (heures) *",
                min_value=1,
                max_value=168,
                value=8,
                step=1
            )
        
        # Description détaillée
        st.subheader("📄 Description & Instructions")
        
        description = st.text_area(
            "Description détaillée de l'intervention *",
            height=150,
            placeholder="""Exemple :
1. Symptômes observés : bruit anormal lors du démarrage
2. Causes suspectées : roulements usés
3. Actions à réaliser :
   - Vérifier l'état des roulements
   - Contrôler l'alignement
   - Remplacer si nécessaire
4. Consommables nécessaires : roulements 6205 (2 unités), graisse"""
        )
        
        # Pièces nécessaires
        st.subheader("📦 Pièces détachées nécessaires")
        
        pieces_selection = st.multiselect(
            "Sélectionnez les pièces nécessaires",
            st.session_state.stocks['Désignation'].tolist(),
            help="Sélectionnez les pièces à utiliser pour cette intervention"
        )
        
        if pieces_selection:
            st.write("**Pièces sélectionnées :**")
            for piece in pieces_selection:
                stock_info = st.session_state.stocks[
                    st.session_state.stocks['Désignation'] == piece
                ].iloc[0]
                
                col_x, col_y, col_z = st.columns([3, 1, 1])
                with col_x:
                    st.write(f"• {piece}")
                with col_y:
                    quantite = st.number_input(
                        f"Quantité {piece[:20]}...",
                        min_value=1,
                        max_value=int(stock_info['Quantité']),
                        value=1,
                        key=f"qty_{piece}"
                    )
                with col_z:
                    st.write(f"Stock: {stock_info['Quantité']}")
        
        # Coût estimé
        st.subheader("💰 Coût estimé")
        
        col_c, col_d, col_e = st.columns(3)
        
        with col_c:
            cout_main_doeuvre = st.number_input(
                "Coût main d'œuvre (€)",
                min_value=0.0,
                value=450.0,
                step=50.0
            )
        
        with col_d:
            cout_pieces = st.number_input(
                "Coût pièces (€)",
                min_value=0.0,
                value=0.0,
                step=10.0
            )
        
        with col_e:
            cout_total = cout_main_doeuvre + cout_pieces
            st.metric("Coût total estimé", f"{cout_total:.2f} €")
        
        # Boutons de soumission
        st.markdown("---")
        
        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        
        with col_btn2:
            submitted = st.form_submit_button(
                "✅ **CRÉER L'INTERVENTION**",
                type="primary",
                use_container_width=True
            )
        
        if submitted:
            if description.strip() == "":
                st.error("❌ Veuillez saisir une description détaillée")
            else:
                # Génération ID
                new_id = f"INT{len(st.session_state.interventions) + 1:03d}"
                
                # Ajout à la base
                nouvelle_intervention = pd.DataFrame({
                    'ID': [new_id],
                    'Équipement': [equipement],
                    'Description': [description],
                    'Technicien': [technicien],
                    'Date': [date_debut.strftime('%d/%m/%Y')],
                    'Statut': ['À planifier'],
                    'Priorité': [priorite],
                    'Durée (h)': [duree_estimee],
                    'Coût estimé (€)': [cout_total]
                })
                
                st.session_state.interventions = pd.concat(
                    [st.session_state.interventions, nouvelle_intervention],
                    ignore_index=True
                )
                
                # Message de succès
                st.success(f"""
                🎉 **INTERVENTION CRÉÉE AVEC SUCCÈS !**
                
                **Détails :**
                - **ID :** {new_id}
                - **Équipement :** {equipement}
                - **Technicien :** {technicien}
                - **Priorité :** {priorite}
                - **Date début :** {date_debut.strftime('%d/%m/%Y')}
                - **Coût estimé :** {cout_total:.2f} €
                """)
                
                st.balloons()
                
                # Option pour créer une autre intervention
                if st.button("➕ Créer une autre intervention"):
                    st.rerun()

# ========== PAGE : ANALYTICS ==========
elif menu == "📊 ANALYTICS & RAPPORTS":
    st.header("📊 Analytics & Rapports")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Performances", "💰 Coûts", "📅 Planning", "📄 Exports"])
    
    with tab1:
        st.subheader("Indicateurs de performance")
        
        # KPI
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            mtbf = 450  # Mean Time Between Failures (simulé)
            st.metric("MTBF", f"{mtbf} h", "+25h")
        
        with col2:
            mttr = 4.2  # Mean Time To Repair (simulé)
            st.metric("MTTR", f"{mttr} h", "-0.8h")
        
        with col3:
            disponibilite = 96.8  # Disponibilité (simulée)
            st.metric("Disponibilité", f"{disponibilite}%", "+1.2%")
        
        with col4:
            cout_maintenance = 12500  # Coût maintenance/mois (simulé)
            st.metric("Coût mensuel", f"{cout_maintenance:,} €".replace(",", " "))
        
        # Graphique évolution
        st.subheader("Évolution sur 12 mois")
        
        mois_data = pd.DataFrame({
            'Mois': ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Jun', 
                    'Jul', 'Aoû', 'Sep', 'Oct', 'Nov', 'Déc'],
            'Interventions': [18, 22, 25, 28, 30, 32, 30, 28, 35, 38, 42, 45],
            'Coût (k€)': [8.2, 9.5, 10.2, 11.8, 12.5, 13.2, 
                         12.8, 11.9, 14.2, 15.5, 16.8, 18.2],
            'Disponibilité %': [94.2, 94.8, 95.1, 95.5, 95.8, 96.2,
                               96.5, 96.8, 97.1, 97.3, 97.5, 97.8]
        })
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=mois_data['Mois'],
            y=mois_data['Interventions'],
            name='Interventions',
            line=dict(color='#3b82f6', width=3),
            mode='lines+markers'
        ))
        
        fig.add_trace(go.Scatter(
            x=mois_data['Mois'],
            y=mois_data['Coût (k€)'],
            name='Coût (k€)',
            yaxis='y2',
            line=dict(color='#ef4444', width=3, dash='dot'),
            mode='lines+markers'
        ))
        
        fig.update_layout(
            height=400,
            yaxis=dict(title="Nombre d'interventions"),
            yaxis2=dict(
                title="Coût (k€)",
                overlaying='y',
                side='right'
            ),
            hovermode='x unified',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("Analyse des coûts")
        
        # Répartition des coûts
        couts_categories = pd.DataFrame({
            'Catégorie': ['Main d\'œuvre', 'Pièces détachées', 'Sous-traitance', 
                         'Formation', 'Outillage', 'Contrôles'],
            'Montant (k€)': [65.2, 42.8, 28.5, 12.3, 8.7, 5.5],
            'Évolution': ['+5.2%', '+8.7%', '-2.1%', '0%', '+1.5%', '+3.2%']
        })
        
        fig = px.sunburst(
            couts_categories,
            path=['Catégorie'],
            values='Montant (k€)',
            color='Montant (k€)',
            color_continuous_scale='Reds'
        )
        
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
        
        # Détail
        st.dataframe(couts_categories, use_container_width=True)
    
    with tab3:
        st.subheader("Planning des ressources")
        
        # Planning hebdomadaire simulé
        planning_data = {
            'Lundi': ['INT045\\nPresse', 'INT048\\nRobot', '', 'INT052\\nTour', ''],
            'Mardi': ['INT046\\nFour', '', 'INT049\\nCompresseur', '', 'INT053\\nConvoyeur'],
            'Mercredi': ['', 'INT047\\nPompe', 'INT050\\nGénérateur', 'INT051\\nSystème', ''],
            'Jeudi': ['Réunion\\néquipe', 'INT054\\nPresse', '', 'INT056\\nRobot', 'Formation'],
            'Vendredi': ['INT055\\nFour', '', 'INT057\\nCompresseur', 'Contrôle\\nqualité', '']
        }
        
        planning_df = pd.DataFrame(planning_data, index=['Jean', 'Marie', 'Paul', 'Sophie', 'Marc'])
        
        st.dataframe(
            planning_df,
            use_container_width=True,
            height=300
        )
        
        st.caption("📅 Planning de la semaine du 02/12/2024 au 06/12/2024")
    
    with tab4:
        st.subheader("Exports et rapports")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**📊 Exporter les données :**")
            
            # Export interventions
            interventions_csv = st.session_state.interventions.to_csv(index=False)
            st.download_button(
                label="📥 Interventions (CSV)",
                data=interventions_csv,
                file_name="gmao_interventions.csv",
                mime="text/csv"
            )
            
            # Export équipements
            equipements_csv = st.session_state.equipements.to_csv(index=False)
            st.download_button(
                label="📥 Équipements (CSV)",
                data=equipements_csv,
                file_name="gmao_equipements.csv",
                mime="text/csv"
            )
            
            # Export stocks
            stocks_csv = st.session_state.stocks.to_csv(index=False)
            st.download_button(
                label="📥 Stocks (CSV)",
                data=stocks_csv,
                file_name="gmao_stocks.csv",
                mime="text/csv"
            )
        
        with col2:
            st.write("**📄 Générer des rapports :**")
            
            if st.button("📋 Rapport mensuel"):
                st.success("Rapport mensuel généré ! (simulation)")
            
            if st.button("📈 Tableau de bord PDF"):
                st.success("PDF généré ! (simulation)")
            
            if st.button("🔄 Synthèse trimestrielle"):
                st.success("Synthèse générée ! (simulation)")

# ========== FOOTER ==========
st.markdown("---")
footer_col1, footer_col2, footer_col3 = st.columns(3)

with footer_col1:
    st.caption("© 2024 GMAO Pro - Tous droits réservés")

with footer_col2:
    st.caption("📧 contact@gmaopro.com • 📞 01 23 45 67 89")

with footer_col3:
    st.caption("🔧 Version 1.0 • Présentation technique")

# Message de fin
st.toast("🚀 Application GMAO Pro chargée avec succès !", icon="✅")
