import sys  
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget, QMessageBox
from data_manager import DataManager

# --- IMPORT DES ONGLETS PERSONNALISÉS ---
from tab_country import CountryTab
from tab_comparison import ComparisonTab
from tab_map_interactive import MapTabInteractive

class MainWindow(QMainWindow):
    """
    Fenêtre Principale de l'application (Le cadre global).
    Elle hérite de QMainWindow, ce qui lui donne accès aux fonctionnalités de base 
    d'une fenêtre (titre, redimensionnement, barre de statut, etc.).
    """
    def __init__(self):
        super().__init__()
        
        # --- CONFIGURATION DE LA FENÊTRE ---
        self.setWindowTitle("Happiness Index Analyzer - Projet Supop")  # Titre affiché dans la barre supérieure
        self.resize(1400, 900)  # Taille initiale de la fenêtre 

        # 1. Chargement des données (CENTRALISÉ)
        self.data_manager = DataManager()
        
        # Sécurité : Vérifier si le chargement a réussi
        if self.data_manager.df.empty:
            QMessageBox.critical(self, "Erreur", "Impossible de charger les données happiness.csv")

        # 2. Création du conteneur d'onglets
        self.tabs = QTabWidget()
        
        self.setCentralWidget(self.tabs)
        
        # 3. Instanciation des onglets 
        self.tab_country = CountryTab(self.data_manager)
        self.tab_comparison = ComparisonTab(self.data_manager)
        self.tab_map = MapTabInteractive(self.data_manager)

        # 4. Ajout visuel des onglets dans la fenêtre
        self.tabs.addTab(self.tab_country, "Vue d'ensemble")
        self.tabs.addTab(self.tab_comparison, "Comparaison")
        self.tabs.addTab(self.tab_map, "Carte")

if __name__ == "__main__":
    # 1. Création de l'application PyQt
    app = QApplication(sys.argv)
    
    # 2. Création de l'objet fenêtre 
    window = MainWindow()
    
    # 3. Rendre la fenêtre visible à l'écran
    window.show()
    
    # 4. Lancement de la "Boucle d'événements" (Event Loop)
    sys.exit(app.exec())