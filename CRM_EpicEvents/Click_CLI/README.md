## Déroulement du programme

Dans le répertoire racine lancer le ou les commandes suivantes

- python -m demo_api users
- python -m demo_api customers
- python -m demo_api contracts
- python -m demo_api events

ces commandes donnent l'aide pour chacune des parties de l'API
Pour chacune de ces parties il est possible de créer , mettre à jour , supprimer , visualiser un ou plusieurs
objets.
Pour la partie user , on a le login et le refresh du token en plus.
ex : on tape `python -m demo_api users create` , le programme invite l'utilisateur à saisir

- son pseudo
- un mot de passe

si l'utilisateur est référencé , un token est généré et l'utilisateur peut saisir les données une par une.
Une fois toutes les données encodées , on fait appel à l'API qui renverra un code retour et un fichier au format
json le cas échéant.
Les erreurs d'encodage et fonctionnelles sont affichées également
