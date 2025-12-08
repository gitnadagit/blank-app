import streamlit as st
import pandas as pd
import datetime
import json
import hashlib
import time
from pathlib import Path

# ========== CONFIGURATION ==========
st.set_page_config(
    page_title="GMAO Pro",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ========== STYLE CSS ==========
st.markdown("""
<style>
    /* Styles globaux */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .login-container {
        background: white;
        border-radius: 20px;
        padding: 40px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        margin: auto;
        max-width: 450px;
    }
    
    .logo-container {
        text-align: center;
        margin-bottom: 30px;
    }
    
    .logo {
        width: 80px;
        height: 80px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 15px;
        color: white;
        font-size: 35px;
    }
    
    .login-title {
        text-align: center;
        color: #2d3748;
        font-size: 28px;
        font-weight: 700;
        margin-bottom: 5px;
    }
    
    .login-subtitle {
        text-align: center;
        color: #718096;
        margin-bottom: 30px;
    }
    
    .input-label {
        color: #4a5568;
        font-weight: 600;
        margin-bottom: 8px;
        display: block;
    }
    
    .stTextInput>div>div>input, .stTextInput>div>div>input:focus {
        border-radius: 10px;
        border: 2px solid #e2e8f0;
        padding: 12px;
        font-size: 16px;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    .login-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 12px !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        width: 100% !important;
        margin-top: 20px !important;
        transition: all 0.3s ease !important;
    }
    
    .login-button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3) !important;
    }
    
    .demo-accounts {
        background: #f7fafc;
        border-radius: 10px;
        padding: 15px;
        margin-top: 20px;
        border-left: 4px solid #667eea;
    }
    
    .error-message {
        background: #fed7d7;
        color: #c53030;
        padding: 12px;
        border-radius: 8px;
        margin: 15px 0;
        border-left: 4px solid #c53030;
    }
    
    .success-message {
        background: #c6f6d5;
        color: #22543d;
        padding: 12px;
        border-radius: 8px;
        margin: 15px 0;
        border-left: 4px solid #38a169;
    }
    
    .footer {
        text-align: center;
        margin-top: 30px;
        color: #718096;
        font-size: 14px;
    }
    
    /* Animation */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fade-in {
        animation: fadeIn 0.6s ease-out;
    }
    
    /* Badges */
    .role-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        margin-left: 10px;
    }
    
    .role-admin { background: #fed7d7; color: #c53030; }
    .role-technicien { background: #bee3f8; color: #2c5282; }
    .role-manager { background: #c6f6d5; color: #22543d; }
</style>
""", unsafe_allow_html=True)

# ========== GESTION DES UTILISATEURS ==========
class UserManager:
    def __init__(self):
        self.users_file = Path("users.json")
        self.load_users()
    
    def load_users(self):
        """Charge les utilisateurs depuis le fichier JSON"""
        if self.users_file.exists():
            with open(self.users_file, 'r', encoding='utf-8') as f:
                self.users = json.load(f)
        else:
            # Créer des utilisateurs par défaut
            self.users = [
                {
                    "id": 1,
                    "username": "admin",
                    "password_hash": self.hash_password("admin123"),
                    "role": "admin",
                    "full_name": "Administrateur Principal",
                    "email": "admin@gmao.com",
                    "avatar": "👑",
                    "last_login": None,
                    "created_at": datetime.datetime.now().isoformat(),
                    "is_active": True
                },
                {
                    "id": 2,
                    "username": "technicien",
                    "password_hash": self.hash_password("tech123"),
                    "role": "technicien",
                    "full_name": "Jean Dupont",
                    "email": "jean.dupont@gmao.com",
                    "avatar": "🔧",
                    "last_login": None,
                    "created_at": datetime.datetime.now().isoformat(),
                    "is_active": True,
                    "specialite": "Électromécanique"
                },
                {
                    "id": 3,
                    "username": "manager",
                    "password_hash": self.hash_password("manager123"),
                    "role": "manager",
                    "full_name": "Marie Martin",
                    "email": "marie.martin@gmao.com",
                    "avatar": "📊",
                    "last_login": None,
                    "created_at": datetime.datetime.now().isoformat(),
                    "is_active": True,
                    "departement": "Maintenance"
                },
                {
                    "id": 4,
                    "username": "technicien2",
                    "password_hash": self.hash_password("tech456"),
                    "role": "technicien",
                    "full_name": "Paul Bernard",
                    "email": "paul.bernard@gmao.com",
                    "avatar": "⚡",
                    "last_login": None,
                    "created_at": datetime.datetime.now().isoformat(),
                    "is_active": True,
                    "specialite": "Informatique Industrielle"
                }
            ]
            self.save_users()
    
    def save_users(self):
        """Sauvegarde les utilisateurs dans le fichier JSON"""
        with open(self.users_file, 'w', encoding='utf-8') as f:
            json.dump(self.users, f, ensure_ascii=False, indent=2)
    
    def hash_password(self, password):
        """Hash un mot de passe"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def authenticate(self, username, password):
        """Authentifie un utilisateur"""
        user = next((u for u in self.users if u["username"] == username and u["is_active"]), None)
        
        if user and user["password_hash"] == self.hash_password(password):
            # Mettre à jour la dernière connexion
            user["last_login"] = datetime.datetime.now().isoformat()
            self.save_users()
            return user
        return None
    
    def get_user_by_username(self, username):
        """Récupère un utilisateur par son username"""
        return next((u for u in self.users if u["username"] == username), None)
    
    def register_user(self, user_data):
        """Enregistre un nouvel utilisateur"""
        # Vérifier si l'utilisateur existe déjà
        if any(u["username"] == user_data["username"] for u in self.users):
            return False, "Ce nom d'utilisateur existe déjà"
        
        # Créer le nouvel utilisateur
        new_user = {
            "id": max(u["id"] for u in self.users) + 1,
            "username": user_data["username"],
            "password_hash": self.hash_password(user_data["password"]),
            "role": user_data.get("role", "technicien"),
            "full_name": user_data["full_name"],
            "email": user_data.get("email", ""),
            "avatar": user_data.get("avatar", "👤"),
            "last_login": None,
            "created_at": datetime.datetime.now().isoformat(),
            "is_active": True
        }
        
        self.users.append(new_user)
        self.save_users()
        return True, new_user

# Initialiser le gestionnaire d'utilisateurs
user_manager = UserManager()

# ========== PAGE D'AUTHENTIFICATION AMÉLIORÉE ==========
def show_login_page():
    """Affiche la page de connexion améliorée"""
    
    # Container principal centré
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="login-container fade-in">', unsafe_allow_html=True)
        
        # Logo et titre
        st.markdown('<div class="logo-container">', unsafe_allow_html=True)
        st.markdown('<div class="logo">🏭</div>', unsafe_allow_html=True)
        st.markdown('<h1 class="login-title">GMAO PRO</h1>', unsafe_allow_html=True)
        st.markdown('<p class="login-subtitle">Gestion de Maintenance Assistée par Ordinateur</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Onglets Connexion/Inscription
        tab1, tab2 = st.tabs(["🔐 Connexion", "📝 Nouveau compte"])
        
        with tab1:
            show_login_form()
        
        with tab2:
            show_register_form()
        
        # Informations de démonstration
        st.markdown('<div class="demo-accounts">', unsafe_allow_html=True)
        st.markdown("**Comptes de démonstration :**")
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("**👑 Admin**")
            st.caption("admin / admin123")
            st.markdown("**🔧 Technicien**")
            st.caption("technicien / tech123")
        
        with col_b:
            st.markdown("**📊 Manager**")
            st.caption("manager / manager123")
            st.markdown("**⚡ Technicien 2**")
            st.caption("technicien2 / tech456")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Footer
        st.markdown('<div class="footer">', unsafe_allow_html=True)
        st.markdown("© 2024 GMAO Pro • Version 2.0 • Sécurisé avec SHA-256")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

def show_login_form():
    """Affiche le formulaire de connexion CORRIGÉ"""
    with st.form("login_form"):
        st.markdown('<div class="input-label">Nom d\'utilisateur</div>', unsafe_allow_html=True)
        username = st.text_input("", key="login_username", placeholder="Entrez votre nom d'utilisateur", label_visibility="collapsed")
        
        st.markdown('<div class="input-label">Mot de passe</div>', unsafe_allow_html=True)
        password = st.text_input("", type="password", key="login_password", placeholder="Entrez votre mot de passe", label_visibility="collapsed")
        
        # Options supplémentaires (EN DEHORS DU FORM)
        col1, col2 = st.columns(2)
        with col1:
            remember_me = st.checkbox("Se souvenir de moi", value=True)
        
        # Bouton de connexion (submit du form)
        submitted = st.form_submit_button("🔓 Se connecter", type="primary", use_container_width=True)
        
        if submitted:
            if not username or not password:
                st.markdown('<div class="error-message">Veuillez remplir tous les champs</div>', unsafe_allow_html=True)
            else:
                with st.spinner("Authentification en cours..."):
                    time.sleep(0.5)  # Simulation de délai
                    user = user_manager.authenticate(username, password)
                    
                    if user:
                        # Enregistrer dans la session
                        st.session_state.authenticated = True
                        st.session_state.user = {
                            "id": user["id"],
                            "username": user["username"],
                            "role": user["role"],
                            "full_name": user["full_name"],
                            "avatar": user["avatar"]
                        }
                        st.session_state.last_login = datetime.datetime.now()
                        
                        # Message de succès
                        st.markdown(f'''
                        <div class="success-message">
                            ✅ Connexion réussie !<br>
                            Bienvenue <strong>{user["full_name"]}</strong>
                        </div>
                        ''', unsafe_allow_html=True)
                        
                        # Redirection après un court délai
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.markdown('<div class="error-message">❌ Identifiants incorrects. Veuillez réessayer.</div>', unsafe_allow_html=True)
    
    # Bouton "Mot de passe oublié" EN DEHORS du formulaire
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("❓ Mot de passe oublié ?", use_container_width=True):
            st.info("Contactez l'administrateur pour réinitialiser votre mot de passe")

def show_register_form():
    """Affiche le formulaire d'inscription"""
    with st.form("register_form"):
        st.markdown("### Créer un nouveau compte")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="input-label">Nom complet</div>', unsafe_allow_html=True)
            full_name = st.text_input("", key="reg_fullname", placeholder="Prénom Nom", label_visibility="collapsed")
        
        with col2:
            st.markdown('<div class="input-label">Adresse email</div>', unsafe_allow_html=True)
            email = st.text_input("", key="reg_email", placeholder="email@entreprise.com", label_visibility="collapsed")
        
        st.markdown('<div class="input-label">Nom d\'utilisateur</div>', unsafe_allow_html=True)
        username = st.text_input("", key="reg_username", placeholder="Choisissez un nom d'utilisateur", label_visibility="collapsed")
        
        col3, col4 = st.columns(2)
        with col3:
            st.markdown('<div class="input-label">Mot de passe</div>', unsafe_allow_html=True)
            password = st.text_input("", type="password", key="reg_password", placeholder="Minimum 8 caractères", label_visibility="collapsed")
        
        with col4:
            st.markdown('<div class="input-label">Confirmer le mot de passe</div>', unsafe_allow_html=True)
            confirm_password = st.text_input("", type="password", key="reg_confirm", placeholder="Retapez le mot de passe", label_visibility="collapsed")
        
        st.markdown('<div class="input-label">Rôle</div>', unsafe_allow_html=True)
        role = st.selectbox("", ["technicien", "manager"], key="reg_role", label_visibility="collapsed")
        
        # Bouton d'inscription
        submitted = st.form_submit_button("📝 Créer le compte", type="primary", use_container_width=True)
        
        if submitted:
            # Validation
            if not all([full_name, username, password, confirm_password]):
                st.markdown('<div class="error-message">Veuillez remplir tous les champs obligatoires</div>', unsafe_allow_html=True)
            elif password != confirm_password:
                st.markdown('<div class="error-message">Les mots de passe ne correspondent pas</div>', unsafe_allow_html=True)
            elif len(password) < 8:
                st.markdown('<div class="error-message">Le mot de passe doit contenir au moins 8 caractères</div>', unsafe_allow_html=True)
            else:
                # Créer le compte
                success, result = user_manager.register_user({
                    "username": username,
                    "password": password,
                    "role": role,
                    "full_name": full_name,
                    "email": email,
                    "avatar": "👤"
                })
                
                if success:
                    st.markdown(f'''
                    <div class="success-message">
                        ✅ Compte créé avec succès !<br>
                        Vous pouvez maintenant vous connecter avec :<br>
                        <strong>{username}</strong>
                    </div>
                    ''', unsafe_allow_html=True)
                    st.balloons()
                else:
                    st.markdown(f'<div class="error-message">❌ {result}</div>', unsafe_allow_html=True)

# ========== PAGE PRINCIPALE DE L'APPLICATION ==========
def show_main_app():
    """Affiche l'application principale après connexion"""
    
    # Sidebar avec informations utilisateur
    with st.sidebar:
        st.markdown("### 👤 Profil")
        
        user = st.session_state.user
        
        # Avatar et infos
        col1, col2 = st.columns([1, 3])
        with col1:
            st.markdown(f'<div style="font-size: 40px; text-align: center;">{user["avatar"]}</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown(f'**{user["full_name"]}**')
            role_badge_class = f"role-{user['role']}"
            st.markdown(f'<span class="role-badge {role_badge_class}">{user["role"].capitalize()}</span>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Menu de navigation
        st.markdown("### 📋 Navigation")
        
        menu_options = ["🏠 Tableau de bord", "🔧 Interventions", "🏭 Équipements", "📦 Stocks"]
        
        if user["role"] == "admin":
            menu_options.extend(["👥 Utilisateurs", "⚙️ Administration"])
        
        selected_menu = st.radio(
            "Menu",
            menu_options,
            label_visibility="collapsed"
        )
        
        st.session_state.selected_menu = selected_menu
        
        st.markdown("---")
        
        # Statistiques rapides
        st.markdown("### 📊 Aperçu")
        col_stat1, col_stat2 = st.columns(2)
        with col_stat1:
            st.metric("Interventions", "24")
        with col_stat2:
            st.metric("En cours", "8")
        
        st.markdown("---")
        
        # Bouton déconnexion
        if st.button("🚪 Déconnexion", type="secondary", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
        
        # Informations de session
        if 'last_login' in st.session_state:
            st.caption(f"Dernière connexion: {st.session_state.last_login.strftime('%H:%M')}")

    # Contenu principal
    st.title(f"🏭 GMAO Pro - Tableau de bord")
    
    # Bienvenue personnalisée
    st.markdown(f"### Bonjour {user['full_name']} ! 👋")
    st.markdown(f"*Prêt à gérer votre maintenance aujourd'hui ?*")
    
    # Contenu selon le menu sélectionné
    menu = st.session_state.get('selected_menu', '🏠 Tableau de bord')
    
    if menu == "🏠 Tableau de bord":
        show_dashboard()
    elif menu == "🔧 Interventions":
        show_interventions()
    elif menu == "🏭 Équipements":
        show_equipements()
    elif menu == "📦 Stocks":
        show_stocks()
    elif menu == "👥 Utilisateurs":
        if user["role"] == "admin":
            show_users()
        else:
            st.error("Accès non autorisé")
    elif menu == "⚙️ Administration":
        if user["role"] == "admin":
            show_admin()
        else:
            st.error("Accès non autorisé")

# ========== PAGES DE L'APPLICATION ==========
def show_dashboard():
    """Affiche le tableau de bord"""
    st.header("📊 Tableau de bord")
    
    # Métriques principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Interventions totales", "156", "+12%")
    
    with col2:
        st.metric("En cours", "24", "+3")
    
    with col3:
        st.metric("Urgentes", "8", "+2")
    
    with col4:
        st.metric("Taux de résolution", "94%", "+2%")
    
    # Graphiques
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.subheader("Interventions par statut")
        status_data = pd.DataFrame({
            "Statut": ["Terminées", "En cours", "À planifier", "En attente"],
            "Nombre": [120, 24, 8, 4]
        })
        st.bar_chart(status_data.set_index("Statut"))
    
    with col_chart2:
        st.subheader("Équipements par état")
        equip_data = pd.DataFrame({
            "État": ["Opérationnel", "Maintenance", "Hors service"],
            "Nombre": [45, 8, 2]
        })
        st.bar_chart(equip_data.set_index("État"))
    
    # Dernières interventions
    st.subheader("🔄 Dernières interventions")
    
    interventions = pd.DataFrame({
        "ID": ["INT-0456", "INT-0455", "INT-0454", "INT-0453"],
        "Équipement": ["Presse hydraulique", "Tour CNC", "Four industriel", "Robot KUKA"],
        "Description": ["Panne moteur", "Révision annuelle", "Chauffage défectueux", "Calibration"],
        "Technicien": ["Jean Dupont", "Marie Martin", "Paul Bernard", "Sophie Laurent"],
        "Statut": ["En cours", "Terminé", "À planifier", "En cours"],
        "Priorité": ["🔴 Haute", "🟢 Basse", "🟡 Moyenne", "🔴 Haute"]
    })
    
    st.dataframe(interventions, use_container_width=True)

def show_interventions():
    """Affiche la page interventions"""
    st.header("🔧 Gestion des interventions")
    
    # Actions rapides
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("➕ Nouvelle intervention", use_container_width=True):
            st.session_state.show_new_intervention = True
    
    with col2:
        if st.button("📥 Exporter les données", use_container_width=True):
            st.success("Export lancé !")
    
    with col3:
        if st.button("🔄 Actualiser", use_container_width=True):
            st.rerun()
    
    # Formulaire de nouvelle intervention
    if st.session_state.get('show_new_intervention', False):
        with st.form("new_intervention_form"):
            st.subheader("Nouvelle intervention")
            
            col_a, col_b = st.columns(2)
            with col_a:
                equipement = st.selectbox("Équipement", ["Presse hydraulique", "Tour CNC", "Four industriel", "Robot KUKA"])
                type_inter = st.selectbox("Type", ["Maintenance préventive", "Réparation", "Contrôle", "Révision"])
            
            with col_b:
                technicien = st.selectbox("Technicien", ["Jean Dupont", "Marie Martin", "Paul Bernard", "Sophie Laurent"])
                priorite = st.select_slider("Priorité", ["Basse", "Moyenne", "Haute"])
            
            description = st.text_area("Description", height=100)
            
            col_submit1, col_submit2 = st.columns([1, 1])
            with col_submit1:
                submit_create = st.form_submit_button("✅ Créer", type="primary", use_container_width=True)
                if submit_create:
                    st.success("Intervention créée avec succès !")
                    st.session_state.show_new_intervention = False
                    st.rerun()
            
            with col_submit2:
                submit_cancel = st.form_submit_button("❌ Annuler", use_container_width=True)
                if submit_cancel:
                    st.session_state.show_new_intervention = False
                    st.rerun()
    
    # Liste des interventions
    st.subheader("Liste des interventions")
    
    interventions = pd.DataFrame({
        "ID": ["INT-0456", "INT-0455", "INT-0454", "INT-0453", "INT-0452", "INT-0451"],
        "Équipement": ["Presse hydraulique", "Tour CNC", "Four industriel", "Robot KUKA", "Compresseur", "Système convoyeur"],
        "Type": ["Réparation", "Maintenance", "Révision", "Calibration", "Contrôle", "Réparation"],
        "Technicien": ["Jean Dupont", "Marie Martin", "Paul Bernard", "Sophie Laurent", "Jean Dupont", "Paul Bernard"],
        "Date": ["25/11/2024", "24/11/2024", "23/11/2024", "22/11/2024", "21/11/2024", "20/11/2024"],
        "Statut": ["En cours", "Terminé", "À planifier", "En cours", "Terminé", "Terminé"],
        "Priorité": ["🔴 Haute", "🟢 Basse", "🟡 Moyenne", "🔴 Haute", "🟢 Basse", "🟡 Moyenne"]
    })
    
    # Filtres
    col_filtre1, col_filtre2, col_filtre3 = st.columns(3)
    with col_filtre1:
        statut_filtre = st.multiselect("Filtrer par statut", interventions["Statut"].unique(), default=["En cours"])
    
    with col_filtre2:
        priorite_filtre = st.multiselect("Filtrer par priorité", ["🔴 Haute", "🟡 Moyenne", "🟢 Basse"])
    
    with col_filtre3:
        technicien_filtre = st.multiselect("Filtrer par technicien", interventions["Technicien"].unique())
    
    # Application des filtres
    filtered_data = interventions.copy()
    if statut_filtre:
        filtered_data = filtered_data[filtered_data["Statut"].isin(statut_filtre)]
    if priorite_filtre:
        filtered_data = filtered_data[filtered_data["Priorité"].isin(priorite_filtre)]
    if technicien_filtre:
        filtered_data = filtered_data[filtered_data["Technicien"].isin(technicien_filtre)]
    
    st.dataframe(filtered_data, use_container_width=True, height=300)

def show_equipements():
    """Affiche la page équipements"""
    st.header("🏭 Parc d'équipements")
    
    equipements = pd.DataFrame({
        "ID": ["EQ-001", "EQ-002", "EQ-003", "EQ-004", "EQ-005"],
        "Nom": ["Presse hydraulique", "Tour CNC", "Four industriel", "Robot KUKA", "Compresseur"],
        "Type": ["Formage", "Usinage", "Traitement thermique", "Assemblage", "Utilitaire"],
        "Localisation": ["Atelier A", "Atelier B", "Zone chauffage", "Ligne 2", "Salle technique"],
        "État": ["✅ Opérationnel", "⚠️ Maintenance", "✅ Opérationnel", "✅ Opérationnel", "❌ Hors service"],
        "Dernière maintenance": ["15/10/2024", "01/11/2024", "20/09/2024", "15/11/2024", "05/11/2024"]
    })
    
    st.dataframe(equipements, use_container_width=True)

def show_stocks():
    """Affiche la page stocks"""
    st.header("📦 Gestion des stocks")
    
    stocks = pd.DataFrame({
        "Référence": ["R001-2024", "R002-2024", "R003-2024", "R004-2024", "R005-2024"],
        "Désignation": ["Roulement 6205", "Courroie B85", "Filtre à air", "Joint étanchéité", "Capteur température"],
        "Quantité": [15, 8, 22, 45, 12],
        "Seuil minimum": [5, 3, 10, 20, 5],
        "État": ["✅ Suffisant", "⚠️ Critique", "✅ Suffisant", "✅ Suffisant", "⚠️ Critique"],
        "Localisation": ["Rack A1", "Rack B3", "Rack C2", "Rack D4", "Rack E5"]
    })
    
    # Alertes
    stocks_critiques = stocks[stocks["État"] == "⚠️ Critique"]
    if len(stocks_critiques) > 0:
        st.error(f"🚨 {len(stocks_critiques)} articles en stock critique !")
    
    st.dataframe(stocks, use_container_width=True)

def show_users():
    """Affiche la page utilisateurs (admin seulement)"""
    st.header("👥 Gestion des utilisateurs")
    
    users = user_manager.users
    
    # Convertir en DataFrame pour affichage
    users_df = pd.DataFrame(users)
    users_display = users_df[["id", "username", "full_name", "role", "email", "last_login", "is_active"]].copy()
    
    st.dataframe(users_display, use_container_width=True)
    
    # Actions d'administration
    with st.expander("⚙️ Actions administrateur"):
        col_admin1, col_admin2 = st.columns(2)
        
        with col_admin1:
            if st.button("🔄 Recharger les utilisateurs", use_container_width=True):
                user_manager.load_users()
                st.success("Utilisateurs rechargés !")
        
        with col_admin2:
            if st.button("📊 Statistiques", use_container_width=True):
                st.metric("Total utilisateurs", len(users))
                st.metric("Techniciens", len([u for u in users if u["role"] == "technicien"]))
                st.metric("Managers", len([u for u in users if u["role"] == "manager"]))

def show_admin():
    """Affiche la page administration (admin seulement)"""
    st.header("⚙️ Administration")
    
    tab1, tab2, tab3 = st.tabs(["Système", "Sécurité", "Backup"])
    
    with tab1:
        st.subheader("Informations système")
        st.metric("Version", "2.0.0")
        st.metric("Utilisateurs actifs", len([u for u in user_manager.users if u["is_active"]]))
        st.metric("Dernière sauvegarde", "Aujourd'hui 08:30")
    
    with tab2:
        st.subheader("Paramètres de sécurité")
        password_min = st.number_input("Longueur minimale mot de passe", min_value=6, max_value=20, value=8)
        max_attempts = st.number_input("Tentatives de connexion max", min_value=1, max_value=10, value=3)
        session_timeout = st.number_input("Timeout session (minutes)", min_value=5, max_value=240, value=60)
        
        if st.button("💾 Sauvegarder les paramètres"):
            st.success("Paramètres sauvegardés !")
    
    with tab3:
        st.subheader("Sauvegarde et restauration")
        
        col_backup1, col_backup2 = st.columns(2)
        
        with col_backup1:
            if st.button("💾 Sauvegarder maintenant", use_container_width=True):
                st.success("Sauvegarde effectuée !")
        
        with col_backup2:
            if st.button("🔄 Restaurer", use_container_width=True):
                st.warning("Cette action va écraser les données actuelles !")
                if st.button("Confirmer la restauration"):
                    st.success("Restauration effectuée !")

# ========== POINT D'ENTRÉE ==========
def main():
    """Point d'entrée principal"""
    
    # Initialiser l'état d'authentification
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    
    # Afficher la page appropriée
    if st.session_state.authenticated:
        show_main_app()
    else:
        show_login_page()

if __name__ == "__main__":
    main()
