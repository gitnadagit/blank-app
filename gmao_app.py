import streamlit as st
import pandas as pd
import datetime
import json
import hashlib
import time
from pathlib import Path

# ========== CONFIGURATION ==========
st.set_page_config(
    page_title="GMAO Pro + Outillages",
    page_icon="🛠️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ========== GESTION DES DONNÉES ==========
class DataManager:
    def __init__(self):
        self.data_dir = Path("data")
        self.data_dir.mkdir(exist_ok=True)
        
        self.users_file = self.data_dir / "users.json"
        self.tiers_file = self.data_dir / "tiers.json"
        self.outillages_file = self.data_dir / "outillages.json"
        
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
        
        # Tiers
        if self.tiers_file.exists():
            with open(self.tiers_file, 'r', encoding='utf-8') as f:
                self.tiers = json.load(f)
        else:
            self.tiers = self.create_default_tiers()
            self.save_tiers()
        
        # Outillages
        if self.outillages_file.exists():
            with open(self.outillages_file, 'r', encoding='utf-8') as f:
                self.outillages = json.load(f)
        else:
            self.outillages = self.create_default_outillages()
            self.save_outillages()
    
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
                    "delai_livraison_moyen": 3,
                    "mode_livraison": "Express",
                    "note_fiabilite": 4.8,
                    "contrat_actif": True,
                    "date_debut_contrat": "2023-01-15",
                    "date_fin_contrat": "2025-01-14",
                    "conditions_paiement": "30 jours net",
                    "notes": "Fournisseur principal pour roulements"
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
                }
            ]
        }
    
    def create_default_outillages(self):
        """Crée les outillages par défaut"""
        return {
            "outillages": [
                {
                    "id": 1,
                    "reference": "OUT-001",
                    "nom": "Clé à choc 1/2\"",
                    "type": "Électroportatif",
                    "marque": "Makita",
                    "modele": "TW0350",
                    "numero_serie": "SN-MKT-2023-001",
                    "etat": "✅ Excellent",
                    "etat_detail": "Neuf, très peu utilisé",
                    "localisation": "Atelier A - Rack O1",
                    "date_acquisition": "2023-03-15",
                    "date_derniere_verification": "2024-10-15",
                    "date_prochaine_verification": "2025-04-15",
                    "prix_acquisition": 450.00,
                    "valeur_actuelle": 380.00,
                    "disponibilite": "🟢 Disponible",
                    "dernier_utilisateur": "Jean Dupont",
                    "date_dernier_emprunt": "2024-11-20",
                    "utilisation": "Montage/Démontage boulons lourds",
                    "consommables_associes": "Douilles 1/2\", Cliquet",
                    "fiche_technique": "Puissance: 650W, Couple: 700 Nm",
                    "notes": "À utiliser avec gants de protection"
                },
                {
                    "id": 2,
                    "reference": "OUT-002",
                    "nom": "Multimètre numérique",
                    "type": "Mesure électrique",
                    "marque": "Fluke",
                    "modele": "87V",
                    "numero_serie": "SN-FLK-2022-045",
                    "etat": "✅ Bon",
                    "etat_detail": "Fonctionne parfaitement, écran légèrement rayé",
                    "localisation": "Atelier B - Armoire mesure",
                    "date_acquisition": "2022-07-10",
                    "date_derniere_verification": "2024-09-20",
                    "date_prochaine_verification": "2025-03-20",
                    "prix_acquisition": 320.00,
                    "valeur_actuelle": 250.00,
                    "disponibilite": "🟢 Disponible",
                    "dernier_utilisateur": "Marie Martin",
                    "date_dernier_emprunt": "2024-11-22",
                    "utilisation": "Mesures tension/courant/résistance",
                    "consommables_associes": "Piles 9V, Pointes de test",
                    "fiche_technique": "Catégorie: CAT III 1000V, Précision: 0.1%",
                    "notes": "Étalonné tous les 6 mois"
                },
                {
                    "id": 3,
                    "nom": "Scie sauteuse",
                    "reference": "OUT-003",
                    "type": "Électroportatif",
                    "marque": "Bosch",
                    "modele": "GST 150 BCE",
                    "numero_serie": "SN-BSH-2021-123",
                    "etat": "🟡 Correct",
                    "etat_detail": "Lame usée à changer, moteur bruyant",
                    "localisation": "Atelier A - Rack O2",
                    "date_acquisition": "2021-11-05",
                    "date_derniere_verification": "2024-08-10",
                    "date_prochaine_verification": "2025-02-10",
                    "prix_acquisition": 180.00,
                    "valeur_actuelle": 90.00,
                    "disponibilite": "🔴 En réparation",
                    "dernier_utilisateur": "Paul Bernard",
                    "date_dernier_emprunt": "2024-11-15",
                    "utilisation": "Découpe métal/bois",
                    "consommables_associes": "Lames T118A, Lubes",
                    "fiche_technique": "Puissance: 720W, Course: 28mm",
                    "notes": "À réviser avant prochaine utilisation"
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
    
    def save_outillages(self):
        """Sauvegarde les outillages"""
        with open(self.outillages_file, 'w', encoding='utf-8') as f:
            json.dump(self.outillages, f, ensure_ascii=False, indent=2)
    
    def authenticate(self, username, password):
        """Authentifie un utilisateur"""
        user = next((u for u in self.users if u["username"] == username and u["is_active"]), None)
        
        if user and user["password_hash"] == self.hash_password(password):
            user["last_login"] = datetime.datetime.now().isoformat()
            self.save_users()
            return user
        return None
    
    def get_all_outillages(self):
        """Retourne tous les outillages"""
        return pd.DataFrame(self.outillages["outillages"])
    
    def add_outillage(self, outillage_data):
        """Ajoute un nouvel outillage"""
        max_id = max([o["id"] for o in self.outillages["outillages"]], default=0)
        outillage_data["id"] = max_id + 1
        self.outillages["outillages"].append(outillage_data)
        self.save_outillages()
        return outillage_data["id"]
    
    def update_outillage(self, outillage_id, outillage_data):
        """Met à jour un outillage"""
        for i, outillage in enumerate(self.outillages["outillages"]):
            if outillage["id"] == outillage_id:
                self.outillages["outillages"][i] = outillage_data
                break
        self.save_outillages()
    
    def delete_outillage(self, outillage_id):
        """Supprime un outillage"""
        self.outillages["outillages"] = [o for o in self.outillages["outillages"] if o["id"] != outillage_id]
        self.save_outillages()
    
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

# Initialiser le gestionnaire de données
data_manager = DataManager()

# ========== PAGE D'AUTHENTIFICATION ==========
def show_login_page():
    """Affiche la page de connexion"""
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div style="background: white; border-radius: 20px; padding: 40px; box-shadow: 0 20px 60px rgba(0,0,0,0.3);">', unsafe_allow_html=True)
        
        # Logo et titre
        st.markdown('<div style="text-align: center; margin-bottom: 30px;">', unsafe_allow_html=True)
        st.markdown('<div style="width: 80px; height: 80px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 15px; color: white; font-size: 35px;">🏭</div>', unsafe_allow_html=True)
        st.markdown('<h1 style="text-align: center; color: #2d3748;">GMAO PRO</h1>', unsafe_allow_html=True)
        st.markdown('<p style="text-align: center; color: #718096;">Gestion complète maintenance</p>', unsafe_allow_html=True)
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

# ========== PAGE DE GESTION DES OUTILLAGES ==========
def show_outillages_management():
    """Affiche la page de gestion des outillages"""
    st.title("🛠️ Gestion des Outillages")
    
    # Onglets
    tab1, tab2, tab3 = st.tabs(["📋 Inventaire", "➕ Nouvel outillage", "🔄 Emprunts"])
    
    with tab1:
        show_outillages_inventory()
    
    with tab2:
        show_new_outillage_form()
    
    with tab3:
        show_emprunts_management()

def show_outillages_inventory():
    """Affiche l'inventaire des outillages"""
    st.subheader("📋 Inventaire des Outillages")
    
    outillages = data_manager.get_all_outillages()
    
    if outillages.empty:
        st.info("Aucun outillage enregistré")
        return
    
    # Filtres
    col1, col2, col3 = st.columns(3)
    with col1:
        type_filter = st.multiselect("Type", outillages["type"].unique())
    
    with col2:
        etat_filter = st.multiselect("État", outillages["etat"].unique(), default=["✅ Excellent", "✅ Bon"])
    
    with col3:
        disponibilite_filter = st.multiselect("Disponibilité", outillages["disponibilite"].unique(), default=["🟢 Disponible"])
    
    # Application filtres
    filtered = outillages.copy()
    
    if type_filter:
        filtered = filtered[filtered["type"].isin(type_filter)]
    
    if etat_filter:
        filtered = filtered[filtered["etat"].isin(etat_filter)]
    
    if disponibilite_filter:
        filtered = filtered[filtered["disponibilite"].isin(disponibilite_filter)]
    
    # Affichage
    if not filtered.empty:
        for _, outillage in filtered.iterrows():
            with st.container():
                col_a1, col_a2 = st.columns([4, 1])
                with col_a1:
                    st.markdown(f"### {outillage['nom']}")
                    st.markdown(f"**Référence:** {outillage['reference']} | **Type:** {outillage['type']}")
                with col_a2:
                    st.markdown(f"**{outillage['disponibilite']}**")
                
                col_b1, col_b2, col_b3 = st.columns(3)
                with col_b1:
                    st.metric("État", outillage["etat"])
                with col_b2:
                    st.metric("Localisation", outillage["localisation"])
                with col_b3:
                    st.metric("Valeur", f"{outillage['valeur_actuelle']:.0f} €")
                
                with st.expander("📝 Détails complets"):
                    col_c1, col_c2 = st.columns(2)
                    with col_c1:
                        st.write(f"**Marque/Modèle:** {outillage['marque']} {outillage['modele']}")
                        st.write(f"**N° Série:** {outillage['numero_serie']}")
                        st.write(f"**Date acquisition:** {outillage['date_acquisition']}")
                        st.write(f"**Utilisation:** {outillage['utilisation']}")
                    
                    with col_c2:
                        st.write(f"**Dernier utilisateur:** {outillage['dernier_utilisateur']}")
                        st.write(f"**Dernière vérif:** {outillage['date_derniere_verification']}")
                        st.write(f"**Prochaine vérif:** {outillage['date_prochaine_verification']}")
                        st.write(f"**Consommables:** {outillage['consommables_associes']}")
                
                col_btn1, col_btn2, col_btn3 = st.columns(3)
                with col_btn1:
                    if st.button("📝 Emprunter", key=f"borrow_{outillage['id']}"):
                        st.session_state.outillage_to_borrow = outillage['id']
                        st.success(f"Formulaire d'emprunt pour {outillage['nom']}")
                
                with col_btn2:
                    if st.button("🔧 Réparer", key=f"repair_{outillage['id']}"):
                        st.info(f"Bon de réparation pour {outillage['nom']}")
                
                with col_btn3:
                    if st.button("🗑️ Supprimer", key=f"delete_{outillage['id']}"):
                        if st.button(f"Confirmer suppression", key=f"confirm_del_{outillage['id']}"):
                            data_manager.delete_outillage(outillage['id'])
                            st.success(f"Outillage {outillage['nom']} supprimé")
                            st.rerun()
                
                st.markdown("---")
    else:
        st.warning("Aucun outillage ne correspond aux filtres")

def show_new_outillage_form():
    """Affiche le formulaire pour ajouter un nouvel outillage"""
    st.subheader("➕ Ajouter un nouvel outillage")
    
    with st.form("new_outillage_form"):
        st.markdown("### Informations générales")
        
        col1, col2 = st.columns(2)
        with col1:
            reference = st.text_input("Référence*", placeholder="EX: OUT-006")
            nom = st.text_input("Nom de l'outillage*", placeholder="Ex: Perceuse à colonne")
            type_outillage = st.selectbox("Type*", ["Électroportatif", "Manuel", "Mesure", "Test", "Sécurité", "Transport", "Soudage", "Autre"])
            marque = st.text_input("Marque")
            modele = st.text_input("Modèle")
        
        with col2:
            numero_serie = st.text_input("Numéro de série")
            etat = st.selectbox("État général*", ["✅ Excellent", "✅ Bon", "🟡 Correct", "🔴 Mauvais"])
            etat_detail = st.text_area("Détails état", placeholder="Décrivez l'état en détail...")
            localisation = st.text_input("Localisation de stockage*", placeholder="Ex: Atelier A - Rack 3")
        
        st.markdown("### Acquisition et valeur")
        col3, col4 = st.columns(2)
        with col3:
            date_acquisition = st.date_input("Date d'acquisition", datetime.date.today())
            prix_acquisition = st.number_input("Prix d'acquisition (€)", min_value=0.0, value=0.0, step=10.0)
        
        with col4:
            date_derniere_verification = st.date_input("Date dernière vérification", datetime.date.today())
            date_prochaine_verification = st.date_input("Date prochaine vérification", datetime.date.today() + datetime.timedelta(days=180))
            valeur_actuelle = st.number_input("Valeur actuelle estimée (€)", min_value=0.0, value=0.0, step=10.0)
        
        st.markdown("### Utilisation et spécifications")
        utilisation = st.text_area("Utilisation prévue*", placeholder="Décrivez l'utilisation principale...")
        consommables_associes = st.text_input("Consommables associés", placeholder="Ex: Lames, forets, piles...")
        fiche_technique = st.text_area("Fiche technique", placeholder="Spécifications techniques...")
        notes = st.text_area("Notes supplémentaires")
        
        disponibilite = st.selectbox("Disponibilité initiale", ["🟢 Disponible", "🟡 En maintenance", "🔴 Hors service"])
        
        submitted = st.form_submit_button("✅ Enregistrer l'outillage", type="primary")
        
        if submitted:
            if not reference or not nom or not type_outillage or not localisation or not utilisation:
                st.error("Veuillez remplir tous les champs obligatoires (*)")
            else:
                outillage_data = {
                    "reference": reference,
                    "nom": nom,
                    "type": type_outillage,
                    "marque": marque,
                    "modele": modele,
                    "numero_serie": numero_serie,
                    "etat": etat,
                    "etat_detail": etat_detail,
                    "localisation": localisation,
                    "date_acquisition": date_acquisition.isoformat(),
                    "date_derniere_verification": date_derniere_verification.isoformat(),
                    "date_prochaine_verification": date_prochaine_verification.isoformat(),
                    "prix_acquisition": prix_acquisition,
                    "valeur_actuelle": valeur_actuelle,
                    "disponibilite": disponibilite,
                    "dernier_utilisateur": "",
                    "date_dernier_emprunt": "",
                    "utilisation": utilisation,
                    "consommables_associes": consommables_associes,
                    "fiche_technique": fiche_technique,
                    "notes": notes
                }
                
                outillage_id = data_manager.add_outillage(outillage_data)
                st.success(f"✅ Outillage {nom} ajouté avec succès ! Référence: {reference}")
                st.balloons()

def show_emprunts_management():
    """Affiche la gestion des emprunts"""
    st.subheader("🔄 Gestion des Emprunts")
    
    outillages = data_manager.get_all_outillages()
    
    # Formulaire d'emprunt
    with st.form("emprunt_form"):
        st.markdown("### Nouvel emprunt")
        
        col1, col2 = st.columns(2)
        with col1:
            disponibles = outillages[outillages["disponibilite"] == "🟢 Disponible"]
            if not disponibles.empty:
                # CORRECTION : Utiliser to_numpy().tolist() pour obtenir une liste de listes
                outillage_options = disponibles[["id", "nom", "reference"]].to_numpy().tolist()
                
                # Debug optionnel
                # st.write("Debug options:", outillage_options[:3])  # Affiche les 3 premières options
                
                outillage_choice = st.selectbox(
                    "Outillage*", 
                    options=outillage_options, 
                    format_func=lambda x: f"{x[2]} - {x[1]}"  # x[2] = reference, x[1] = nom
                )
                outillage_id = outillage_choice[0] if outillage_choice else None
            else:
                st.warning("Aucun outillage disponible")
                outillage_id = None
        
        with col2:
            utilisateur = st.selectbox("Utilisateur*", ["Jean Dupont", "Marie Martin", "Paul Bernard", "Sophie Laurent", "Autre"])
            if utilisateur == "Autre":
                utilisateur = st.text_input("Nom utilisateur")
        
        date_emprunt = st.date_input("Date emprunt*", datetime.date.today())
        date_retour_prevue = st.date_input("Date retour prévue*", datetime.date.today() + datetime.timedelta(days=7))
        motif = st.text_area("Motif de l'emprunt*", placeholder="Décrivez l'utilisation prévue...")
        
        if st.form_submit_button("📝 Enregistrer l'emprunt", type="primary"):
            if outillage_id and utilisateur and motif:
                # Chercher l'outillage par ID
                outillage = None
                for o in data_manager.outillages["outillages"]:
                    if o["id"] == outillage_id:
                        outillage = o.copy()
                        break
                
                if outillage:
                    outillage["disponibilite"] = "🟡 Emprunté"
                    outillage["dernier_utilisateur"] = utilisateur
                    outillage["date_dernier_emprunt"] = date_emprunt.isoformat()
                    outillage["date_retour_prevue"] = date_retour_prevue.isoformat()
                    
                    data_manager.update_outillage(outillage_id, outillage)
                    
                    st.success(f"✅ Emprunt enregistré ! {outillage['nom']} emprunté par {utilisateur}")
                    st.balloons()
                    st.rerun()
                else:
                    st.error("Erreur : outillage non trouvé")
            else:
                st.error("Veuillez remplir tous les champs")
    
    # Liste des emprunts en cours
    st.markdown("### 📋 Emprunts en cours")
    emprunts_en_cours = outillages[outillages["disponibilite"] == "🟡 Emprunté"]
    
    if not emprunts_en_cours.empty:
        for _, emprunt in emprunts_en_cours.iterrows():
            with st.container():
                col_e1, col_e2, col_e3 = st.columns([3, 2, 1])
                with col_e1:
                    st.write(f"**{emprunt['nom']}** ({emprunt['reference']})")
                    st.write(f"Emprunté par: {emprunt['dernier_utilisateur']}")
                
                with col_e2:
                    st.write(f"Depuis: {emprunt['date_dernier_emprunt']}")
                    if "date_retour_prevue" in emprunt and emprunt["date_retour_prevue"]:
                        try:
                            if isinstance(emprunt["date_retour_prevue"], str):
                                retour_date = datetime.datetime.fromisoformat(emprunt["date_retour_prevue"]).date()
                            else:
                                retour_date = emprunt["date_retour_prevue"]
                                
                            if retour_date < datetime.date.today():
                                st.error(f"⚠️ Retard depuis {retour_date}")
                            else:
                                st.write(f"Retour prévu: {retour_date}")
                        except:
                            st.write("Date retour: Non spécifiée")
                
                with col_e3:
                    if st.button("✅ Retourner", key=f"return_{emprunt['id']}"):
                        # Récupérer l'outillage depuis les données
                        for o in data_manager.outillages["outillages"]:
                            if o["id"] == emprunt["id"]:
                                o["disponibilite"] = "🟢 Disponible"
                                o["date_dernier_emprunt"] = ""
                                o["date_retour_prevue"] = ""
                                break
                        
                        data_manager.save_outillages()
                        st.success(f"{emprunt['nom']} retourné avec succès")
                        st.rerun()
                
                st.markdown("---")
    else:
        st.info("Aucun emprunt en cours")

# ========== PAGES SIMPLIFIÉES POUR LES AUTRES SECTIONS ==========
def show_interventions():
    """Page interventions simplifiée"""
    st.title("🔧 Interventions")
    st.write("Gestion des interventions de maintenance")
    st.info("Fonctionnalité à développer")

def show_equipements():
    """Page équipements simplifiée"""
    st.title("🏭 Équipements")
    st.write("Gestion du parc machines")
    st.info("Fonctionnalité à développer")

def show_stocks():
    """Page stocks simplifiée"""
    st.title("📦 Stocks")
    st.write("Gestion des pièces détachées")
    st.info("Fonctionnalité à développer")

def show_tiers_management():
    """Page tiers simplifiée"""
    st.title("🤝 Tiers")
    st.write("Gestion fournisseurs et sous-traitants")
    st.info("Fonctionnalité à développer")

def show_admin():
    """Page admin simplifiée"""
    st.title("⚙️ Administration")
    st.write("Paramètres système")
    st.info("Fonctionnalité à développer")

def show_dashboard():
    """Tableau de bord simplifié"""
    st.title("🏠 Tableau de bord")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Interventions", "24")
    with col2:
        outillages = data_manager.get_all_outillages()
        total_outillages = len(outillages) if not outillages.empty else 0
        st.metric("Outillages", total_outillages)
    with col3:
        st.metric("Équipements", "12")
    with col4:
        st.metric("Alertes", "3")

# ========== APPLICATION PRINCIPALE ==========
def show_main_app():
    """Affiche l'application principale"""
    
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
        
        menu_options = ["🏠 Tableau de bord", "🔧 Interventions", "🏭 Équipements", "📦 Stocks", "🛠️ Outillages", "🤝 Tiers"]
        
        if user["role"] == "admin":
            menu_options.append("⚙️ Administration")
        
        selected_menu = st.radio("Menu", menu_options, label_visibility="collapsed")
        st.session_state.selected_menu = selected_menu
        
        st.markdown("---")
        
        if st.button("🚪 Déconnexion", type="secondary", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
    # Contenu
    menu = st.session_state.get('selected_menu', '🏠 Tableau de bord')
    
    if menu == "🏠 Tableau de bord":
        show_dashboard()
    elif menu == "🔧 Interventions":
        show_interventions()
    elif menu == "🏭 Équipements":
        show_equipements()
    elif menu == "📦 Stocks":
        show_stocks()
    elif menu == "🛠️ Outillages":
        show_outillages_management()
    elif menu == "🤝 Tiers":
        show_tiers_management()
    elif menu == "⚙️ Administration" and user["role"] == "admin":
        show_admin()

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
