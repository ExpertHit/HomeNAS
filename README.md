# HomeNAS

Pour commencer il faut installer trois paquets :

Flask 

     python -m pip install flask

Request

     python -m pip install requests

Et psutil

     python -m pip install psutil

Si vous voulez changer le dossier du serveur, rendez-vous dans BackEnd_HomeNAS.py et modifier cette variable:

     storage_path = "C:\\Partage"

Pour modifier le chemin sur MacOS modifier la même variable mais avec le chemin complet

     storage_path = "/Users/antho/Partage"

Pour lancer l'application, lancer le FrontEnd_Home.py
