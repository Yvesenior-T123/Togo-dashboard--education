# 🇹🇬 Adéquation Formation-Emploi au Togo

> **Challenge DataLab Togo — Éducation Défi 2**  
> Tableau de bord interactif mesurant l'alignement entre l'offre de formation, le financement public et l'insertion professionnelle.

---

## 🚀 Démo en ligne

🔗 **[Voir le dashboard en direct](TON_URL_ICI)** *(à remplacer après déploiement)*

---

## 📊 Fonctionnalités

| Onglet | Description |
|--------|-------------|
| 🗺️ **Cartographie** | Carte interactive des 200+ établissements de formation technique géolocalisés |
| 🎓 **Indicateurs Clés** | Effectifs, féminisation (51,5%), filières STEM (23,62%), ratio étudiant/enseignant (91:1) |
| 💰 **Budget & Dépenses** | Budget voté vs exécuté, dépenses par étudiant, part du PIB |
| 🏛️ **Établissements** | Répartition par ville, type et statut (public/privé) |
| 💼 **Chômage & Emploi** | Taux de chômage des diplômés, corrélation inscription/chômage |
| 💡 **Recommandations** | 7 recommandations stratégiques chiffrées avec matrice d'impact |
| 🔮 **Simulateur** | *Fonctionnalité exclusive* — ajustez les leviers et voyez l'impact prédictif sur 2030 |

---

## 🎯 Fonctionnalités différenciantes

- 🚨 **Alertes automatiques** : Détection des anomalies (ratio critique, chômage élevé, sous-exécution budgétaire)
- 🔮 **Simulateur de scénarios** : Modèle prédictif interactif pour 2030
- 📈 **Corrélations** : Analyse budget vs chômage, inscription vs insertion

---

## 📁 Structure du projet

```
.
├── app.py                          # Application Streamlit principale
├── requirements.txt                # Dépendances Python
├── Dockerfile                      # Conteneurisation Docker
├── render.yaml                     # Configuration Render
├── README.md                       # Ce fichier
└── data/
    ├── formations_techniques_clean.csv
    ├── indicateurs_cles_wide.csv
    ├── budget_wide.csv
    ├── repartition_etablissements_clean.csv
    ├── chomage_clean.csv
    ├── depenses_clean.csv
    └── inscriptions_clean.csv
```

---

## 🛠️ Installation locale

```bash
# 1. Cloner le repo
git clone https://github.com/TON_USERNAME/togo-education-dashboard.git
cd togo-education-dashboard

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Lancer l'application
streamlit run app.py
```

L'application sera accessible sur `http://localhost:8501`

---

## 🐳 Docker

```bash
# Construire l'image
docker build -t togo-education-dashboard .

# Lancer le conteneur
docker run -p 8501:8501 togo-education-dashboard
```

---

## ☁️ Déploiement

### Option 1 — Streamlit Cloud (Recommandé)
1. Connecter le repo sur [share.streamlit.io](https://share.streamlit.io)
2. Sélectionner `app.py`
3. Déployer

### Option 2 — Render
1. Connecter le repo sur [render.com](https://render.com)
2. Créer un Web Service avec Docker
3. Déployer automatiquement

---

## 📊 Données utilisées

Toutes les données proviennent de la plateforme **DataLab Togo** :
- Établissements de formations techniques
- Indicateurs clés de l'enseignement supérieur
- Budget de l'enseignement supérieur
- Répartition des établissements par type/statut/localisation
- Inscriptions scolaires dans l'enseignement supérieur
- Dépenses publiques par étudiant
- Chômage des diplômés de l'enseignement supérieur

---

## 🏆 Challenge

**Togo Data AI Lab — Challenge Éducation — Défi 2**  
*Construire un tableau de bord mesurant l'adéquation formation-emploi au Togo*

---

## 👤 Auteur

**[VOTRE NOM]**  
Participant au Challenge Togo Data AI Lab

---

## 📄 Licence

Projet réalisé dans le cadre du Challenge DataLab Togo — Éducation Défi 2.
