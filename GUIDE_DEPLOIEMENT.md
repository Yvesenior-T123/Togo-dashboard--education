# 🚀 GUIDE DE DÉPLOIEMENT COMPLET

Ce guide explique comment déployer le dashboard sur **Render** (Option B) et **Streamlit Cloud** (Option A).

---

## OPTION B — RENDER (Recommandé pour ce challenge)

### ÉTAPE 1 : Créer un repository GitHub

1. Va sur [github.com](https://github.com) et connecte-toi
2. Clique sur le bouton vert **"New"** (ou "+") en haut à droite → **"New repository"**
3. Remplis les champs :
   - **Repository name** : `togo-education-dashboard`
   - **Description** : `Dashboard Togo Data AI - Education Defi 2`
   - **Public** ✅ (cocher)
   - **Add a README file** ❌ (décocher, on en a déjà un)
4. Clique sur **"Create repository"**

### ÉTAPE 2 : Uploader les fichiers sur GitHub

**Méthode A — Interface web (la plus simple pour débutant)**

1. Sur la page de ton repo, clique sur **"Add file"** → **"Upload files"**
2. Glisse-dépose TOUS les fichiers du dossier `togo_education_dashboard/` :
   - `app.py`
   - `requirements.txt`
   - `Dockerfile`
   - `render.yaml`
   - `README.md`
   - `.gitignore`
   - Le dossier `data/` (avec tous les CSV)
3. En bas, écris un message de commit : `Initial commit - Dashboard Togo Education`
4. Clique sur **"Commit changes"**

**Méthode B — Ligne de commande (plus pro)**

```bash
# Se placer dans le dossier du projet
cd togo_education_dashboard

# Initialiser Git
git init

# Ajouter tous les fichiers
git add .

# Commit
git commit -m "Initial commit - Dashboard Togo Education Defi 2"

# Connecter au repo GitHub (remplace TON_USERNAME)
git remote add origin https://github.com/TON_USERNAME/togo-education-dashboard.git

# Pousser les fichiers
git branch -M main
git push -u origin main
```

### ÉTAPE 3 : Déployer sur Render

1. Va sur [render.com](https://render.com) et crée un compte (gratuit)
2. Clique sur **"New +"** → **"Web Service"**
3. Connecte ton compte **GitHub**
4. Sélectionne le repository `togo-education-dashboard`
5. Remplis les champs :
   - **Name** : `togo-education-dashboard`
   - **Runtime** : **Docker** (sélectionner dans le menu déroulant)
   - **Branch** : `main`
   - **Dockerfile Path** : `./Dockerfile`
   - **Plan** : `Free`
6. Clique sur **"Create Web Service"**
7. Render va automatiquement :
   - Builder l'image Docker
   - Installer les dépendances
   - Lancer l'application sur le port 8501
8. Attends 2-3 minutes... et c'est en ligne ! 🎉

**URL finale** : `https://togo-education-dashboard.onrender.com`

---

## OPTION A — STREAMLIT CLOUD (Plus simple encore)

### ÉTAPE 1 : Pousser sur GitHub

Faire les étapes 1 et 2 ci-dessus (créer le repo + uploader les fichiers).

### ÉTAPE 2 : Déployer sur Streamlit Cloud

1. Va sur [share.streamlit.io](https://share.streamlit.io)
2. Connecte-toi avec ton compte **GitHub**
3. Clique sur **"New app"**
4. Sélectionne :
   - **Repository** : `TON_USERNAME/togo-education-dashboard`
   - **Branch** : `main`
   - **Main file path** : `app.py`
5. Clique sur **"Deploy"**
6. Attends 1-2 minutes... le dashboard est en ligne ! 🎉

**URL finale** : `https://ton-username-togo-education-dashboard.streamlit.app`

---

## 🔧 Dépannage

| Problème | Solution |
|----------|----------|
| "Module not found" | Vérifier que `requirements.txt` contient bien toutes les dépendances |
| "Port already in use" | Vérifier que le Dockerfile expose le port 8501 |
| "File not found" | Vérifier que le dossier `data/` est bien poussé sur GitHub |
| Render ne démarre pas | Vérifier que `render.yaml` est présent à la racine |

---

## 📧 Support

Si tu bloques, vérifie les logs sur Render/Streamlit Cloud. Le message d'erreur t'indiquera exactement ce qui ne va pas.
