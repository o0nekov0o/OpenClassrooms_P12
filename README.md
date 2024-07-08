
# Développer une architecture back-end sécurisée avec Python et SQL (Projet Python 12 OpenClassrooms)

Ci-dessous l'objectif donné pour ce projet :\
*Monter en compétences en développement back-end*\
Pour se faire, il a fallu faire les choses suivantes :

- Réaliser des bases de données relationnelles avec SQL
- Assurer la sécurisation et l’authentification du back-end

Autres choses faisant parti des demandes :
- S'initier à la modélisation de données relationnelles
- S'initier à la journalisation et le suivi des erreurs

## Installation

Télécharger le projet via le lien ci-dessous :\
https://github.com/o0nekov0o/OpenClassrooms_P12/archive/refs/heads/master.zip

Télécharger Postgres via le lien ci-dessous,\
pour lancer le serveur PostgreSQL :
https://www.postgresql.org/download/

Télécharger PgAdmin via le lien ci-dessous,\
pour superviser le serveur PosgreSQL :
https://www.pgadmin.org/download/

Créer ensuite votre serveur via Postgres.\
Utiliser les informations de connexion,\
pour connecter votre serveur sur PgAdmin.

Depuis PgAdmin, créer une nouvelle base de données sur votre serveur.\
Via un clic droit sur votre base de données, faites un *Restore*\
Sélectionner maintenant le fichier *database.sql* présent dans le projet.\
Maintenant que les données du projet sont bien initialisées,\
Créer un fichier .env en racine du projet que vous compléterez comme ceci :\
(DH_HOST et DB_PORT étant généralement ceux par défaut)

```bash
DB_NAME=NomDeVotreBaseDeDonnees
DB_USER=NomDeConnexionAuServeur
DB_PASSWORD=MotdePasseDuServeur
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY=django-insecure-n2wl_y!1kei7%(9a+l81yx^y%_*pd6+5g*!f#$_&bxm*6@hvpd
```

SECRET_KEY sert à la journalisation et le suivi des erreurs via Sentry.\
Dès à présent, le projet est prêt et le serveur peut être lancé via ces commandes,\
En s'assurant en amont d'avoir démarré l'ensemble des dépendances :

Se placer en racine du projet,\
puis depuis un poste Windows :
```bash
python -m venv venv
call venv/Scripts/activate.bat
```
Si échec de la dernière commande,\
depuis une console Powershell admin,\
puis de nouveau depuis le terminal :
```bash
Set-ExecutionPolicy RemoteSigned
venv/Scripts/activate
```
Se placer en racine du projet,\
puis depuis un autre OS :
```bash
python -m venv venv
source venv/bin/activate
```
Etapes suivantes quelque soit l'OS :
```bash
cd CRM_EpicEvents
pip3 install -r requirements.txt
python3 manage.py runserver
```

## Utilisation du programme

Dans le répertoire racine,\
lancer une des commandes suivantes :

```bash
python -m Click_CLI users    
python -m Click_CLI customers
python -m Click_CLI contracts
python -m Click_CLI events
```
La structure de l'API repose sur 4 parties,\
Ces 4 parties étant les 4 modèles de l'application.\
En exécutant les commandes précédentes,\
on obtient de l'aide pour chacune des parties de l'API.\
Pour chacune de ces parties, il est possible de : 
- créer
- mettre à jour
- supprimer
- visualiser des objets.

Pour chaque partie, un login est demandé avant chaque exécution d'action.\
Par exemple, en saisissant la commande `python -m Click_CLI users create`,\
Pour vérifier les permissions, le programme invite l'utilisateur à saisir :

- son nom d'utilisateur
- son mot de passe

Si l'utilisateur est référencé, un token est généré pour l'authentifier.\
L'utilisateur peut alors saisir les données de création une par une.\
Une fois toutes les données encodées, le programme sollicite l'API qui renverra :

- soit un code retour (200 ou 400 selon succès ou échec de la commande)
- soit un fichier json le cas échéant (commandes de visualisation).

Les erreurs d'encodage et fonctionnelles sont affichées également.
