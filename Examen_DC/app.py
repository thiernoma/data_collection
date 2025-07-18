import streamlit as st
import pandas as pd
from datetime import datetime
import webbrowser
import os
from scraper import scrape_dakar_auto, scrape_dakar_moto, scrape_dakar_location

# Configuration de la page
st.set_page_config(
    page_title="Dakar Auto Scraper", 
    layout="wide",
    page_icon="🚗"
)

# Chemins des fichiers CSV
DATA_FOLDER = "Data"
CSV_FILES = {
    'voitures': os.path.join(DATA_FOLDER, "dakar_voitures.csv"),
    'motos': os.path.join(DATA_FOLDER, "dakar_motos.csv"),
    'locations': os.path.join(DATA_FOLDER, "dakar_locations.csv")
}

# Initialisation des données
if 'scraped_data' not in st.session_state:
    st.session_state.scraped_data = {
        'voitures': {'df': None, 'time': None, 'source': None},
        'motos': {'df': None, 'time': None, 'source': None},
        'locations': {'df': None, 'time': None, 'source': None}
    }

# Sidebar
with st.sidebar:
    st.title("📋 Menu")
    
    selected_option = st.selectbox(
        "Choisissez une action :",
        options=[
            "Scraper des données",
            "Télécharger les données",
            "Visualiser les données",
            "Noter l'application"
        ]
    )
    
    if selected_option == "Scraper des données":
        num_pages = st.slider("Nombre de pages", 1, 20, 1)

# Fonctions de chargement
def load_csv_data(category):
    try:
        df = pd.read_csv(CSV_FILES[category])
        return {
            'df': df,
            'time': datetime.fromtimestamp(os.path.getmtime(CSV_FILES[category])),
            'source': 'fichier'
        }
    except Exception as e:
        st.error(f"Erreur de chargement du fichier {category}: {str(e)}")
        return None

# Contenu principal
st.title("🚗 Dakar Auto - Outil de Données")

# Mode Scraping
if selected_option == "Scraper des données":
    st.header("🔎 Scraping en direct")
    
    col1, col2, col3 = st.columns(3)
    
    scrapers = {
        'voitures': (scrape_dakar_auto, "🚗 Voitures"),
        'motos': (scrape_dakar_moto, "🏍️ Motos"),
        'locations': (scrape_dakar_location, "🏠 Locations")
    }
    
    for idx, (category, (scraper, btn_text)) in enumerate(scrapers.items()):
        with [col1, col2, col3][idx]:
            if st.button(btn_text, use_container_width=True):
                with st.spinner(f"Scraping des {category}..."):
                    data = scraper(pages=num_pages)
                    st.session_state.scraped_data[category] = {
                        'df': data,
                        'time': datetime.now(),
                        'source': 'scraping'
                    }
                st.success(f"{len(data)} {category} scrapées!")
                
                # Afficher les données juste après le scraping
                st.subheader(f"Données {category} scrapées")
                st.dataframe(data)  # Affiche les premières lignes

# Mode Téléchargement
elif selected_option == "Télécharger les données":
    st.header("📂 Données Locales (CSV)")
    
    data_type = st.selectbox("Catégorie", ["Voitures", "Motos", "Locations"])
    category = data_type.lower()
    
    try:
        # Chargement direct depuis le fichier CSV seulement
        data_info = load_csv_data(category)
        
        if data_info and data_info['df'] is not None:
            st.info(f"Données {category} (source: fichier local) - {len(data_info['df'])} annonces")
            
            # Bouton de téléchargement
            csv = data_info['df'].to_csv(index=False).encode('utf-8')
            st.download_button(
                "📥 Télécharger CSV",
                csv,
                f"dakar_{category}.csv",
                "text/csv",
                use_container_width=True
            )
            
            # Aperçu des données
            st.subheader("Aperçu des données")
            st.dataframe(data_info['df'].head())
            
            # Statistiques basiques
            st.subheader("Statistiques")
            st.write(f"Dernière mise à jour: {data_info['time'].strftime('%d/%m/%Y %H:%M')}")
            st.write(f"Nombre total d'annonces: {len(data_info['df'])}")
            
        else:
            st.warning(f"Aucun fichier CSV trouvé pour les {category}")
            
    except Exception as e:
        st.error(f"Erreur lors du chargement des données: {str(e)}")

# Mode Visualisation
elif selected_option == "Visualiser les données":
    st.header("📊 Visualisation des données")
    
    # Choix du type de véhicule
    choix = st.selectbox(
        "Quelles données visualiser ?",
        ["Voitures", "Motos", "Locations"]
    )
    
    # Correspondance avec les fichiers
    fichiers = {
        "Voitures": "Data/dakar_voitures.csv",
        "Motos": "Data/dakar_motos.csv", 
        "Locations": "Data/dakar_locations.csv"
    }
    
    try:
        # Chargement du fichier
        df = pd.read_csv(fichiers[choix])
        
        # Supprimer les 4 premières colonnes si elles existent
        if len(df.columns) > 4:
            df = df.iloc[:, 4:]
        
        # Nettoyage des données
        if 'brand' in df.columns:
            # Prendre seulement la première partie de la marque
            df['brand'] = df['brand'].str.split().str[0].str.strip()
            df['brand'] = df['brand'].replace('', 'Inconnu')
        
        if 'year' in df.columns:
            # Extraire seulement l'année
            df['year'] = df['year'].str.extract(r'(\d{4})')[0]
            df['year'] = df['year'].replace('', 'Inconnu')
        
        if 'price' in df.columns:
            # Nettoyage des prix
            df['price'] = df['price'].str.replace('F CFA', '').str.strip()
            
            # Création d'une colonne numérique pour les calculs (avec gestion des erreurs)
            df['prix_num'] = df['price'].str.replace('[^\d]', '', regex=True)
            df['prix_num'] = pd.to_numeric(df['prix_num'], errors='coerce')  # Convertit les erreurs en NaN
        
        if 'kms_driven' in df.columns:
            # Extraire seulement le nombre de kilomètres
            df['kms_driven'] = df['kms_driven'].str.extract(r'(\d+)')[0]
            df['kms_driven'] = pd.to_numeric(df['kms_driven'], errors='coerce')
        
        # Affichage des infos de base
        st.write(f"Nombre d'annonces : {len(df)}")
        
        if 'prix_num' in df.columns:
            # Calcul des statistiques en ignorant les NaN
            prix_mean = df['prix_num'].mean(skipna=True)
            prix_median = df['prix_num'].median(skipna=True)
            
            # Affichage des prix
            col1, col2 = st.columns(2)
            col1.metric("Prix moyen", f"{prix_mean:,.0f} XOF" if not pd.isna(prix_mean) else "Non disponible")
            col2.metric("Prix médian", f"{prix_median:,.0f} XOF" if not pd.isna(prix_median) else "Non disponible")
            
            # Graphique simple (en excluant les NaN)
            st.subheader("Distribution des prix")
            st.bar_chart(df['prix_num'].value_counts(dropna=True).head(10))
        
        # Afficher d'autres visualisations
        if 'brand' in df.columns:
            st.subheader("Répartition par marque")
            st.bar_chart(df['brand'].value_counts().head(10))
            
        if 'year' in df.columns:
            st.subheader("Répartition par année")
            st.bar_chart(df['year'].value_counts().sort_index())
        
        # Aperçu des données nettoyées
        st.subheader("Aperçu des données nettoyées")
        st.dataframe(df.head(10))
        
        # Afficher les statistiques manquantes
        st.subheader("Données manquantes")
        missing_data = df.isnull().sum()
        st.write(missing_data[missing_data > 0])
        
    except FileNotFoundError:
        st.error("Fichier non trouvé. Vérifiez que le fichier existe dans le dossier Data.")
    except Exception as e:
        st.error(f"Une erreur est survenue : {str(e)}")

# Mode Formulaire
elif selected_option == "Noter l'application":
    st.header("⭐ Évaluation")
    if st.button("Ouvrir le formulaire d'évaluation"):
        webbrowser.open_new_tab("https://ee.kobotoolbox.org/x/JO5GM8b2")
        st.success("Formulaire ouvert dans un nouvel onglet!")