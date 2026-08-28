# SoftDesk — Suivi d'avancement vs cahier des charges

Dernière mise à jour : 2026-07-24 — recalé sur le PDF officiel « Exigences de
sécurité et d'optimisation » fourni par Hugo (citations exactes ci-dessous),
après une première version qui s'appuyait sur le brief standard OpenClassrooms.

## Vue d'ensemble

Le cœur fonctionnel est solide : JWT, modèles avec auteur, permissions par
contributeur, RGPD (âge, consentement). Mais la relecture du PDF fait remonter
un **vrai bug de permission** (priorité absolue ci-dessous) : la règle
« seul l'auteur d'une issue/d'un commentaire peut le modifier ou le
supprimer » n'est pas celle réellement appliquée dans le code. Pagination et
gestion des dépendances (Pipenv/Poetry) sont, elles, des exigences explicites
et encore non traitées.

## Ce qui est fait

### Authentification & utilisateurs
- JWT opérationnel via `djangorestframework_simplejwt` : [config/settings.py:126](config/settings.py#L126) et routes `token/`, `token/refresh/` dans [authentication/urls.py:12-13](authentication/urls.py#L12-L13). Couvre l'exigence « Authentification : utilisez JWT... » du PDF.
- Modèle `User` personnalisé avec les champs RGPD : [authentication/models.py](authentication/models.py) — `age`, `can_be_contacted`, `can_data_be_shared`.
- Vérification de l'âge (15 ans, cf. PDF « l'âge légal pour donner son consentement seul est de 15 ans ») en double : `clean()` modèle + `validate_age()` serializer : [authentication/serializers.py:22-27](authentication/serializers.py#L22-L27).
- Mot de passe haché (`set_password`) à la création et à la mise à jour : [authentication/serializers.py:29-42](authentication/serializers.py#L29-L42).
- Inscription ouverte (`AllowAny`), tout le reste protégé (`IsAuthenticated`) : [authentication/viewsets.py:12-15](authentication/viewsets.py#L12-L15) — couvre « seuls les utilisateurs authentifiés doivent être en mesure d'accéder à quoi que ce soit ».
- `IsSelfOrReadOnly` : seul le propriétaire du compte peut le modifier — couvre le droit d'accès/rectification RGPD : [authentication/permissions.py](authentication/permissions.py).

### Projets, contributeurs, issues, commentaires
- Quatre `ModelViewSet` complets, branchés au routeur : [softdesk/viewsets.py](softdesk/viewsets.py), [softdesk/urls.py](softdesk/urls.py).
- `get_queryset` restreint chaque ressource aux projets dont l'utilisateur est contributeur — couvre « un utilisateur ne doit pas être autorisé à accéder à un projet pour lequel il n'est pas ajouté en tant que contributeur ».
- Chaque modèle porte bien une clé étrangère `author` (Project, Issue, Comment) — couvre « ajouter des autorisations à vos modèles en spécifiant l'auteur ».
- Filtres par requête `?project_id=` / `?issue_id=`, création auto de l'auteur + premier contributeur à la création d'un projet.

### RGPD
- Consentement (`can_be_contacted`, `can_data_be_shared`) et âge minimum : faits.
- Accès/rectification du profil : faits (`UserViewSet` + `IsSelfOrReadOnly`).

## ✅ Fait depuis la dernière relecture

- **Bug de permission Issue/Comment corrigé** : [softdesk/permissions.py:41-56](softdesk/permissions.py#L41-L56) compare désormais `obj.author` pour Issue/Comment, `project.author` seulement pour Project/Contributor.
- **JWT recalé sur l'esprit « prudent par défaut »** : [config/settings.py:131-134](config/settings.py#L131-L134) — `ACCESS_TOKEN_LIFETIME` 30 min, `REFRESH_TOKEN_LIFETIME` 1 jour (au lieu de 365 jours).
- **Collection Postman réparée** pour la démo multi-utilisateurs : plus de tokens codés en dur, dossier Comment pointant enfin vers `/api/comment/`, noms de dossiers corrigés (Karim).
- **Pagination configurée et testée** : `DEFAULT_PAGINATION_CLASS` (`PageNumberPagination`) + `PAGE_SIZE=10` dans [config/settings.py:125-130](config/settings.py#L125-L130), couvre toutes les ressources automatiquement (config globale). Vérifié en conditions réelles avec des jeux de données à 12 éléments (projets, issues, commentaires) : la coupure 10+2 et les `next`/`previous` fonctionnent.

## Ce qui reste à faire / à corriger, avec citation du PDF

### 🟠 Gestion des dépendances — Pipenv/Poetry demandés, requirements.txt utilisé
Citation (page 2, « Gestion des dépendances ») :
> « nous utiliserons Pipenv ou Poetry afin de faciliter les mises à jour et l'interdépendance des bibliothèques tierces. »

Le projet a `softDesk/requirements.txt`, pas de `Pipfile` ni `pyproject.toml`. À migrer vers l'un des deux avant le rendu si l'évaluation vérifie ce point précisément.

### 🟠 Configuration à durcir avant rendu (OWASP)
Toujours dans [config/settings.py](config/settings.py) : `SECRET_KEY` en clair (valeur par défaut de `startproject`), `DEBUG = True`, `ALLOWED_HOSTS = []`. Le PDF ne les cite pas nommément mais ils relèvent du même esprit AAA/OWASP mis en avant en introduction.

### 🟡 Contributeurs : suppression à re-vérifier après correction du bug ci-dessus
`IsProjectMember.has_permission` réserve déjà la création de contributeurs à l'auteur du projet — cohérent avec le PDF qui ne mentionne que l'auteur/le contributeur pour les autorisations. Une fois le bug d'auteur corrigé pour Issue/Comment, revérifier que `Contributor` n'a pas le même problème (`has_object_permission` s'applique aussi à lui via `_get_project`).

### 🟡 Droit à l'oubli — à vérifier concrètement
Citation (page 2, RGPD) :
> « un utilisateur doit pouvoir supprimer ses données personnelles sans qu'il reste aucune subsistance dans l'application. »

`UserViewSet` autorise `DELETE` par le propriétaire du compte. Les `on_delete` des modèles suppriment en cascade les issues/commentaires de l'utilisateur (`CASCADE`) et détachent son autorat de projet (`SET_NULL`) — à confirmer par un essai réel (créer un compte, poster une issue/un commentaire, supprimer le compte, vérifier qu'il ne reste aucune trace en base ni dans les réponses API).

### 🟢 Documentation projet
Le [README.md](README.md) est réduit à trois lignes — à enrichir avant rendu (installation, migrations, variables d'environnement, import de la collection Postman).

### ⚪ Tests automatisés — non exigés par le CDC
Confirmé par Hugo : pas d'exigence de suite de tests dans le CDC de ce projet. D'ailleurs le PDF lui-même pointe que la génération de tests automatisés en CI « peut aussi prendre beaucoup de ressources [...] elle est à optimiser » — cohérent avec le fait de ne pas en faire une priorité ici.

## Suggestion d'ordre de priorité

1. Migration vers Pipenv/Poetry.
2. Durcissement `SECRET_KEY` / `DEBUG` / `ALLOWED_HOSTS`.
3. Vérification concrète du droit à l'oubli + README.
