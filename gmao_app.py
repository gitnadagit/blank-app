import streamlit as st
import pandas as pd
import datetime
import json
import os
import hashlib
from pathlib import Path

# ========== CONFIGURATION ==========
st.set_page_config(
    page_title="GMAO Pro",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== FONCTIONS DE SAUVEGARDE ==========
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

USERS_FILE = DATA_DIR / "users.json"
INTERVENTIONS_FILE = DATA_DIR / "interventions.json"
EQUIPEMENTS_FILE = DATA_DIR / "equipements.json"
STOCKS_FILE = DATA_DIR / "stocks.json"

def load_json(file_path):
    """Charge les données depuis un fichier JSON"""
    try:
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        st.error(f"Erreur de chargement: {e}")
    return []

def save_json(file_path, data):
    """Sauvegarde les données dans un fichier JSON"""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        st.error(f"Erreur de sauvegarde: {e}")
        return False

def hash_password(password):
    """Hash un mot de passe (simplifié pour la démo)"""
    return hashlib.sha256(password.encode()).hexdigest()

# ========== INITIALISATION DES UTILISATEURS ==========
def init_users():
    """Initialise les utilisateurs par défaut"""
    default_users = [
        {
            "username": "admin",
            "password_hash": hash_password("admin123"),
            "role": "admin",
            "full_name": "Administrateur GMAO",
            "email": "admin@gmao.com"
        },
        {
            "username": "technicien",
            "password_hash": hash_password("tech123"),
            "role": "technicien",
            "full_name": "Jean Dupont",
            "email": "jean@gmao.com"
        },
        {
            "username": "manager",
            "password_hash": hash_password("manager123"),
            "role": "manager",
            "full_name": "Marie Martin",
            "email": "marie@gmao.com"
        }
    ]
    
    if not USERS_FILE.exists():
        save_json(USERS_FILE, default_users)
    
    return load_json(USERS_FILE)

# ========== INITIALISATION DES DONNÉES ==========
def init_default_data():
    """Initialise les données par défaut"""
    # Interventions
    default_interventions = [
        {
            "ID": "INT001",
            "Équipement": "Presse hydraulique 100T",
            "Description": "Panne moteur principal",
            "Technicien": "Jean Dupont",
            "Date": "25/11/2024",
            "Statut": "En cours",
            "Priorité": "🔴 Haute",
            "Durée (h)": 8,
            "Coût estimé (€)": 850,
            "Créé par": "admin",
            "Date création": "24/11/2024"
        },
        {
            "ID": "INT002",
            "Équipement": "Tour CNC 5 axes",
            "Description": "Révision annuelle programmée",
            "Technicien": "Marie Martin",
            "Date": "26/11/2024",
            "Statut": "Terminé",
            "Priorité": "🟢 Basse",
            "Durée (h)": 4,
            "Coût estimé (€)": 300,
            "Créé par": "admin",
            "Date création": "23/11/2024"
        }
    ]
    
    # Équipements
    default_equipements = [
        {
            "ID": "EQ001",
            "Nom": "Presse hydraulique 100T",
            "Localisation": "Atelier A - Zone 1",
            "Type": "Formage",
            "État": "✅ Opérationnel",
            "Date installation": "15/03/2020",
            "Prochaine maintenance": "15/01/2025"
        }
    ]
    
    # Stocks
    default_stocks = [
        {
            "Référence": "R001-2024",
            "Désignation": "Roulement 6205-2RS",
            "Quantité": 15,
            "Seuil minimum": 5,
            "Unité": "pièce",
            "Localisation": "Rack A1-3",
            "Fournisseur": "SKF France",
            "Prix unitaire (€)": 45.50
        }
    ]
    
    if not INTERVENTIONS_FILE.exists():
        save_json(INTERVENTIONS_FILE, default_interventions)
    
    if not EQUIPEMENTS_FILE.exists():
        save_json(EQUIPEMENTS_FILE, default_equipements)
    
    if not STOCKS_FILE.exists():
        save_json(STOCKS_FILE, default_stocks)

# ========== PAGE DE CONNEXION ==========
def login_page():
    """Affiche la page de connexion"""
    st.title("🔐 Connexion - GMAO Pro")
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.container():
            st.subheader("Identifiez-vous")
            
            username = st.text_input("Nom d'utilisateur")
            password = st.text_input("Mot de passe", type="password")
            
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                if st.button("🔓 Se connecter", use_container_width=True):
                    users = load_json(USERS_FILE)
                    user = next((u for u in users if u["username"] == username), None)
                    
                    if user and user["password_hash"] == hash_password(password):
                        st.session_state["authenticated"] = True
                        st.session_state["user"] = {
                            "username": user["username"],
                            "role": user["role"],
                            "full_name": user["full_name"]
                        }
                        st.success(f"Bienvenue {user['full_name']} !")
                        st.rerun()
                    else:
                        st.error("Identifiants incorrects")
            
            with col_btn2:
                if st.button("🆕 Compte démo", use_container_width=True):
                    st.info("Utilisez : admin / admin123")
            
            st.markdown("---")
            st.caption("**Comptes de démonstration :**")
            st.caption("• Admin : admin / admin123")
            st.caption("• Technicien : technicien / tech123")
            st.caption("• Manager : manager / manager123")

# ========== FONCTIONS POUR L'APPLICATION ==========
def load_data():
    """Charge toutes les données depuis les fichiers"""
    if 'interventions' not in st.session_state:
        st.session_state.interventions = pd.DataFrame(load_json(INTERVENTIONS_FILE))
    
    if 'equipements' not in st.session_state:
        st.session_state.equipements = pd.DataFrame(load_json(EQUIPEMENTS_FILE))
    
    if 'stocks' not in st.session_state:
        stocks_data = load_json(STOCKS_FILE)
        for item in stocks_data:
            item["Valeur stock"] = item["Quantité"] * item["Prix unitaire (€)"]
        st.session_state.stocks = pd.DataFrame(stocks_data)

def save_data():
    """Sauvegarde toutes les données"""
    if 'interventions' in st.session_state:
        interventions_list = st.session_state.interventions.to_dict('records')
        save_json(INTERVENTIONS_FILE, interventions_list)
    
    if 'equipements' in st.session_state:
        equipements_list = st.session_state.equipements.to_dict('records')
        save_json(EQUIPEMENTS_FILE, equipements_list)
    
    if 'stocks' in st.session_state:
        stocks_list = st.session_state.stocks.to_dict('records')
        # Retirer la colonne calculée avant sauvegarde
        for item in stocks_list:
            item.pop("Valeur stock", None)
        save_json(STOCKS_FILE, stocks_list)

def logout():
    """Déconnexion de l'utilisateur"""
    for key in list(st.session_state.keys()):
        if key != 'rerun':
            del st.session_state[key]
    st.rerun()

# ========== SIDEBAR AVEC MENU ==========
def show_sidebar():
    """Affiche la sidebar avec le menu"""
    with st.sidebar:
        # En-tête avec info utilisateur
        col1, col2 = st.columns([1, 3])
        with col1:
            st.image("https://cdn-icons-png.flaticon.com/512/3067/3067256.png", width=50)
        with col2:
            user = st.session_state.user
            st.write(f"**{user['full_name']}**")
            st.caption(f"Rôle: {user['role']}")
        
        st.markdown("---")
        
        # Menu selon le rôle
        if user["role"] == "admin":
            menu_options = [
                "🏠 Tableau de bord",
                "🔧 Interventions",
                "🏭 Équipements",
                "📦 Stocks",
                "➕ Nouvelle intervention",
                "👥 Gestion des utilisateurs",
                "⚙️ Administration",
                "📊 Rapports"
            ]
        elif user["role"] == "manager":
            menu_options = [
                "🏠 Tableau de bord",
                "🔧 Interventions",
                "🏭 Équipements",
                "📦 Stocks",
                "📊 Rapports"
            ]
        else:  # technicien
            menu_options = [
                "🏠 Tableau de bord",
                "🔧 Mes interventions",
                "➕ Nouvelle intervention"
            ]
        
        st.session_state.menu = st.radio(
            "📋 **NAVIGATION**",
            menu_options,
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Statistiques rapides
        if 'interventions' in st.session_state:
            interventions_en_cours = len(
                st.session_state.interventions[
                    st.session_state.interventions['Statut'] == 'En cours'
                ]
            )
            st.metric("🔄 En cours", interventions_en_cours)
        
        # Bouton sauvegarde
        if st.button("💾 Sauvegarder", use_container_width=True):
            save_data()
            st.success("Données sauvegardées !")
        
        # Bouton déconnexion
        if st.button("🚪 Déconnexion", type="secondary", use_container_width=True):
            logout()
        
        st.markdown("---")
        st.caption(f"GMAO Pro • {datetime.date.today().strftime('%d/%m/%Y')}")

# ========== PAGES DE L'APPLICATION ==========
def dashboard_page():
    """Page tableau de bord"""
    st.header("📊 Tableau de bord")
    
    # KPI
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total = len(st.session_state.interventions)
        st.metric("Interventions", total)
    
    with col2:
        en_cours = len(st.session_state.interventions[
            st.session_state.interventions['Statut'] == 'En cours'
        ])
        st.metric("En cours", en_cours)
    
    with col3:
        urgentes = len(st.session_state.interventions[
            st.session_state.interventions['Priorité'] == '🔴 Haute'
        ])
        st.metric("Urgentes", urgentes)
    
    with col4:
        cout_total = st.session_state.interventions['Coût estimé (€)'].sum()
        st.metric("Coût total", f"{cout_total:,.0f} €".replace(",", " "))
    
    # Graphiques
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Par statut")
        statut_counts = st.session_state.interventions['Statut'].value_counts()
        st.bar_chart(statut_counts)
    
    with col2:
        st.subheader("👨‍🔧 Par technicien")
        tech_counts = st.session_state.interventions['Technicien'].value_counts()
        st.bar_chart(tech_counts)
    
    # Dernières interventions
    st.subheader("🔄 Interventions récentes")
    st.dataframe(
        st.session_state.interventions.sort_values('Date', ascending=False).head(10),
        use_container_width=True
    )

def interventions_page():
    """Page gestion des interventions"""
    st.header("🔧 Gestion des interventions")
    
    # Filtres
    col1, col2, col3 = st.columns(3)
    
    with col1:
        statut_filter = st.multiselect(
            "Statut",
            options=st.session_state.interventions['Statut'].unique(),
            default=['En cours']
        )
    
    with col2:
        priorite_filter = st.multiselect(
            "Priorité",
            options=st.session_state.interventions['Priorité'].unique(),
            default=['🔴 Haute', '🟡 Moyenne']
        )
    
    with col3:
        technicien_filter = st.multiselect(
            "Technicien",
            options=st.session_state.interventions['Technicien'].unique()
        )
    
    # Filtrage
    df = st.session_state.interventions.copy()
    
    if statut_filter:
        df = df[df['Statut'].isin(statut_filter)]
    
    if priorite_filter:
        df = df[df['Priorité'].isin(priorite_filter)]
    
    if technicien_filter:
        df = df[df['Technicien'].isin(technicien_filter)]
    
    # Affichage
    st.dataframe(df, use_container_width=True, height=400)
    
    # Actions
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Actualiser", use_container_width=True):
            st.rerun()
    
    with col2:
        csv = df.to_csv(index=False)
        st.download_button(
            "📥 Exporter CSV",
            data=csv,
            file_name="interventions.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col3:
        if st.button("💾 Sauvegarder", use_container_width=True):
            save_data()
            st.success("Données sauvegardées !")

def new_intervention_page():
    """Page création d'intervention"""
    st.header("➕ Nouvelle intervention")
    
    with st.form("nouvelle_intervention", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            equipement = st.selectbox(
                "Équipement *",
                st.session_state.equipements['Nom'].tolist()
            )
            
            type_inter = st.selectbox(
                "Type *",
                ["Maintenance préventive", "Réparation corrective", "Contrôle", "Révision"]
            )
            
            priorite = st.select_slider(
                "Priorité *",
                options=['🟢 Basse', '🟡 Moyenne', '🔴 Haute']
            )
        
        with col2:
            technicien = st.selectbox(
                "Technicien *",
                ["Jean Dupont", "Marie Martin", "Paul Bernard", "Sophie Laurent"]
            )
            
            date_inter = st.date_input("Date *", datetime.date.today())
            
            duree = st.number_input("Durée estimée (h) *", min_value=1, max_value=168, value=4)
        
        description = st.text_area("Description détaillée *", height=100)
        
        submitted = st.form_submit_button("✅ CRÉER L'INTERVENTION", type="primary")
        
        if submitted and description:
            # Générer ID
            new_id = f"INT{len(st.session_state.interventions) + 1:03d}"
            
            # Calcul coût estimé
            cout_estime = duree * 75  # 75€/h en moyenne
            
            # Créer nouvelle intervention
            nouvelle = pd.DataFrame({
                'ID': [new_id],
                'Équipement': [equipement],
                'Description': f"{type_inter}: {description}",
                'Technicien': [technicien],
                'Date': [date_inter.strftime('%d/%m/%Y')],
                'Statut': ['À planifier'],
                'Priorité': [priorite],
                'Durée (h)': [duree],
                'Coût estimé (€)': [cout_estime],
                'Créé par': [st.session_state.user['username']],
                'Date création': [datetime.date.today().strftime('%d/%m/%Y')]
            })
            
            # Ajouter aux données
            st.session_state.interventions = pd.concat(
                [st.session_state.interventions, nouvelle],
                ignore_index=True
            )
            
            # Sauvegarder
            save_data()
            
            st.success(f"✅ Intervention {new_id} créée et sauvegardée !")
            st.balloons()
            
            # Afficher récapitulatif
            with st.expander("📋 Récapitulatif", expanded=True):
                st.write(f"**ID:** {new_id}")
                st.write(f"**Équipement:** {equipement}")
                st.write(f"**Technicien:** {technicien}")
                st.write(f"**Priorité:** {priorite}")
                st.write(f"**Date:** {date_inter.strftime('%d/%m/%Y')}")
                st.write(f"**Coût estimé:** {cout_estime} €")
        
        elif submitted:
            st.error("Veuillez remplir la description")

def users_management_page():
    """Page gestion des utilisateurs (admin seulement)"""
    st.header("👥 Gestion des utilisateurs")
    
    users = load_json(USERS_FILE)
    
    # Affichage des utilisateurs
    st.subheader("Liste des utilisateurs")
    
    for user in users:
        with st.expander(f"👤 {user['full_name']} ({user['username']})"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Rôle:** {user['role']}")
                st.write(f"**Email:** {user['email']}")
            
            with col2:
                if st.button(f"Modifier", key=f"edit_{user['username']}"):
                    st.info("Fonctionnalité à implémenter")
    
    # Ajout d'utilisateur
    st.subheader("➕ Ajouter un utilisateur")
    
    with st.form("add_user_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            new_username = st.text_input("Nom d'utilisateur")
            new_fullname = st.text_input("Nom complet")
            new_email = st.text_input("Email")
        
        with col2:
            new_password = st.text_input("Mot de passe", type="password")
            new_role = st.selectbox("Rôle", ["technicien", "manager", "admin"])
        
        if st.form_submit_button("Ajouter l'utilisateur"):
            if new_username and new_password:
                # Vérifier si l'utilisateur existe déjà
                if any(u["username"] == new_username for u in users):
                    st.error("Cet utilisateur existe déjà")
                else:
                    new_user = {
                        "username": new_username,
                        "password_hash": hash_password(new_password),
                        "role": new_role,
                        "full_name": new_fullname,
                        "email": new_email
                    }
                    users.append(new_user)
                    save_json(USERS_FILE, users)
                    st.success(f"Utilisateur {new_username} ajouté !")
                    st.rerun()
            else:
                st.error("Veuillez remplir tous les champs")

def admin_page():
    """Page administration"""
    st.header("⚙️ Administration")
    
    tab1, tab2, tab3 = st.tabs(["📊 Statistiques", "🧹 Maintenance", "🔧 Configuration"])
    
    with tab1:
        st.subheader("Statistiques système")
        
        # Informations sur les données
        st.write(f"**Interventions:** {len(st.session_state.interventions)}")
        st.write(f"**Équipements:** {len(st.session_state.equipements)}")
        st.write(f"**Articles en stock:** {len(st.session_state.stocks)}")
        
        # Espace disque simulé
        st.progress(65, text="Espace de stockage utilisé: 65%")
    
    with tab2:
        st.subheader("Maintenance des données")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("💾 Sauvegarder maintenant", use_container_width=True):
                save_data()
                st.success("Sauvegarde effectuée !")
            
            if st.button("🔄 Recharger les données", use_container_width=True):
                load_data()
                st.success("Données rechargées !")
        
        with col2:
            if st.button("🗑️ Vider le cache", use_container_width=True):
                st.info("Cache vidé (simulation)")
            
            if st.button("📋 Exporter tout", use_container_width=True):
                st.info("Export complet (simulation)")
    
    with tab3:
        st.subheader("Configuration")
        
        # Thème
        theme = st.selectbox("Thème de l'application", ["Clair", "Sombre", "Auto"])
        
        # Notifications
        notif_email = st.checkbox("Notifications par email", value=True)
        notif_alert = st.checkbox("Alertes urgentes", value=True)
        
        if st.button("💾 Sauvegarder la configuration"):
            st.success("Configuration sauvegardée !")

# ========== APPLICATION PRINCIPALE ==========
def main_app():
    """Application principale après connexion"""
    # Initialisation des données
    init_default_data()
    load_data()
    
    # Sidebar
    show_sidebar()
    
    # Affichage de la page sélectionnée
    menu = st.session_state.get('menu', '🏠 Tableau de bord')
    
    if menu == "🏠 Tableau de bord":
        dashboard_page()
    
    elif menu == "🔧 Interventions" or menu == "🔧 Mes interventions":
        interventions_page()
    
    elif menu == "🏭 Équipements":
        st.header("🏭 Équipements")
        st.dataframe(st.session_state.equipements, use_container_width=True)
    
    elif menu == "📦 Stocks":
        st.header("📦 Gestion des stocks")
        st.dataframe(st.session_state.stocks, use_container_width=True)
    
    elif menu == "➕ Nouvelle intervention":
        new_intervention_page()
    
    elif menu == "👥 Gestion des utilisateurs":
        if st.session_state.user["role"] == "admin":
            users_management_page()
        else:
            st.error("Accès non autorisé")
    
    elif menu == "⚙️ Administration":
        if st.session_state.user["role"] == "admin":
            admin_page()
        else:
            st.error("Accès non autorisé")
    
    elif menu == "📊 Rapports":
        st.header("📊 Rapports")
        
        # Génération de rapport simple
        if st.button("📄 Générer rapport mensuel"):
            st.success("Rapport généré (simulation)")
            
            # Afficher quelques statistiques
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Interventions ce mois", 24)
                st.metric("Taux de résolution", "92%")
            
            with col2:
                st.metric("Coût total", "18,450 €")
                st.metric("Équipements actifs", 15)

# ========== POINT D'ENTRÉE ==========
def main():
    """Point d'entrée principal de l'application"""
    # Initialisation des utilisateurs
    init_users()
    
    # Vérification de l'authentification
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    
    if not st.session_state.authenticated:
        login_page()
    else:
        main_app()

if __name__ == "__main__":
    main()
