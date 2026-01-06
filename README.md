# 🌍 Happiness Index Analyzer

**Happiness Index Analyzer** est une application de bureau interactive développée en Python. Elle permet d'explorer, de filtrer et de visualiser les données mondiales du bonheur (World Happiness Report) sur plusieurs années.

L'application combine la puissance de **Pandas** pour le traitement des données, **PyQt6** pour l'interface graphique et **Matplotlib** pour la génération de graphiques dynamiques.

## 🚀 Fonctionnalités Principales

L'application est divisée en deux onglets majeurs pour répondre à différents besoins d'analyse :

### 1. Onglet Exploration (Un Pays)
Cet onglet est dédié à l'analyse détaillée et au filtrage précis des données.
* **Filtres Avancés :** Filtrage par Région, Pays, et bornes numériques (sliders) pour tous les indicateurs (Score de bonheur, PIB, Famille, Espérance de vie, etc.).
* **Visualisation de Données :**
    * **Tableau interactif :** Affiche les données brutes filtrées.
    * **Graphiques :** Diagrammes circulaires (Répartition par région) et Histogrammes (Distribution des scores).
* **Indicateurs dynamiques :** Mise à jour en temps réel des graphiques selon les filtres actifs.

### 2. Onglet Comparaison
Cet onglet permet de croiser les données pour identifier des tendances ou des corrélations.
* **Nuage de points (Scatter Plot) :** Permet de visualiser la corrélation entre deux variables au choix (ex: *PIB* vs *Score de Bonheur*).
* **Évolution Temporelle (Line Chart) :** Trace l'évolution d'une métrique spécifique au fil des années pour un ou plusieurs pays sélectionnés simultanément.
* **Sélection multiple :** Choisissez plusieurs pays dans une liste pour comparer leurs trajectoires.

## 🛠️ Technologies Utilisées

* **Python 3.x**
* **PyQt6** : Gestion de l'interface utilisateur (Fenêtres, Onglets, Widgets).
* **Pandas** : Chargement, nettoyage et manipulation du fichier CSV (`happiness.csv`).
* **Matplotlib** : Moteur de rendu graphique intégré dans l'interface Qt.

## 📂 Structure du Projet

Voici une brève description des fichiers source :

* `main.py` : Point d'entrée de l'application. Initialise la fenêtre principale et charge les onglets.
* `data_manager.py` : Gère le chargement du fichier CSV, le nettoyage des colonnes et la logique de filtrage des données.
* `happiness.csv` : Le jeu de données source (délimiteur `;`).
* **Interface (UI)**
    * `tab_country.py` : Logique et mise en page de l'onglet "Exploration".
    * `tab_comparison.py` : Logique et mise en page de l'onglet "Comparaison".
* **Graphiques**
    * `graph_base.py` : Classe mère configurant le canevas Matplotlib pour PyQt.
    * `graph_country.py` : Gère les graphiques de l'onglet Exploration (Pie, Hist).
    * `graph_compare.py` : Gère les graphiques de l'onglet Comparaison (Scatter, Line).

## ⚙️ Installation et Lancement

### 1. Prérequis
Assurez-vous d'avoir Python installé sur votre machine. Installez ensuite les dépendances nécessaires via pip :

```bash
pip install PyQt6 pandas matplotlib
