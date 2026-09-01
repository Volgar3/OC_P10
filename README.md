# SoftDesk API

Projet OpenClassrooms n°10 : SoftDesk

L'objectif du projet est de créer une API RESTful (Django REST Framework) permettant de gérer des **projets**, leurs **contributeurs**, des **issues** (tickets) et des **commentaires**, avec une authentification par token JWT.

## Règles de gestion

- Seul **l'auteur d'un projet** peut modifier ou supprimer ce projet.
- Les **contributeurs** d'un projet peuvent créer, modifier et supprimer des issues et des commentaires (les leurs uniquement).
- Seul l'auteur d'un projet peut ajouter des contributeurs à celui-ci.
- Toutes les routes nécessitent d'être authentifié, et un utilisateur ne voit que les projets auxquels il contribue.

## Installation

### Prérequis

- Python 3.12
- [Poetry](https://python-poetry.org/)

### 1. Cloner le projet

```bash
git clone <url-du-repo>
cd softDesk
```

### 2. Installer les dépendances avec Poetry

Le projet utilise **Poetry** plutôt qu'un simple `requirements.txt`. Poetry gère à la fois les dépendances et leurs versions exactes (fichier `poetry.lock`), ce qui garantit que tout le monde travaille avec les mêmes versions de paquets et évite les failles liées à des versions non maîtrisées. Il permet aussi de séparer les dépendances de développement (linters...) de celles nécessaires en production.

```bash
poetry install
```

### 3. Configurer les variables d'environnement

Créer un fichier `.env` à la racine (sur la base de `.env.example`) et y renseigner une clé secrète Django :

```bash
cp .env.example .env
```

```
SECRET_KEY=<votre-clé-secrète>
```

Vous pouvez générer une clé aléatoire avec la commande suivante :

```bash
poetry run python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 4. Appliquer les migrations

```bash
poetry run python manage.py migrate
```

### 5. Lancer le serveur en local

```bash
poetry run python manage.py runserver
```

L'API est alors disponible sur `http://127.0.0.1:8000/`.

## Endpoints

### Authentification

| Méthode | URL | Description |
|---|---|---|
| POST | `/auth/users/` | Créer un compte utilisateur |
| GET / PUT / DELETE | `/auth/users/{id}/` | Consulter / modifier / supprimer son propre compte |
| POST | `/auth/token/` | Se connecter et obtenir un token JWT |
| POST | `/auth/token/refresh/` | Rafraîchir son token JWT |

### Projets

| Méthode | URL | Description |
|---|---|---|
| GET | `/api/project/` | Lister les projets auxquels on contribue |
| POST | `/api/project/` | Créer un projet (l'auteur devient automatiquement contributeur) |
| GET | `/api/project/{id}/` | Détail d'un projet |
| PUT / PATCH | `/api/project/{id}/` | Modifier un projet (auteur uniquement) |
| DELETE | `/api/project/{id}/` | Supprimer un projet (auteur uniquement) |

### Contributeurs

| Méthode | URL | Description |
|---|---|---|
| GET | `/api/contributor/` | Lister les contributeurs |
| GET | `/api/contributor/?project_id={id}` | Lister les contributeurs d'un projet donné |
| POST | `/api/contributor/` | Ajouter un contributeur à un projet (auteur du projet uniquement) |
| DELETE | `/api/contributor/{id}/` | Retirer un contributeur |

### Issues

| Méthode | URL | Description |
|---|---|---|
| GET | `/api/issue/` | Lister les issues des projets auxquels on contribue |
| GET | `/api/issue/?project_id={id}` | Lister les issues d'un projet donné |
| POST | `/api/issue/` | Créer une issue |
| GET | `/api/issue/{id}/` | Détail d'une issue |
| PUT / PATCH | `/api/issue/{id}/` | Modifier une issue (auteur de l'issue uniquement) |
| DELETE | `/api/issue/{id}/` | Supprimer une issue (auteur de l'issue uniquement) |

### Commentaires

| Méthode | URL | Description |
|---|---|---|
| GET | `/api/comment/` | Lister les commentaires |
| GET | `/api/comment/?issue_id={id}` | Lister les commentaires d'une issue donnée |
| POST | `/api/comment/` | Créer un commentaire |
| GET | `/api/comment/{id}/` | Détail d'un commentaire |
| PUT / PATCH | `/api/comment/{id}/` | Modifier un commentaire (auteur du commentaire uniquement) |
| DELETE | `/api/comment/{id}/` | Supprimer un commentaire (auteur du commentaire uniquement) |
