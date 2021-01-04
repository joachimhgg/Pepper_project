#################### robot Petpper ####################


# AUTEURS:
 - Honegger Joachim
 - GUY Nicolas
 - PASSEMARD Antoine

 

 
# YOUTUBE:
 - https://www.youtube.com/watch?v=JjFhL1Lx0Cc&feature=youtu.be&fbclid=IwAR0lzD4wU5eNUaQQOTve_z2XVaRB_OMAjzYoRVOUJ6C48lwvLRIaxHlbiWM
 
# GITHUB:
 - https://github.com/NicoPepper/Projet_Majeur.git
 

 
# Projet initial commun :
 - Done 
 	- Simulation d'un monde avec un robot pepper 3 objets et 3 emplacements
 	- Interface homme/robot: l'utlisateur demande au robot de prendre un objet et de le deplacer dans un stockage
 	- reconnaissance de l'objet avec Algorithmia

 
# BONUS:
 - Numéro 4 :
	- Done
		-Création d'un joli monde (une animalerie) avec un scénario réalisé sur l'IHM
		-Ajout d'un sol et d'une maison ressemblant à une animalerie
	- Todo :
		- mise en place de différentes cage selon l'animal choisi. 
		- Détection par laser pour avoir des coordonnées de table et cages inconnues



# ABORESCENCE DES FICHIERS
 - README.md : Ce fichier

 - Projet_majeur : 
	- SimplWebPython:
		-html:
			index.html
			-js:
				sample.js
		-simpled_en.top
		
	- fichier_Objet2:
		tout les fichiers urdf jpg png..	
	- code_final.py  (notre main)

 - [Présentation] : 
	- projet_majeur_petpper.pptx

#######################################################

#  PROCEDURE D'INSTALLATION

Utilisation de la VM:

- installer la librairie Pygame pour la musique : pip install pygame 

-Télecharger projet_majeur
-Ouvrir le dossier et mettre le code python : "code_final.py" dans le dossier: /home/tp/softbankRobotics/apps de la VM

Déplacer le dossier "SimpleWebPython" dans le dossier "/home/tp/softbankRobotics/apps" de la VM

-Deplacer tout les fichier situer dans le dossier "fichier_Objet2" .urdf .obj .mtl et png ou jpg dans le dossier "/home/tp/.local/lib/pyhton2.7/site-packages/pybullet_data"

installer pybullet_data


 Mettre à jour votre .bashrc  : 

« 
export PYTHONPATH=${PYTHONPATH}:/softwares/INFO/Pepper/pynaoqi-python2.7-2.5.5.5-linux64/lib/python2.7/site-packages
export PATH=$PATH:"/softwares/INFO/Pepper/choregraphe-suite-2.5.5.5-linux64/bin"


export PATH="/softwares/INFO/Pepper/python/python-2.7.16/bin":$PATH
export PYTHONPATH=/softwares/INFO/Pepper/python/python-2.7.16/lib/python2.7/site-packages:${PYTHONPATH}
export PYTHONPATH=${PYTHONPATH}:/softwares/INFO/Pepper/pynaoqi-python2.7-2.5.5.5-linux64/lib/python2.7/site-packages

export PYTHONPATH=${HOME}/qibullet:${PYTHONPATH} 
»


# PROCEDURES DE MISE EN ROUTE
-lancer terminator:
- Lancer l’instruction « naoqi-bin » dans un terminal 1
- Lancer l’instruction « choregraphe_launcher» dans un terminal 2
- Dans un terminal 3, se placer dans naoqi-tablet-simulators et exécuter la commande suivante : ./launcher.sh
- Ouvrir le fichier « [Chemin jusqu’à l’emplacement du Projet]/nts-examples/nts/web/page.html » dans un navigateur web
- Vérifier que la tablette est bien connecté
- Dans un terminal 4, se placer dans apps puis lancer le python: python "code_final.py"


