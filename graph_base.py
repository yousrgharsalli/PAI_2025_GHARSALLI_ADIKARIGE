import sys
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
# Import du "backend" spécifique qui permet à Matplotlib de s'afficher DANS une fenêtre Qt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

class GraphBase(QWidget):
    """
    Classe de base pour tous les widgets graphiques.
    Elle prépare le terrain (la toile vide) où les courbes et barres seront dessinées.
    Elle hérite de QWidget pour pouvoir être intégrée dans l'interface PyQt.
    """
    def __init__(self):
        super().__init__()
        
        # --- GESTION DU REDIMENSIONNEMENT ---
        # Définit la politique de taille du widget sur "Expanding".
        # Cela signifie que le graphique essaiera de prendre toute la place disponible
        # dans la fenêtre si on l'agrandit.
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        # --- MISE EN PAGE (LAYOUT) ---
        # On utilise un layout vertical. Même s'il n'y a qu'un seul élément (le graphe),
        # le layout est nécessaire pour que le graphe se redimensionne avec la fenêtre.
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        # --- INITIALISATION DE MATPLOTLIB ---
        # 1. Création de la Figure : C'est le conteneur global (la feuille de papier blanche).
        # figsize=(10, 5) : Taille par défaut en pouces (largeur, hauteur).
        # dpi=100 : Résolution (points par pouce).
        self.figure = Figure(figsize=(10, 5), dpi=100)
        
        # 2. Création du Canvas : C'est le "pont" entre Matplotlib et PyQt.
        # Le Canvas transforme la Figure Matplotlib en un Widget PyQt affichable.
        self.canvas = FigureCanvas(self.figure)
        
        # 3. Ajout du Canvas dans le layout de notre widget pour qu'il soit visible.
        self.layout.addWidget(self.canvas)
        
        # --- CRÉATION DES AXES ---
        # add_subplot(111) signifie :
        # - 1ère grille verticale
        # - 1ère grille horizontale
        # - 1er graphique (index)
        # C'est l'objet 'self.ax' qui servira à tracer les courbes (plot, bar, scatter...).
        self.ax = self.figure.add_subplot(111)

    def clear_ax(self):
        """
        Nettoie le graphique pour le prochain tracé.
        Indispensable avant de redessiner un graphe quand on change de filtre,
        sinon les anciens dessins restent en fond et tout se superpose.
        """
        self.ax.clear()