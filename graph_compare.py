from graph_base import GraphBase
import matplotlib.pyplot as plt

class CompareGraph(GraphBase):
    """
    Classe spécialisée pour les graphiques de comparaison.
    Elle hérite de GraphBase, donc elle a déjà accès à self.figure, self.ax et self.canvas.
    """
    def __init__(self):
        # Appelle le constructeur parent pour initialiser la fenêtre Matplotlib
        super().__init__()
        # Palette de couleurs manuelle ('b'=blue, 'g'=green, etc.)
        # Utilisée pour distinguer visuellement les pays quand on trace plusieurs courbes
        self.colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'orange', 'purple', 'brown']

    def plot_scatter(self, df, col_x, col_y):
        """1. Nuage de points (Permet de voir la corrélation entre deux variables)"""
        # Efface le graphique précédent (sinon les points s'accumulent)
        self.clear_ax()
        
        # Gestion de cas vide (éviter de planter si le filtre est trop restrictif)
        if df.empty:
            self.ax.text(0.5, 0.5, "Pas de données", ha='center')
        else:
            # Récupération des colonnes à comparer
            x = df[col_x]
            y = df[col_y]
            
            # Tracé du Scatter plot (nuage de points)
            # alpha=0.7 : Transparence (0 à 1) pour voir les points superposés
            # edgecolors='k' : Contour noir autour des cercles bleus pour la netteté
            self.ax.scatter(x, y, alpha=0.7, c='blue', edgecolors='k')

            # --- Habillage du graphique ---
            self.ax.set_xlabel(col_x) # Label axe X
            self.ax.set_ylabel(col_y) # Label axe Y
            self.ax.set_title(f"Corrélation : {col_x} vs {col_y}")
            # Grille en pointillés pour faciliter la lecture
            self.ax.grid(True, linestyle='--', alpha=0.6)

        # Ajustement des marges pour éviter que les titres soient coupés
        self.figure.tight_layout()
        # Commande vitale : Demande à PyQt de redessiner le widget avec la nouvelle image
        self.canvas.draw()

    def plot_bar(self, df, col_metric):
        """2. Diagramme en barres horizontales (Classement)"""
        self.clear_ax()
        
        if df.empty:
            self.ax.text(0.5, 0.5, "Pas de données", ha='center')
        else:
            # --- Préparation des données pour un classement lisible ---
            # 1. sort_values : On trie les données par ordre croissant
            # 2. tail(15) : On prend les 15 dernières valeurs (donc les 15 plus grandes)
            #    Dans un barh (horizontal), les dernières valeurs s'affichent en haut.
            df_sorted = df.sort_values(by=col_metric, ascending=True).tail(15) 
            
            countries = df_sorted['Country']
            values = df_sorted[col_metric]

            # Tracé des barres horizontales (barH)
            self.ax.barh(countries, values, color='skyblue', edgecolor='black')
            
            # --- Habillage ---
            self.ax.set_xlabel(col_metric)
            self.ax.set_title(f"Classement par : {col_metric}")
            # Grille verticale seulement (axis='x') pour comparer la longueur des barres
            self.ax.grid(axis='x', linestyle='--', alpha=0.6)

        self.figure.tight_layout()
        self.canvas.draw()

    def plot_multi_curves(self, df, col_metric):
        """3. Courbes d'évolution superposables (Analyse temporelle)"""
        self.clear_ax()
        
        if df.empty:
            self.ax.text(0.5, 0.5, "Pas de données\nSélectionnez des pays", ha='center')
        else:
            # On récupère la liste unique des pays présents dans le DataFrame filtré
            countries_list = df['Country'].unique()
            
            # --- Boucle de traçage ---
            # Pour chaque pays, on trace une ligne distincte sur le MEME graphique
            for i, country in enumerate(countries_list):
                # 1. On isole les données de CE pays
                # 2. On trie par année pour que la ligne ne fasse pas des zig-zags temporels
                df_country = df[df['Country'] == country].sort_values(by='Year')
                
                # Sélection de la couleur :
                # i % len(self.colors) permet de boucler sur la liste si on a plus de pays que de couleurs
                # (ex: si i=10 et len=10, on reprend la couleur 0)
                color = self.colors[i % len(self.colors)]
                
                # Tracé de la courbe
                # marker='o' : Ajoute un point à chaque année
                # label=country : Indispensable pour la légende
                self.ax.plot(df_country['Year'], df_country[col_metric], 
                             marker='o', label=country, color=color)

            # --- Habillage ---
            self.ax.set_xlabel("Année")
            self.ax.set_ylabel(col_metric)
            self.ax.set_title(f"Évolution temporelle : {col_metric}")
            # Affiche la légende (boîte avec noms des pays) en utilisant les 'label' définis plus haut
            self.ax.legend() 
            self.ax.grid(True)

        self.figure.tight_layout()
        self.canvas.draw()