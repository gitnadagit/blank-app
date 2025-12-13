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
        self.personnels_file = self.data_dir / "personnels.json"
        
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
        
        # Personnels - NOUVEAU
        if self.personnels_file.exists():
            with open(self.personnels_file, 'r', encoding='utf-8') as f:
                self.personnels = json.load(f)
        else:
            self.personnels = self.create_default_personnels()
            self.save_personnels()
    
    def create_default_personnels(self):
        """Crée les personnels par défaut avec noms tunisiens"""
        return [
            {
                "id": 1,
                "nom": "Ahmed Ben Salah",
                "matricule": "PER-001",
                "poste": "Ingénieur Maintenance",
                "service": "Direction Maintenance",
                "cout_horaire": 75.50,
                "statut": "🟢 Actif",
                "experience": "12 ans",
                "competences": ["TPM", "Lean Maintenance", "Gestion de projet", "Analyse de données"],
                "habilitations": [
                    "Habilitation Électrique B2V-H2V",
                    "Sauveteur Secouriste du Travail (SST)",
                    "TPM - Total Productive Maintenance",
                    "Certification Siemens TIA Portal",
                    "Auditeur Qualité ISO 9001:2015",
                    "Arabe : Langue maternelle",
                    "Français : Courant professionnel"
                ],
                "date_embauche": "2012-05-15",
                "derniere_evaluation": "2024-10-15",
                "notes": "Responsable du département maintenance",
                "telephone": "+216 71 123 456",
                "email": "ahmed.bensalah@entreprise.tn",
                "type_contrat": "CDI",
                "adresse": "15 Avenue Habib Bourguiba, Tunis",
                "diplome": "Diplôme d'Ingénieur en Maintenance Industrielle",
                "specialite": "Génie Mécanique et Maintenance",
                "date_creation": "2024-01-01T00:00:00",
                "date_naissance": "1985-03-20"
            },
            {
                "id": 2,
                "nom": "Fatma Jebali",
                "matricule": "PER-002",
                "poste": "Responsable Qualité",
                "service": "Qualité & Contrôle",
                "cout_horaire": 68.00,
                "statut": "🟢 Actif",
                "experience": "8 ans",
                "competences": ["Contrôle qualité", "Audit", "ISO 9001", "Reporting"],
                "habilitations": [
                    "Auditeur Qualité ISO 9001:2015",
                    "Certifié ISO 14001:2015",
                    "Lean Six Sigma Green Belt",
                    "AMDEC - Analyse des Défaillances",
                    "5S - Management visuel",
                    "Arabe : Langue maternelle",
                    "Français : Courant professionnel",
                    "Anglais : Technique"
                ],
                "date_embauche": "2016-03-22",
                "derniere_evaluation": "2024-09-20",
                "notes": "Responsable assurance qualité maintenance",
                "telephone": "+216 71 234 567",
                "email": "fatma.jebali@entreprise.tn",
                "type_contrat": "CDI",
                "adresse": "22 Rue de Carthage, La Marsa",
                "diplome": "Master en Qualité Industrielle",
                "specialite": "Management de la Qualité",
                "date_creation": "2024-01-01T00:00:00",
                "date_naissance": "1990-07-15"
            }
             {
            "id": 3,
            "nom": "Mohamed Trabelsi",
            "matricule": "PER-003",
            "poste": "Technicien Supérieur",
            "service": "Maintenance Automatisme",
            "cout_horaire": 48.50,
            "statut": "🟢 Actif",
            "experience": "10 ans",
            "competences": ["Automatisme Siemens", "PLC Allen Bradley", "Diagnostic Avancé", "Robotique"],
            "habilitations": [
                "Habilitation Électrique B2V-H2V",
                "Certification Siemens TIA Portal",
                "Sauveteur Secouriste du Travail (SST)",
                "CACES 1 - Chariots élévateurs",
                "Arabe : Langue maternelle",
                "Français : Courant professionnel"
            ],
            "date_embauche": "2014-08-10",
            "derniere_evaluation": "2024-08-05",
            "notes": "Spécialiste automates et régulation",
            "telephone": "+216 71 345 678",
            "email": "mohamed.trabelsi@entreprise.tn",
            "type_contrat": "CDI",
            "adresse": "8 Rue Abou Kacem Chebbi, Ben Arous",
            "diplome": "BTS Maintenance Industrielle",
            "specialite": "Automatisme et Informatique Industrielle",
            "date_creation": "2024-01-01T00:00:00",
            "date_naissance": "1988-11-30"
        },
        {
            "id": 4,
            "nom": "Sonia Hammami",
            "matricule": "PER-004",
            "poste": "Gestionnaire de Stock",
            "service": "Logistique & Stock",
            "cout_horaire": 42.00,
            "statut": "🟢 Actif",
            "experience": "6 ans",
            "competences": ["Gestion de stock", "CMMS", "Logistique", "Reporting", "SAP"],
            "habilitations": [
                "Gestion des Non-Conformités",
                "5S - Management visuel",
                "SAP PM (Plant Maintenance)",
                "Power BI / Tableau - Reporting",
                "Arabe : Langue maternelle",
                "Français : Courant professionnel"
            ],
            "date_embauche": "2018-11-05",
            "derniere_evaluation": "2024-07-30",
            "notes": "Gère les stocks de pièces détachées",
            "telephone": "+216 71 456 789",
            "email": "sonia.hammami@entreprise.tn",
            "type_contrat": "CDI",
            "adresse": "45 Avenue de la Liberté, Tunis",
            "diplome": "Licence en Logistique",
            "specialite": "Gestion des Stocks Industriels",
            "date_creation": "2024-01-01T00:00:00",
            "date_naissance": "1992-04-25"
        },
        {
            "id": 5,
            "nom": "Karim Chaouch",
            "matricule": "PER-005",
            "poste": "Chef d'Équipe",
            "service": "Maintenance Mécanique",
            "cout_horaire": 55.00,
            "statut": "🟢 Actif",
            "experience": "15 ans",
            "competences": ["Soudage TIG/MIG", "Usinage", "Management d'équipe", "Planification", "Sécurité"],
            "habilitations": [
                "CACES 1 - Chariots élévateurs",
                "Soudeur Certifié ISO 9606",
                "Sauveteur Secouriste du Travail (SST)",
                "Travaux en Hauteur Niveau 3",
                "Arabe : Langue maternelle",
                "Français : Courant professionnel"
            ],
            "date_embauche": "2009-02-18",
            "derniere_evaluation": "2024-06-25",
            "notes": "Responsable équipe mécanique lourde",
            "telephone": "+216 71 567 890",
            "email": "karim.chaouch@entreprise.tn",
            "type_contrat": "CDI",
            "adresse": "32 Rue de Marrakech, Sfax",
            "diplome": "Diplôme de Technicien Supérieur",
            "specialite": "Mécanique Industrielle",
            "date_creation": "2024-01-01T00:00:00",
            "date_naissance": "1982-09-12"
        }
        ]
    
    def save_personnels(self):
        """Sauvegarde les personnels"""
        with open(self.personnels_file, 'w', encoding='utf-8') as f:
            json.dump(self.personnels, f, ensure_ascii=False, indent=2)
    
    def get_all_personnels(self):
        """Retourne tous les personnels"""
        return self.personnels
    
    def add_personnel(self, personnel_data):
        """Ajoute un nouveau personnel"""
        if self.personnels:
            max_id = max([p["id"] for p in self.personnels], default=0)
            personnel_data["id"] = max_id + 1
        else:
            personnel_data["id"] = 1
        
        self.personnels.append(personnel_data)
        self.save_personnels()
        return personnel_data["id"]
    
    def update_personnel(self, personnel_id, personnel_data):
        """Met à jour un personnel"""
        for i, personnel in enumerate(self.personnels):
            if personnel["id"] == personnel_id:
                self.personnels[i] = personnel_data
                break
        self.save_personnels()
    
    def delete_personnel(self, personnel_id):
        """Supprime un personnel"""
        self.personnels = [p for p in self.personnels if p["id"] != personnel_id]
        self.save_personnels()
    
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
                "full_name": "Ali ben salah",
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
                    "dernier_utilisateur": "Ali ben salah",
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
            username = st.text_input("Nom d'utilisateur", value="")
            password = st.text_input("Mot de passe", type="password", value="")
            
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
            utilisateur = st.selectbox("Utilisateur*", ["Ali ben salah", "Marie Martin", "Paul Bernard", "Sophie Laurent", "Autre"])
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

# ========== GESTION DES INTERVENTIONS ==========
def calculer_priorite(criticite, impact_production):
    """Calcule la priorité en fonction de la criticité et de l'impact"""
    if criticite == "Critique" or impact_production == "Arrêt total":
        return "Urgente"
    elif criticite == "Haute" or impact_production == "Arrêt partiel":
        return "Haute"
    elif criticite == "Moyenne" or impact_production == "Ralentissement":
        return "Normale"
    else:
        return "Basse"
def show_interventions():
    """Page principale des interventions"""
    st.title("🔧 Gestion des Interventions")
    
    # Onglets principaux
    tab_corrective, tab_preventive = st.tabs(["🔴 Interventions Correctives", "🟢 Maintenance Préventive"])
    
    with tab_corrective:
        show_corrective_interventions()
    
    with tab_preventive:
        show_preventive_interventions()

# ========== PARTIE CORRECTIVE ==========
def show_corrective_interventions():
    """Affiche la gestion des interventions correctives"""
    st.subheader("🔴 Interventions Correctives")
    
    # Sous-onglets pour la partie corrective
    tab1, tab2, tab3 = st.tabs(["📝 Demande d'Intervention", "📋 Bons de Travail", "📊 Suivi en cours"])
    
    with tab1:
        show_demande_intervention()
    
    with tab2:
        show_bons_travail_correctifs()
    
    with tab3:
        show_suivi_correctif()

def show_demande_intervention():
    """Formulaire de demande d'intervention corrective"""
    st.markdown("### 📝 Nouvelle Demande d'Intervention")
    
    demande_soumise = False
    demande_data = None
    
    with st.form("demande_intervention_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            # Information sur l'équipement
            st.markdown("#### Information Équipement")
            equipement_nom = st.text_input("Nom de l'équipement*", placeholder="Ex: Pompe centrifuge P-101")
            reference_equipement = st.text_input("Référence équipement*", placeholder="Ex: EQUIP-023")
            localisation = st.selectbox("Localisation*", ["Atelier A", "Atelier B", "Salle des machines", "Extérieur", "Autre"])
            if localisation == "Autre":
                localisation = st.text_input("Précisez la localisation")
            
            # Nature du problème
            st.markdown("#### Nature du problème")
            type_panne = st.selectbox("Type de panne*", 
                ["Mécanique", "Électrique", "Hydraulique", "Pneumatique", "Électronique", "Automatisme", "Autre"])
            criticite = st.select_slider("Criticité*", 
                options=["Faible", "Moyenne", "Haute", "Critique"], 
                value="Moyenne")
        
        with col2:
            # Information demandeur
            st.markdown("#### Information Demandeur")
            demandeur = st.text_input("Nom du demandeur*", 
                value=st.session_state.user.get("full_name", ""))
            departement = st.selectbox("Département*", 
                ["Production", "Maintenance", "Qualité", "Sécurité", "Autre"])
            date_detection = st.date_input("Date de détection*", datetime.date.today())
            heure_detection = st.time_input("Heure de détection*", datetime.datetime.now().time())
            
            # Description problème
            st.markdown("#### Description")
            symptomes = st.text_area("Symptômes observés*", 
                placeholder="Décrivez ce qui ne fonctionne pas, les bruits anormaux, les voyants...")
            impact_production = st.selectbox("Impact sur la production", 
                ["Aucun", "Ralentissement", "Arrêt partiel", "Arrêt total"])
        
        # Actions déjà entreprises
        actions_deja_prises = st.text_area("Actions déjà entreprises", 
            placeholder="Décrivez les vérifications, réglages ou réparations déjà effectués")
        
        # Pièces jointes (simulées)
        with st.expander("📎 Pièces jointes"):
            st.caption("(Fonctionnalité de téléchargement en développement)")
            photo = st.checkbox("Photo disponible")
            video = st.checkbox("Vidéo disponible")
            schema = st.checkbox("Schéma technique joint")
        
        submitted = st.form_submit_button("📤 Soumettre la demande", type="primary")
        
        if submitted:
            if equipement_nom and reference_equipement and localisation and type_panne and demandeur:
                demande_data = {
                    "id": time.time_ns(),  # ID unique
                    "equipement_nom": equipement_nom,
                    "reference_equipement": reference_equipement,
                    "localisation": localisation,
                    "type_panne": type_panne,
                    "criticite": criticite,
                    "demandeur": demandeur,
                    "departement": departement,
                    "date_detection": date_detection.isoformat(),
                    "heure_detection": heure_detection.isoformat(),
                    "symptomes": symptomes,
                    "impact_production": impact_production,
                    "actions_deja_prises": actions_deja_prises,
                    "statut": "🟡 En attente",
                    "date_soumission": datetime.datetime.now().isoformat(),
                    "priorite": calculer_priorite(criticite, impact_production)
                }
                
                demande_soumise = True
                st.session_state.last_demande = demande_data
                
                st.success(f"✅ Demande d'intervention pour {equipement_nom} soumise avec succès !")
                st.info(f"Numéro de demande: DI-{demande_data['id']}")
            else:
                st.error("Veuillez remplir tous les champs obligatoires (*)")
    
    # Bouton pour générer le BT - EN DEHORS du formulaire
    if demande_soumise:
        st.markdown("---")
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            if st.button("📄 Générer le Bon de Travail", type="primary"):
                if demande_data:
                    show_generer_bt(demande_data)
                elif 'last_demande' in st.session_state:
                    show_generer_bt(st.session_state.last_demande)
        
        with col_btn2:
            if st.button("📋 Voir toutes les demandes"):
                st.session_state.show_demandes_list = True
    
    # Afficher la liste des demandes si demandé
    if st.session_state.get('show_demandes_list', False):
        show_liste_demandes()

def show_bons_travail_correctifs():
    """Affiche la gestion des Bons de Travail correctifs"""
    st.markdown("### 📋 Bons de Travail Correctifs")
    
    # Filtres
    col1, col2, col3 = st.columns(3)
    with col1:
        statut_filter = st.multiselect("Statut", 
            ["🟡 En attente", "🔵 En cours", "🟢 Terminé", "🔴 Annulé"], 
            default=["🟡 En attente", "🔵 En cours"])
    
    with col2:
        priorite_filter = st.multiselect("Priorité", 
            ["Basse", "Normale", "Haute", "Urgente"])
    
    with col3:
        technicien_filter = st.multiselect("Technicien", 
            ["Ali ben salah", "Marie Martin", "Paul Bernard", "Sophie Laurent"])
    
    # Bouton pour créer un nouveau BT
    if st.button("➕ Créer un nouveau BT", type="primary"):
        st.session_state.creating_bt = True
    
    if st.session_state.get("creating_bt", False):
        show_creer_bt_correctif()
    
    # Liste des BTs (données simulées)
    st.markdown("#### Liste des Bons de Travail")
    
    # Données de démo
    bts_demo = [
        {
            "id": "BT-C-001",
            "equipement": "Pompe centrifuge P-101",
            "reference": "EQUIP-023",
            "type": "Mécanique",
            "technicien": "Ali ben salah",
            "date_creation": "2024-11-25",
            "date_debut": "2024-11-26",
            "date_fin": "2024-11-26",
            "statut": "🔵 En cours",
            "priorite": "Haute",
            "temps_estime": "4h",
            "temps_reel": "3h30"
        },
        {
            "id": "BT-C-002",
            "equipement": "Convoyeur bande C-205",
            "reference": "EQUIP-045",
            "type": "Électrique",
            "technicien": "Marie Martin",
            "date_creation": "2024-11-24",
            "date_debut": "2024-11-25",
            "date_fin": "2024-11-25",
            "statut": "🟢 Terminé",
            "priorite": "Normale",
            "temps_estime": "2h",
            "temps_reel": "1h45"
        }
    ]
    
    for bt in bts_demo:
        if statut_filter and bt["statut"] not in statut_filter:
            continue
        if priorite_filter and bt["priorite"] not in priorite_filter:
            continue
        if technicien_filter and bt["technicien"] not in technicien_filter:
            continue
        
        with st.container():
            col_a1, col_a2, col_a3 = st.columns([3, 2, 1])
            with col_a1:
                st.markdown(f"**{bt['id']} - {bt['equipement']}**")
                st.caption(f"Type: {bt['type']} | Technicien: {bt['technicien']}")
            
            with col_a2:
                st.write(f"Créé le: {bt['date_creation']}")
                if bt['date_debut']:
                    st.write(f"Début: {bt['date_debut']}")
            
            with col_a3:
                color = "green" if bt["statut"] == "🟢 Terminé" else "blue" if bt["statut"] == "🔵 En cours" else "orange"
                st.markdown(f'<span style="color: {color}; font-weight: bold;">{bt["statut"]}</span>', 
                           unsafe_allow_html=True)
            
            # Actions
            col_b1, col_b2, col_b3, col_b4 = st.columns(4)
            with col_b1:
                if st.button(f"👁️ Voir", key=f"view_{bt['id']}"):
                    st.session_state.selected_bt = bt
            with col_b2:
                if bt["statut"] != "🟢 Terminé":
                    if st.button(f"✏️ Modifier", key=f"edit_{bt['id']}"):
                        st.info(f"Modification du BT {bt['id']}")
            with col_b3:
                if st.button(f"📄 PDF", key=f"pdf_{bt['id']}"):
                    st.success(f"Génération PDF pour {bt['id']}")
            with col_b4:
                if st.button(f"📊 Rapport", key=f"report_{bt['id']}"):
                    show_rapport_bt(bt)
            
            st.markdown("---")

def show_suivi_correctif():
    """Affiche le suivi des interventions correctives"""
    st.markdown("### 📊 Suivi des Interventions Correctives")
    
    # Métriques
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("En attente", "5")
    with col2:
        st.metric("En cours", "3")
    with col3:
        st.metric("Terminées (mois)", "24")
    with col4:
        st.metric("Temps moyen", "2.3h")
    
    # Graphiques
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown("#### Répartition par type")
        types_data = pd.DataFrame({
            'Type': ['Mécanique', 'Électrique', 'Hydraulique', 'Pneumatique'],
            'Nombre': [12, 8, 5, 3]
        })
        st.bar_chart(types_data.set_index('Type'))
    
    with col_b:
        st.markdown("#### Évolution mensuelle")
        evolution_data = pd.DataFrame({
            'Mois': ['Sep', 'Oct', 'Nov'],
            'Interventions': [18, 22, 15]
        })
        st.line_chart(evolution_data.set_index('Mois'))

# ========== PARTIE PRÉVENTIVE ==========
def show_preventive_interventions():
    """Affiche la gestion de la maintenance préventive"""
    st.subheader("🟢 Maintenance Préventive")
    
    # Sous-onglets pour la partie préventive
    tab1, tab2, tab3 = st.tabs(["📅 Planning", "📋 Bons Préventifs", "📈 Statistiques"])
    
    with tab1:
        show_planning_preventif()
    
    with tab2:
        show_bons_preventifs()
    
    with tab3:
        show_statistiques_preventives()

def show_planning_preventif():
    """Affiche le planning de maintenance préventive"""
    st.markdown("### 📅 Planning de Maintenance Préventive")
    
    # Filtres
    col1, col2, col3 = st.columns(3)
    with col1:
        periode = st.selectbox("Période", 
            ["Semaine en cours", "Mois en cours", "Trimestre", "Année"])
    
    with col2:
        type_maintenance = st.multiselect("Type maintenance",
            ["Hebdomadaire", "Mensuelle", "Trimestrielle", "Semestrielle", "Annuelle"])
    
    with col3:
        etat = st.multiselect("État",
            ["🟢 Planifié", "🟡 En cours", "🔵 Réalisé", "🔴 Reporté"])
    
    # Planning (données de démo)
    st.markdown("#### Calendrier des interventions")
    
    planning_data = [
        {
            "equipement": "Pompe centrifuge P-101",
            "type": "Mensuelle",
            "date_prevue": "2024-12-02",
            "technicien": "Ali ben salah",
            "duree_estimee": "2h",
            "etat": "🟢 Planifié",
            "derniere_realisation": "2024-11-02"
        },
        {
            "equipement": "Convoyeur bande C-205",
            "type": "Hebdomadaire",
            "date_prevue": "2024-12-03",
            "technicien": "Marie Martin",
            "duree_estimee": "1h",
            "etat": "🟢 Planifié",
            "derniere_realisation": "2024-11-26"
        },
        {
            "equipement": "Compresseur d'air COMP-01",
            "type": "Trimestrielle",
            "date_prevue": "2024-12-10",
            "technicien": "Paul Bernard",
            "duree_estimee": "4h",
            "etat": "🟡 En cours",
            "derniere_realisation": "2024-09-10"
        }
    ]
    
    for plan in planning_data:
        if type_maintenance and plan["type"] not in type_maintenance:
            continue
        if etat and plan["etat"] not in etat:
            continue
        
        with st.container():
            col_a1, col_a2, col_a3 = st.columns([3, 2, 1])
            with col_a1:
                st.markdown(f"**{plan['equipement']}**")
                st.caption(f"Type: {plan['type']} | Technicien: {plan['technicien']}")
            
            with col_a2:
                st.write(f"Date prévue: {plan['date_prevue']}")
                st.write(f"Durée: {plan['duree_estimee']}")
            
            with col_a3:
                color = "green" if plan["etat"] == "🟢 Planifié" else "orange" if plan["etat"] == "🟡 En cours" else "blue"
                st.markdown(f'<span style="color: {color}; font-weight: bold;">{plan["etat"]}</span>', 
                           unsafe_allow_html=True)
            
            # Actions
            col_b1, col_b2, col_b3 = st.columns(3)
            with col_b1:
                if plan["etat"] == "🟢 Planifié":
                    if st.button(f"📄 Générer BT", key=f"gen_{plan['equipement']}"):
                        show_generer_bt_preventif(plan)
            with col_b2:
                if st.button(f"🔄 Reporter", key=f"report_{plan['equipement']}"):
                    st.warning(f"Report de l'intervention sur {plan['equipement']}")
            with col_b3:
                if st.button(f"📋 Historique", key=f"hist_{plan['equipement']}"):
                    show_historique_preventif(plan)
            
            st.markdown("---")
    
    # Bouton pour planifier une nouvelle intervention
    if st.button("➕ Planifier une nouvelle intervention", type="primary"):
        show_planifier_intervention()

def show_bons_preventifs():
    """Affiche les Bons de Travail préventifs"""
    st.markdown("### 📋 Bons de Travail Préventifs")
    
    # Filtres
    col1, col2 = st.columns(2)
    with col1:
        periode_bt = st.selectbox("Période de réalisation",
            ["Tous", "Semaine", "Mois", "Trimestre"])
    
    with col2:
        statut_bt = st.multiselect("Statut du BT",
            ["🟢 Planifié", "🟡 En cours", "🔵 Réalisé", "✅ Clôturé"])
    
    # Liste des BTs préventifs
    bts_preventifs = [
        {
            "id": "BT-P-001",
            "equipement": "Pompe centrifuge P-101",
            "type": "Mensuelle",
            "technicien": "Ali ben salah",
            "date_planifiee": "2024-12-02",
            "date_realisation": None,
            "statut": "🟢 Planifié",
            "checklist": ["Vérifier vibrations", "Contrôler température", "Graisser roulements"]
        },
        {
            "id": "BT-P-002",
            "equipement": "Convoyeur bande C-205",
            "type": "Hebdomadaire",
            "technicien": "Marie Martin",
            "date_planifiee": "2024-12-03",
            "date_realisation": None,
            "statut": "🟢 Planifié",
            "checklist": ["Vérifier tension courroie", "Nettoyer rouleaux", "Contrôler alignement"]
        }
    ]
    
    for bt in bts_preventifs:
        with st.container():
            col_a1, col_a2 = st.columns([3, 1])
            with col_a1:
                st.markdown(f"**{bt['id']} - {bt['equipement']}**")
                st.caption(f"Type: {bt['type']} | Technicien: {bt['technicien']}")
                st.write(f"Date planifiée: {bt['date_planifiee']}")
            
            with col_a2:
                st.markdown(f"**{bt['statut']}**")
            
            # Checklist
            with st.expander("📋 Checklist de maintenance"):
                for item in bt['checklist']:
                    st.checkbox(item, key=f"{bt['id']}_{item}")
            
            # Actions
            col_b1, col_b2, col_b3 = st.columns(3)
            with col_b1:
                if bt["statut"] == "🟢 Planifié":
                    if st.button(f"▶️ Démarrer", key=f"start_{bt['id']}"):
                        st.session_state.bt_en_cours = bt
                        st.success(f"BT {bt['id']} démarré")
            with col_b2:
                if st.button(f"📝 Remplir BT", key=f"fill_{bt['id']}"):
                    show_remplir_bt_preventif(bt)
            with col_b3:
                if st.button(f"📊 Consulter", key=f"consult_{bt['id']}"):
                    show_details_bt_preventif(bt)
            
            st.markdown("---")

# ========== FONCTIONS AUXILIAIRES ==========
def calculer_priorite(criticite, impact_production):
    """Calcule la priorité en fonction de la criticité et de l'impact"""
    if criticite == "Critique" or impact_production == "Arrêt total":
        return "Urgente"
    elif criticite == "Haute" or impact_production == "Arrêt partiel":
        return "Haute"
    elif criticite == "Moyenne" or impact_production == "Ralentissement":
        return "Normale"
    else:
        return "Basse"

def show_generer_bt(demande_data):
    """Affiche le formulaire pour générer un Bon de Travail"""
    st.markdown("### 📄 Génération du Bon de Travail")
    
    with st.form("generer_bt_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Informations BT")
            bt_numero = st.text_input("Numéro BT", f"BT-C-{int(time.time())}")
            technicien_assign = st.selectbox("Technicien assigné*",
                ["Ali ben salah", "Marie Martin", "Paul Bernard", "Sophie Laurent", "À affecter"])
            date_intervention = st.date_input("Date prévue d'intervention*", datetime.date.today())
            temps_estime = st.selectbox("Temps estimé*", ["1h", "2h", "4h", "8h", "1 jour", "Plus"])
        
        with col2:
            st.markdown("#### Ressources nécessaires")
            outillages = st.multiselect("Outillages nécessaires",
                ["Clé à choc", "Multimètre", "Scie sauteuse", "Perceuse", "Autre"])
            pieces_detachees = st.text_area("Pièces détachées",
                placeholder="Listez les pièces nécessaires...")
            risques = st.multiselect("Risques identifiés",
                ["Électrique", "Hauteur", "Manutention", "Chimique", "Bruit", "Autre"])
        
        # Description des travaux
        st.markdown("#### Description des travaux")
        travaux_a_effectuer = st.text_area("Travaux à effectuer*",
            placeholder="Décrivez en détail les travaux à réaliser...",
            height=100)
        
        # Procédures de sécurité
        with st.expander("⚠️ Procédures de sécurité"):
            epi_necessaires = st.multiselect("ÉPI nécessaires",
                ["Casque", "Lunettes", "Gants", "Chaussures de sécurité", "Harnais", "Masque"])
            consignes_securite = st.text_area("Consignes de sécurité spécifiques")
            verif_debranche = st.checkbox("Vérification débranchement électrique")
            verif_isolement = st.checkbox("Vérification isolement zone de travail")
        
        submitted = st.form_submit_button("✅ Générer le Bon de Travail", type="primary")
        
        if submitted:
            if technicien_assign and travaux_a_effectuer:
                bt_data = {
                    **demande_data,
                    "bt_numero": bt_numero,
                    "technicien": technicien_assign,
                    "date_intervention": date_intervention.isoformat(),
                    "temps_estime": temps_estime,
                    "outillages": outillages,
                    "pieces_detachees": pieces_detachees,
                    "risques": risques,
                    "travaux_a_effectuer": travaux_a_effectuer,
                    "epi_necessaires": epi_necessaires,
                    "consignes_securite": consignes_securite,
                    "statut_bt": "🟡 En attente"
                }
                
                st.success(f"✅ Bon de Travail {bt_numero} généré avec succès !")
                st.balloons()
                
                # Option de téléchargement (simulé)
                if st.button("📄 Télécharger le BT au format PDF"):
                    st.info("Fonctionnalité PDF en développement")
            else:
                st.error("Veuillez remplir tous les champs obligatoires")

def show_creer_bt_correctif():
    """Affiche le formulaire pour créer un BT correctif manuellement"""
    st.markdown("### ➕ Création manuelle d'un Bon de Travail")
    
    with st.form("creer_bt_manuel_form"):
        st.markdown("#### Information Équipement")
        col1, col2 = st.columns(2)
        with col1:
            equipement = st.text_input("Équipement*", placeholder="Nom de l'équipement")
            reference = st.text_input("Référence")
            localisation = st.text_input("Localisation*")
        
        with col2:
            type_intervention = st.selectbox("Type d'intervention*",
                ["Réparation", "Remplacement", "Réglage", "Diagnostic"])
            priorite = st.selectbox("Priorité*",
                ["Basse", "Normale", "Haute", "Urgente"])
        
        st.markdown("#### Description du problème")
        description = st.text_area("Description*", height=100,
            placeholder="Décrivez le problème...")
        
        st.markdown("#### Affectation")
        col3, col4 = st.columns(2)
        with col3:
            technicien = st.selectbox("Technicien responsable*",
                ["Ali ben salah", "Marie Martin", "Paul Bernard", "Sophie Laurent"])
            date_planifiee = st.date_input("Date planifiée*", datetime.date.today())
        
        with col4:
            temps_estime = st.number_input("Temps estimé (heures)*", 0.5, 24.0, 2.0, 0.5)
        
        submitted = st.form_submit_button("📝 Créer le BT", type="primary")
        
        if submitted:
            if equipement and localisation and description and technicien:
                st.success(f"✅ BT créé pour {equipement}")
                st.session_state.creating_bt = False
                st.rerun()
            else:
                st.error("Veuillez remplir tous les champs obligatoires")

def show_rapport_bt(bt_data):
    """Affiche un rapport détaillé pour un BT"""
    st.markdown(f"### 📊 Rapport détaillé - {bt_data['id']}")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Informations générales")
        st.write(f"**Équipement:** {bt_data['equipement']}")
        st.write(f"**Référence:** {bt_data['reference']}")
        st.write(f"**Technicien:** {bt_data['technicien']}")
        st.write(f"**Date création:** {bt_data['date_creation']}")
        st.write(f"**Priorité:** {bt_data['priorite']}")
    
    with col2:
        st.markdown("#### Chronologie")
        st.write(f"**Date début:** {bt_data['date_debut']}")
        st.write(f"**Date fin:** {bt_data['date_fin']}")
        st.write(f"**Temps estimé:** {bt_data['temps_estime']}")
        st.write(f"**Temps réel:** {bt_data['temps_reel']}")
        st.write(f"**Statut:** {bt_data['statut']}")
    
    # Section commentaires
    st.markdown("#### Commentaires et observations")
    commentaires = st.text_area("Ajouter des commentaires", 
        placeholder="Notez ici vos observations...")
    
    if st.button("💾 Enregistrer le rapport"):
        st.success("Rapport enregistré avec succès")

def show_generer_bt_preventif(plan_data):
    """Génère un BT préventif à partir du planning"""
    st.markdown(f"### 📄 Génération BT Préventif - {plan_data['equipement']}")
    
    with st.form("bt_preventif_form"):
        st.markdown("#### Checklist de maintenance")
        
        # Checklist générique selon le type
        checklist_items = []
        if plan_data['type'] == "Mensuelle":
            checklist_items = [
                "Vérifier les niveaux de fluide",
                "Contrôler les températures de fonctionnement",
                "Inspecter les joints et étanchéités",
                "Nettoyer les filtres",
                "Graisser les points de lubrification"
            ]
        elif plan_data['type'] == "Hebdomadaire":
            checklist_items = [
                "Vérifier les bruits anormaux",
                "Contrôler les vibrations",
                "Nettoyer les surfaces",
                "Vérifier les serrages"
            ]
        
        for item in checklist_items:
            st.checkbox(item, key=f"check_{hash(item)}")
        
        # Mesures à prendre
        st.markdown("#### Mesures à enregistrer")
        col1, col2, col3 = st.columns(3)
        with col1:
            temperature = st.number_input("Température (°C)", value=25.0)
        with col2:
            pression = st.number_input("Pression (bar)", value=1.0)
        with col3:
            vibration = st.number_input("Vibration (mm/s)", value=0.5)
        
        # Observations
        observations = st.text_area("Observations", 
            placeholder="Notez ici toute observation particulière...")
        
        if st.form_submit_button("✅ Générer le BT Préventif", type="primary"):
            st.success(f"BT préventif généré pour {plan_data['equipement']}")
            st.info("Le BT a été ajouté à la liste des Bons Préventifs")

def show_remplir_bt_preventif(bt_data):
    """Formulaire pour remplir un BT préventif"""
    st.markdown(f"### 📝 Remplissage du BT Préventif - {bt_data['id']}")
    
    with st.form("remplir_bt_preventif_form"):
        # Checklist
        st.markdown("#### Checklist - Cocher les éléments réalisés")
        for item in bt_data.get('checklist', []):
            st.checkbox(item, key=f"done_{hash(item)}")
        
        # Mesures réalisées
        st.markdown("#### Mesures réalisées")
        col1, col2 = st.columns(2)
        with col1:
            date_realisation = st.date_input("Date de réalisation", datetime.date.today())
            heure_debut = st.time_input("Heure de début", datetime.time(9, 0))
        with col2:
            heure_fin = st.time_input("Heure de fin", datetime.time(11, 0))
            temps_passe = st.number_input("Temps total passé (heures)", 0.5, 8.0, 2.0, 0.5)
        
        # Anomalies constatées
        st.markdown("#### Anomalies constatées")
        anomalies = st.text_area("Décrivez les anomalies constatées", 
            placeholder="Si aucune anomalie, laisser vide...")
        
        # Actions correctives
        if anomalies:
            actions_correctives = st.text_area("Actions correctives proposées")
        
        # Consommables utilisés
        consommables = st.text_area("Consommables utilisés", 
            placeholder="Graisse, joints, filtres, etc.")  # CORRECTION ICI
        
        # Signature
        signature = st.text_input("Nom et signature du technicien",
            value=bt_data.get('technicien', ''))
        
        submitted = st.form_submit_button("✅ Clôturer le BT", type="primary")
        
        if submitted:
            st.success(f"BT {bt_data['id']} clôturé avec succès !")
            st.balloons()

def show_details_bt_preventif(bt_data):
    """Affiche les détails d'un BT préventif"""
    st.markdown(f"### 📋 Détails du BT Préventif - {bt_data['id']}")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Informations")
        st.write(f"**Équipement:** {bt_data['equipement']}")
        st.write(f"**Type de maintenance:** {bt_data['type']}")
        st.write(f"**Technicien:** {bt_data['technicien']}")
        st.write(f"**Date planifiée:** {bt_data['date_planifiee']}")
    
    with col2:
        st.markdown("#### Checklist")
        for item in bt_data.get('checklist', []):
            st.write(f"✓ {item}")
    
    st.markdown("#### Historique des interventions")
    # Tableau d'historique simulé
    historique = pd.DataFrame({
        'Date': ['2024-11-02', '2024-10-02', '2024-09-02'],
        'Technicien': ['Ali ben salah', 'Ali ben salah', 'Paul Bernard'],
        'Statut': ['Réalisé', 'Réalisé', 'Réalisé'],
        'Commentaire': ['OK', 'Roulements à surveiller', 'OK']
    })
    st.dataframe(historique, use_container_width=True)

def show_historique_preventif(plan_data):
    """Affiche l'historique des interventions préventives pour un équipement"""
    st.markdown(f"### 📊 Historique des interventions - {plan_data['equipement']}")
    
    # Données d'historique simulées
    historique_data = [
        {
            "date": "2024-11-02",
            "technicien": "Ali ben salah",
            "type": plan_data["type"],
            "statut": "✅ Réalisé",
            "duree": "2h",
            "observations": "Tout est normal, graissage effectué"
        },
        {
            "date": "2024-10-02",
            "technicien": "Ali ben salah",
            "type": plan_data["type"],
            "statut": "✅ Réalisé",
            "duree": "1h45",
            "observations": "Vérification OK, pas d'anomalie"
        },
        {
            "date": "2024-09-02",
            "technicien": "Paul Bernard",
            "type": plan_data["type"],
            "statut": "✅ Réalisé",
            "duree": "2h15",
            "observations": "Roulements à surveiller lors de la prochaine intervention"
        },
        {
            "date": "2024-08-02",
            "technicien": "Marie Martin",
            "type": plan_data["type"],
            "statut": "✅ Réalisé",
            "duree": "2h",
            "observations": "Intervention standard, tout fonctionne correctement"
        }
    ]
    
    # Affichage de l'historique
    for hist in historique_data:
        with st.container():
            col1, col2, col3 = st.columns([2, 2, 2])
            with col1:
                st.write(f"**Date:** {hist['date']}")
                st.write(f"**Technicien:** {hist['technicien']}")
            with col2:
                st.write(f"**Type:** {hist['type']}")
                st.write(f"**Statut:** {hist['statut']}")
            with col3:
                st.write(f"**Durée:** {hist['duree']}")
            
            with st.expander("📝 Observations"):
                st.write(hist['observations'])
            
            st.markdown("---")
    
    # Statistiques de l'historique
    st.markdown("#### 📈 Statistiques de l'équipement")
    
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.metric("Interventions totales", len(historique_data))
    with col_b:
        # Calcul du taux de réalisation
        taux = (len([h for h in historique_data if h["statut"] == "✅ Réalisé"]) / len(historique_data)) * 100
        st.metric("Taux de réalisation", f"{taux:.0f}%")
    with col_c:
        # Calcul de la durée moyenne
        durees = []
        for h in historique_data:
            if "h" in h["duree"]:
                try:
                    heures = float(h["duree"].replace("h", "").strip())
                    durees.append(heures)
                except:
                    continue
        duree_moy = sum(durees) / len(durees) if durees else 0
        st.metric("Durée moyenne", f"{duree_moy:.1f}h")
    
    # Graphique de fréquence
    st.markdown("#### 📅 Fréquence des interventions")
    dates = [h["date"] for h in historique_data]
    frequence_df = pd.DataFrame({
        'Mois': pd.to_datetime(dates).strftime('%Y-%m'),
        'Nombre': [1] * len(dates)
    })
    frequence_agg = frequence_df.groupby('Mois').count().reset_index()
    st.bar_chart(frequence_agg.set_index('Mois'))
    
    # Bouton pour exporter l'historique
    if st.button("📄 Exporter l'historique en PDF"):
        st.info("Export PDF en cours de développement...")
        st.success(f"Historique de {plan_data['equipement']} prêt pour l'export")

def show_planifier_intervention():
    """Formulaire pour planifier une nouvelle intervention préventive"""
    st.markdown("### ➕ Planifier une nouvelle intervention préventive")
    
    with st.form("planifier_intervention_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            equipement = st.text_input("Équipement*", placeholder="Nom de l'équipement")
            reference = st.text_input("Référence équipement")
            type_maintenance = st.selectbox("Type de maintenance*",
                ["Hebdomadaire", "Mensuelle", "Trimestrielle", "Semestrielle", "Annuelle"])
        
        with col2:
            frequence = st.number_input("Fréquence (jours)*", 7, 365, 30, 7)
            date_premiere = st.date_input("Date première intervention*", datetime.date.today())
            technicien = st.selectbox("Technicien responsable",
                ["Ali ben salah", "Marie Martin", "Paul Bernard", "Sophie Laurent", "Rotation"])
        
        # Description des tâches
        description_taches = st.text_area("Tâches à réaliser*", height=100,
            placeholder="Décrivez les tâches de maintenance préventive...")
        
        # Documents associés
        with st.expander("📎 Documents de référence"):
            st.file_uploader("Procédure de maintenance", type=['pdf', 'docx'])
            st.text_input("Référence du manuel")
        
        submitted = st.form_submit_button("📅 Planifier l'intervention", type="primary")
        
        if submitted:
            if equipement and type_maintenance and description_taches:
                st.success(f"Intervention planifiée pour {equipement}")
                st.info(f"Prochaine intervention: {date_premiere}")
            else:
                st.error("Veuillez remplir tous les champs obligatoires")

def show_statistiques_preventives():
    """Affiche les statistiques de maintenance préventive"""
    st.markdown("### 📈 Statistiques de Maintenance Préventive")
    
    # Métriques
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("BT planifiés", "18")
    with col2:
        st.metric("BT réalisés", "15")
    with col3:
        st.metric("Taux réalisation", "83%")
    with col4:
        st.metric("Économies estimées", "45k€")  # CORRECTION ICI
    
    # Graphiques
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown("#### Répartition par type")
        types_data = pd.DataFrame({
            'Type': ['Mensuelle', 'Hebdomadaire', 'Trimestrielle', 'Annuelle'],
            'Nombre': [8, 5, 3, 2]
        })
        st.bar_chart(types_data.set_index('Type'))
    
    with col_b:
        st.markdown("#### Taux de réalisation")
        taux_data = pd.DataFrame({
            'Mois': ['Sep', 'Oct', 'Nov'],
            'Taux': [85, 90, 83]
        })
        st.line_chart(taux_data.set_index('Mois'))
    
    # Tableau des retards
    st.markdown("#### Interventions en retard")
    retards = pd.DataFrame({
        'Équipement': ['Compresseur COMP-01', 'Pompe P-203', 'Ventilateur V-045'],
        'Type': ['Trimestrielle', 'Trimestrielle', 'Trimestrielle'],  # Correction : liste de strings
        'Date prévue': ['2024-11-15', '2024-11-20', '2024-11-25'],
        'Jours retard': [15, 10, 5]
    })
    st.dataframe(retards, use_container_width=True)
def show_equipements():
    """Affiche la page équipements"""
    st.title("🏭 Parc d'Équipements")
    
    # Métriques
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total équipements", "48")
    with col2:
        st.metric("Opérationnels", "42", "+2")
    with col3:
        st.metric("En maintenance", "5", "-1")
    with col4:
        st.metric("Hors service", "1", "0")
    
    # Onglets
    tab1, tab2 = st.tabs(["📋 Inventaire", "➕ Ajouter"])
    
    with tab1:
        # Données exemple
        equipements = pd.DataFrame({
            "ID": ["EQ-001", "EQ-002", "EQ-003", "EQ-004", "EQ-005"],
            "Nom": ["Presse hydraulique 100T", "Tour CNC 5 axes", "Four industriel 800°C", "Robot soudeur KUKA", "Compresseur Atlas"],
            "Type": ["Formage", "Usinage", "Traitement thermique", "Assemblage", "Utilitaire"],
            "Localisation": ["Atelier A", "Atelier B", "Zone chauffage", "Ligne 2", "Salle technique"],
            "État": ["✅ Opérationnel", "⚠️ Maintenance", "✅ Opérationnel", "✅ Opérationnel", "❌ Hors service"],
            "Date installation": ["2020-03-15", "2021-07-22", "2019-11-10", "2022-09-05", "2018-12-18"],
            "Prochaine maintenance": ["2025-01-15", "2024-12-22", "2024-11-30", "2025-02-05", "-"]
        })
        
        # Filtres
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            type_filter = st.multiselect("Type", equipements["Type"].unique())
        
        with col_f2:
            etat_filter = st.multiselect("État", equipements["État"].unique(), default=["✅ Opérationnel"])
        
        # Application filtres
        if type_filter:
            equipements = equipements[equipements["Type"].isin(type_filter)]
        if etat_filter:
            equipements = equipements[equipements["État"].isin(etat_filter)]
        
        st.dataframe(equipements, use_container_width=True, height=400)
        
        # Actions
        if st.button("📊 Générer rapport équipements", type="primary"):
            st.success("Rapport généré !")
    
    with tab2:
        st.subheader("Ajouter un équipement")
        with st.form("new_equipement"):
            col1, col2 = st.columns(2)
            with col1:
                nom = st.text_input("Nom de l'équipement*")
                type_eq = st.selectbox("Type*", ["Formage", "Usinage", "Traitement thermique", "Assemblage", "Utilitaire", "Transport", "Contrôle"])
                marque = st.text_input("Marque")
                modele = st.text_input("Modèle")
            
            with col2:
                localisation = st.text_input("Localisation*")
                num_serie = st.text_input("Numéro de série")
                date_installation = st.date_input("Date d'installation", datetime.date.today())
                etat = st.selectbox("État*", ["✅ Opérationnel", "⚠️ Maintenance", "❌ Hors service"])
            
            notes = st.text_area("Notes techniques")
            
            if st.form_submit_button("✅ Ajouter l'équipement", type="primary"):
                st.success(f"Équipement {nom} ajouté avec succès !")
                st.balloons()

def show_stocks():
    """Affiche la page stocks"""
    st.title("📦 Gestion des Stocks")
    
    # Métriques
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Articles en stock", "156")
    with col2:
        st.metric("Valeur totale", "18,450 €")
    with col3:
        st.metric("À réapprovisionner", "12", "+2")
    with col4:
        st.metric("Ruptures", "3", "-1")
    
    # Onglets
    tab1, tab2, tab3 = st.tabs(["📋 Inventaire", "🚨 Alertes", "📦 Réapprovisionnement"])
    
    with tab1:
        # Données exemple
        stocks = pd.DataFrame({
            "Référence": ["R001-2024", "R002-2024", "R003-2024", "R004-2024", "R005-2024"],
            "Désignation": ["Roulement 6205-2RS", "Courroie synchronisée B85", "Filtre à air industriel", "Joint d'étanchéité Ø150mm", "Capteur température PT100"],
            "Catégorie": ["Roulement", "Transmission", "Filtration", "Étanchéité", "Capteur"],
            "Quantité": [15, 8, 22, 45, 12],
            "Seuil minimum": [5, 3, 10, 20, 5],
            "Unité": ["pièce", "pièce", "pièce", "pièce", "pièce"],
            "Prix unitaire": [45.50, 32.80, 120.00, 8.75, 89.99],
            "Valeur": [682.50, 262.40, 2640.00, 393.75, 1079.88],
            "État": ["✅ Suffisant", "⚠️ Critique", "✅ Suffisant", "✅ Suffisant", "⚠️ Critique"]
        })
        
        st.dataframe(stocks, use_container_width=True, height=400)
        
        # Export
        csv = stocks.to_csv(index=False)
        st.download_button("📥 Exporter l'inventaire", data=csv, file_name="inventaire_stock.csv", mime="text/csv")
    
    with tab2:
        st.subheader("🚨 Alertes stock")
        
        # Alertes critiques
        alertes = pd.DataFrame({
            "Article": ["Courroie B85", "Capteur PT100", "Graisse industrielle"],
            "Quantité actuelle": [8, 12, 5],
            "Seuil minimum": [10, 15, 8],
            "Manquant": [2, 3, 3],
            "Dernière commande": ["2024-10-15", "2024-10-20", "2024-10-25"],
            "Fournisseur": ["Gates Europe", "Endress+Hauser", "Total Energies"]
        })
        
        for _, alerte in alertes.iterrows():
            with st.container():
                st.error(f"**{alerte['Article']}** - Seuil critique: {alerte['Quantité actuelle']}/{alerte['Seuil minimum']}")
                col_a1, col_a2 = st.columns(2)
                with col_a1:
                    st.write(f"Fournisseur: {alerte['Fournisseur']}")
                with col_a2:
                    if st.button(f"Commander {alerte['Article']}", key=f"cmd_{alerte['Article']}"):
                        st.success(f"Commande lancée pour {alerte['Article']}")
                st.markdown("---")
    
    with tab3:
        st.subheader("Réapprovisionnement")
        
        with st.form("reappro_form"):
            article = st.selectbox("Article", ["Roulement 6205", "Courroie B85", "Filtre à air", "Joint étanchéité", "Capteur PT100"])
            fournisseur = st.selectbox("Fournisseur", ["SKF France", "Gates Europe", "Donaldson", "Freudenberg", "Endress+Hauser"])
            quantite = st.number_input("Quantité", min_value=1, value=10)
            delai_livraison = st.number_input("Délai estimé (jours)", min_value=1, max_value=30, value=5)
            urgence = st.selectbox("Urgence", ["Normale", "Urgente", "Très urgente"])
            
            if st.form_submit_button("📦 Passer commande", type="primary"):
                st.success(f"Commande passée pour {quantite} {article} chez {fournisseur}")
                st.balloons()

def show_tiers_management():
    """Page de gestion des tiers (fournisseurs et sous-traitants)"""
    st.title("🤝 Gestion des Tiers")
    
    # Onglets
    tab1, tab2, tab3 = st.tabs(["📋 Liste des Tiers", "🏭 Fournisseurs", "🔧 Sous-traitants"])
    
    with tab1:
        show_all_tiers()
    
    with tab2:
        show_fournisseurs()
    
    with tab3:
        show_soustraitants()

def show_all_tiers():
    """Affiche tous les tiers"""
    st.subheader("📋 Liste complète des Tiers")
    
    # Récupérer tous les tiers
    all_tiers = data_manager.get_all_tiers()
    
    if all_tiers.empty:
        st.info("Aucun tiers enregistré")
        return
    
    # Filtres
    col1, col2, col3 = st.columns(3)
    with col1:
        type_filter = st.multiselect("Type", ["fournisseur", "soustraitant"])
    with col2:
        contrat_filter = st.multiselect("Contrat", ["Actif", "Inactif"])
    with col3:
        search_term = st.text_input("Rechercher par nom")
    
    # Appliquer les filtres
    filtered = all_tiers.copy()
    
    if type_filter:
        filtered = filtered[filtered["type"].isin(type_filter)]
    
    if contrat_filter:
        if "Actif" in contrat_filter:
            filtered = filtered[filtered["contrat_actif"] == True]
        elif "Inactif" in contrat_filter:
            filtered = filtered[filtered["contrat_actif"] == False]
    
    if search_term:
        filtered = filtered[filtered["nom"].str.contains(search_term, case=False, na=False)]
    
    # Affichage
    if not filtered.empty:
        for _, tier in filtered.iterrows():
            with st.container():
                col_a1, col_a2 = st.columns([3, 1])
                with col_a1:
                    st.markdown(f"### {tier['nom']}")
                    st.markdown(f"**Type:** {tier['type'].capitalize()} | **Spécialité:** {tier.get('specialite', 'N/A')}")
                
                with col_a2:
                    status = "🟢 Actif" if tier.get('contrat_actif', False) else "🔴 Inactif"
                    st.markdown(f"**{status}**")
                
                col_b1, col_b2 = st.columns(2)
                with col_b1:
                    st.write(f"**Contact:** {tier['contact_nom']}")
                    st.write(f"**Email:** {tier['contact_email']}")
                    st.write(f"**Téléphone:** {tier['contact_telephone']}")
                
                with col_b2:
                    st.write(f"**Adresse:** {tier['adresse']}")
                    if 'date_debut_contrat' in tier and tier['date_debut_contrat']:
                        st.write(f"**Contrat depuis:** {tier['date_debut_contrat']}")
                    
                    # Affichage spécifique selon le type
                    if tier['type'] == 'fournisseur':
                        if 'delai_livraison_moyen' in tier:
                            st.write(f"**Délai livraison:** {tier['delai_livraison_moyen']} jours")
                    
                    elif tier['type'] == 'soustraitant':
                        if 'taux_horaire' in tier:
                            st.write(f"**Taux horaire:** {tier['taux_horaire']} €/h")
                
                with st.expander("📝 Détails complets"):
                    # Affichage spécifique selon le type
                    if tier['type'] == 'fournisseur':
                        col_c1, col_c2 = st.columns(2)
                        with col_c1:
                            st.write(f"**Mode livraison:** {tier.get('mode_livraison', 'N/A')}")
                            st.write(f"**Note fiabilité:** {tier.get('note_fiabilite', 'N/A')}")
                            st.write(f"**Date début contrat:** {tier.get('date_debut_contrat', 'N/A')}")
                            st.write(f"**Date fin contrat:** {tier.get('date_fin_contrat', 'N/A')}")
                        
                        with col_c2:
                            st.write(f"**Conditions paiement:** {tier.get('conditions_paiement', 'N/A')}")
                            st.write(f"**Notes:** {tier.get('notes', 'Aucune')}")
                    
                    elif tier['type'] == 'soustraitant':
                        col_c1, col_c2 = st.columns(2)
                        with col_c1:
                            st.write(f"**Type intervention:** {tier.get('intervention_type', 'N/A')}")
                            st.write(f"**Zone intervention:** {tier.get('zone_intervention', 'N/A')}")
                            st.write(f"**Certifications:** {', '.join(tier.get('certifications', []))}")
                            st.write(f"**Date début contrat:** {tier.get('date_debut_contrat', 'N/A')}")
                        
                        with col_c2:
                            st.write(f"**Date fin contrat:** {tier.get('date_fin_contrat', 'N/A')}")
                            st.write(f"**Assurance RC Pro:** {'✅ Oui' if tier.get('assurance_rc_pro', False) else '❌ Non'}")
                            if tier.get('assurance_rc_pro', False):
                                st.write(f"**Montant assurance:** {tier.get('montant_assurance', 'N/A')}")
                            st.write(f"**Notes:** {tier.get('notes', 'Aucune')}")
                
                col_btn1, col_btn2, col_btn3 = st.columns(3)
                with col_btn1:
                    if st.button("✏️ Modifier", key=f"edit_{tier['id']}"):
                        st.info(f"Modification de {tier['nom']} - Fonctionnalité en développement")
                
                with col_btn2:
                    if tier.get('contrat_actif', False):
                        if st.button("❌ Désactiver", key=f"deactivate_{tier['id']}"):
                            st.warning(f"Désactivation de {tier['nom']} - Fonctionnalité en développement")
                    else:
                        if st.button("✅ Activer", key=f"activate_{tier['id']}"):
                            st.success(f"Activation de {tier['nom']} - Fonctionnalité en développement")
                
                with col_btn3:
                    if st.button("📧 Contacter", key=f"contact_{tier['id']}"):
                        st.info(f"Contact {tier['contact_email']} - Fonctionnalité en développement")
                
                st.markdown("---")
    else:
        st.warning("Aucun tiers ne correspond aux critères")

def show_fournisseurs():
    """Affiche la gestion des fournisseurs"""
    st.subheader("🏭 Fournisseurs")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("**Ajouter un nouveau fournisseur**")
        
        with st.form("new_fournisseur_form"):
            nom = st.text_input("Nom de l'entreprise*", placeholder="Ex: SKF France")
            specialite = st.text_input("Spécialité*", placeholder="Ex: Roulements et joints")
            contact_nom = st.text_input("Nom du contact*", placeholder="Ex: Pierre Dubois")
            contact_email = st.text_input("Email*", placeholder="Ex: p.dubois@skf.fr")
            contact_telephone = st.text_input("Téléphone*", placeholder="Ex: 01 23 45 67 89")
            adresse = st.text_area("Adresse*", placeholder="Ex: 12 Rue des Industries, 75000 Paris")
            
            col_a, col_b = st.columns(2)
            with col_a:
                delai_livraison_moyen = st.number_input("Délai livraison moyen (jours)", min_value=1, value=3)
                mode_livraison = st.selectbox("Mode livraison", ["Express", "Standard", "Économique"])
                note_fiabilite = st.slider("Note de fiabilité", 1.0, 5.0, 4.0, 0.1)
            
            with col_b:
                date_debut = st.date_input("Date début contrat", datetime.date.today())
                date_fin = st.date_input("Date fin contrat", datetime.date.today() + datetime.timedelta(days=365))
                conditions_paiement = st.selectbox("Conditions paiement", ["30 jours net", "60 jours net", "Comptant", "Sur facture"])
            
            notes = st.text_area("Notes", placeholder="Informations complémentaires...")
            
            if st.form_submit_button("➕ Ajouter le fournisseur", type="primary"):
                if nom and specialite and contact_nom and contact_email and contact_telephone and adresse:
                    fournisseur_data = {
                        "id": max([f["id"] for f in data_manager.tiers["fournisseurs"]], default=0) + 1,
                        "nom": nom,
                        "type": "fournisseur",
                        "specialite": specialite,
                        "contact_nom": contact_nom,
                        "contact_email": contact_email,
                        "contact_telephone": contact_telephone,
                        "adresse": adresse,
                        "delai_livraison_moyen": delai_livraison_moyen,
                        "mode_livraison": mode_livraison,
                        "note_fiabilite": note_fiabilite,
                        "contrat_actif": True,
                        "date_debut_contrat": date_debut.isoformat(),
                        "date_fin_contrat": date_fin.isoformat(),
                        "conditions_paiement": conditions_paiement,
                        "notes": notes
                    }
                    
                    data_manager.tiers["fournisseurs"].append(fournisseur_data)
                    data_manager.save_tiers()
                    st.success(f"✅ Fournisseur {nom} ajouté avec succès !")
                    st.balloons()
                else:
                    st.error("Veuillez remplir tous les champs obligatoires (*)")
    
    with col2:
        st.markdown("### Statistiques")
        fournisseurs = data_manager.get_fournisseurs()
        
        if not fournisseurs.empty:
            st.metric("Nombre", len(fournisseurs))
            actifs = len(fournisseurs[fournisseurs["contrat_actif"] == True])
            st.metric("Contrats actifs", actifs)
            
            # Fournisseurs avec contrat expirant bientôt
            today = datetime.date.today()
            soon = today + datetime.timedelta(days=30)
            contracts_expiring = 0
            
            for f in data_manager.tiers["fournisseurs"]:
                if f.get("contrat_actif", False) and f.get("date_fin_contrat"):
                    try:
                        date_fin = datetime.datetime.fromisoformat(f["date_fin_contrat"]).date()
                        if today <= date_fin <= soon:
                            contracts_expiring += 1
                    except:
                        continue
            
            if contracts_expiring > 0:
                st.warning(f"⚠️ {contracts_expiring} contrat(s) expire(nt) bientôt")
            else:
                st.success("✅ Aucun contrat n'expire dans les 30 jours")
        else:
            st.info("Aucun fournisseur")

def show_soustraitants():
    """Affiche la gestion des sous-traitants"""
    st.subheader("🔧 Sous-traitants")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("**Ajouter un nouveau sous-traitant**")
        
        with st.form("new_soustraitant_form"):
            nom = st.text_input("Nom de l'entreprise*", placeholder="Ex: Méca Pro Services")
            specialite = st.text_input("Spécialité*", placeholder="Ex: Maintenance mécanique lourde")
            contact_nom = st.text_input("Nom du contact*", placeholder="Ex: Robert Chen")
            contact_email = st.text_input("Email*", placeholder="Ex: r.chen@mecapro.fr")
            contact_telephone = st.text_input("Téléphone*", placeholder="Ex: 04 56 78 90 12")
            adresse = st.text_area("Adresse*", placeholder="Ex: 123 Rue de la Réparation, 59000 Lille")
            
            col_a, col_b = st.columns(2)
            with col_a:
                intervention_type = st.selectbox("Type d'intervention", ["Urgences 24/7", "Planifiée", "Spécialisée", "Générale"])
                taux_horaire = st.number_input("Taux horaire (€)", min_value=0.0, value=85.0, step=5.0)
                zone_intervention = st.text_input("Zone d'intervention", placeholder="Ex: Région Nord")
            
            with col_b:
                certifications = st.multiselect("Certifications", ["ISO 9001", "Qualibat", "MASE", "ISO 14001", "Autre"])
                if "Autre" in certifications:
                    autre_certif = st.text_input("Autre certification")
                    if autre_certif:
                        certifications.remove("Autre")
                        certifications.append(autre_certif)
                
                date_debut = st.date_input("Date début contrat", datetime.date.today())
                date_fin = st.date_input("Date fin contrat", datetime.date.today() + datetime.timedelta(days=365))
            
            assurance_rc_pro = st.checkbox("Assurance RC Professionnelle", value=True)
            montant_assurance = st.text_input("Montant assurance", value="5 000 000 €") if assurance_rc_pro else ""
            
            notes = st.text_area("Notes", placeholder="Informations complémentaires...")
            
            if st.form_submit_button("➕ Ajouter le sous-traitant", type="primary"):
                if nom and specialite and contact_nom and contact_email and contact_telephone and adresse:
                    soustraitant_data = {
                        "id": max([s["id"] for s in data_manager.tiers["soustraitants"]], default=100) + 1,
                        "nom": nom,
                        "type": "soustraitant",
                        "specialite": specialite,
                        "contact_nom": contact_nom,
                        "contact_email": contact_email,
                        "contact_telephone": contact_telephone,
                        "adresse": adresse,
                        "intervention_type": intervention_type,
                        "taux_horaire": taux_horaire,
                        "zone_intervention": zone_intervention,
                        "certifications": certifications,
                        "contrat_actif": True,
                        "date_debut_contrat": date_debut.isoformat(),
                        "date_fin_contrat": date_fin.isoformat(),
                        "assurance_rc_pro": assurance_rc_pro,
                        "montant_assurance": montant_assurance if assurance_rc_pro else "",
                        "notes": notes
                    }
                    
                    data_manager.tiers["soustraitants"].append(soustraitant_data)
                    data_manager.save_tiers()
                    st.success(f"✅ Sous-traitant {nom} ajouté avec succès !")
                    st.balloons()
                else:
                    st.error("Veuillez remplir tous les champs obligatoires (*)")
    
    with col2:
        st.markdown("### Statistiques")
        soustraitants = data_manager.get_soustraitants()
        
        if not soustraitants.empty:
            st.metric("Nombre", len(soustraitants))
            
            # Calcul taux horaire moyen
            taux_moyen = soustraitants["taux_horaire"].mean()
            st.metric("Taux horaire moyen", f"{taux_moyen:.0f} €")
            
            # Sous-traitants avec assurance
            avec_assurance = len(soustraitants[soustraitants["assurance_rc_pro"] == True])
            st.metric("Avec assurance RC", f"{avec_assurance}/{len(soustraitants)}")
        else:
            st.info("Aucun sous-traitant")

# ========== GESTION DES PERSONNELS (VERSION PERSISTANTE - NOMS TUNISIENS) ==========
def show_personnels_management():
    """Page de gestion des personnels"""
    st.title("👥 Gestion du Personnel")
    
    # === AJOUTE CETTE SECTION ===
    # Bouton de réinitialisation (visible uniquement pour admin)
    if st.session_state.user.get("role") == "admin":
        col_reset1, col_reset2 = st.columns([6, 1])
        with col_reset2:
            if st.button("🔄", help="Réinitialiser avec noms tunisiens", key="reset_tunisian"):
                if st.button("✅ Confirmer", key="confirm_reset"):
                    success = data_manager.reset_to_tunisian_personnels()
                    if success:
                        time.sleep(2)
                        st.rerun()
    
    # Vérifier si on est en mode édition
    if 'editing_personnel' in st.session_state and st.session_state.editing_personnel:
        show_modifier_technicien(st.session_state.editing_personnel)
        return
    
    # Onglets principaux
    tab1, tab2, tab3, tab4 = st.tabs([
        "📋 Liste du Personnel", 
        "➕ Ajouter un Personnel", 
        "🎓 Habilitations", 
        "📊 Statistiques"
    ])
    
    with tab1:
        show_liste_personnel()
    
    with tab2:
        show_ajouter_personnel()
    
    with tab3:
        show_gestion_habilitations()
    
    with tab4:
        show_statistiques_personnel()

def show_liste_personnel():
    """Affiche la liste du personnel"""
    st.subheader("📋 Liste du Personnel")
    
    # Récupérer les personnels depuis DataManager
    personnels = data_manager.get_all_personnels()
    
    if not personnels:
        st.info("Aucun personnel enregistré. Ajoutez votre premier membre !")
        return
    
    # Filtres
    col1, col2, col3 = st.columns(3)
    with col1:
        services = sorted(list(set([p.get("service", "Non spécifié") for p in personnels])))
        service_filter = st.multiselect("Service/Département", services)
    
    with col2:
        statuts = sorted(list(set([p.get("statut", "Non spécifié") for p in personnels])))
        statut_filter = st.multiselect("Statut", statuts)
    
    with col3:
        search_term = st.text_input("Rechercher par nom/matricule")
    
    # Application des filtres
    filtered_personnels = personnels.copy()
    
    if service_filter:
        filtered_personnels = [p for p in filtered_personnels if p.get("service") in service_filter]
    
    if statut_filter:
        filtered_personnels = [p for p in filtered_personnels if p.get("statut") in statut_filter]
    
    if search_term:
        search_term = search_term.lower()
        filtered_personnels = [
            p for p in filtered_personnels 
            if search_term in p.get("nom", "").lower() or search_term in p.get("matricule", "").lower()
        ]
    
    # Métriques
    st.markdown(f"**Total:** {len(personnels)} membres | **Filtrés:** {len(filtered_personnels)}")
    
    # Affichage
    if not filtered_personnels:
        st.warning("Aucun personnel ne correspond aux critères")
        return
    
    for personnel in filtered_personnels:
        with st.container():
            col_a1, col_a2, col_a3 = st.columns([3, 2, 1])
            with col_a1:
                st.markdown(f"### {personnel.get('nom', 'Non nommé')}")
                st.markdown(f"**{personnel.get('poste', 'Non spécifié')}** | *{personnel.get('service', 'Non spécifié')}*")
                st.caption(f"Matricule: {personnel.get('matricule', 'N/A')} | Expérience: {personnel.get('experience', 'N/A')}")
            
            with col_a2:
                st.metric("Coût horaire", f"{personnel.get('cout_horaire', 0)} €")
                if personnel.get('date_embauche'):
                    st.write(f"**Embauché le:** {personnel['date_embauche'][:10]}")
            
            with col_a3:
                statut = personnel.get('statut', 'Non spécifié')
                if "Actif" in statut:
                    color = "green"
                elif "Congés" in statut:
                    color = "orange"
                elif "Formation" in statut:
                    color = "purple"
                else:
                    color = "red"
                st.markdown(f'<span style="color: {color}; font-weight: bold; font-size: 18px;">{statut}</span>', 
                           unsafe_allow_html=True)
            
            # Compétences et habilitations
            col_b1, col_b2 = st.columns(2)
            with col_b1:
                if personnel.get('competences'):
                    with st.expander("🔧 Compétences principales"):
                        for comp in personnel['competences'][:5]:
                            st.markdown(f"• {comp}")
                        if len(personnel['competences']) > 5:
                            st.caption(f"+ {len(personnel['competences']) - 5} autres...")
            
            with col_b2:
                if personnel.get('habilitations'):
                    with st.expander("🎓 Habilitations"):
                        for hab in personnel['habilitations'][:5]:
                            st.markdown(f"✓ {hab}")
                        if len(personnel['habilitations']) > 5:
                            st.caption(f"+ {len(personnel['habilitations']) - 5} autres...")
            
            # Notes
            if personnel.get("notes"):
                st.info(f"**Notes:** {personnel['notes'][:100]}...")
            
            # Actions
            col_c1, col_c2, col_c3, col_c4 = st.columns(4)
            with col_c1:
                if st.button(f"✏️ Modifier", key=f"edit_{personnel['id']}"):
                    st.session_state.editing_personnel = personnel
                    st.rerun()
            
            with col_c2:
                if st.button(f"📅 Planning", key=f"planning_{personnel['id']}"):
                    show_planning_technicien(personnel)
            
            with col_c3:
                if st.button(f"📊 Performance", key=f"perf_{personnel['id']}"):
                    show_performance_technicien(personnel)
            
            with col_c4:
                if st.button(f"🗑️", key=f"delete_{personnel['id']}", help="Supprimer"):
                    # Confirmation dans un popover
                    with st.popover("⚠️ Confirmer la suppression"):
                        st.warning(f"Êtes-vous sûr de vouloir supprimer {personnel['nom']} ?")
                        col_conf1, col_conf2 = st.columns(2)
                        with col_conf1:
                            if st.button(f"✅ Oui", key=f"confirm_yes_{personnel['id']}"):
                                # Supprimer via DataManager
                                data_manager.delete_personnel(personnel['id'])
                                st.success(f"Personnel {personnel['nom']} supprimé avec succès")
                                time.sleep(1)
                                st.rerun()
                        with col_conf2:
                            if st.button(f"❌ Non", key=f"confirm_no_{personnel['id']}"):
                                st.rerun()
            
            st.markdown("---")

def show_ajouter_personnel():
    """Formulaire pour ajouter un nouveau membre du personnel"""
    st.subheader("➕ Ajouter un Nouveau Membre du Personnel")
    
    with st.form("form_ajouter_personnel"):
        st.markdown("### Informations personnelles")
        
        col1, col2 = st.columns(2)
        with col1:
            nom = st.text_input("Nom complet*", placeholder="Ex: Ahmed Ben Salah")
            matricule = st.text_input("Matricule*", placeholder="Ex: PER-006")
            date_naissance = st.date_input("Date de naissance", datetime.date(1990, 1, 1))
            adresse = st.text_area("Adresse", placeholder="Adresse complète...")
        
        with col2:
            telephone = st.text_input("Téléphone*", placeholder="Ex: +216 23 456 789")
            email = st.text_input("Email professionnel*", placeholder="Ex: ahmed.bensalah@entreprise.tn")
            date_embauche = st.date_input("Date d'embauche*", datetime.date.today())
            type_contrat = st.selectbox("Type de contrat*",
                ["CDI", "CDD", "Intérim", "Apprentissage", "Stage", "Consultant"])
        
        st.markdown("### Informations professionnelles")
        col3, col4 = st.columns(2)
        with col3:
            # Poste avec nouvelles options
            poste = st.selectbox("Poste/Fonction*",
                [
                    "Ingénieur Maintenance", "Ingénieur Électrique", "Ingénieur Mécanique",
                    "Responsable Maintenance", "Responsable d'Atelier", "Responsable Qualité",
                    "Technicien Supérieur", "Technicien Mécanicien", "Technicien Électricien", 
                    "Technicien Polyvalent", "Technicien Instrumentation",
                    "Chef d'Équipe", "Superviseur", "Contremaître",
                    "Gestionnaire de Stock", "Planificateur Maintenance", "Coordinateur",
                    "Apprenti", "Stagiaire", "Opérateur", "Autre"
                ])
            if poste == "Autre":
                poste = st.text_input("Précisez le poste")
            
            # Service/Département avec nouvelles options
            service = st.selectbox("Service/Département*",
                [
                    "Direction Maintenance", "Maintenance Industrielle", "Maintenance Mécanique",
                    "Maintenance Électrique", "Maintenance Automatisme", "Maintenance Instrumentation",
                    "Maintenance Préventive", "Maintenance Corrective", "Gestion de Parc",
                    "Qualité & Contrôle", "Sécurité Industrielle", "Logistique & Stock",
                    "Production", "Ingénierie", "Support Technique", "Formation", "Management"
                ])
        
        with col4:
            cout_horaire = st.number_input("Coût horaire (€)*", 15.0, 150.0, 45.0, 0.5)
            niveau_experience = st.selectbox("Niveau d'expérience",
                ["Débutant (<2 ans)", "Intermédiaire (2-5 ans)", "Confirmé (5-10 ans)", "Expert (>10 ans)", "Sénior (>15 ans)"])
            statut = st.selectbox("Statut*", ["🟢 Actif", "🟡 Congés", "🔴 Absent", "🟣 Formation", "⚫ Détaché"])
        
        st.markdown("### Compétences techniques")
        competences = st.multiselect("Compétences principales",
            [
                "Soudage TIG/MIG", "Usinage CNC", "Électricité BT/HT", "Automatisme Siemens", 
                "PLC Allen Bradley", "Hydraulique Industrielle", "Pneumatique", "Diagnostic Avancé",
                "Lecture de plans", "Contrôle qualité", "Maintenance préventive", "Gestion de stock",
                "Formation", "Management d'équipe", "Lean Maintenance", "TPM", "CMMS",
                "Robotique", "Instrumentation", "Régulation", "Sécurité Industrielle",
                "Gestion de projet", "Analyse de données", "Reporting", "Audit"
            ])
        
        autres_competences = st.text_input("Autres compétences (séparées par des virgules)",
            placeholder="Ex: Robotique KUKA, Instrumentation Endress+Hauser, Régulation Siemens...")
        
        st.markdown("### Habilitations & Certifications")
        habilitations = st.multiselect("Habilitations",
            [
                "Électricien H0V B2V BR", "Chariot élévateur CACES 1-3-5", "Nacelle CACES", 
                "Travaux en hauteur", "SST (Sauveteur Secouriste)", "Habilitation ATEX",
                "Certifié ISO 9001", "Certifié ISO 14001", "Certifié OHSAS 18001",
                "Formateur interne", "Auditeur interne", "Permis poids lourd",
                "Soudage certifié", "Certification Siemens", "Certification Rockwell",
                "Certification Schneider", "Certification Endress+Hauser", "Autre"
            ])
        
        autre_habilitation = st.text_input("Autre habilitation/certification",
            placeholder="Précisez si autre")
        
        st.markdown("### Diplômes et formations")
        diplome = st.text_input("Diplôme le plus élevé",
            placeholder="Ex: Diplôme d'Ingénieur en Maintenance Industrielle, BTS, Licence...")
        specialite = st.text_input("Spécialisation",
            placeholder="Ex: Automatisme et Informatique Industrielle, Génie Mécanique...")
        
        # Notes
        notes = st.text_area("Notes et observations",
            placeholder="Informations complémentaires, projets spécifiques, langues parlées...")
        
        submitted = st.form_submit_button("✅ Ajouter le Personnel", type="primary")
        
        if submitted:
            if nom and matricule and telephone and email and poste and service:
                # Vérifier si le matricule existe déjà
                personnels = data_manager.get_all_personnels()
                matricule_existe = any(p.get("matricule") == matricule for p in personnels)
                
                if matricule_existe:
                    st.error(f"❌ Le matricule {matricule} existe déjà ! Veuillez utiliser un matricule unique.")
                else:
                    # Calcul de l'expérience
                    today = datetime.date.today()
                    annees_experience = today.year - date_embauche.year
                    if today.month < date_embauche.month or (today.month == date_embauche.month and today.day < date_embauche.day):
                        annees_experience -= 1
                    experience = f"{annees_experience} an(s)"
                    
                    # Ajouter les compétences supplémentaires
                    toutes_competences = competences.copy()
                    if autres_competences:
                        autres = [c.strip() for c in autres_competences.split(",") if c.strip()]
                        toutes_competences.extend(autres)
                    
                    # Ajouter les habilitations
                    toutes_habilitations = habilitations.copy()
                    if autre_habilitation:
                        toutes_habilitations.append(autre_habilitation)
                    
                    personnel_data = {
                        "nom": nom,
                        "matricule": matricule,
                        "poste": poste,
                        "service": service,
                        "cout_horaire": float(cout_horaire),
                        "statut": statut,
                        "experience": experience,
                        "competences": toutes_competences,
                        "habilitations": toutes_habilitations,
                        "date_embauche": date_embauche.isoformat(),
                        "date_naissance": date_naissance.isoformat(),
                        "telephone": telephone,
                        "email": email,
                        "type_contrat": type_contrat,
                        "adresse": adresse,
                        "diplome": diplome,
                        "specialite": specialite,
                        "notes": notes,
                        "date_creation": datetime.datetime.now().isoformat(),
                        "derniere_evaluation": datetime.date.today().isoformat()
                    }
                    
                    # Ajouter via DataManager
                    nouveau_id = data_manager.add_personnel(personnel_data)
                    
                    st.success(f"✅ Personnel {nom} ajouté avec succès !")
                    st.balloons()
                    st.info(f"Matricule: {matricule} | Service: {service}")
                    
                    # Afficher un résumé
                    with st.expander("📋 Voir le détail du personnel ajouté"):
                        col_sum1, col_sum2 = st.columns(2)
                        with col_sum1:
                            st.write(f"**Nom:** {nom}")
                            st.write(f"**Matricule:** {matricule}")
                            st.write(f"**Poste:** {poste}")
                            st.write(f"**Service:** {service}")
                            st.write(f"**Coût horaire:** {cout_horaire} €")
                        
                        with col_sum2:
                            st.write(f"**Statut:** {statut}")
                            st.write(f"**Expérience:** {experience}")
                            st.write(f"**Type contrat:** {type_contrat}")
                            st.write(f"**Date embauche:** {date_embauche}")
                            st.write(f"**Diplôme:** {diplome}")
                    
                    # Attendre 3 secondes puis réinitialiser
                    time.sleep(3)
                    st.rerun()
            else:
                st.error("Veuillez remplir tous les champs obligatoires (*)")
    
    # Bouton pour voir la liste
    if st.button("📋 Voir la liste du personnel"):
        st.info("Revenez à l'onglet 'Liste du Personnel' pour voir tous les membres")

def show_modifier_technicien(personnel):
    """Affiche le formulaire pour modifier un membre du personnel existant"""
    st.subheader(f"✏️ Modifier le Personnel: {personnel.get('nom', '')}")
    
    # Bouton de retour
    if st.button("↩️ Retour à la liste"):
        st.session_state.editing_personnel = None
        st.rerun()
    
    st.markdown("---")
    
    with st.form(f"form_modifier_personnel_{personnel['id']}"):
        st.markdown("### Informations personnelles")
        
        col1, col2 = st.columns(2)
        with col1:
            nom = st.text_input("Nom complet*", 
                value=personnel.get('nom', ''))
            
            matricule = st.text_input("Matricule*", 
                value=personnel.get('matricule', ''))
            
            # Date de naissance
            date_naissance_default = datetime.date(1990, 1, 1)
            if personnel.get('date_naissance'):
                try:
                    date_naissance_default = datetime.datetime.fromisoformat(
                        personnel['date_naissance'].split('T')[0]
                    ).date()
                except:
                    pass
            date_naissance = st.date_input("Date de naissance", value=date_naissance_default)
            
            adresse = st.text_area("Adresse", 
                value=personnel.get('adresse', ''))
        
        with col2:
            telephone = st.text_input("Téléphone*", 
                value=personnel.get('telephone', ''))
            
            email = st.text_input("Email professionnel*", 
                value=personnel.get('email', ''))
            
            # Date d'embauche
            date_embauche_default = datetime.date.today()
            if personnel.get('date_embauche'):
                try:
                    date_embauche_default = datetime.datetime.fromisoformat(
                        personnel['date_embauche'].split('T')[0]
                    ).date()
                except:
                    pass
            date_embauche = st.date_input("Date d'embauche*", value=date_embauche_default)
            
            # Type de contrat
            type_contrat_options = ["CDI", "CDD", "Intérim", "Apprentissage", "Stage", "Consultant"]
            type_contrat_value = personnel.get('type_contrat', 'CDI')
            type_contrat_index = type_contrat_options.index(type_contrat_value) if type_contrat_value in type_contrat_options else 0
            type_contrat = st.selectbox("Type de contrat*", type_contrat_options, index=type_contrat_index)
        
        st.markdown("### Informations professionnelles")
        col3, col4 = st.columns(2)
        
        with col3:
            # Poste avec nouvelles options
            poste_options = [
                "Ingénieur Maintenance", "Ingénieur Électrique", "Ingénieur Mécanique",
                "Responsable Maintenance", "Responsable d'Atelier", "Responsable Qualité",
                "Technicien Supérieur", "Technicien Mécanicien", "Technicien Électricien", 
                "Technicien Polyvalent", "Technicien Instrumentation",
                "Chef d'Équipe", "Superviseur", "Contremaître",
                "Gestionnaire de Stock", "Planificateur Maintenance", "Coordinateur",
                "Apprenti", "Stagiaire", "Opérateur", "Autre"
            ]
            poste_value = personnel.get('poste', 'Technicien Mécanicien')
            if poste_value not in poste_options:
                poste_options.append(poste_value)
            poste_index = poste_options.index(poste_value)
            poste = st.selectbox("Poste/Fonction*", poste_options, index=poste_index)
            
            # Service/Département avec nouvelles options
            service_options = [
                "Direction Maintenance", "Maintenance Industrielle", "Maintenance Mécanique",
                "Maintenance Électrique", "Maintenance Automatisme", "Maintenance Instrumentation",
                "Maintenance Préventive", "Maintenance Corrective", "Gestion de Parc",
                "Qualité & Contrôle", "Sécurité Industrielle", "Logistique & Stock",
                "Production", "Ingénierie", "Support Technique", "Formation", "Management"
            ]
            service_value = personnel.get('service', 'Maintenance Industrielle')
            if service_value not in service_options:
                service_options.append(service_value)
            service_index = service_options.index(service_value)
            service = st.selectbox("Service/Département*", service_options, index=service_index)
        
        with col4:
            # Coût horaire
            cout_horaire = st.number_input("Coût horaire (€)*", 
                min_value=15.0, 
                max_value=150.0, 
                value=float(personnel.get('cout_horaire', 45.0)), 
                step=0.5)
            
            # Niveau d'expérience
            niveau_options = ["Débutant (<2 ans)", "Intermédiaire (2-5 ans)", "Confirmé (5-10 ans)", "Expert (>10 ans)", "Sénior (>15 ans)"]
            experience_value = personnel.get('experience', '')
            niveau_index = 1  # Valeur par défaut
            for i, option in enumerate(niveau_options):
                if any(word in experience_value for word in option.split()[:2]):
                    niveau_index = i
                    break
            niveau_experience = st.selectbox("Niveau d'expérience", niveau_options, index=niveau_index)
            
            # Statut
            statut_options = ["🟢 Actif", "🟡 Congés", "🔴 Absent", "🟣 Formation", "⚫ Détaché"]
            statut_value = personnel.get('statut', '🟢 Actif')
            statut_index = statut_options.index(statut_value) if statut_value in statut_options else 0
            statut = st.selectbox("Statut*", statut_options, index=statut_index)
        
        st.markdown("### Compétences techniques")
        
        # Compétences existantes
        competences_existantes = personnel.get('competences', [])
        competences_options = [
            "Soudage TIG/MIG", "Usinage CNC", "Électricité BT/HT", "Automatisme Siemens", 
            "PLC Allen Bradley", "Hydraulique Industrielle", "Pneumatique", "Diagnostic Avancé",
            "Lecture de plans", "Contrôle qualité", "Maintenance préventive", "Gestion de stock",
            "Formation", "Management d'équipe", "Lean Maintenance", "TPM", "CMMS",
            "Robotique", "Instrumentation", "Régulation", "Sécurité Industrielle",
            "Gestion de projet", "Analyse de données", "Reporting", "Audit"
        ]
        
        # Ajouter les compétences existantes qui ne sont pas dans la liste
        for comp in competences_existantes:
            if comp not in competences_options:
                competences_options.append(comp)
        
        competences = st.multiselect("Compétences principales", 
            options=competences_options,
            default=[c for c in competences_existantes if c in competences_options])
        
        # Autres compétences
        autres_competences_existantes = [c for c in competences_existantes if c not in competences_options]
        autres_competences = st.text_input("Autres compétences (séparées par des virgules)",
            value=", ".join(autres_competences_existantes))
        
        st.markdown("### Habilitations & Certifications")
        
        # Habilitations existantes
        habilitations_existantes = personnel.get('habilitations', [])
        habilitations_options = [
            "Électricien H0V B2V BR", "Chariot élévateur CACES 1-3-5", "Nacelle CACES", 
            "Travaux en hauteur", "SST (Sauveteur Secouriste)", "Habilitation ATEX",
            "Certifié ISO 9001", "Certifié ISO 14001", "Certifié OHSAS 18001",
            "Formateur interne", "Auditeur interne", "Permis poids lourd",
            "Soudage certifié", "Certification Siemens", "Certification Rockwell",
            "Certification Schneider", "Certification Endress+Hauser", "Autre"
        ]
        
        # Ajouter les habilitations existantes qui ne sont pas dans la liste
        for hab in habilitations_existantes:
            if hab not in habilitations_options:
                habilitations_options.append(hab)
        
        habilitations = st.multiselect("Habilitations & Certifications", 
            options=habilitations_options,
            default=[h for h in habilitations_existantes if h in habilitations_options])
        
        # Autre habilitation
        autre_habilitation_existante = next((h for h in habilitations_existantes if h not in habilitations_options), "")
        autre_habilitation = st.text_input("Autre habilitation/certification", value=autre_habilitation_existante)
        
        st.markdown("### Diplômes et formations")
        
        diplome = st.text_input("Diplôme le plus élevé", value=personnel.get('diplome', ''))
        specialite = st.text_input("Spécialisation", value=personnel.get('specialite', ''))
        
        # Notes
        notes = st.text_area("Notes et observations", value=personnel.get('notes', ''))
        
        col_submit1, col_submit2 = st.columns(2)
        with col_submit1:
            submitted = st.form_submit_button("💾 Enregistrer", type="primary")
        with col_submit2:
            cancel = st.form_submit_button("❌ Annuler")
        
        if submitted:
            if nom and matricule and telephone and email and poste and service:
                # Vérifier si le matricule est unique (sauf pour le personnel en cours)
                personnels = data_manager.get_all_personnels()
                matricule_existe = False
                for p in personnels:
                    if p["matricule"] == matricule and p["id"] != personnel["id"]:
                        matricule_existe = True
                        break
                
                if matricule_existe:
                    st.error(f"❌ Le matricule {matricule} existe déjà pour un autre membre !")
                else:
                    # Calcul de l'expérience mise à jour
                    today = datetime.date.today()
                    annees_experience = today.year - date_embauche.year
                    if today.month < date_embauche.month or (today.month == date_embauche.month and today.day < date_embauche.day):
                        annees_experience -= 1
                    experience = f"{annees_experience} an(s)"
                    
                    # Fusionner les compétences
                    toutes_competences = competences.copy()
                    if autres_competences:
                        autres = [c.strip() for c in autres_competences.split(",") if c.strip()]
                        toutes_competences.extend(autres)
                    
                    # Fusionner les habilitations
                    toutes_habilitations = habilitations.copy()
                    if autre_habilitation:
                        toutes_habilitations.append(autre_habilitation.strip())
                    
                    # Mettre à jour le personnel
                    personnel_data = {
                        "id": personnel['id'],
                        "nom": nom,
                        "matricule": matricule,
                        "poste": poste,
                        "service": service,
                        "cout_horaire": float(cout_horaire),
                        "statut": statut,
                        "experience": experience,
                        "competences": toutes_competences,
                        "habilitations": toutes_habilitations,
                        "date_embauche": date_embauche.isoformat(),
                        "date_naissance": date_naissance.isoformat(),
                        "telephone": telephone,
                        "email": email,
                        "type_contrat": type_contrat,
                        "adresse": adresse,
                        "diplome": diplome,
                        "specialite": specialite,
                        "notes": notes,
                        "date_creation": personnel.get('date_creation', datetime.datetime.now().isoformat()),
                        "derniere_evaluation": datetime.date.today().isoformat(),
                        "date_modification": datetime.datetime.now().isoformat()
                    }
                    
                    # Mettre à jour via DataManager
                    data_manager.update_personnel(personnel['id'], personnel_data)
                    
                    st.success(f"✅ Personnel {nom} modifié avec succès !")
                    st.balloons()
                    
                    # Attendre 2 secondes puis revenir à la liste
                    time.sleep(2)
                    st.session_state.editing_personnel = None
                    st.rerun()
            else:
                st.error("Veuillez remplir tous les champs obligatoires (*)")
        
        elif cancel:
            st.session_state.editing_personnel = None
            st.rerun()

def show_gestion_habilitations():
    """Gestion des habilitations du personnel"""
    st.subheader("🎓 Gestion des Habilitations")
    
    # Onglets pour les habilitations
    tab1, tab2, tab3 = st.tabs(["📋 Habilitations par Personne", "📅 Validités", "➕ Ajouter Habilitation"])
    
    with tab1:
        show_habilitations_par_personne()
    
    with tab2:
        show_validites_habilitations()
    
    with tab3:
        show_ajouter_habilitation()

def show_habilitations_par_personne():
    """Affiche les habilitations par personne"""
    st.markdown("### 📋 Habilitations par Technicien")
    
    personnels = data_manager.get_all_personnels()
    
    if not personnels:
        st.info("Aucun technicien enregistré")
        return
    
    for personnel in personnels:
        with st.container():
            st.markdown(f"**{personnel.get('nom')}** ({personnel.get('matricule')})")
            
            habilitations = personnel.get('habilitations', [])
            if habilitations:
                for hab in habilitations:
                    col_h1, col_h2 = st.columns([4, 1])
                    with col_h1:
                        st.write(f"• {hab}")
                    with col_h2:
                        st.success("✓ Valide")
            else:
                st.info("Aucune habilitation enregistrée")
            
            st.markdown("---")

def show_validites_habilitations():
    """Affiche les validités des habilitations"""
    st.markdown("### 📅 Suivi des Validités")
    
    st.info("Fonctionnalité en développement")
    st.write("Cette section permettra de suivre les dates d'expiration des habilitations")

def show_ajouter_habilitation():
    """Formulaire pour ajouter une habilitation"""
    st.markdown("### ➕ Ajouter une Nouvelle Habilitation")
    
    st.info("Fonctionnalité en développement")
    st.write("Cette section permettra d'ajouter de nouvelles habilitations aux techniciens")

def show_statistiques_personnel():
    """Affiche les statistiques du personnel"""
    st.subheader("📊 Statistiques du Personnel")
    
    personnels = data_manager.get_all_personnels()
    
    if not personnels:
        st.info("Aucune statistique disponible")
        return
    
    # Métriques
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Effectif total", str(len(personnels)))
    
    with col2:
        actifs = len([p for p in personnels if p.get('statut') == '🟢 Actif'])
        st.metric("Techniciens actifs", str(actifs))
    
    with col3:
        if personnels:
            cout_moyen = sum(p.get('cout_horaire', 0) for p in personnels) / len(personnels)
            st.metric("Coût moyen/h", f"{cout_moyen:.2f} €")
        else:
            st.metric("Coût moyen/h", "0 €")
    
    with col4:
        st.metric("Services", str(len(set(p.get('service', '') for p in personnels))))
    
    # Graphiques
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown("#### Répartition par service")
        service_data = {}
        for p in personnels:
            service = p.get('service', 'Non spécifié')
            service_data[service] = service_data.get(service, 0) + 1
        
        if service_data:
            service_df = pd.DataFrame({
                'Service': list(service_data.keys()),
                'Effectif': list(service_data.values())
            })
            st.bar_chart(service_df.set_index('Service'))
        else:
            st.info("Aucune donnée de service")
    
    with col_b:
        st.markdown("#### Répartition par statut")
        statut_data = {}
        for p in personnels:
            statut = p.get('statut', 'Non spécifié')
            statut_data[statut] = statut_data.get(statut, 0) + 1
        
        if statut_data:
            statut_df = pd.DataFrame({
                'Statut': list(statut_data.keys()),
                'Nombre': list(statut_data.values())
            })
            st.bar_chart(statut_df.set_index('Statut'))
        else:
            st.info("Aucune donnée de statut")

def show_planning_technicien(personnel):
    """Affiche le planning d'un technicien"""
    st.markdown(f"### 📅 Planning de {personnel.get('nom')}")
    st.info("Fonctionnalité en développement")
    st.write("Cette section affichera le planning des interventions du technicien")

def show_performance_technicien(personnel):
    """Affiche les performances d'un technicien"""
    st.markdown(f"### 📊 Performance de {personnel.get('nom')}")
    st.info("Fonctionnalité en développement")
    st.write("Cette section affichera les statistiques de performance du technicien")

def show_admin():
    """Affiche la page administration"""
    st.title("⚙️ Administration")
    
    if st.session_state.user["role"] != "admin":
        st.error("⛔ Accès réservé aux administrateurs")
        return
    
    # Onglets
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Système", "👥 Utilisateurs", "🔐 Sécurité", "💾 Backup"])
    
    with tab1:
        st.subheader("Informations système")
        
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            st.metric("Version", "2.0.0")
            st.metric("Utilisateurs actifs", "3")
            st.metric("Base de données", "JSON")
        
        with col_s2:
            st.metric("Espace disque", "85%")
            st.metric("Dernière sauvegarde", "Aujourd'hui 08:30")
            st.metric("Uptime", "99.8%")
        
        # Logs système
        with st.expander("📝 Logs système"):
            logs = pd.DataFrame({
                "Date": ["2024-11-29 08:30:00", "2024-11-29 08:15:00", "2024-11-29 08:00:00", "2024-11-28 23:45:00"],
                "Type": ["INFO", "INFO", "WARNING", "INFO"],
                "Message": ["Sauvegarde automatique effectuée", "Connexion utilisateur: admin", "Stock critique détecté", "Maintenance nocturne"],
                "Utilisateur": ["Système", "admin", "Système", "Système"]
            })
            st.dataframe(logs, use_container_width=True)
    
    with tab2:
        st.subheader("Gestion des utilisateurs")
        
        # Liste utilisateurs
        users = pd.DataFrame(data_manager.users)
        if not users.empty:
            display_users = users[["id", "username", "full_name", "role", "email", "last_login", "is_active"]].copy()
            st.dataframe(display_users, use_container_width=True)
        
        # Actions
        col_u1, col_u2, col_u3 = st.columns(3)
        with col_u1:
            if st.button("🔄 Actualiser", use_container_width=True):
                data_manager.load_all_data()
                st.success("Données rechargées !")
        
        with col_u2:
            if st.button("➕ Ajouter utilisateur", use_container_width=True):
                st.info("Formulaire d'ajout d'utilisateur")
        
        with col_u3:
            if st.button("📊 Statistiques", use_container_width=True):
                st.metric("Total", len(users))
                st.metric("Actifs", len(users[users["is_active"] == True]))
    
    with tab3:
        st.subheader("Paramètres de sécurité")
        
        with st.form("security_form"):
            password_length = st.slider("Longueur minimale mot de passe", 6, 20, 8)
            max_attempts = st.number_input("Tentatives max avant blocage", 1, 10, 3)
            session_timeout = st.number_input("Timeout session (minutes)", 5, 240, 60)
            two_factor = st.checkbox("Authentification à deux facteurs", value=False)
            logging_level = st.selectbox("Niveau de log", ["DEBUG", "INFO", "WARNING", "ERROR"])
            
            if st.form_submit_button("💾 Sauvegarder paramètres", type="primary"):
                st.success("Paramètres de sécurité sauvegardés !")
    
    with tab4:
        st.subheader("Sauvegarde et restauration")
        
        col_b1, col_b2 = st.columns(2)
        
        with col_b1:
            st.markdown("### 💾 Sauvegarde")
            if st.button("Sauvegarder maintenant", use_container_width=True):
                st.success("Sauvegarde effectuée !")
            
            if st.button("Exporter en CSV", use_container_width=True):
                st.success("Export CSV lancé !")
            
            backup_freq = st.selectbox("Fréquence auto", ["Quotidienne", "Hebdomadaire", "Mensuelle"])
        
        with col_b2:
            st.markdown("### 🔄 Restauration")
            backup_file = st.file_uploader("Choisir fichier de sauvegarde", type=["json", "csv"])
            
            if st.button("Restaurer depuis fichier", type="secondary", use_container_width=True):
                if backup_file:
                    st.warning("⚠️ Cette action écrasera les données actuelles !")
                    if st.button("Confirmer la restauration", type="primary"):
                        st.success("Restauration réussie !")
                else:
                    st.error("Veuillez sélectionner un fichier")

def show_dashboard():
    """Tableau de bord amélioré avec KPI de maintenance (sans matplotlib)"""
    st.title("🏠 Tableau de Bord Maintenance")
    
    # Données pour les métriques
    outillages = data_manager.get_all_outillages()
    total_outillages = len(outillages) if not outillages.empty else 0
    outillages_disponibles = len(outillages[outillages["disponibilite"] == "🟢 Disponible"]) if not outillages.empty else 0
    
    # ========== PREMIÈRE LIGNE : KPI PRINCIPAUX ==========
    st.markdown("### 📊 KPI Principaux")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            label="Taux Disponibilité",
            value="92.4%",
            delta="+1.2%",
            delta_color="normal"
        )
        st.caption("Équipements opérationnels")
    
    with col2:
        st.metric(
            label="MTBF Moyen",
            value="450h",
            delta="+25h",
            delta_color="normal"
        )
        st.caption("Mean Time Between Failures")
    
    with col3:
        st.metric(
            label="MTTR Moyen",
            value="3.2h",
            delta="-0.8h",
            delta_color="inverse"
        )
        st.caption("Mean Time To Repair")
    
    with col4:
        taux_preventive = 78  # Donnée simulée
        st.metric(
            label="Maintenance Préventive",
            value=f"{taux_preventive}%",
            delta="+5%",
            delta_color="normal"
        )
        st.caption("Part préventive vs corrective")
    
    with col5:
        st.metric(
            label="Coût Maintenance/Mois",
            value="12.4k€",
            delta="-1.2k€",
            delta_color="inverse"
        )
        st.caption("Économies réalisées")
    
    # ========== DEUXIÈME LIGNE : STATISTIQUES ==========
    st.markdown("### 📈 Statistiques d'Activité")
    
    col_a, col_b, col_c, col_d = st.columns(4)
    
    with col_a:
        st.metric(
            label="Interventions",
            value="24",
            delta="+3",
            delta_color="normal"
        )
        st.caption("Ce mois")
    
    with col_b:
        st.metric(
            label="Outillages",
            value=str(total_outillages),
            delta=f"{outillages_disponibles} dispo",
            delta_color="off"
        )
        st.caption(f"{outillages_disponibles}/{total_outillages} disponibles")
    
    with col_c:
        st.metric(
            label="Équipements",
            value="12",
            delta="0",
            delta_color="off"
        )
        st.caption("En service")
    
    with col_d:
        st.metric(
            label="Alertes",
            value="3",
            delta="-2",
            delta_color="inverse"
        )
        st.caption("À traiter")
    
    # ========== TROISIÈME LIGNE : GRAPHIQUES AVEC STREAMLIT ==========
    st.markdown("### 📊 Analyse de la Maintenance")
    
    # Premier row de visualisations
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.markdown("#### 🔧 Répartition des Interventions")
        
        # Données pour le tableau
        intervention_data = {
            'Type': ['Préventive', 'Corrective', 'Améliorative', 'Urgente'],
            'Nombre': [65, 25, 8, 2],
            'Pourcentage': ['65%', '25%', '8%', '2%']
        }
        
        # Affichage sous forme de tableau avec barres de progression
        for i, (type_int, nombre, pourcent) in enumerate(zip(
            intervention_data['Type'], 
            intervention_data['Nombre'], 
            intervention_data['Pourcentage']
        )):
            col_type, col_prog = st.columns([2, 5])
            with col_type:
                if type_int == 'Préventive':
                    st.markdown(f"🟢 **{type_int}**")
                elif type_int == 'Corrective':
                    st.markdown(f"🟡 **{type_int}**")
                elif type_int == 'Améliorative':
                    st.markdown(f"🔵 **{type_int}**")
                else:
                    st.markdown(f"🔴 **{type_int}**")
            
            with col_prog:
                progress_value = nombre / 100
                if type_int == 'Préventive':
                    st.progress(progress_value, text=pourcent)
                elif type_int == 'Corrective':
                    st.progress(progress_value, text=pourcent)
                elif type_int == 'Améliorative':
                    st.progress(progress_value, text=pourcent)
                else:
                    st.progress(progress_value, text=pourcent)
        
        st.caption("Objectif: ≥80% de maintenance préventive")
    
    with chart_col2:
        st.markdown("#### 📅 Évolution Mensuelle")
        
        # Données pour le tableau
        evolution_data = pd.DataFrame({
            'Mois': ['Septembre', 'Octobre', 'Novembre', 'Décembre'],
            'Préventive': [18, 20, 22, 24],
            'Corrective': [8, 6, 5, 4],
            'Total': [26, 26, 27, 28]
        })
        
        # Affichage du tableau
        st.dataframe(
            evolution_data,
            column_config={
                "Mois": st.column_config.TextColumn("Mois"),
                "Préventive": st.column_config.ProgressColumn(
                    "Préventive",
                    help="Nombre d'interventions préventives",
                    format="%d",
                    min_value=0,
                    max_value=30,
                ),
                "Corrective": st.column_config.ProgressColumn(
                    "Corrective",
                    help="Nombre d'interventions correctives",
                    format="%d",
                    min_value=0,
                    max_value=30,
                ),
                "Total": st.column_config.NumberColumn(
                    "Total",
                    help="Total des interventions",
                    format="%d"
                )
            },
            hide_index=True,
            use_container_width=True
        )
        
        # Mini-graphique avec st.bar_chart
        chart_data = evolution_data.set_index('Mois')[['Préventive', 'Corrective']]
        st.bar_chart(chart_data)
    
    # Deuxième row de visualisations
    chart_col3, chart_col4 = st.columns(2)
    
    with chart_col3:
        st.markdown("#### ⏱️ Temps d'Intervention (MTTR)")
        
        # Données pour MTTR
        mttr_data = pd.DataFrame({
            'Équipement': ['Pompes', 'Ventilateurs', 'Convoyeurs', 'Compresseurs', 'Autres'],
            'MTTR (h)': [4.2, 2.8, 3.5, 5.1, 2.3],
            'Objectif (h)': [3.5, 2.5, 3.0, 4.0, 2.0]
        })
        
        # Affichage avec barres de progression
        for _, row in mttr_data.iterrows():
            col_name, col_mttr = st.columns([3, 4])
            with col_name:
                st.write(f"**{row['Équipement']}**")
            
            with col_mttr:
                # Calcul du pourcentage par rapport à l'objectif
                if row['MTTR (h)'] <= row['Objectif (h)']:
                    # En dessous de l'objectif = bon
                    ratio = 1 - (row['MTTR (h)'] / row['Objectif (h)'])
                    st.progress(min(ratio, 1), text=f"{row['MTTR (h)']}h")
                    st.caption(f"✓ Objectif: {row['Objectif (h)']}h")
                else:
                    # Au-dessus de l'objectif = à améliorer
                    ratio = row['Objectif (h)'] / row['MTTR (h)']
                    st.progress(min(ratio, 1), text=f"{row['MTTR (h)']}h")
                    st.caption(f"⚠️ Objectif: {row['Objectif (h)']}h")
    
    with chart_col4:
        st.markdown("#### 💰 Coûts de Maintenance")
        
        # Données pour les coûts
        cost_data = pd.DataFrame({
            'Mois': ['Sept', 'Oct', 'Nov'],
            'Préventive (k€)': [8.5, 9.2, 9.8],
            'Corrective (k€)': [4.2, 3.8, 3.2],
            'Urgente (k€)': [1.2, 0.8, 0.6],
            'Total (k€)': [13.9, 13.8, 13.6]
        })
        
        # Affichage sous forme de tableau
        st.dataframe(
            cost_data,
            column_config={
                "Mois": st.column_config.TextColumn("Mois"),
                "Préventive (k€)": st.column_config.NumberColumn(
                    "Préventive",
                    help="Coût maintenance préventive",
                    format="%.1f k€"
                ),
                "Corrective (k€)": st.column_config.NumberColumn(
                    "Corrective",
                    help="Coût maintenance corrective",
                    format="%.1f k€"
                ),
                "Urgente (k€)": st.column_config.NumberColumn(
                    "Urgente",
                    help="Coût maintenance urgente",
                    format="%.1f k€"
                ),
                "Total (k€)": st.column_config.NumberColumn(
                    "Total",
                    help="Coût total maintenance",
                    format="%.1f k€"
                )
            },
            hide_index=True,
            use_container_width=True
        )
        
        # Graphique linéaire des totaux
        total_chart_data = cost_data.set_index('Mois')['Total (k€)']
        st.line_chart(total_chart_data)
    
    # ========== QUATRIÈME LIGNE : ÉQUIPEMENTS CRITIQUES ==========
    st.markdown("### ⚠️ Équipements Critiques")
    
    col_crit1, col_crit2, col_crit3 = st.columns(3)
    
    with col_crit1:
        with st.container():
            st.markdown("#### 🔴 À Surveiller")
            critical_equipment = [
                {"nom": "Compresseur CMP-01", "probleme": "Vibrations élevées", "jours": 3},
                {"nom": "Pompe P-205", "probleme": "Température anormale", "jours": 7},
                {"nom": "Convoyeur CV-12", "probleme": "Courroie usée", "jours": 2}
            ]
            
            for eq in critical_equipment:
                st.markdown(f"**{eq['nom']}**")
                st.caption(f"{eq['probleme']} - Depuis {eq['jours']} jours")
                st.progress(min(eq['jours'] * 10, 100) / 100)
    
    with col_crit2:
        with st.container():
            st.markdown("#### 🟡 Maintenance Planifiée")
            planned_maintenance = [
                {"nom": "Four F-03", "date": "15/12/2024", "type": "Trimestrielle"},
                {"nom": "Ventilateur V-45", "date": "18/12/2024", "type": "Mensuelle"},
                {"nom": "Générateur G-02", "date": "22/12/2024", "type": "Annuelle"}
            ]
            
            for pm in planned_maintenance:
                st.markdown(f"**{pm['nom']}**")
                st.caption(f"{pm['type']} - {pm['date']}")
                days_left = (datetime.date(2024, 12, int(pm['date'].split('/')[0])) - datetime.date.today()).days
                if days_left >= 0:
                    st.info(f"Dans {days_left} jour(s)")
    
    with col_crit3:
        with st.container():
            st.markdown("#### 📦 Stocks Faibles")
            low_stocks = [
                {"piece": "Roulement 6205", "stock": 2, "seuil": 10},
                {"piece": "Joint SPI 50mm", "stock": 5, "seuil": 15},
                {"piece": "Courroie 5PK800", "stock": 3, "seuil": 8}
            ]
            
            for stock in low_stocks:
                percentage = (stock['stock'] / stock['seuil']) * 100
                st.markdown(f"**{stock['piece']}**")
                st.caption(f"Stock: {stock['stock']} / Seuil: {stock['seuil']}")
                if percentage < 30:
                    st.error(f"⚠️ {percentage:.0f}% du seuil")
                elif percentage < 50:
                    st.warning(f"⚠️ {percentage:.0f}% du seuil")
                else:
                    st.info(f"{percentage:.0f}% du seuil")
    
    # ========== CINQUIÈME LIGNE : INDICATEURS CLÉS ==========
    st.markdown("### 🎯 Indicateurs Clés de Performance")
    
    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
    
    with kpi_col1:
        st.markdown("#### 🎯 OEE")
        st.markdown('<div style="text-align: center; font-size: 36px; font-weight: bold; color: #4CAF50;">86.2%</div>', 
                   unsafe_allow_html=True)
        st.caption("Overall Equipment Effectiveness")
        st.progress(0.862)
    
    with kpi_col2:
        st.markdown("#### ⚡ Disponibilité")
        st.markdown('<div style="text-align: center; font-size: 36px; font-weight: bold; color: #2196F3;">94.7%</div>', 
                   unsafe_allow_html=True)
        st.caption("Taux de disponibilité équipements")
        st.progress(0.947)
    
    with kpi_col3:
        st.markdown("#### ✅ Qualité")
        st.markdown('<div style="text-align: center; font-size: 36px; font-weight: bold; color: #9C27B0;">98.3%</div>', 
                   unsafe_allow_html=True)
        st.caption("Taux de bonne qualité")
        st.progress(0.983)
    
    with kpi_col4:
        st.markdown("#### 📊 Performance")
        st.markdown('<div style="text-align: center; font-size: 36px; font-weight: bold; color: #FF9800;">91.5%</div>', 
                   unsafe_allow_html=True)
        st.caption("Performance opérationnelle")
        st.progress(0.915)
    
    # ========== DERNIÈRE LIGNE : BOUTONS RAPIDES ==========
    st.markdown("### 🚀 Actions Rapides")
    
    action_col1, action_col2, action_col3, action_col4 = st.columns(4)
    
    with action_col1:
        if st.button("📝 Nouvelle Intervention", use_container_width=True, type="primary"):
            st.session_state.selected_menu = "🔧 Interventions"
            st.rerun()
    
    with action_col2:
        if st.button("🛠️ Gérer Outillages", use_container_width=True):
            st.session_state.selected_menu = "🛠️ Outillages"
            st.rerun()
    
    with action_col3:
        if st.button("📦 Vérifier Stocks", use_container_width=True):
            st.session_state.selected_menu = "📦 Stocks"
            st.rerun()
    
    with action_col4:
        if st.button("📊 Exporter Rapport", use_container_width=True):
            st.success("Rapport généré avec succès !")
            st.info("Téléchargement disponible dans les prochaines secondes...")

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
        
        # CORRECTION DE L'INDENTATION ICI :
        menu_options = ["🏠 Tableau de bord", "🔧 Interventions", "🏭 Équipements", 
                       "📦 Stocks", "🛠️ Outillages", "👥 Personnels", "🤝 Tiers"]
        
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
    elif menu == "👥 Personnels":
        show_personnels_management()
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

