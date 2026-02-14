from graph_base import GraphBase

class CountryGraph(GraphBase):
    def __init__(self):
        super().__init__()    
    # =========================================================================
    # 1. LE DIAGRAMME CIRCULAIRE (CAMEMBERT)
    # =========================================================================
    def plot_pie(self, df):
        """Affiche la répartition des données par Région"""
        
        # Effacer le dessin précédent :
        self.clear_ax()

        if df.empty:
            self.ax.text(0.5, 0.5, "Pas de données", ha='center')
        else:
            # Préparation des données :
            counts = df['Region'].value_counts()
            
            # Création du Camembert
            self.ax.pie(counts, labels=counts.index, autopct='%1.1f%%', startangle=90)
            self.ax.set_title("Répartition par Région")

        #  Mise en page :
        self.figure.tight_layout() # Ajustement marges
        self.canvas.draw() # Affichage

    # =========================================================================
    # 2. LA COURBE D'ÉVOLUTION 
    # =========================================================================
    def plot_line(self, df):
        """
        Affiche l'évolution du score au fil des années
        - Si 1 seul pays est sélectionné : évolution de ce pays
        - Sinon : évolution du score moyen (tous pays filtrés)
        """

        self.clear_ax()

        if df.empty:
            self.ax.text(0.5, 0.5, "Pas de données", ha='center')
            self.figure.tight_layout()
            self.canvas.draw()
            return

        # Sécurité: 
        df = df.copy()
        df["Year"] = df["Year"].astype(int)

        nb_countries = df["Country"].nunique()

        if nb_countries == 1:
            # --- CAS 1 : Un seul pays ---
            country_name = df["Country"].iloc[0]
            df_sorted = df.sort_values("Year")

            years = df_sorted["Year"].values
            scores = df_sorted["Happiness Score"].values

            self.ax.plot(years, scores, marker='o', linestyle='-', label=country_name)
            self.ax.grid(True)
            self.ax.set_title(f"Évolution du Score — {country_name}")

        else:
            # --- CAS 2 : Plusieurs pays (moyenne par année) ---
            df_grouped = df.groupby("Year")["Happiness Score"].mean().sort_index()

            years = df_grouped.index.values
            scores = df_grouped.values

            self.ax.plot(years, scores, marker='o', linestyle='-', label="Score Moyen")
            self.ax.set_title("Évolution du Score Moyen")

            self.ax.set_xlabel("Année")
            self.ax.set_ylabel("Score")
            self.ax.set_title("Évolution du Score")
            self.ax.grid(True)
            
        self.figure.tight_layout() # Ajustement marges
        self.canvas.draw() # Affichage

    # =========================================================================
    # 3. L'HISTOGRAMME (DISTRIBUTION)
    # =========================================================================
    def plot_hist(self, df):
        """Affiche combien de pays se trouvent dans chaque tranche de score"""
        
        self.clear_ax() 
        
        if df.empty:
            self.ax.text(0.5, 0.5, "Pas de données", ha='center')
        else:
            # Récupération de la colonne des scores
            data = df['Happiness Score']
            
            # Création des intervalles 
            #bins = [i * 0.5 for i in range(21)] 
            
            # Tracage de l'histogramme.
            #self.ax.hist(data, bins=bins, color='#4CAF50', edgecolor='black', alpha=0.8, rwidth=0.9)
            self.ax.hist(data, bins=30, color='#4CAF50',edgecolor='black', alpha=0.8)
            self.ax.set_xlim(0, 10)
            self.ax.set_xticks(bin)
            self.ax.set_xticklabels([str(b) for b in bin], rotation=45, fontsize=9)
            self.ax.set_xlabel("Score de Bonheur (0 à 10)")
            self.ax.set_ylabel("Nombre de Pays")
            self.ax.set_title("Distribution des Scores de Bonheur")
            self.ax.grid(axis='y', alpha=0.5, linestyle='--')

        self.figure.tight_layout() # Ajustement marges
        self.canvas.draw() # Affichage