# King County Real Estate Lab

Application Streamlit d'analyse immobiliere construite autour du dataset `kc_house_data.csv` afin d'explorer le marche du comte de King (region de Seattle, WA), evaluer des proprietes individuelles et generer des syntheses textuelles avec Gemini.

## Objectif du projet

Ce projet a ete realise dans une logique de "vibe coding" et de developpement assiste par IA pour repondre a un besoin metier simple:

- explorer rapidement un jeu de donnees immobilier reel
- identifier des tendances de marche par zone et par typologie de biens
- comparer une propriete cible a des transactions similaires
- produire une courte note d'investissement a l'aide d'un LLM

## Fonctionnalites

- Dashboard d'accueil avec KPI du marche
- Exploration interactive du marche avec filtres
- Visualisations financieres avec `matplotlib`
- Analyse d'une propriete existante ou saisie manuellement
- Selection automatique de comparables
- Estimation simple de valorisation
- Generation de syntheses texte avec Gemini

## Dataset

Le projet utilise `kc_house_data.csv`, un historique de **21 613 transactions** immobilieres avec notamment:

- prix
- date de vente
- nombre de chambres et salles de bain
- surface habitable et terrain
- grade et condition
- annee de construction et renovation
- code postal
- latitude / longitude

Le fichier `dictionnaire_variables (1).txt` fournit la description des variables.

## Stack technique

- Python
- Streamlit
- pandas
- matplotlib
- google-genai
- python-dotenv

## Structure du projet

```text
quiz4-analyseur-immobilier/
|-- app.py
|-- pages/
|   |-- home.py
|   |-- market.py
|   |-- property_analysis.py
|   `-- ai_assistant.py
|-- src/
|   |-- data.py
|   |-- charts.py
|   |-- comparables.py
|   |-- metrics.py
|   |-- llm.py
|   `-- ui.py
|-- kc_house_data.csv
|-- gemini_demo.py
`-- requirements.txt
```

## Installation

1. Cloner le depot
2. Installer les dependances

```bash
python -m pip install -r requirements.txt
```

3. Creer un fichier `.env` a la racine du projet

```env
GOOGLE_API_KEY=VOTRE_CLE_API
GEMINI_MODEL=gemini-3.1-flash-lite-preview
```

`GEMINI_MODEL` est optionnelle et peut etre remplacee par un autre modele compatible.

## Lancer l'application

```bash
python -m streamlit run app.py
```

Une fois l'application demarree, Streamlit ouvre une interface locale dans le navigateur.

## Pages de l'application

### 1. Accueil

- vue d'ensemble du dataset
- KPI principaux
- top codes postaux
- premiere lecture visuelle du marche

### 2. Marche

- filtres par prix, surface, chambres, grade, condition, annee, waterfront, renovation
- distributions de prix
- prix par code postal
- transactions dans le temps
- carte geographique des ventes

### 3. Propriete

- selection d'un bien du dataset
- ou saisie manuelle d'une opportunite
- recherche de comparables
- estimation simple de valorisation
- lecture rapide de sous-valorisation / survalorisation

### 4. Assistant IA

- synthese du marche filtre
- note de propriete basee sur les comparables
- prompts ancres sur des statistiques calculees avec `pandas`

## Exemple de script Gemini

Un script de test est disponible dans `gemini_demo.py`:

```bash
python gemini_demo.py
```

## Points pedagogiques couverts

- manipulation d'un jeu de donnees reel avec `pandas`
- calcul d'indicateurs de marche
- creation de visualisations avec `matplotlib`
- construction d'une application interactive avec `Streamlit`
- integration d'un LLM pour generer des analyses textuelles

## Ameliorations possibles

- ajout d'un modele de prediction de prix
- export PDF ou CSV des analyses
- ajout d'une carte interactive type `pydeck` ou `plotly`
- gestion plus fine des comparables avec filtres geographiques
- suivi de plusieurs proprietes dans une watchlist

## Auteur

Projet realise par Audrey Lapointe dans le cadre d'un exercice d'analyse immobiliere et d'integration IA.
