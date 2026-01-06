# On importe la classe parent GraphBase.
# Cela nous permet de récupérer toute la configuration technique (la fenêtre vide, le canevas, etc.)
# sans avoir à la réécrire. C'est le principe de l'héritage.
from graph_base import GraphBase

class CountryGraph(GraphBase):
    def __init__(self):
        # On initialise la classe parent (GraphBase) pour que la fenêtre se crée.
        super().__init__()
        # Pour l'instant, pas d'initialisation spécifique supplémentaire,
        # mais on pourrait par exemple définir des couleurs personnalisées ici plus tard.
        
    # =========================================================================
    # 1. LE DIAGRAMME CIRCULAIRE (CAMEMBERT)
    # =========================================================================
    def plot_pie(self, df):
        """Affiche la répartition des données par Région"""
        
        # Etape 1 : On efface le dessin précédent.
        # Si on ne fait pas ça, le nouveau graphique se dessine PAR DESSUS l'ancien.
        self.clear_ax()

        # Etape 2 : Sécurité. Si le tableau de données (df) est vide (ex: filtres trop stricts),
        # on affiche juste un message texte au milieu pour ne pas faire planter l'appli.
        if df.empty:
            self.ax.text(0.5, 0.5, "Pas de données", ha='center')
        else:
            # Etape 3 : Préparation des données.
            # 'value_counts()' compte combien de fois chaque région apparaît dans la colonne.
            counts = df['Region'].value_counts()
            
            # Etape 4 : Création du Camembert.
            # - counts : les données chiffrées
            # - labels : les noms des régions (Europe, Asia, etc.)
            # - autopct='%1.1f%%' : affiche le pourcentage avec 1 chiffre après la virgule
            # - startangle=90 : tourne le graph pour que la 1ère part commence en haut (plus esthétique)
            self.ax.pie(counts, labels=counts.index, autopct='%1.1f%%', startangle=90)
            
            # On ajoute un titre
            self.ax.set_title("Répartition par Région")

        # Etape 5 : Mise en page automatique.
        # 'tight_layout' ajuste les marges pour éviter que le texte (titre, labels) ne soit coupé.
        self.figure.tight_layout()
        
        # Etape 6 : Rafraîchissement.
        # C'est l'ordre "Affiche-toi maintenant !" envoyé à l'interface graphique.
        self.canvas.draw()

    # =========================================================================
    # 2. LA COURBE D'ÉVOLUTION (LINE CHART)
    # =========================================================================
    def plot_line(self, df):
        """Affiche l'évolution du score moyen au fil des années"""
        
        self.clear_ax() # On nettoie
        
        if df.empty:
            self.ax.text(0.5, 0.5, "Pas de données", ha='center')
        else:
            # Etape 3 : Regroupement par Année.
            # Si on a sélectionné plusieurs pays, on ne peut pas tracer 50 lignes d'un coup.
            # On calcule la MOYENNE (mean) du 'Happiness Score' pour chaque année.
            # 'sort_index()' assure que les années sont bien dans l'ordre (2015, 2016...).
            df_grouped = df.groupby('Year')['Happiness Score'].mean().sort_index()
            
            # On sépare les X (Années) et les Y (Scores) pour le dessin
            years = df_grouped.index
            scores = df_grouped.values
            
            # Etape 4 : Tracé de la courbe.
            # - marker='o' : met un petit point sur chaque année
            # - linestyle='-' : relie les points par une ligne continue
            # - color='b' : bleu (blue)
            self.ax.plot(years, scores, marker='o', linestyle='-', color='b', label='Score Moyen')
            
            # Configuration des axes
            self.ax.set_xlabel("Année")
            self.ax.set_ylabel("Score")
            self.ax.set_title("Évolution du Score")
            
            # Ajout d'une grille pour faciliter la lecture
            self.ax.grid(True)
            
        self.figure.tight_layout() # Ajustement marges
        self.canvas.draw() # Affichage

    # =========================================================================
    # 3. L'HISTOGRAMME (DISTRIBUTION)
    # =========================================================================
    def plot_hist(self, df):
        """Affiche combien de pays se trouvent dans chaque tranche de score"""
        
        self.clear_ax() # On nettoie
        
        if df.empty:
            self.ax.text(0.5, 0.5, "Pas de données", ha='center')
        else:
            # On récupère uniquement la colonne des scores
            data = df['Happiness Score']
            
            # Création des "bins" (les intervalles).
            # On veut des barres tous les 0.5 points, de 0 à 10.
            # range(21) donne 0, 1, ... 20. Multiplié par 0.5, ça donne 0.0, 0.5, 1.0 ... 10.0
            bins = [i * 0.5 for i in range(21)] 
            
            # Etape 4 : Tracé de l'histogramme.
            # - color : couleur de remplissage (vert hexadécimal)
            # - edgecolor : contour noir autour des barres pour bien les séparer
            # - alpha : transparence (0.8 = un peu transparent)
            # - rwidth : largeur des barres (0.9 laisse un petit espace entre elles)
            self.ax.hist(data, bins=bins, color='#4CAF50', edgecolor='black', alpha=0.8, rwidth=0.9)
            
            # Etape 5 : Forcer l'échelle.
            # Même si les pays n'ont que des scores entre 3 et 7, on veut voir l'axe de 0 à 10
            # pour avoir une vision globale.
            self.ax.set_xlim(0, 10)
            
            # On définit les graduations (ticks) sur l'axe X pour qu'elles matchent nos barres
            self.ax.set_xticks(bins)
            # On écrit les labels en biais (45 degrés) pour qu'ils ne se chevauchent pas
            self.ax.set_xticklabels([str(b) for b in bins], rotation=45, fontsize=9)
            
            # Titres
            self.ax.set_xlabel("Score de Bonheur (0 à 10)")
            self.ax.set_ylabel("Nombre de Pays")
            self.ax.set_title("Distribution des Scores de Bonheur")
            
            # Grille horizontale seulement (axis='y') et en pointillés (linestyle='--')
            self.ax.grid(axis='y', alpha=0.5, linestyle='--')

        self.figure.tight_layout() # Ajustement marges
        self.canvas.draw() # Affichage