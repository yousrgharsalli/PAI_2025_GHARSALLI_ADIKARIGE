from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QComboBox, QGroupBox, QFormLayout, QListWidget, 
                             QAbstractItemView, QPushButton)
from PyQt6.QtCore import Qt
from graph_compare import CompareGraph

class ComparisonTab(QWidget):
    """
    Onglet principal de comparaison.
    Il contient un panneau de contrôle à gauche (filtres) et le graphique à droite.
    Il fait le lien entre les choix de l'utilisateur et l'affichage graphique.
    """
    def __init__(self, data_manager):
        super().__init__()
        # On stocke le gestionnaire de données pour pouvoir accéder au DataFrame plus tard
        self.data_manager = data_manager
        
        # Liste des colonnes numériques disponibles pour l'analyse
        # (Sert à remplir les menus déroulants Axe X et Axe Y)
        self.numeric_cols = [
            "Happiness Score", "Economy (GDP per Capita)", "Family", 
            "Health (Life Expectancy)", "Freedom", 
            "Trust (Government Corruption)", "Generosity"
        ]

        # Disposition horizontale principale : [ Panneau Gauche | Graphique Droite ]
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        
        # Construction de l'interface
        self.setup_ui()
        
        # Initialisation de l'état des widgets (cacher/montrer selon le type par défaut)
        self.update_inputs_visibility()
        # Premier affichage du graphique (souvent vide au début)
        self.refresh()

    def setup_ui(self):
        """Construction de tous les éléments visuels de l'onglet"""
        
        # --- COLONNE GAUCHE : PARAMÈTRES ---
        # QGroupBox crée un cadre avec un titre autour des options
        self.panel_left = QGroupBox("Paramètres")
        self.panel_left.setFixedWidth(320) # Largeur fixe pour que le graphe ait de la place
        left_layout = QVBoxLayout(self.panel_left)

        # 1. Type de Graphique
        left_layout.addWidget(QLabel("<b>Type de Graphique :</b>"))
        self.combo_type = QComboBox()
        self.combo_type.addItems([
            "1. Nuage de Points (Corrélation)", 
            "2. Diagramme en Barres (Comparaison)", 
            "3. Courbes d'évolution (Temporel)"
        ])
        # Connexion : Quand on change le type, on lance 'on_type_changed'
        self.combo_type.currentIndexChanged.connect(self.on_type_changed)
        left_layout.addWidget(self.combo_type)
        
        left_layout.addSpacing(10) # Petit espace vide pour aérer

        # 2. Formulaire (Année / Axes)
        # QFormLayout aligne proprement "Libellé : Widget"
        self.form_layout = QFormLayout()
        
        # Choix de l'année
        self.combo_year = QComboBox()
        self.combo_year.addItems(self.data_manager.get_all_years())
        self.combo_year.currentTextChanged.connect(self.refresh) # Rafraîchir dès changement
        self.form_layout.addRow("Année :", self.combo_year)

        # Choix de l'Axe X (ou de la métrique principale pour les barres)
        self.combo_x = QComboBox()
        self.combo_x.addItems(self.numeric_cols)
        self.combo_x.currentTextChanged.connect(self.refresh)
        self.form_layout.addRow("Axe X / Indicateur :", self.combo_x)

        # Choix de l'Axe Y (utile uniquement pour le Scatter plot)
        self.combo_y = QComboBox()
        self.combo_y.addItems(self.numeric_cols)
        # Par défaut, on sélectionne le 2ème item pour ne pas avoir X=Happiness et Y=Happiness
        if len(self.numeric_cols) > 1: self.combo_y.setCurrentIndex(1)
        self.combo_y.currentTextChanged.connect(self.refresh)
        
        self.lbl_y = QLabel("Axe Y :") # On garde une référence pour pouvoir le cacher
        self.form_layout.addRow(self.lbl_y, self.combo_y)

        left_layout.addLayout(self.form_layout)
        left_layout.addSpacing(10)

        # --- BOUTONS DE SÉLECTION RAPIDE ---
        buttons_layout = QHBoxLayout()
        
        self.btn_select_all = QPushButton("✅ Tout sélectionner")
        self.btn_select_all.clicked.connect(self.select_all_global)
        
        self.btn_reset = QPushButton("🗑️ Tout désélectionner")
        self.btn_reset.clicked.connect(self.reset_selection)
        
        buttons_layout.addWidget(self.btn_select_all)
        buttons_layout.addWidget(self.btn_reset)
        left_layout.addLayout(buttons_layout)
        
        left_layout.addSpacing(5)

        # --- LISTE 1 : RÉGIONS (Filtre parent) ---
        left_layout.addWidget(QLabel("<b>1. Filtrer par Régions (Ctrl+Clic) :</b>"))
        self.list_regions = QListWidget()
        # ExtendedSelection permet de sélectionner plusieurs lignes avec Ctrl ou Shift
        self.list_regions.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.list_regions.setFixedHeight(100)
        self.list_regions.addItems(self.data_manager.get_all_regions())
        
        # Quand on clique sur une région, on met à jour la liste des pays (cascade)
        self.list_regions.itemSelectionChanged.connect(self.apply_region_filter)
        left_layout.addWidget(self.list_regions)

        # --- LISTE 2 : PAYS (Sélection finale) ---
        left_layout.addWidget(QLabel("<b>2. Pays sélectionnés (Ctrl+Clic) :</b>"))
        self.list_countries = QListWidget()
        self.list_countries.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.list_countries.addItems(self.data_manager.get_all_countries())
        
        # Quand on change les pays, on redessine le graphique
        self.list_countries.itemSelectionChanged.connect(self.refresh)
        left_layout.addWidget(self.list_countries)

        # Ajout du panneau gauche au layout principal
        self.layout.addWidget(self.panel_left)

        # --- COLONNE DROITE : GRAPHIQUE ---
        # Instance de notre classe personnalisée (voir fichier graph_compare.py)
        self.graph = CompareGraph()
        self.layout.addWidget(self.graph)

    # --- LOGIQUE MÉTIER ---

    def select_all_global(self):
        """Sélectionne tous les pays directement sans passer par les régions"""
        # .blockSignals(True) est CRUCIAL ici :
        # Cela empêche la liste d'envoyer un signal "J'ai changé" à chaque ligne qu'on coche.
        # Sans ça, l'appli calculerait le graphique 150 fois de suite et gèlerait.
        self.list_countries.blockSignals(True)
        
        # Optionnel : On vide la sélection région pour éviter la confusion visuelle
        self.list_regions.clearSelection() 
        
        # On parcourt toute la liste et on coche tout
        for i in range(self.list_countries.count()):
            self.list_countries.item(i).setSelected(True)
            
        # On réactive les signaux
        self.list_countries.blockSignals(False)
        # On lance un seul rafraîchissement manuel à la fin
        self.refresh()

    def reset_selection(self):
        """Vide les deux listes (Régions et Pays)"""
        self.list_regions.blockSignals(True)
        self.list_countries.blockSignals(True)
        
        self.list_regions.clearSelection()
        self.list_countries.clearSelection()
        
        self.list_regions.blockSignals(False)
        self.list_countries.blockSignals(False)
        self.refresh()

    def apply_region_filter(self):
        """
        Logique de CASCADE : Région -> Pays.
        Cette fonction est appelée quand l'utilisateur clique sur une région.
        Elle coche automatiquement tous les pays appartenant aux régions sélectionnées.
        """
        # 1. On récupère les noms des régions sélectionnées (ex: ['Western Europe', 'North America'])
        selected_region_items = self.list_regions.selectedItems()
        selected_region_names = [i.text() for i in selected_region_items]

        # 2. Accès aux données brutes
        df = self.data_manager.df
        if df.empty: return

        # Cas particulier : Si l'utilisateur décoche tout, on décoche aussi tous les pays
        if not selected_region_names:
            self.list_countries.clearSelection()
            self.refresh()
            return

        # 3. Filtrage des données pour trouver quels pays correspondent à ces régions
        # .isin() vérifie si la région de la ligne est dans notre liste
        target_countries = df[df['Region'].isin(selected_region_names)]['Country'].unique()

        # 4. Mise à jour visuelle de la liste des pays
        self.list_countries.blockSignals(True) # On bloque pour éviter 100 refreshes
        
        for i in range(self.list_countries.count()):
            item = self.list_countries.item(i)
            
            # Si le nom du pays est dans notre liste cible -> On coche
            if item.text() in target_countries:
                item.setSelected(True)
            # Sinon -> On décoche (pour enlever les pays des régions qu'on vient de désélectionner)
            else:
                item.setSelected(False)
        
        self.list_countries.blockSignals(False)
        self.refresh()

    def on_type_changed(self):
        """Gère le changement de type de graphique (Scatter vs Bar vs Curve)"""
        self.update_inputs_visibility() # Masque/Affiche les options inutiles
        self.refresh() # Redessine le graphe

    def update_inputs_visibility(self):
        """
        Adapte l'interface selon le graphique choisi pour ne pas embrouiller l'utilisateur.
        Ex: Pas besoin d'Axe Y pour un diagramme en barres.
        Ex: Pas besoin de choisir une année précise pour une courbe d'évolution temporelle.
        """
        mode = self.combo_type.currentIndex() 
        
        # Mode 0 : Scatter Plot (Besoin de X et Y)
        if mode == 0: 
            self.combo_y.show()
            self.lbl_y.show()
        # Mode 1 et 2 : Bar et Courbes (Besoin que de X)
        else:
            self.combo_y.hide()
            self.lbl_y.hide()

        # Mode 2 : Courbes d'évolution (Temporel)
        if mode == 2: 
            # On désactive le choix de l'année car on veut voir TOUTES les années
            self.combo_year.setDisabled(True)
        else:
            self.combo_year.setDisabled(False)

    def refresh(self):
        """
        C'est le CERVEAU de l'onglet.
        1. Récupère toutes les valeurs du formulaire.
        2. Filtre le DataFrame.
        3. Envoie les données filtrées au widget Graphique pour dessin.
        """
        # 1. Récupération des entrées utilisateur
        mode = self.combo_type.currentIndex()
        year = self.combo_year.currentText()
        col_x = self.combo_x.currentText()
        col_y = self.combo_y.currentText()

        # Récupération des pays cochés dans la liste
        selected_items = self.list_countries.selectedItems()
        selected_countries = [item.text() for item in selected_items]

        # 2. Filtrage des données
        # On travaille sur une copie pour ne pas casser l'original
        df = self.data_manager.df.copy()

        # Filtre Pays
        if selected_countries:
            df = df[df['Country'].isin(selected_countries)]
        else:
            # Si aucun pays n'est sélectionné, on vide le tableau pour afficher "Pas de données"
            df = df.iloc[0:0] 

        # Filtre Année (Sauf pour le mode 2 "Courbes" qui a besoin de l'historique complet)
        if mode != 2: 
            df = df[df['Year'] == year]

        # 3. Appel de la bonne fonction de dessin dans CompareGraph
        if mode == 0:
            self.graph.plot_scatter(df, col_x, col_y)
        elif mode == 1:
            self.graph.plot_bar(df, col_x)
        elif mode == 2:
            self.graph.plot_multi_curves(df, col_x)