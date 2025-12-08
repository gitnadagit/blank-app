import streamlit as st
import pandas as pd
import datetime
import sqlite3
import hashlib
from pathlib import Path
import json

# ========== CONFIGURATION ==========
st.set_page_config(
    page_title="GMAO Pro DB",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== CHEMIN DE LA BASE ==========
DB_PATH = Path("gmao_database.db")

# ========== FONCTIONS DE BASE DE DONNÉES ==========
def get_connection():
    """Retourne une connexion à la base de données"""
    return sqlite3.connect(DB_PATH)

def init_database():
    """Initialise la base de données AVANT tout usage"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Table des utilisateurs - CRÉATION SIMPLIFIÉE
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL,
        full_name TEXT NOT NULL,
        email TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        is_active BOOLEAN DEFAULT 1
    )
    ''')
    
    conn.commit()
    
    # Vérifier si des utilisateurs existent
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        # Insérer utilisateurs par défaut
        default_users = [
            ('admin', hash_password('admin123'), 'admin', 'Administrateur', 'admin@gmao.com'),
            ('technicien1', hash_password('tech123'), 'technicien', 'Jean Dupont', 'jean@gmao.com'),
            ('technicien2', hash_password('tech123'), 'technicien', 'Marie Martin', 'marie@gmao.com'),
            ('manager', hash_password('manager123'), 'manager', 'Paul Bernard', 'paul@gmao.com')
        ]
        
        cursor.executemany('''
        INSERT INTO users (username, password_hash, role, full_name, email)
        VALUES (?, ?, ?, ?, ?)
        ''', default_users)
        
        conn.commit()
    
    # Créer les autres tables si elles n'existent pas
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS equipements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT UNIQUE NOT NULL,
        nom TEXT NOT NULL,
        type TEXT,
        localisation TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS interventions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT UNIQUE NOT NULL,
        equipement_id INTEGER,
        description TEXT NOT NULL,
        technicien_id INTEGER,
        date_planifiee DATE,
        statut TEXT DEFAULT 'a_planifier',
        priorite TEXT DEFAULT 'moyenne',
        duree_estimee INTEGER,
        cout_estime REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS stocks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        reference TEXT UNIQUE NOT NULL,
        designation TEXT NOT NULL,
        quantite INTEGER DEFAULT 0,
        seuil_minimum INTEGER DEFAULT 5,
        prix_unitaire REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    conn.commit()
    conn.close()

def hash_password(password):
    """Hash un mot de passe"""
    return hashlib.sha256(password.encode()).hexdigest()

def get_user(username):
    """Récupère un utilisateur par son username"""
    # S'assurer que la base est initialisée
    init_database()
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND is_active = 1", (username,))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return {
            'id': user[0],
            'username': user[1],
            'password_hash': user[2],
            'role': user[3],
            'full_name': user[4],
            'email': user[5]
        }
    return None

# ========== PAGE DE CONNEXION SIMPLIFIÉE ==========
def login_page():
    """Affiche la page de connexion"""
    st.title("🔐 Connexion - GMAO Pro")
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.container():
            st.subheader("Identifiez-vous")
            
            username = st.text_input("Nom d'utilisateur", value="admin")
            password = st.text_input("Mot de passe", type="password", value="admin123")
            
            if st.button("🔓 Se connecter", type="primary", use_container_width=True):
                if username and password:
                    # Initialiser la base AVANT de chercher l'utilisateur
                    init_database()
                    
                    user = get_user(username)
                    
                    if user and user["password_hash"] == hash_password(password):
                        st.session_state["authenticated"] = True
                        st.session_state["user"] = {
                            "id": user["id"],
                            "username": user["username"],
                            "role": user["role"],
                            "full_name": user["full_name"]
                        }
                        st.success(f"✅ Bienvenue {user['full_name']} !")
                        st.rerun()
                    else:
                        st.error("❌ Identifiants incorrects")
                else:
                    st.warning("Veuillez saisir nom d'utilisateur et mot de passe")
            
            st.markdown("---")
            st.caption("**Comptes de démonstration :**")
            st.caption("• **Admin** : admin / admin123")
            st.caption("• **Technicien 1** : technicien1 / tech123")
            st.caption("• **Technicien 2** : technicien2 / tech123")
            st.caption("• **Manager** : manager / manager123")

# ========== FONCTIONS DE RÉCUPÉRATION DE DONNÉES ==========
def query_to_dataframe(query, params=()):
    """Exécute une requête et retourne un DataFrame"""
    init_database()  # S'assurer que la base existe
    conn = get_connection()
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df

def execute_query(query, params=()):
    """Exécute une requête d'écriture"""
    init_database()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    conn.close()
    return cursor.lastrowid

def get_all_interventions():
    """Récupère toutes les interventions"""
    query = '''
    SELECT 
        i.*,
        e.nom as equipement_nom,
        u.full_name as technicien_nom
    FROM interventions i
    LEFT JOIN equipements e ON i.equipement_id = e.id
    LEFT JOIN users u ON i.technicien_id = u.id
    ORDER BY i.date_planifiee DESC
    '''
    return query_to_dataframe(query)

def get_all_equipements():
    """Récupère tous les équipements"""
    return query_to_dataframe("SELECT * FROM equipements ORDER BY nom")

def get_all_stocks():
    """Récupère tous les stocks"""
    return query_to_dataframe("SELECT * FROM stocks ORDER BY designation")

def get_all_users():
    """Récupère tous les utilisateurs"""
    return query_to_dataframe("SELECT id, username, role, full_name, email FROM users WHERE is_active = 1")

# ========== SIDEBAR ==========
def show_sidebar():
    """Affiche la sidebar avec le menu"""
    with st.sidebar:
        # En-tête
        st.image("https://cdn-icons-png.flaticon.com/512/3067/3067256.png", width=60)
        st.markdown("### GMAO Database")
        
        user = st.session_state.user
        st.write(f"**👤 {user['full_name']}**")
        st.caption(f"Rôle: {user['role'].capitalize()}")
        
        st.markdown("---")
        
        # Menu simple
        menu_options = ["🏠 Dashboard", "🔧 Interventions", "🏭 Équipements", "📦 Stocks", "➕ Nouvelle"]
        
        if user["role"] == "admin":
            menu_options.append("👥 Utilisateurs")
        
        st.session_state.menu = st.radio(
            "**NAVIGATION**",
            menu_options,
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Boutons
        if st.button("🔄 Rafraîchir", use_container_width=True):
            st.rerun()
        
        if st.button("🚪 Déconnexion", type="secondary", use_container_width=True):
            for key in list(st.session_state.keys()):
                if key != 'rerun':
                    del st.session_state[key]
            st.rerun()
        
        st.markdown("---")
        st.caption(f"📅 {datetime.date.today().strftime('%d/%m/%Y')}")

# ========== PAGES PRINCIPALES ==========
def dashboard_page():
    """Page tableau de bord"""
    st.header("📊 Tableau de bord")
    
    # Charger les données
    interventions = get_all_interventions()
    equipements = get_all_equipements()
    stocks = get_all_stocks()
    
    # Insérer des données d'exemple si vide
    if interventions.empty:
        st.info("Aucune donnée. Insertion d'exemples...")
        insert_example_data()
        interventions = get_all_interventions()
        equipements = get_all_equipements()
        stocks = get_all_stocks()
    
    # KPI
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Interventions", len(interventions))
    
    with col2:
        en_cours = len(interventions[interventions['statut'] == 'en_cours'])
        st.metric("En cours", en_cours)
    
    with col3:
        st.metric("Équipements", len(equipements))
    
    with col4:
        st.metric("Articles en stock", len(stocks))
    
    # Graphiques
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Interventions par statut")
        if not interventions.empty:
            statut_counts = interventions['statut'].value_counts()
            st.bar_chart(statut_counts)
    
    with col2:
        st.subheader("Données récentes")
        if not interventions.empty:
            st.dataframe(interventions.head(5), use_container_width=True)

def interventions_page():
    """Page interventions"""
    st.header("🔧 Interventions")
    
    interventions = get_all_interventions()
    
    if interventions.empty:
        st.info("Aucune intervention. Créez-en une nouvelle !")
    else:
        # Filtres simples
        col1, col2 = st.columns(2)
        with col1:
            statuts = interventions['statut'].unique()
            statut_filtre = st.multiselect("Statut", statuts, default=['en_cours'])
        
        # Affichage
        if statut_filtre:
            df_filtre = interventions[interventions['statut'].isin(statut_filtre)]
        else:
            df_filtre = interventions
        
        st.dataframe(df_filtre, use_container_width=True, height=400)
        
        # Export
        csv = df_filtre.to_csv(index=False)
        st.download_button(
            "📥 Exporter CSV",
            data=csv,
            file_name="interventions.csv",
            mime="text/csv"
        )

def equipements_page():
    """Page équipements"""
    st.header("🏭 Équipements")
    
    equipements = get_all_equipements()
    
    if equipements.empty:
        st.info("Aucun équipement enregistré")
    else:
        st.dataframe(equipements, use_container_width=True)
        
        # Ajout rapide
        with st.expander("➕ Ajouter un équipement"):
            with st.form("add_equipement"):
                code = st.text_input("Code")
                nom = st.text_input("Nom")
                type_eq = st.text_input("Type")
                localisation = st.text_input("Localisation")
                
                if st.form_submit_button("Ajouter"):
                    if code and nom:
                        execute_query(
                            "INSERT INTO equipements (code, nom, type, localisation) VALUES (?, ?, ?, ?)",
                            (code, nom, type_eq, localisation)
                        )
                        st.success(f"Équipement {nom} ajouté !")
                        st.rerun()

def stocks_page():
    """Page stocks"""
    st.header("📦 Stocks")
    
    stocks = get_all_stocks()
    
    if stocks.empty:
        st.info("Aucun article en stock")
    else:
        # Calcul valeur
        stocks['valeur'] = stocks['quantite'] * stocks['prix_unitaire']
        
        # Alertes
        stocks_critiques = stocks[stocks['quantite'] <= stocks['seuil_minimum']]
        if len(stocks_critiques) > 0:
            st.error(f"🚨 {len(stocks_critiques)} articles en stock critique !")
        
        st.dataframe(stocks, use_container_width=True)

def new_intervention_page():
    """Nouvelle intervention"""
    st.header("➕ Nouvelle intervention")
    
    # Récupérer données pour les selects
    equipements = get_all_equipements()
    techniciens = query_to_dataframe("SELECT id, full_name FROM users WHERE role = 'technicien'")
    
    with st.form("new_intervention_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            if not equipements.empty:
                equipement_id = st.selectbox(
                    "Équipement",
                    options=equipements[['id', 'nom']].itertuples(index=False, name=None),
                    format_func=lambda x: x[1]
                )[0]
            else:
                st.warning("Aucun équipement disponible")
                equipement_id = None
            
            type_inter = st.selectbox("Type", ["maintenance", "reparation", "controle"])
            priorite = st.selectbox("Priorité", ["basse", "moyenne", "haute"])
        
        with col2:
            if not techniciens.empty:
                technicien_id = st.selectbox(
                    "Technicien",
                    options=techniciens[['id', 'full_name']].itertuples(index=False, name=None),
                    format_func=lambda x: x[1]
                )[0]
            else:
                technicien_id = None
            
            date_plan = st.date_input("Date planifiée", datetime.date.today())
            duree = st.number_input("Durée estimée (h)", min_value=1, value=4)
        
        description = st.text_area("Description", height=100)
        
        if st.form_submit_button("✅ Créer l'intervention", type="primary"):
            if description and equipement_id and technicien_id:
                # Générer code
                last_id = execute_query("SELECT COALESCE(MAX(id), 0) FROM interventions")
                code = f"INT{last_id + 1:04d}"
                
                # Calcul coût
                cout = duree * 75  # 75€/h
                
                execute_query('''
                INSERT INTO interventions 
                (code, equipement_id, description, technicien_id, date_planifiee, 
                 statut, priorite, duree_estimee, cout_estime)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (code, equipement_id, description, technicien_id, 
                     date_plan.strftime('%Y-%m-%d'), 'a_planifier', 
                     priorite, duree, cout))
                
                st.success(f"✅ Intervention {code} créée !")
                st.balloons()
            else:
                st.error("Veuillez remplir tous les champs")

def users_page():
    """Page utilisateurs (admin seulement)"""
    st.header("👥 Utilisateurs")
    
    users = get_all_users()
    
    if users.empty:
        st.info("Aucun utilisateur")
    else:
        st.dataframe(users, use_container_width=True)
        
        # Ajout utilisateur
        with st.expander("➕ Ajouter un utilisateur"):
            with st.form("add_user_form"):
                username = st.text_input("Nom d'utilisateur")
                password = st.text_input("Mot de passe", type="password")
                full_name = st.text_input("Nom complet")
                role = st.selectbox("Rôle", ["technicien", "manager", "admin"])
                
                if st.form_submit_button("Ajouter"):
                    if username and password:
                        execute_query(
                            "INSERT INTO users (username, password_hash, role, full_name) VALUES (?, ?, ?, ?)",
                            (username, hash_password(password), role, full_name)
                        )
                        st.success(f"Utilisateur {username} ajouté !")
                        st.rerun()

def insert_example_data():
    """Insère des données d'exemple"""
    # Équipements
    equipements = [
        ('EQ001', 'Presse hydraulique', 'Formage', 'Atelier A'),
        ('EQ002', 'Tour CNC', 'Usinage', 'Atelier B'),
        ('EQ003', 'Four industriel', 'Thermique', 'Zone chaud')
    ]
    
    for eq in equipements:
        execute_query(
            "INSERT OR IGNORE INTO equipements (code, nom, type, localisation) VALUES (?, ?, ?, ?)",
            eq
        )
    
    # Stocks
    stocks = [
        ('R001', 'Roulement 6205', 15, 5, 45.50),
        ('R002', 'Courroie B85', 8, 3, 32.80),
        ('R003', 'Filtre à air', 22, 10, 120.00)
    ]
    
    for stock in stocks:
        execute_query(
            "INSERT OR IGNORE INTO stocks (reference, designation, quantite, seuil_minimum, prix_unitaire) VALUES (?, ?, ?, ?, ?)",
            stock
        )
    
    # Interventions (si on a des équipements et techniciens)
    equipements_df = get_all_equipements()
    techniciens_df = query_to_dataframe("SELECT id FROM users WHERE role = 'technicien'")
    
    if not equipements_df.empty and not techniciens_df.empty:
        interventions = [
            ('INT0001', 1, 'Panne moteur', 2, '2024-11-25', 'en_cours', 'haute', 8, 600),
            ('INT0002', 2, 'Révision annuelle', 3, '2024-11-26', 'termine', 'moyenne', 4, 300)
        ]
        
        for interv in interventions:
            execute_query('''
            INSERT OR IGNORE INTO interventions 
            (code, equipement_id, description, technicien_id, date_planifiee, statut, priorite, duree_estimee, cout_estime)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', interv)

# ========== APPLICATION PRINCIPALE ==========
def main_app():
    """Application après connexion"""
    # Initialiser la base (au cas où)
    init_database()
    
    # Sidebar
    show_sidebar()
    
    # Page sélectionnée
    menu = st.session_state.get('menu', '🏠 Dashboard')
    
    if menu == "🏠 Dashboard":
        dashboard_page()
    elif menu == "🔧 Interventions":
        interventions_page()
    elif menu == "🏭 Équipements":
        equipements_page()
    elif menu == "📦 Stocks":
        stocks_page()
    elif menu == "➕ Nouvelle":
        new_intervention_page()
    elif menu == "👥 Utilisateurs":
        if st.session_state.user["role"] == "admin":
            users_page()
        else:
            st.error("Accès non autorisé")

# ========== POINT D'ENTRÉE ==========
def main():
    """Point d'entrée principal"""
    # Initialiser session
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    
    if not st.session_state.authenticated:
        login_page()
    else:
        main_app()

if __name__ == "__main__":
    main()
