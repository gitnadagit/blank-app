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

# ========== INITIALISATION BASE DE DONNÉES ==========
DB_PATH = Path("gmao_database.db")

def init_database():
    """Initialise la base de données avec les tables nécessaires"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Table des utilisateurs
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
    
    # Table des équipements
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS equipements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT UNIQUE NOT NULL,
        nom TEXT NOT NULL,
        type TEXT,
        localisation TEXT,
        marque TEXT,
        modele TEXT,
        num_serie TEXT,
        date_installation DATE,
        etat TEXT DEFAULT 'operationnel',
        prochaine_maintenance DATE,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        created_by INTEGER,
        FOREIGN KEY (created_by) REFERENCES users(id)
    )
    ''')
    
    # Table des interventions
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS interventions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT UNIQUE NOT NULL,
        equipement_id INTEGER NOT NULL,
        type TEXT NOT NULL,
        description TEXT NOT NULL,
        technicien_id INTEGER NOT NULL,
        date_planifiee DATE,
        date_debut DATE,
        date_fin DATE,
        duree_estimee INTEGER,  -- en heures
        duree_reelle INTEGER,   -- en heures
        priorite TEXT DEFAULT 'moyenne',
        statut TEXT DEFAULT 'a_planifier',
        cout_estime REAL,
        cout_reel REAL,
        cause TEXT,
        solution TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        created_by INTEGER,
        FOREIGN KEY (equipement_id) REFERENCES equipements(id),
        FOREIGN KEY (technicien_id) REFERENCES users(id),
        FOREIGN KEY (created_by) REFERENCES users(id)
    )
    ''')
    
    # Table des stocks
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS stocks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        reference TEXT UNIQUE NOT NULL,
        designation TEXT NOT NULL,
        categorie TEXT,
        quantite INTEGER DEFAULT 0,
        seuil_minimum INTEGER DEFAULT 5,
        unite TEXT DEFAULT 'piece',
        localisation TEXT,
        fournisseur TEXT,
        prix_unitaire REAL,
        date_derniere_commande DATE,
        date_prochaine_commande DATE,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Table d'historique (logs)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS historique (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        table_name TEXT NOT NULL,
        record_id INTEGER NOT NULL,
        action TEXT NOT NULL,
        details TEXT,
        user_id INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    ''')
    
    # Table des pièces utilisées dans les interventions
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS pieces_utilisees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        intervention_id INTEGER NOT NULL,
        stock_id INTEGER NOT NULL,
        quantite INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (intervention_id) REFERENCES interventions(id),
        FOREIGN KEY (stock_id) REFERENCES stocks(id)
    )
    ''')
    
    conn.commit()
    conn.close()
    
    # Insérer les utilisateurs par défaut
    insert_default_data()

def hash_password(password):
    """Hash un mot de passe"""
    return hashlib.sha256(password.encode()).hexdigest()

def insert_default_data():
    """Insère les données par défaut"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Vérifier si des utilisateurs existent déjà
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
        
        # Insérer équipements par défaut
        default_equipements = [
            ('EQ001', 'Presse hydraulique 100T', 'Formage', 'Atelier A', 'Hydrapress', 'HP-100T', 'SN2020-001', '2020-03-15', 'operationnel', '2025-01-15'),
            ('EQ002', 'Tour CNC 5 axes', 'Usinage', 'Atelier B', 'CNC Master', 'T5X-2021', 'SN2021-045', '2021-07-22', 'operationnel', '2024-12-22'),
            ('EQ003', 'Four industriel 800°C', 'Traitement thermique', 'Zone chauffage', 'ThermoPro', 'F800-2019', 'SN2019-123', '2019-11-10', 'maintenance', '2024-11-30'),
            ('EQ004', 'Robot soudeur KUKA', 'Assemblage', 'Ligne 2', 'KUKA', 'KR210', 'SN2022-078', '2022-09-05', 'operationnel', '2025-02-05'),
            ('EQ005', 'Compresseur Atlas', 'Utilitaire', 'Salle technique', 'Atlas Copco', 'GA75', 'SN2018-256', '2018-12-18', 'hors_service', NULL)
        ]
        
        cursor.executemany('''
        INSERT INTO equipements (code, nom, type, localisation, marque, modele, num_serie, date_installation, etat, prochaine_maintenance)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', default_equipements)
        
        # Insérer interventions par défaut
        default_interventions = [
            ('INT001', 1, 'reparation', 'Panne moteur principal - bruit anormal', 2, '2024-11-25', NULL, NULL, 8, NULL, 'haute', 'en_cours', 850, NULL, 'Roulements usés', 'Changer roulements'),
            ('INT002', 2, 'maintenance', 'Révision annuelle programmée', 3, '2024-11-26', '2024-11-26', '2024-11-26', 4, 3.5, 'moyenne', 'termine', 300, 280, 'Maintenance préventive', 'Graissage et contrôle'),
            ('INT003', 3, 'revision', 'Changement des résistances chauffantes', 2, '2024-11-27', NULL, NULL, 12, NULL, 'haute', 'a_planifier', 1200, NULL, 'Résistances vieillissantes', 'Remplacer 6 résistances')
        ]
        
        cursor.executemany('''
        INSERT INTO interventions (code, equipement_id, type, description, technicien_id, date_planifiee, 
                                  date_debut, date_fin, duree_estimee, duree_reelle, priorite, statut, 
                                  cout_estime, cout_reel, cause, solution)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', default_interventions)
        
        # Insérer stocks par défaut
        default_stocks = [
            ('R001-2024', 'Roulement 6205-2RS', 'Roulement', 15, 5, 'piece', 'Rack A1-3', 'SKF France', 45.50),
            ('R002-2024', 'Courroie synchronisée B85', 'Transmission', 8, 3, 'piece', 'Rack B3-2', 'Gates Europe', 32.80),
            ('R003-2024', 'Filtre à air industriel', 'Filtration', 22, 10, 'piece', 'Rack C2-1', 'Donaldson', 120.00),
            ('R004-2024', 'Joint d\'étanchéité Ø150mm', 'Etanchéité', 45, 20, 'piece', 'Rack D4-4', 'Freudenberg', 8.75),
            ('R005-2024', 'Capteur température PT100', 'Capteur', 12, 5, 'piece', 'Rack E5-1', 'Endress+Hauser', 89.99)
        ]
        
        cursor.executemany('''
        INSERT INTO stocks (reference, designation, categorie, quantite, seuil_minimum, unite, 
                           localisation, fournisseur, prix_unitaire)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', default_stocks)
        
        # Insérer pièces utilisées
        default_pieces = [
            (1, 1, 2),  # INT001 a utilisé 2 roulements
            (2, 2, 1)   # INT002 a utilisé 1 courroie
        ]
        
        cursor.executemany('''
        INSERT INTO pieces_utilisees (intervention_id, stock_id, quantite)
        VALUES (?, ?, ?)
        ''', default_pieces)
        
        conn.commit()
    
    conn.close()

# ========== FONCTIONS D'ACCÈS À LA BASE ==========
def get_connection():
    """Retourne une connexion à la base de données"""
    return sqlite3.connect(DB_PATH)

def query_to_dataframe(query, params=()):
    """Exécute une requête et retourne un DataFrame"""
    conn = get_connection()
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df

def execute_query(query, params=()):
    """Exécute une requête d'écriture"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    conn.close()
    return cursor.lastrowid

# ========== FONCTIONS SPÉCIFIQUES ==========
def get_user(username):
    """Récupère un utilisateur par son username"""
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

def get_all_interventions():
    """Récupère toutes les interventions avec détails"""
    query = '''
    SELECT 
        i.*,
        e.nom as equipement_nom,
        e.code as equipement_code,
        u.full_name as technicien_nom,
        uc.full_name as createur_nom
    FROM interventions i
    LEFT JOIN equipements e ON i.equipement_id = e.id
    LEFT JOIN users u ON i.technicien_id = u.id
    LEFT JOIN users uc ON i.created_by = uc.id
    ORDER BY i.date_planifiee DESC
    '''
    return query_to_dataframe(query)

def get_all_equipements():
    """Récupère tous les équipements"""
    return query_to_dataframe("SELECT * FROM equipements ORDER BY nom")

def get_all_stocks():
    """Récupère tous les stocks avec valeur calculée"""
    query = '''
    SELECT *,
           quantite * prix_unitaire as valeur_stock
    FROM stocks
    ORDER BY designation
    '''
    return query_to_dataframe(query)

def add_intervention(data):
    """Ajoute une nouvelle intervention"""
    query = '''
    INSERT INTO interventions 
    (code, equipement_id, type, description, technicien_id, date_planifiee,
     duree_estimee, priorite, statut, cout_estime, created_by)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''
    
    # Générer un code unique
    last_id = execute_query("SELECT COALESCE(MAX(id), 0) FROM interventions")
    code = f"INT{last_id + 1:04d}"
    
    params = (
        code,
        data['equipement_id'],
        data['type'],
        data['description'],
        data['technicien_id'],
        data['date_planifiee'],
        data['duree_estimee'],
        data['priorite'],
        'a_planifier',
        data['duree_estimee'] * 75,  # Coût estimé
        data['created_by']
    )
    
    return execute_query(query, params)

def update_stock_quantity(stock_id, quantity_change):
    """Met à jour la quantité en stock"""
    query = '''
    UPDATE stocks 
    SET quantite = quantite + ?
    WHERE id = ?
    '''
    execute_query(query, (quantity_change, stock_id))

def log_action(table_name, record_id, action, details, user_id=None):
    """Log une action dans l'historique"""
    query = '''
    INSERT INTO historique (table_name, record_id, action, details, user_id)
    VALUES (?, ?, ?, ?, ?)
    '''
    execute_query(query, (table_name, record_id, action, details, user_id))

# ========== PAGE DE CONNEXION ==========
def login_page():
    """Affiche la page de connexion"""
    st.title("🔐 Connexion - GMAO Pro Database")
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
                    user = get_user(username)
                    
                    if user and user["password_hash"] == hash_password(password):
                        st.session_state["authenticated"] = True
                        st.session_state["user"] = {
                            "id": user["id"],
                            "username": user["username"],
                            "role": user["role"],
                            "full_name": user["full_name"]
                        }
                        
                        # Log la connexion
                        log_action('users', user["id"], 'login', 'Connexion réussie', user["id"])
                        
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
            st.caption("• Technicien 1 : technicien1 / tech123")
            st.caption("• Technicien 2 : technicien2 / tech123")
            st.caption("• Manager : manager / manager123")

# ========== SIDEBAR ==========
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
                "🏠 Dashboard",
                "🔧 Interventions",
                "🏭 Équipements",
                "📦 Stocks",
                "➕ Nouvelle intervention",
                "👥 Utilisateurs",
                "📊 Rapports",
                "⚙️ Base de données"
            ]
        elif user["role"] == "manager":
            menu_options = [
                "🏠 Dashboard",
                "🔧 Interventions",
                "🏭 Équipements",
                "📦 Stocks",
                "📊 Rapports"
            ]
        else:  # technicien
            menu_options = [
                "🏠 Dashboard",
                "🔧 Mes interventions",
                "➕ Nouvelle intervention",
                "📦 Stocks"
            ]
        
        st.session_state.menu = st.radio(
            "📋 **NAVIGATION**",
            menu_options,
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Statistiques rapides
        interventions = get_all_interventions()
        if len(interventions) > 0:
            en_cours = len(interventions[interventions['statut'] == 'en_cours'])
            st.metric("🔄 En cours", en_cours)
        
        # Bouton rafraîchir
        if st.button("🔄 Rafraîchir", use_container_width=True):
            st.rerun()
        
        # Bouton déconnexion
        if st.button("🚪 Déconnexion", type="secondary", use_container_width=True):
            logout()
        
        st.markdown("---")
        st.caption(f"GMAO Database • {datetime.date.today().strftime('%d/%m/%Y')}")

# ========== PAGES PRINCIPALES ==========
def dashboard_page():
    """Page tableau de bord"""
    st.header("📊 Tableau de bord")
    
    # Charger les données
    interventions = get_all_interventions()
    equipements = get_all_equipements()
    stocks = get_all_stocks()
    
    # KPI
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total = len(interventions)
        st.metric("Interventions", total)
    
    with col2:
        en_cours = len(interventions[interventions['statut'] == 'en_cours'])
        st.metric("En cours", en_cours)
    
    with col3:
        equip_hs = len(equipements[equipements['etat'] == 'hors_service'])
        st.metric("Équipements HS", equip_hs)
    
    with col4:
        cout_total = interventions['cout_estime'].sum()
        st.metric("Coût estimé", f"{cout_total:,.0f} €".replace(",", " "))
    
    # Graphiques
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Interventions par statut")
        statut_counts = interventions['statut'].value_counts()
        st.bar_chart(statut_counts)
    
    with col2:
        st.subheader("🔴 Équipements par état")
        etat_counts = equipements['etat'].value_counts()
        st.bar_chart(etat_counts)
    
    # Alertes
    st.subheader("🚨 Alertes")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Stocks critiques
        stocks_critiques = stocks[stocks['quantite'] <= stocks['seuil_minimum']]
        if len(stocks_critiques) > 0:
            st.error(f"**Stocks critiques : {len(stocks_critiques)}**")
            for _, stock in stocks_critiques.iterrows():
                st.write(f"• {stock['designation']} : {stock['quantite']} restants")
        else:
            st.success("✅ Aucun stock critique")
    
    with col2:
        # Interventions urgentes
        interventions_urgentes = interventions[
            (interventions['priorite'] == 'haute') & 
            (interventions['statut'] == 'en_cours')
        ]
        if len(interventions_urgentes) > 0:
            st.warning(f"**Interventions urgentes : {len(interventions_urgentes)}**")
            for _, interv in interventions_urgentes.head(3).iterrows():
                st.write(f"• {interv['equipement_nom']} - {interv['description'][:50]}...")
        else:
            st.success("✅ Aucune intervention urgente")

def interventions_page():
    """Page gestion des interventions"""
    st.header("🔧 Gestion des interventions")
    
    interventions = get_all_interventions()
    
    # Filtres
    col1, col2, col3 = st.columns(3)
    
    with col1:
        statut_filter = st.multiselect(
            "Statut",
            options=interventions['statut'].unique(),
            default=['en_cours', 'a_planifier']
        )
    
    with col2:
        priorite_filter = st.multiselect(
            "Priorité",
            options=interventions['priorite'].unique(),
            default=['haute', 'moyenne']
        )
    
    with col3:
        technicien_filter = st.multiselect(
            "Technicien",
            options=interventions['technicien_nom'].unique()
        )
    
    # Filtrage
    df = interventions.copy()
    
    if statut_filter:
        df = df[df['statut'].isin(statut_filter)]
    
    if priorite_filter:
        df = df[df['priorite'].isin(priorite_filter)]
    
    if technicien_filter:
        df = df[df['technicien_nom'].isin(technicien_filter)]
    
    # Formatage pour affichage
    df_display = df[[
        'code', 'equipement_nom', 'description', 'technicien_nom',
        'date_planifiee', 'statut', 'priorite', 'duree_estimee', 'cout_estime'
    ]].copy()
    
    df_display.columns = [
        'Code', 'Équipement', 'Description', 'Technicien',
        'Date planifiée', 'Statut', 'Priorité', 'Durée (h)', 'Coût estimé (€)'
    ]
    
    # Affichage
    st.dataframe(df_display, use_container_width=True, height=400)
    
    # Actions
    col1, col2 = st.columns(2)
    
    with col1:
        csv = df_display.to_csv(index=False)
        st.download_button(
            "📥 Exporter CSV",
            data=csv,
            file_name="interventions.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col2:
        if st.button("🔄 Rafraîchir données", use_container_width=True):
            st.rerun()

def new_intervention_page():
    """Page création d'intervention"""
    st.header("➕ Nouvelle intervention")
    
    # Charger les données nécessaires
    equipements = get_all_equipements()
    techniciens = query_to_dataframe("SELECT id, full_name FROM users WHERE role = 'technicien'")
    
    with st.form("nouvelle_intervention", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            equipement_id = st.selectbox(
                "Équipement *",
                options=equipements[['id', 'nom']].itertuples(index=False, name=None),
                format_func=lambda x: f"{x[1]}"
            )[0]
            
            type_inter = st.selectbox(
                "Type *",
                ["maintenance", "reparation", "revision", "controle", "autre"]
            )
            
            priorite = st.select_slider(
                "Priorité *",
                options=['basse', 'moyenne', 'haute']
            )
        
        with col2:
            technicien_id = st.selectbox(
                "Technicien *",
                options=techniciens[['id', 'full_name']].itertuples(index=False, name=None),
                format_func=lambda x: x[1]
            )[0]
            
            date_planifiee = st.date_input("Date planifiée *", datetime.date.today())
            
            duree_estimee = st.number_input("Durée estimée (h) *", min_value=1, max_value=168, value=4)
        
        description = st.text_area("Description détaillée *", height=100)
        
        submitted = st.form_submit_button("✅ CRÉER L'INTERVENTION", type="primary")
        
        if submitted and description:
            data = {
                'equipement_id': equipement_id,
                'type': type_inter,
                'description': description,
                'technicien_id': technicien_id,
                'date_planifiee': date_planifiee.strftime('%Y-%m-%d'),
                'duree_estimee': duree_estimee,
                'priorite': priorite,
                'created_by': st.session_state.user['id']
            }
            
            try:
                intervention_id = add_intervention(data)
                
                # Log l'action
                log_action('interventions', intervention_id, 'create', 
                          f'Nouvelle intervention créée par {st.session_state.user["full_name"]}',
                          st.session_state.user['id'])
                
                st.success(f"✅ Intervention créée avec succès ! ID: {intervention_id}")
                st.balloons()
                
                # Afficher récapitulatif
                with st.expander("📋 Récapitulatif", expanded=True):
                    equipement_nom = equipements[equipements['id'] == equipement_id]['nom'].iloc[0]
                    technicien_nom = techniciens[techniciens['id'] == technicien_id]['full_name'].iloc[0]
                    
                    st.write(f"**Code:** INT{intervention_id:04d}")
                    st.write(f"**Équipement:** {equipement_nom}")
                    st.write(f"**Technicien:** {technicien_nom}")
                    st.write(f"**Priorité:** {priorite}")
                    st.write(f"**Date:** {date_planifiee.strftime('%d/%m/%Y')}")
                    st.write(f"**Coût estimé:** {duree_estimee * 75} €")
                    
            except Exception as e:
                st.error(f"Erreur lors de la création : {e}")
        
        elif submitted:
            st.error("Veuillez remplir la description")

def database_page():
    """Page administration de la base de données"""
    st.header("⚙️ Base de données")
    
    tab1, tab2, tab3 = st.tabs(["📊 Statistiques", "🧹 Maintenance", "🔧 SQL"])
    
    with tab1:
        st.subheader("Statistiques de la base")
        
        # Récupérer les statistiques
        stats = {}
        
        conn = get_connection()
        cursor = conn.cursor()
        
        tables = ['users', 'equipements', 'interventions', 'stocks', 'historique']
        
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            stats[table] = cursor.fetchone()[0]
        
        conn.close()
        
        # Afficher les stats
        col1, col2 = st.columns(2)
        
        with col1:
            for table, count in list(stats.items())[:3]:
                st.metric(table.capitalize(), count)
        
        with col2:
            for table, count in list(stats.items())[3:]:
                st.metric(table.capitalize(), count)
        
        # Taille de la base
        db_size = DB_PATH.stat().st_size / 1024  # en KB
        st.progress(min(db_size / 1024, 1), text=f"Taille de la base: {db_size:.1f} KB")
    
    with tab2:
        st.subheader("Maintenance")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔄 Vérifier l'intégrité", use_container_width=True):
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("PRAGMA integrity_check")
                result = cursor.fetchone()
                conn.close()
                
                if result[0] == 'ok':
                    st.success("✅ Base de données intègre")
                else:
                    st.error(f"Problème détecté : {result[0]}")
            
            if st.button("💾 Sauvegarde manuelle", use_container_width=True):
                backup_path = DB_PATH.with_suffix('.backup.db')
                import shutil
                shutil.copy2(DB_PATH, backup_path)
                st.success(f"✅ Sauvegarde créée : {backup_path.name}")
        
        with col2:
            if st.button("🗑️ Vider l'historique", use_container_width=True):
                execute_query("DELETE FROM historique WHERE created_at < date('now', '-30 days')")
                st.success("✅ Historique nettoyé (30+ jours)")
            
            if st.button("📋 Exporter en JSON", use_container_width=True):
                st.info("Fonctionnalité à implémenter")
    
    with tab3:
        st.subheader("Exécuter une requête SQL")
        
        query = st.text_area("Requête SQL", height=150)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("▶️ Exécuter", type="primary"):
                if query:
                    try:
                        if query.strip().upper().startswith('SELECT'):
                            df = query_to_dataframe(query)
                            st.dataframe(df, use_container_width=True)
                            st.success(f"✅ {len(df)} lignes retournées")
                        else:
                            execute_query(query)
                            st.success("✅ Requête exécutée avec succès")
                    except Exception as e:
                        st.error(f"❌ Erreur SQL : {e}")
        
        with col2:
            if st.button("📋 Requêtes exemples"):
                st.code("""
-- Exemples de requêtes :
SELECT * FROM interventions LIMIT 5;
SELECT statut, COUNT(*) FROM interventions GROUP BY statut;
SELECT e.nom, COUNT(i.id) FROM equipements e LEFT JOIN interventions i ON e.id = i.equipement_id GROUP BY e.id;
                """)

# ========== FONCTIONS UTILITAIRES ==========
def logout():
    """Déconnexion de l'utilisateur"""
    # Log la déconnexion
    if 'user' in st.session_state:
        log_action('users', st.session_state.user['id'], 'logout', 'Déconnexion', st.session_state.user['id'])
    
    for key in list(st.session_state.keys()):
        if key != 'rerun':
            del st.session_state[key]
    st.rerun()

# ========== APPLICATION PRINCIPALE ==========
def main_app():
    """Application principale après connexion"""
    # Initialiser la base si besoin
    init_database()
    
    # Sidebar
    show_sidebar()
    
    # Affichage de la page sélectionnée
    menu = st.session_state.get('menu', '🏠 Dashboard')
    
    if menu == "🏠 Dashboard":
        dashboard_page()
    
    elif menu == "🔧 Interventions" or menu == "🔧 Mes interventions":
        interventions_page()
    
    elif menu == "🏭 Équipements":
        st.header("🏭 Équipements")
        equipements = get_all_equipements()
        st.dataframe(equipements, use_container_width=True)
    
    elif menu == "📦 Stocks":
        st.header("📦 Gestion des stocks")
        stocks = get_all_stocks()
        st.dataframe(stocks, use_container_width=True)
    
    elif menu == "➕ Nouvelle intervention":
        new_intervention_page()
    
    elif menu == "👥 Utilisateurs":
        if st.session_state.user["role"] == "admin":
            st.header("👥 Gestion des utilisateurs")
            users = query_to_dataframe("SELECT id, username, role, full_name, email, created_at FROM users")
            st.dataframe(users, use_container_width=True)
        else:
            st.error("Accès non autorisé")
    
    elif menu == "📊 Rapports":
        st.header("📊 Rapports")
        
        # Générer un rapport simple
        interventions = get_all_interventions()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Interventions ce mois", 
                     len(interventions[interventions['date_planifiee'] >= datetime.date.today().strftime('%Y-%m-01')]))
            st.metric("Coût total estimé", f"{interventions['cout_estime'].sum():,.0f} €".replace(",", " "))
        
        with col2:
            taux_termine = len(interventions[interventions['statut'] == 'termine']) / len(interventions) * 100
            st.metric("Taux de réalisation", f"{taux_termine:.1f}%")
            st.metric("Durée moyenne", f"{interventions['duree_estimee'].mean():.1f}h")
    
    elif menu == "⚙️ Base de données":
        if st.session_state.user["role"] == "admin":
            database_page()
        else:
            st.error("Accès non autorisé")

# ========== POINT D'ENTRÉE ==========
def main():
    """Point d'entrée principal de l'application"""
    # Vérification de l'authentification
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    
    if not st.session_state.authenticated:
        login_page()
    else:
        main_app()

if __name__ == "__main__":
    main()
