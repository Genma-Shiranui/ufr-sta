#  Guide GitHub — Travail collaboratif
## Projet UFR STA

---

## 1. Mise en place du dépôt (à faire une seule fois)

### Le chef de groupe crée le dépôt

1. Aller sur [github.com](https://github.com) → **New repository**
2. Nom du dépôt : `ufr-sta`
3. Visibilité : **Public** (ou Private)
4. Ne pas initialiser avec README (on a déjà le nôtre)
5. Cliquer **Create repository**

### Initialiser le projet en local et pousser

```bash
cd ufr-sta
git init
git add .
git commit -m "Initial commit : structure complète du projet UFR STA"
git branch -M main
git remote add origin https://github.com/<votre-username>/ufr-sta.git
git push -u origin main
```

### Inviter les coéquipiers

1. Aller dans **Settings** → **Collaborators** → **Add people**
2. Entrer le nom GitHub de chaque membre
3. Chaque membre accepte l'invitation reçue par email

---

## 2. Chaque membre clone le projet

```bash
git clone https://github.com/<chef-de-groupe>/ufr-sta.git
cd ufr-sta
python -m venv venv
source venv/bin/activate
pip install flask
python app.py
```

---

## 3. Workflow quotidien (à suivre à chaque session)

### Avant de commencer à coder — toujours synchroniser

```bash
git checkout main
git pull origin main
```

### Créer une branche pour sa fonctionnalité

```bash
# Exemples de noms de branches
git checkout -b feature/page-enseignants
git checkout -b feature/module-galerie
git checkout -b fix/navbar-mobile
git checkout -b style/responsive-contact
```

### Coder, puis sauvegarder régulièrement

```bash
# Voir ce qui a changé
git status

# Ajouter les fichiers modifiés
git add templates/enseignants.html
git add static/css/style.css

# Ou tout ajouter d'un coup
git add .

# Faire un commit avec un message clair
git commit -m "feat: ajouter page enseignants avec grille responsive"
git commit -m "fix: corriger alignement navbar sur mobile"
git commit -m "style: améliorer couleurs section héro"
```

### Pousser sa branche sur GitHub

```bash
git push origin feature/page-enseignants
```

### Créer une Pull Request sur GitHub

1. Aller sur le dépôt GitHub
2. Cliquer **Compare & pull request**
3. Décrire les changements effectués
4. Assigner un coéquipier pour relire
5. Cliquer **Create pull request**

### Fusionner dans main (après validation)

```bash
git checkout main
git merge feature/page-enseignants
git push origin main
```

---

## 4. Résoudre un conflit de fusion

Quand deux personnes modifient le même fichier :

```bash
# Git signale un conflit
git merge feature/ma-branche
# CONFLICT (content): Merge conflict in templates/base.html

# Ouvrir le fichier — chercher les marqueurs
<<<<<<< HEAD
  <-- code de main -->
=======
  <-- code de ta branche -->
>>>>>>> feature/ma-branche

# Choisir quelle version garder, supprimer les marqueurs
# Puis finaliser
git add templates/base.html
git commit -m "merge: résoudre conflit navbar base.html"
```

---

## 5. Bonnes pratiques des messages de commit

| Préfixe | Usage | Exemple |
|---------|-------|---------|
| `feat:` | Nouvelle fonctionnalité | `feat: ajouter formulaire contact` |
| `fix:` | Correction de bug | `fix: corriger route admin logout` |
| `style:` | CSS / design | `style: responsive galerie mobile` |
| `refactor:` | Restructuration | `refactor: extraire helper get_db` |
| `docs:` | Documentation | `docs: mettre à jour README` |
| `chore:` | Divers | `chore: ajouter .gitignore` |

---

## 6. Commandes utiles à retenir

```bash
git status              # État du dépôt local
git log --oneline       # Historique des commits
git diff                # Voir les modifications non commitées
git branch              # Lister les branches
git branch -a           # Toutes les branches (local + remote)
git stash               # Mettre de côté des modifications en cours
git stash pop           # Récupérer les modifications mises de côté
git pull origin main    # Récupérer les dernières mises à jour
```

---

## 7. Ce que l'examinateur vérifiera

- ✅ Historique de commits **réguliers** de chaque membre
- ✅ Utilisation de **branches** pour les fonctionnalités
- ✅ Messages de commits **explicites**
- ✅ Pull Requests documentées
- ✅ Pas de gros commit unique à la dernière minute

---

*Bonne collaboration ! *
