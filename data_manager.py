import pandas as pd  # Importation de la bibliothèque Pandas pour la manipulation de données (Tableaux)
import os  # Importation du module OS pour gérer les chemins de fichiers sur le système d'exploitation

class DataManager:
    def __init__(self, filename="happiness.csv"):
        # --- GESTION DU CHEMIN DU FICHIER ---
        # Récupère le dossier où se trouve le script actuel (.py) pour éviter les erreurs de chemin relatif
        current_folder = os.path.dirname(os.path.abspath(__file__))
        # Construit le chemin complet (ex: C:/Projet/happiness.csv) compatible Windows/Mac/Linux
        file_path = os.path.join(current_folder, filename)
        
        # Initialisation d'un DataFrame vide par sécurité au démarrage
        self.df = pd.DataFrame()

        # Vérification de l'existence du fichier avant d'essayer de le lire
        if not os.path.exists(file_path):
            print(f"❌ ERREUR : Le fichier est introuvable ici : {file_path}")
            return

        try:
            # --- TENTATIVE DE CHARGEMENT (PLAN A) ---
            # On essaie d'abord avec le séparateur point-virgule (standard CSV Excel français)
            self.df = pd.read_csv(file_path, sep=';', decimal='.')
            
            # Nettoyage des noms de colonnes :
            # 1. .str.strip() : Enlève les espaces avant/après les noms (ex: " Region " devient "Region")
            # 2. .replace('\ufeff', '') : Enlève le BOM (Byte Order Mark), un caractère invisible parfois ajouté par Excel
            self.df.columns = self.df.columns.str.strip().str.replace('\ufeff', '')

            # Vérification si la colonne 'Year' a bien été détectée (signe que le séparateur ';' était le bon)
            if 'Year' in self.df.columns:
                # Conversion de l'année en texte (str) pour faciliter l'affichage dans les menus déroulants
                self.df['Year'] = self.df['Year'].astype(str)
            else:
                # --- TENTATIVE DE CHARGEMENT (PLAN B) ---
                # Si la colonne 'Year' n'est pas trouvée, le séparateur était probablement mauvais.
                # On réessaie avec la virgule (standard CSV international)
                self.df = pd.read_csv(file_path, sep=',', decimal='.')
                
                # On refait le même nettoyage des noms de colonnes
                self.df.columns = self.df.columns.str.strip().str.replace('\ufeff', '')
                
                if 'Year' in self.df.columns:
                    self.df['Year'] = self.df['Year'].astype(str)

        except Exception as e:
            # Capture toute erreur technique (ex: fichier corrompu, problème de permissions)
            print(f"❌ ERREUR TECHNIQUE : {e}")

    def get_all_years(self):
        # Renvoie une liste vide si le fichier n'a pas été chargé
        if self.df.empty: return []
        # Renvoie la liste des années uniques, triées par ordre croissant
        return sorted(self.df['Year'].unique())

    def get_all_regions(self):
        # Vérifie si la colonne 'Region' existe pour éviter un crash
        if self.df.empty or 'Region' not in self.df.columns: return []
        # .dropna() enlève les valeurs vides (NaN) avant de chercher les valeurs uniques
        return sorted(self.df['Region'].dropna().unique())

    def get_all_countries(self):
        if self.df.empty: return []
        return sorted(self.df['Country'].unique())
    
    # --- NOUVELLE FONCTION DE FILTRAGE AVANCÉ ---
    def filter_data_advanced(self, year, region, country, 
                             happ_min, happ_max,
                             gdp_min, gdp_max,
                             fam_min, fam_max,
                             health_min, health_max,
                             free_min, free_max,
                             trust_min, trust_max,
                             gen_min, gen_max):
        
        # Sécurité : si aucune donnée n'est chargée, on renvoie un tableau vide tout de suite
        if self.df.empty: return pd.DataFrame()
        
        # IMPORTANT : On travaille sur une COPIE (.copy()) du DataFrame original.
        # Cela évite de supprimer définitivement les données de la mémoire de l'application.
        df = self.df.copy()

        # 1. Filtres Textuels (Listes déroulantes)
        # On n'applique le filtre que si l'utilisateur n'a pas choisi "Toutes"
        if year != "Toutes":
            df = df[df['Year'] == year]
        if region != "Toutes":
            df = df[df['Region'] == region]
        if country != "Toutes":
            df = df[df['Country'] == country]

        # 2. Filtres Numériques (Bornes Min et Max - Sliders)
        # On utilise le nom exact des colonnes tel qu'écrit dans le fichier CSV
        try:
            # On applique tous les filtres en même temps avec l'opérateur '&' (ET logique).
            # Une ligne n'est gardée que si elle respecte TOUTES ces conditions.
            df = df[
                (df['Happiness Score'] >= happ_min) & (df['Happiness Score'] <= happ_max) &
                (df['Economy (GDP per Capita)'] >= gdp_min) & (df['Economy (GDP per Capita)'] <= gdp_max) &
                (df['Family'] >= fam_min) & (df['Family'] <= fam_max) &
                (df['Health (Life Expectancy)'] >= health_min) & (df['Health (Life Expectancy)'] <= health_max) &
                (df['Freedom'] >= free_min) & (df['Freedom'] <= free_max) &
                (df['Trust (Government Corruption)'] >= trust_min) & (df['Trust (Government Corruption)'] <= trust_max) &
                (df['Generosity'] >= gen_min) & (df['Generosity'] <= gen_max)
            ]
        except KeyError as e:
            # Cette erreur arrive si une colonne (ex: 'Happiness Score') n'existe pas dans le CSV chargé
            print(f"⚠️ Erreur de colonne manquante lors du filtrage : {e}")
        
        # On retourne le résultat filtré pour affichage
        return df