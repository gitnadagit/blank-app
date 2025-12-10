import streamlit as st
import pandas as pd
import datetime
import json
import hashlib
import time
from pathlib import Path

# ========== CONFIGURATION ==========
st.set_page_config(
    page_title="GMAO Pro + Tiers",
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
    
    .supplier-card {
        background: white;
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-left: 5px solid #3B82F6;
        transition: transform 0.3s ease;
    }
    
    .supplier-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0,0,0,0.1);
    }
    
    .supplier-type {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        margin-right: 10px;
    }
    
    .type-fournisseur { background: #DBEAFE; color: #1E40AF; }
    .type-soustraitant { background: #D1FAE5; color: #065F46; }
    
    .delivery-badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 15px;
        font-size: 11px;
        font-weight: 600;
        margin-left: 10px;
    }
    
    .delivery-fast { background: #D1FAE5; color: #065F46; }
    .delivery-medium { background: #FEF3C7; color: #92400E; }
    .delivery-slow { background: #FEE2E2; color: #991B1B; }
    
    .contact-info {
        background: #F8FAFC;
        border-radius: 10px;
        padding: 15px;
        margin-top: 15px;
    }
    
    .contract-status {
        font-size: 12px;
        padding: 4px 10px;
        border-radius: 15px;
        font-weight: 600;
    }
    
    .contract-active { background: #D1FAE5; color: #065F46; }
    .contract-expired { background: #FEE2E2; color: #991B1B; }
    .contract-pending { background: #FEF3C7; color: #92400E; }
</style>
""", unsafe_allow_html=True)

# ========== GESTION DES DONNÉES ==========
class DataManager:
    def __init__(self):
        self.data_dir = Path("data")
        self.data_dir.mkdir(exist_ok=True)
        
        self.users_file = self.data_dir / "users.json"
        self.tiers_file = self.data_dir / "tiers.json"
        
        self.load_all_data()
    
    def load_all_data(self):
        """Charge toutes les données"""
        # Utilisateurs
        if self.users_file.exists():
            with open(self.users_file, 'r', encoding='utf-8') as f:
                self.users = json.load(f)
        else:
            self.users = self.create_default_users()
            self.save_users()
        
        # Tiers (fournisseurs & sous-traitants)
        if self.tiers_file.exists():
            with open(self.tiers_file, 'r', encoding='utf-8') as f:
                self.tiers = json.load(f)
        else:
            self.tiers = self.create_default_tiers()
            self.save_tiers()
    
    def create_default_users(self):
        """Crée les utilisateurs par défaut"""
        return [
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
                "is_active": True
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
                "is_active": True
            }
        ]
    
    def create_default_tiers(self):
        """Crée les tiers par défaut"""
        return {
            "fournisseurs": [
                {
                    "id": 1,
                    "nom": "SKF France",
                    "type": "fournisseur",
                    "specialite": "Roulements et joints",
                    "contact_nom": "Pierre Dubois",
                    "contact_email": "p.dubois@skf.fr",
                    "contact_telephone": "01 23 45 67 89",
                    "adresse": "12 Rue des Industries, 75000 Paris",
                    "delai_livraison_moyen": 3,  # jours
                    "mode_livraison": "Express",
                    "note_fiabilite": 4.8,
                    "contrat_actif": True,
                    "date_debut_contrat": "2023-01-15",
                    "date_fin_contrat": "2025-01-14",
                    "conditions_paiement": "30 jours net",
                    "notes": "Fournisseur principal pour roulements"
                },
                {
                    "id": 2,
                    "nom": "Gates Europe",
                    "type": "fournisseur",
                    "specialite": "Courroies et kits",
                    "contact_nom": "Sophie Lambert",
                    "contact_email": "s.lambert@gates-europe.com",
                    "contact_telephone": "02 34 56 78 90",
                    "adresse": "45 Avenue du Commerce, 69000 Lyon",
                    "delai_livraison_moyen": 5,
                    "mode_livraison": "Standard",
                    "note_fiabilite": 4.5,
                    "contrat_actif": True,
                    "date_debut_contrat": "2023-03-10",
                    "date_fin_contrat": "2024-12-31",
                    "conditions_paiement": "45 jours",
                    "notes": "Livraison gratuite à partir de 500€"
                },
                {
                    "id": 3,
                    "nom": "Donaldson Filtration",
                    "type": "fournisseur",
                    "specialite": "Filtres industriels",
                    "contact_nom": "Thomas Moreau",
                    "contact_email": "t.moreau@donaldson.fr",
                    "contact_telephone": "03 45 67 89 01",
                    "adresse": "78 Boulevard des Usines, 31000 Toulouse",
                    "delai_livraison_moyen": 7,
                    "mode_livraison": "Économique",
                    "note_fiabilite": 4.2,
                    "contrat_actif": True,
                    "date_debut_contrat": "2023-06-20",
                    "date_fin_contrat": "2024-06-19",
                    "conditions_paiement": "60 jours",
                    "notes": "Échantillons gratuits disponibles"
                }
            ],
            "soustraitants": [
                {
                    "id": 101,
                    "nom": "Méca Pro Services",
                    "type": "soustraitant",
                    "specialite": "Maintenance mécanique lourde",
                    "contact_nom": "Robert Chen",
                    "contact_email": "r.chen@mecapro.fr",
                    "contact_telephone": "04 56 78 90 12",
                    "adresse": "123 Rue de la Réparation, 59000 Lille",
                    "intervention_type": "Urgences 24/7",
                    "taux_horaire": 85.00,
                    "zone_intervention": "Région Nord",
                    "certifications": ["ISO 9001", "Qualibat"],
                    "contrat_actif": True,
                    "date_debut_contrat": "2023-02-01",
                    "date_fin_contrat": "2024-11-30",
                    "assurance_rc_pro": True,
                    "montant_assurance": "5 000 000 €",
                    "notes": "Intervention sous 4h garantie"
                },
                {
                    "id": 102,
                    "nom": "Élec Solutions",
                    "type": "soustraitant",
                    "specialite": "Électricité industrielle",
                    "contact_nom": "Laura Petit",
                    "contact_email": "l.petit@elec-solutions.fr",
                    "contact_telephone": "05 67 89 01 23",
                    "adresse": "456 Avenue Volta, 13000 Marseille",
                    "intervention_type": "Maintenance préventive",
                    "taux_horaire": 95.00,
                    "zone_intervention": "Sud-Est",
                    "certifications": ["ISO 14001", "UTE"],
                    "contrat_actif": True,
                    "date_debut_contrat": "2023-04-15",
                    "date_fin_contrat": "2025-04-14",
                    "assurance_rc_pro": True,
                    "montant_assurance": "3 000 000 €",
                    "notes": "Spécialiste automates programmables"
                },
                {
                    "id": 103,
                    "nom": "Hydrau Tech",
                    "type": "soustraitant",
                    "specialite": "Hydraulique industrielle",
                    "contact_nom": "Marc Bernard",
                    "contact_email": "m.bernard@hydrautech.com",
                    "contact_telephone": "06 78 90 12 34",
                    "adresse": "789 Chemin des Presses, 44000 Nantes",
                    "intervention_type": "Dépannage et installation",
                    "taux_horaire": 78.00,
                    "zone_intervention": "Ouest",
                    "certifications": ["ISO 45001"],
                    "contrat_actif": False,
                    "date_debut_contrat": "2022-09-01",
                    "date_fin_contrat": "2023-08-31",
                    "assurance_rc_pro": True,
                    "montant_assurance": "2 500 000 €",
                    "notes": "Contrat à renouveler"
                }
            ]
        }
    
    def hash_password(self, password):
        """Hash un mot de passe"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def save_users(self):
        """Sauvegarde les utilisateurs"""
        with open(self.users_file, 'w', encoding='utf-8') as f:
            json.dump(self.users, f, ensure_ascii=False, indent=2)
    
    def save_tiers(self):
        """Sauvegarde les tiers"""
        with open(self.tiers_file, 'w', encoding='utf-8') as f:
            json.dump(self.tiers, f, ensure_ascii=False, indent=2)
    
    def authenticate(self, username, password):
        """Authentifie un utilisateur"""
        user = next((u for u in self.users if u["username"] == username and u["is_active"]), None)
        
        if user and user["password_hash"] == self.hash_password(password):
            user["last_login"] = datetime.datetime.now().isoformat()
            self.save_users()
            return user
        return None
    
    def get_all_tiers(self):
        """Retourne tous les tiers"""
        all_tiers = self.tiers["fournisseurs"] + self.tiers["soustraitants"]
        return pd.DataFrame(all_tiers)
    
    def get_fournisseurs(self):
        """Retourne tous les fournisseurs"""
        return pd.DataFrame(self.tiers["fournisseurs"])
    
    def get_soustraitants(self):
        """Retourne tous les sous-traitants"""
        return pd.DataFrame(self.tiers["soustraitants"])
    
    def add_tier(self, tier_data):
        """Ajoute un nouveau tier"""
        if tier_data["type"] == "fournisseur":
            # Trouver le prochain ID
            max_id = max([t["id"] for t in self.tiers["fournisseurs"]], default=0)
            tier_data["id"] = max_id + 1
            self.tiers["fournisseurs"].append(tier_data)
        else:
            max_id = max([t["id"] for t in self.tiers["soustraitants"]], default=100)
            tier_data["id"] = max_id + 1
            self.tiers["soustraitants"].append(tier_data)
        
        self.save_tiers()
        return tier_data["id"]
    
    def update_tier(self, tier_id, tier_data):
        """Met à jour un tier"""
        tier_type = tier_data["type"]
        
        if tier_type == "fournisseur":
            for i, tier in enumerate(self.tiers["fournisseurs"]):
                if tier["id"] == tier_id:
                    self.tiers["fournisseurs"][i] = tier_data
                    break
        else:
            for i, tier in enumerate(self.tiers["soustraitants"]):
                if tier["id"] == tier_id:
                    self.tiers["soustraitants"][i] = tier_data
                    break
        
        self.save_tiers()
    
    def delete_tier(self, tier_id, tier_type):
        """Supprime un tier"""
        if tier_type == "fournisseur":
            self.tiers["fournisseurs"] = [t for t in self.tiers["fournisseurs"] if t["id"] != tier_id]
        else:
            self.tiers["soustraitants"] = [t for t in self.tiers["soustraitants"] if t["id"] != tier_id]
        
        self.save_tiers()

# Initialiser le gestionnaire de données
data_manager = DataManager()

# ========== PAGE D'AUTHENTIFICATION ==========
def show_login_page():
    """Affiche la page de connexion"""
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        
        # Logo et titre
        st.markdown('<div class="logo-container">', unsafe_allow_html=True)
        st.markdown('<div class="logo">🏭</div>', unsafe_allow_html=True)
        st.markdown('<h1 style="text-align: center; color: #2d3748;">GMAO PRO + TIERS</h1>', unsafe_allow_html=True)
        st.markdown('<p style="text-align: center; color: #718096;">Gestion complète maintenance et fournisseurs</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Formulaire de connexion
        with st.form("login_form"):
            username = st.text_input("Nom d'utilisateur", value="admin")
            password = st.text_input("Mot de passe", type="password", value="admin123")
            
            submitted = st.form_submit_button("🔓 Se connecter", type="primary", use_container_width=True)
            
            if submitted:
                if not username or not password:
                    st.error("Veuillez remplir tous les champs")
                else:
                    with st.spinner("Connexion..."):
                        time.sleep(0.5)
                        user = data_manager.authenticate(username, password)
                        
                        if user:
                            st.session_state.authenticated = True
                            st.session_state.user = {
                                "id": user["id"],
                                "username": user["username"],
                                "role": user["role"],
                                "full_name": user["full_name"],
                                "avatar": user["avatar"]
                            }
                            st.success(f"✅ Bienvenue {user['full_name']} !")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error("❌ Identifiants incorrects")
        
        # Informations de démo
        st.markdown("---")
        st.markdown("**Comptes de démonstration :**")
        st.caption("👑 **Admin** : admin / admin123")
        st.caption("🔧 **Technicien** : technicien / tech123")
        st.caption("📊 **Manager** : manager / manager123")
        
        st.markdown('</div>', unsafe_allow_html=True)

# ========== PAGES PRINCIPALES ==========
def show_main_app():
    """Affiche l'application principale"""
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 👤 Profil")
        
        user = st.session_state.user
        
        col1, col2 = st.columns([1, 3])
        with col1:
            st.markdown(f'<div style="font-size: 40px; text-align: center;">{user["avatar"]}</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown(f'**{user["full_name"]}**')
            role_color = "#DC2626" if user["role"] == "admin" else "#2563EB" if user["role"] == "manager" else "#059669"
            st.markdown(f'<span style="background: {role_color}20; color: {role_color}; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 600;">{user["role"].capitalize()}</span>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Menu
        st.markdown("### 📋 Navigation")
        
        menu_options = ["🏠 Tableau de bord", "🔧 Interventions", "🏭 Équipements", "📦 Stocks", "🤝 Gestion des Tiers"]
        
        if user["role"] == "admin":
            menu_options.append("⚙️ Administration")
        
        selected_menu = st.radio("Menu", menu_options, label_visibility="collapsed")
        st.session_state.selected_menu = selected_menu
        
        st.markdown("---")
        
        # Déconnexion
        if st.button("🚪 Déconnexion", type="secondary", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
    # Contenu principal
    menu = st.session_state.selected_menu
    
    if menu == "🏠 Tableau de bord":
        show_dashboard()
    elif menu == "🔧 Interventions":
        show_interventions()
    elif menu == "🏭 Équipements":
        show_equipements()
    elif menu == "📦 Stocks":
        show_stocks()
    elif menu == "🤝 Gestion des Tiers":
        show_tiers_management()
    elif menu == "⚙️ Administration" and user["role"] == "admin":
        show_admin()

# ========== GESTION DES TIERS ==========
def show_tiers_management():
    """Affiche la page de gestion des tiers"""
    
    st.title("🤝 Gestion des Tiers")
    st.markdown("**Fournisseurs et sous-traitants**")
    
    # Onglets
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Liste complète", "🏭 Fournisseurs", "👷 Sous-traitants", "➕ Nouveau tier"])
    
    with tab1:
        show_all_tiers()
    
    with tab2:
        show_fournisseurs()
    
    with tab3:
        show_soustraitants()
    
    with tab4:
        show_new_tier_form()

def show_all_tiers():
    """Affiche tous les tiers"""
    st.subheader("📊 Vue d'ensemble des tiers")
    
    all_tiers = data_manager.get_all_tiers()
    
    if all_tiers.empty:
        st.info("Aucun tier enregistré")
        return
    
    # Métriques
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total = len(all_tiers)
        st.metric("Total tiers", total)
    
    with col2:
        fournisseurs = len(all_tiers[all_tiers["type"] == "fournisseur"])
        st.metric("Fournisseurs", fournisseurs)
    
    with col3:
        soustraitants = len(all_tiers[all_tiers["type"] == "soustraitant"])
        st.metric("Sous-traitants", soustraitants)
    
    with col4:
        actifs = len(all_tiers[all_tiers["contrat_actif"] == True])
        st.metric("Contrats actifs", actifs)
    
    # Filtres
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        type_filter = st.multiselect("Type", ["fournisseur", "soustraitant"], default=["fournisseur", "soustraitant"])
    
    with col_f2:
        contrat_filter = st.multiselect("État contrat", ["Actif", "Inactif"], default=["Actif"])
    
    # Application filtres
    filtered = all_tiers.copy()
    
    if type_filter:
        filtered = filtered[filtered["type"].isin(type_filter)]
    
    if "Actif" in contrat_filter or "Inactif" in contrat_filter:
        actif_filter = "Actif" in contrat_filter
        filtered = filtered[filtered["contrat_actif"] == actif_filter]
    
    # Affichage
    if not filtered.empty:
        # Préparer l'affichage - VERSION CORRIGÉE
        display_df = filtered.copy()
        
        # Créer les colonnes d'affichage
        display_cols = ["nom", "type", "specialite", "contact_nom", "contact_telephone", "contrat_actif"]
        
        # Ajouter les colonnes conditionnelles
        if "delai_livraison_moyen" in display_df.columns:
            display_cols.append("delai_livraison_moyen")
        
        if "taux_horaire" in display_df.columns:
            display_cols.append("taux_horaire")
        
        # Sélectionner uniquement les colonnes qui existent
        existing_cols = [col for col in display_cols if col in display_df.columns]
        display_df = display_df[existing_cols]
        
        # Renommer les colonnes
        rename_dict = {
            "nom": "Nom",
            "type": "Type",
            "specialite": "Spécialité",
            "contact_nom": "Contact",
            "contact_telephone": "Téléphone",
            "contrat_actif": "Contrat Actif",
            "delai_livraison_moyen": "Délai livraison",
            "taux_horaire": "Taux horaire"
        }
        
        # Appliquer le renommage uniquement aux colonnes présentes
        rename_mapping = {col: rename_dict[col] for col in existing_cols if col in rename_dict}
        display_df = display_df.rename(columns=rename_mapping)
        
        # Afficher le dataframe
        st.dataframe(display_df, use_container_width=True, height=400)
    else:
        st.warning("Aucun résultat avec ces filtres")

def show_fournisseurs():
    """Affiche la liste des fournisseurs"""
    st.subheader("🏭 Fournisseurs de pièces détachées")
    
    fournisseurs = data_manager.get_fournisseurs()
    
    if fournisseurs.empty:
        st.info("Aucun fournisseur enregistré")
        return
    
    # Affichage par cartes avec Streamlit natif
    for _, fournisseur in fournisseurs.iterrows():
        with st.container():
            # Carte du fournisseur
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"### {fournisseur['nom']}")
                st.markdown(f"**Spécialité:** {fournisseur['specialite']}")
            with col2:
                st.markdown('<span class="type-fournisseur">Fournisseur</span>', unsafe_allow_html=True)
            
            # Métriques
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                delai_color = "🟢" if fournisseur['delai_livraison_moyen'] <= 3 else "🟡" if fournisseur['delai_livraison_moyen'] <= 7 else "🔴"
                st.metric("Délai livraison", f"{delai_color} {fournisseur['delai_livraison_moyen']} jours")
            
            with col_b:
                st.metric("Fiabilité", f"{fournisseur['note_fiabilite']}/5")
            
            with col_c:
                contrat_status = "✅ Actif" if fournisseur['contrat_actif'] else "❌ Inactif"
                st.metric("Contrat", contrat_status)
            
            # Informations de contact
            with st.expander("📞 Informations de contact", expanded=False):
                st.write(f"**Contact:** {fournisseur['contact_nom']}")
                st.write(f"**Email:** {fournisseur['contact_email']}")
                st.write(f"**Téléphone:** {fournisseur['contact_telephone']}")
                st.write(f"**Adresse:** {fournisseur['adresse']}")
                st.write(f"**Conditions paiement:** {fournisseur['conditions_paiement']}")
                st.write(f"**Mode livraison:** {fournisseur['mode_livraison']}")
            
            # Boutons d'action
            col_btn1, col_btn2, col_btn3 = st.columns(3)
            with col_btn1:
                if st.button("📦 Commander", key=f"cmd_{fournisseur['id']}"):
                    st.session_state.selected_supplier = fournisseur['id']
                    st.info(f"Ouverture formulaire commande pour {fournisseur['nom']}")
            
            with col_btn2:
                if st.button("📋 Voir détails", key=f"detail_{fournisseur['id']}"):
                    st.info(f"Détails de {fournisseur['nom']}")
            
            with col_btn3:
                if st.button("📞 Contacter", key=f"contact_{fournisseur['id']}"):
                    st.success(f"Email préparé pour {fournisseur['contact_nom']}")
            
            st.markdown("---")

def show_soustraitants():
    """Affiche la liste des sous-traitants"""
    st.subheader("👷 Sous-traitants de maintenance")
    
    soustraitants = data_manager.get_soustraitants()
    
    if soustraitants.empty:
        st.info("Aucun sous-traitant enregistré")
        return
    
    # Affichage par cartes avec Streamlit natif
    for _, soustraitant in soustraitants.iterrows():
        with st.container():
            # Carte du sous-traitant
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"### {soustraitant['nom']}")
                st.markdown(f"**Spécialité:** {soustraitant['specialite']}")
            with col2:
                st.markdown('<span class="type-soustraitant">Sous-traitant</span>', unsafe_allow_html=True)
            
            # Métriques
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric("Taux horaire", f"{soustraitant['taux_horaire']} €/h")
            
            with col_b:
                st.metric("Zone d'intervention", soustraitant['zone_intervention'])
            
            with col_c:
                assurance = "✅ Oui" if soustraitant['assurance_rc_pro'] else "❌ Non"
                st.metric("Assurance RC Pro", assurance)
            
            # Informations de contact
            with st.expander("📞 Informations de contact", expanded=False):
                st.write(f"**Contact:** {soustraitant['contact_nom']}")
                st.write(f"**Email:** {soustraitant['contact_email']}")
                st.write(f"**Téléphone:** {soustraitant['contact_telephone']}")
                st.write(f"**Adresse:** {soustraitant['adresse']}")
                st.write(f"**Type intervention:** {soustraitant['intervention_type']}")
                
                if soustraitant['certifications']:
                    st.write("**Certifications:**")
                    for cert in soustraitant['certifications']:
                        st.write(f"- {cert}")
            
            # Boutons d'action
            col_btn1, col_btn2, col_btn3 = st.columns(3)
            with col_btn1:
                if st.button("🔧 Demander intervention", key=f"inter_{soustraitant['id']}"):
                    st.session_state.selected_contractor = soustraitant['id']
                    st.info(f"Demande d'intervention à {soustraitant['nom']}")
            
            with col_btn2:
                if st.button("📋 Voir détails", key=f"cdetail_{soustraitant['id']}"):
                    st.info(f"Détails de {soustraitant['nom']}")
            
            with col_btn3:
                if st.button("📅 Planifier", key=f"plan_{soustraitant['id']}"):
                    st.success(f"Planning ouvert pour {soustraitant['nom']}")
            
            st.markdown("---")
def show_new_tier_form():
    """Affiche le formulaire pour ajouter un nouveau tier"""
    st.subheader("➕ Ajouter un nouveau tier")
    
    tier_type = st.radio("Type de tier", ["🏭 Fournisseur", "👷 Sous-traitant"], horizontal=True)
    
    if tier_type == "🏭 Fournisseur":
        with st.form("new_fournisseur_form"):
            st.markdown("### Informations du fournisseur")
            
            col1, col2 = st.columns(2)
            with col1:
                nom = st.text_input("Nom de l'entreprise*")
                specialite = st.text_input("Spécialité*", placeholder="Ex: Roulements, Courroies...")
                delai_livraison = st.number_input("Délai livraison moyen (jours)*", min_value=1, max_value=30, value=5)
                mode_livraison = st.selectbox("Mode de livraison", ["Express", "Standard", "Économique"])
            
            with col2:
                contact_nom = st.text_input("Nom du contact*")
                contact_email = st.text_input("Email*")
                contact_telephone = st.text_input("Téléphone*")
                note_fiabilite = st.slider("Note de fiabilité", 1.0, 5.0, 4.0, 0.1)
            
            adresse = st.text_area("Adresse complète*")
            conditions_paiement = st.text_input("Conditions de paiement", value="30 jours net")
            notes = st.text_area("Notes supplémentaires")
            
            col_date1, col_date2 = st.columns(2)
            with col_date1:
                date_debut = st.date_input("Date début contrat", datetime.date.today())
            with col_date2:
                date_fin = st.date_input("Date fin contrat", datetime.date.today() + datetime.timedelta(days=365))
            
            contrat_actif = st.checkbox("Contrat actif", value=True)
            
            if st.form_submit_button("✅ Enregistrer le fournisseur", type="primary"):
                if nom and specialite and contact_nom and contact_email and adresse:
                    tier_data = {
                        "type": "fournisseur",
                        "nom": nom,
                        "specialite": specialite,
                        "contact_nom": contact_nom,
                        "contact_email": contact_email,
                        "contact_telephone": contact_telephone,
                        "adresse": adresse,
                        "delai_livraison_moyen": delai_livraison,
                        "mode_livraison": mode_livraison,
                        "note_fiabilite": note_fiabilite,
                        "contrat_actif": contrat_actif,
                        "date_debut_contrat": date_debut.isoformat(),
                        "date_fin_contrat": date_fin.isoformat(),
                        "conditions_paiement": conditions_paiement,
                        "notes": notes
                    }
                    
                    data_manager.add_tier(tier_data)
                    st.success(f"✅ Fournisseur {nom} ajouté avec succès !")
                    st.balloons()
                else:
                    st.error("Veuillez remplir tous les champs obligatoires (*)")
    
    else:  # Sous-traitant
        with st.form("new_soustraitant_form"):
            st.markdown("### Informations du sous-traitant")
            
            col1, col2 = st.columns(2)
            with col1:
                nom = st.text_input("Nom de l'entreprise*")
                specialite = st.text_input("Spécialité*", placeholder="Ex: Électricité, Mécanique...")
                intervention_type = st.selectbox("Type d'intervention", ["Urgences 24/7", "Maintenance préventive", "Dépannage", "Installation"])
                taux_horaire = st.number_input("Taux horaire (€)*", min_value=30.0, max_value=200.0, value=85.0)
            
            with col2:
                contact_nom = st.text_input("Nom du contact*")
                contact_email = st.text_input("Email*")
                contact_telephone = st.text_input("Téléphone*")
                zone_intervention = st.text_input("Zone d'intervention*", placeholder="Ex: Région Île-de-France")
            
            adresse = st.text_area("Adresse complète*")
            certifications = st.text_area("Certifications (une par ligne)")
            
            col_cert1, col_cert2 = st.columns(2)
            with col_cert1:
                date_debut = st.date_input("Date début contrat", datetime.date.today())
            with col_cert2:
                date_fin = st.date_input("Date fin contrat", datetime.date.today() + datetime.timedelta(days=365))
            
            assurance_rc_pro = st.checkbox("Assurance RC Professionnelle", value=True)
            montant_assurance = st.text_input("Montant assurance", value="3 000 000 €") if assurance_rc_pro else ""
            notes = st.text_area("Notes supplémentaires")
            contrat_actif = st.checkbox("Contrat actif", value=True)
            
            if st.form_submit_button("✅ Enregistrer le sous-traitant", type="primary"):
                if nom and specialite and contact_nom and contact_email and adresse and zone_intervention:
                    tier_data = {
                        "type": "soustraitant",
                        "nom": nom,
                        "specialite": specialite,
                        "contact_nom": contact_nom,
                        "contact_email": contact_email,
                        "contact_telephone": contact_telephone,
                        "adresse": adresse,
                        "intervention_type": intervention_type,
                        "taux_horaire": taux_horaire,
                        "zone_intervention": zone_intervention,
                        "certifications": certifications.split("\n") if certifications else [],
                        "contrat_actif": contrat_actif,
                        "date_debut_contrat": date_debut.isoformat(),
                        "date_fin_contrat": date_fin.isoformat(),
                        "assurance_rc_pro": assurance_rc_pro,
                        "montant_assurance": montant_assurance,
                        "notes": notes
                    }
                    
                    data_manager.add_tier(tier_data)
                    st.success(f"✅ Sous-traitant {nom} ajouté avec succès !")
                    st.balloons()
                else:
                    st.error("Veuillez remplir tous les champs obligatoires (*)")

# ========== AUTRES PAGES (simplifiées pour l'exemple) ==========
def show_dashboard():
    """Affiche le tableau de bord"""
    st.title("🏠 Tableau de bord")
    
    # Métriques
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Interventions", "156", "+12%")
    with col2:
        st.metric("Équipements", "48", "+3")
    with col3:
        st.metric("Tiers", f"{len(data_manager.get_all_tiers())}", "+2")
    with col4:
        st.metric("Stock critique", "3", "-1")
    
    # Derniers tiers ajoutés
    st.subheader("🤝 Derniers tiers ajoutés")
    all_tiers = data_manager.get_all_tiers()
    if not all_tiers.empty:
        recent_tiers = all_tiers.head(3)
        for _, tier in recent_tiers.iterrows():
            type_badge = "type-fournisseur" if tier["type"] == "fournisseur" else "type-soustraitant"
            type_text = "Fournisseur" if tier["type"] == "fournisseur" else "Sous-traitant"
            st.info(f"**{tier['nom']}** - {type_text} - {tier['specialite']}")

def show_interventions():
    """Affiche la page interventions"""
    st.title("🔧 Interventions")
    st.write("Page interventions - À implémenter")

def show_equipements():
    """Affiche la page équipements"""
    st.title("🏭 Équipements")
    st.write("Page équipements - À implémenter")

def show_stocks():
    """Affiche la page stocks"""
    st.title("📦 Stocks")
    st.write("Page stocks - À implémenter")

def show_admin():
    """Affiche la page administration"""
    st.title("⚙️ Administration")
    st.write("Page administration - À implémenter")

# ========== POINT D'ENTRÉE ==========
def main():
    """Point d'entrée principal"""
    
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    
    if not st.session_state.authenticated:
        show_login_page()
    else:
        show_main_app()

if __name__ == "__main__":
    main()
