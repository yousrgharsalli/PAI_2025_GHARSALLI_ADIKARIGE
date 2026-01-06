from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QComboBox, QGroupBox, QFormLayout, QDoubleSpinBox, 
                             QTableWidget, QTableWidgetItem, QPushButton)
from PyQt6.QtCore import Qt
# On importe notre propre widget graphique (celui qui contient Matplotlib)
from graph_country import CountryGraph

class CountryTab(QWidget):
    def __init__(self, data_manager):
        # Initialisation de la classe parente (QWidget)
        super().__init__()
        
        # On stocke le gestionnaire de données (DataManager) pour pouvoir l'utiliser
        # dans toute la classe (pour filtrer, récupérer les listes, etc.)
        self.data_manager = data_manager

        # Cette variable sert de "mémoire" : elle retient quel graphique est
        # actuellement affiché ('pie', 'line' ou 'hist'). Par défaut : pie.
        self.current_graph_mode = "pie"

        # --- Mise en page principale ---
        # On utilise un layout Horizontal (QHBoxLayout).
        # Imagine l'écran divisé en deux colonnes : Gauche (Filtres) | Droite (Résultats)
        self.main_layout = QHBoxLayout()
        self.setLayout(self.main_layout)

        # Appel de la méthode qui crée tous les boutons et menus
        self.setup_ui()
        
        # Une fois l'interface créée, on lance un premier rafraîchissement
        # pour afficher les données par défaut (sans filtres).
        self.refresh()

    def setup_ui(self):
        # --- ZONE 1 : FILTRES (Colonne de Gauche) ---
        # QGroupBox crée un cadre avec un titre autour des filtres pour faire propre.
        self.group_filters = QGroupBox("1. Filtres")
        self.group_filters.setFixedWidth(350) # On fixe la largeur à 350px.
        
        # QFormLayout est parfait pour les formulaires : il aligne "Libellé : Champ de saisie"
        filter_layout = QFormLayout(self.group_filters)

        # --- Création des menus déroulants (Année, Pays, Région) ---
        
        # 1. Menu Année
        self.combo_year = QComboBox()
        self.combo_year.addItem("Toutes") # Option par défaut
        # On demande au DataManager la liste des années disponibles dans le CSV
        self.combo_year.addItems(self.data_manager.get_all_years())
        
        # 2. Menu Pays
        self.combo_country = QComboBox()
        self.combo_country.addItem("Toutes")
        self.combo_country.addItems(self.data_manager.get_all_countries())

        # 3. Menu Région
        self.combo_region = QComboBox()
        self.combo_region.addItem("Toutes")
        self.combo_region.addItems(self.data_manager.get_all_regions())

        # On ajoute ces menus au layout du formulaire
        filter_layout.addRow("Année :", self.combo_year)
        filter_layout.addRow("Pays :", self.combo_country)
        filter_layout.addRow("Région :", self.combo_region)

        # --- Création des filtres numériques (Min / Max) ---
        # Pour ne pas écrire 7 fois le même code, on utilise une fonction "helper" 
        # (add_range_filter) définie plus bas. Elle crée les deux cases (min/max) d'un coup.
        
        self.spin_happ_min, self.spin_happ_max = self.add_range_filter(filter_layout, "Happiness", 0, 10, 0, 10)
        self.spin_gdp_min, self.spin_gdp_max = self.add_range_filter(filter_layout, "Economy", 0, 2, 0, 2)
        self.spin_fam_min, self.spin_fam_max = self.add_range_filter(filter_layout, "Family", 0, 2, 0, 2)
        self.spin_health_min, self.spin_health_max = self.add_range_filter(filter_layout, "Health", 0, 1, 0, 1)
        self.spin_free_min, self.spin_free_max = self.add_range_filter(filter_layout, "Freedom", 0, 1, 0, 1)
        self.spin_trust_min, self.spin_trust_max = self.add_range_filter(filter_layout, "Trust", 0, 1, 0, 1)
        self.spin_gen_min, self.spin_gen_max = self.add_range_filter(filter_layout, "Generosity", 0, 1, 0, 1)

        # --- Connexion des signaux (L'interactivité) ---
        # C'est ICI que la magie opère. On dit au programme : 
        # "Si l'utilisateur touche à quoi que ce soit, lance la fonction self.refresh()"
        
        all_widgets = [self.combo_year, self.combo_country, self.combo_region,
                       self.spin_happ_min, self.spin_happ_max, self.spin_gdp_min, self.spin_gdp_max,
                       self.spin_fam_min, self.spin_fam_max, self.spin_health_min, self.spin_health_max,
                       self.spin_free_min, self.spin_free_max, self.spin_trust_min, self.spin_trust_max,
                       self.spin_gen_min, self.spin_gen_max]
        
        for w in all_widgets:
            if isinstance(w, QComboBox):
                # Pour les menus déroulants, le signal est "currentTextChanged"
                w.currentTextChanged.connect(self.refresh)
            else:
                # Pour les boîtes à nombres, le signal est "valueChanged"
                w.valueChanged.connect(self.refresh)

        # Enfin, on ajoute tout ce groupe (Filtres) à gauche de la fenêtre principale
        self.main_layout.addWidget(self.group_filters)

        # --- ZONE DROITE (Tableau + Graphiques) ---
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget) # Layout Vertical : Tableau en haut, Graph en bas

        # --- A. Le Tableau ---
        self.table_data = QTableWidget()
        # On ajoute un titre simple au-dessus du tableau
        right_layout.addWidget(QLabel("<b>2. Tableau des données</b>"))
        right_layout.addWidget(self.table_data)

        # --- B. Les Graphiques ---
        right_layout.addWidget(QLabel("<b>3. Graphiques</b>"))
        
        # Création d'une ligne horizontale pour aligner les 3 boutons
        buttons_layout = QHBoxLayout()
        self.btn_pie = QPushButton("🥧 Répartition Régionale")
        self.btn_line = QPushButton("📈 Évolution Moyenne")
        self.btn_hist = QPushButton("📊 Distribution")

        # --- Connexion des boutons ---
        # On utilise "lambda" (une fonction anonyme) pour passer un paramètre.
        # Sans lambda, on ne pourrait pas dire "switch_mode('pie')".
        # Quand on clique, on change le mode du graphique.
        self.btn_pie.clicked.connect(lambda: self.switch_graph_mode("pie"))
        self.btn_line.clicked.connect(lambda: self.switch_graph_mode("line"))
        self.btn_hist.clicked.connect(lambda: self.switch_graph_mode("hist"))

        # Ajout des boutons à leur layout
        buttons_layout.addWidget(self.btn_pie)
        buttons_layout.addWidget(self.btn_line)
        buttons_layout.addWidget(self.btn_hist)
        # Ajout de la ligne de boutons à la colonne de droite
        right_layout.addLayout(buttons_layout)

        # --- C. Le Widget Graphique (Matplotlib) ---
        self.graph = CountryGraph()
        # IMPORTANT : On force une hauteur mini, sinon le tableau écrase le graphique
        self.graph.setMinimumHeight(450) 
        right_layout.addWidget(self.graph)

        # On ajoute toute la colonne de droite à la fenêtre principale
        self.main_layout.addWidget(right_widget)

    def add_range_filter(self, layout, label_text, min_val, max_val, default_min, default_max):
        # On crée un conteneur vide pour tenir nos 3 éléments sur une ligne
        container = QWidget()
        h_layout = QHBoxLayout(container)
        h_layout.setContentsMargins(0,0,0,0) # Enlève les marges inutiles
        
        # Boîte Min
        spin_min = QDoubleSpinBox()
        spin_min.setRange(min_val, max_val)
        spin_min.setValue(default_min)
        spin_min.setSingleStep(0.05) # Quand on clique sur la flèche, ça monte de 0.05

        # Boîte Max
        spin_max = QDoubleSpinBox()
        spin_max.setRange(min_val, max_val)
        spin_max.setValue(default_max)
        spin_max.setSingleStep(0.05)
        
        # On assemble : "Min:" -> [Boite Min] -> "Max:" -> [Boite Max]
        h_layout.addWidget(QLabel("Min:"))
        h_layout.addWidget(spin_min)
        h_layout.addWidget(QLabel("Max:"))
        h_layout.addWidget(spin_max)
        
        # On ajoute cette ligne au formulaire parent
        layout.addRow(label_text, container)
        
        # On renvoie les deux boîtes pour pouvoir les connecter plus tard
        return spin_min, spin_max

    def switch_graph_mode(self, mode):
        """Fonction appelée quand on clique sur un bouton de graphique"""
        self.current_graph_mode = mode # On mémorise le nouveau mode (ex: "hist")
        self.refresh() # On redessine tout

    def refresh(self):
        """Fonction centrale qui met à jour les données, le tableau et le graphique"""
        
        # --- ETAPE 1 : Récupérer les données filtrées ---
        # On appelle la grosse fonction du DataManager en lui envoyant
        # la valeur actuelle de CHAQUE filtre (texte et nombres).
        df = self.data_manager.filter_data_advanced(
            self.combo_year.currentText(),
            self.combo_region.currentText(),
            self.combo_country.currentText(),
            self.spin_happ_min.value(), self.spin_happ_max.value(),
            self.spin_gdp_min.value(), self.spin_gdp_max.value(),
            self.spin_fam_min.value(), self.spin_fam_max.value(),
            self.spin_health_min.value(), self.spin_health_max.value(),
            self.spin_free_min.value(), self.spin_free_max.value(),
            self.spin_trust_min.value(), self.spin_trust_max.value(),
            self.spin_gen_min.value(), self.spin_gen_max.value()
        )

        # --- ETAPE 2 : Remplir le Tableau ---
        self.table_data.setSortingEnabled(False) # On désactive le tri pendant qu'on remplit (plus rapide)
        self.table_data.clear() # On vide l'ancien tableau
        
        columns = list(df.columns) # On récupère les noms de colonnes du CSV
        self.table_data.setColumnCount(len(columns))
        self.table_data.setHorizontalHeaderLabels(columns) # On met les titres
        self.table_data.setRowCount(len(df)) # On prépare le nombre de lignes
        
        # On boucle sur chaque cellule pour la remplir
        for i in range(len(df)):
            for j, col_name in enumerate(columns):
                val = df.iloc[i][col_name]
                # QTableWidgetItem transforme le texte en "case de tableau"
                self.table_data.setItem(i, j, QTableWidgetItem(str(val)))
        
        self.table_data.setSortingEnabled(True) # On réactive le tri (click sur colonne)

        # --- ETAPE 3 : Dessiner le Graphique ---
        # On regarde quel est le mode actif et on appelle la fonction correspondante
        # dans notre widget graphique, en lui passant les données filtrées (df).
        if self.current_graph_mode == "pie":
            self.graph.plot_pie(df)
        elif self.current_graph_mode == "line":
            self.graph.plot_line(df)
        elif self.current_graph_mode == "hist":
            self.graph.plot_hist(df)