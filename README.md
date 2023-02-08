# Authentification x Django


## Introduction

Ce produit tient la même promesse que tchap-identite (une authentification forte mais simple, sans mot de passe, sans identification), pour un autre public de développeuses.

Pile technique :

- Python 3.10
- Django 4
- PostgreSQL

## Installation

### Dépendances Python

Installez pipenv si ce n'est déjà fait :

```
pip install --user pipenv
```

Vérifiez que `pipenv` est bien dans votre `$PATH`.

Installez les dépendances et copiez les variables d'environnement :

```
pipenv install
cp .env.example .env
```

### Installation de PostgreSQL

Installez PostgreSQL en fonction de votre OS : https://www.postgresql.org/download/

Puis lancez l'invite de commande PostgreSQL : 

```
psql
```

Dans l'invite de commande psql, vous pouvez à présent créer la base de données et l'utilisateur :

```sql
CREATE USER authentification_team PASSWORD 'authentification_pwd';
CREATE DATABASE authentification OWNER authentification_team;
ALTER USER authentification_team CREATEDB;
```

Vous pouvez à présent quitter l'invite de commande psql.

### Installation de pre-commit

[Pre-commit](https://pre-commit.com/#install) permet de linter et formatter votre code avant chaque commit. Par défaut ici, il exécute :

- [black](https://github.com/psf/black) pour formatter automatiquement vos fichiers `.py` en conformité avec la PEP 8 (gestion des espaces, longueur des lignes, etc)
- [flake8](https://github.com/pycqa/flake8) pour soulever les "infractions" restantes (`import` non utilisés, etc.)
- [isort](https://github.com/pycqa/isort) pour ordonner vos imports

Pour l'installer, depuis la racine de votre projet :

```bash
pre-commit install
```

Vous pouvez effectuer un premier passage sur tous les fichiers du repo avec :

```bash
pre-commit run --all-files
```

## Lancer le serveur en local

```bash
pipenv run python manage.py runserver 3000
```

## Exécuter les tests

```bash
pipenv run python manage.py test
```
