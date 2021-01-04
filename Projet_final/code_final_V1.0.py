# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 10:04:31 2019

@author: Nicolas Guy, Joachim Honegger, Antoine Passemard
"""

import random
import cv2
import time
import pybullet
import pybullet_data
from qibullet import PepperVirtual
from qibullet import SimulationManager
import Algorithmia
#import pepper_kinematics as pk
import numpy as np
import time
import pygame
import qi
import argparse
import sys
import signal


flagObjetTrouve = 0
PositionObjetTrouve=0
objetg=0
panierg=0

#-----------------------------Initialisation-----------------------------------
def main():
    global objetg
    global panierg

    "Initialisation des variables nécessaires au déploiement de la simulation"
    simulation_manager = SimulationManager()        
    clientEnv = simulation_manager.launchSimulation(gui=True)
    pepper = simulation_manager.spawnPepper(clientEnv, spawn_ground_plane=True)
    #pybullet.setAdditionalSearchPath(pybullet_data.getDataPath())
    pybullet.setAdditionalSearchPath("/home/tp/.local/lib/python2.7/site-packages/pybullet_data/")

    "Appel des fonctions"

    Environnement(clientEnv)
    pygame.mixer.init() #qibullet ne gère pas le son donc on est passé par là
    musique =  pygame.mixer.Sound("animal-crossing-new-leaf-music-main-theme.wav")
    musique.play(-1) # -1 pour reloop

    Init_camera(pepper)

    connect_qi()

    #simulation_manager.stopSimulation(clientEnv)     
    
    while True:

        if panierg != 0 and objetg != 0: #si les variables ont été modifiées dans les callbacks <=> on a terminé de choisir avec la tablette 
		objet_recherche = name_objet() #permet de corriger les malversions de la reconnaissance d'objet
		main_master(pepper,objet_recherche,panierg) #fonction recherche
		raw_input("\n Appuyez sur une entrée pour choisir un autre objet")
		panierg=0
		objetg=0
	time.sleep(0.1) #évite une boucle infinie et vide
    
def main_master(pepper,objet_recherche,panier):

    Placement(pepper) #place pepper pour prendre les photos
    Prise_Photo(pepper,objet_recherche) #prends la photo, la stocke et l'envoi à la fonction de détection d'image
    for i in range(2): #on parcourt chaque objet jusqu'à ce qu'on trouve l'objet (flagObjetTrouve=1)
        if flagObjetTrouve == 0:
            pepper.moveTo(0,0.8,0)
            time.sleep(0.5)
            Prise_Photo(pepper,objet_recherche)

    Catch_Objet(pepper) #on attrape l'objet selon la position où on est (droite, milieu , gauche <=> 1,2,3)
    Retour_Depart(pepper) #on revient à la position de départ selon la position à laquelle on est
    Lacher_Objet(pepper, panier) #on pose l'objet dans le panier voulu  


#-------------------------------gestion des événements de la tablette-------------------------------   
def name_objet(): #permet de corriger les malversions de la reconnaissance d'objet
    if objetg == "parrot":
        objet_recherche = "bird"
    elif objetg == "monkey":
        objet_recherche = "person"
    #elif objetg == "":
     #   objet_recherche = "cat"
    else:
	print("error #2 : l'objet recherché n'existe pas")

    return objet_recherche

def mycallback(objet): #permet de récupérer l'argument envoyé par le js
    global objetg
    objetg=objet
    print "l'animal choisi est:", objet

def mycallback1(panier):
    global panierg
    panierg=panier
    print "le panier choisi est:",panier

def connect_qi(): #permet d'initialiser une session qi pour utiliser le service ALTabletService

    ip = "127.0.0.1"
    port = "9559"
    connection_url = "tcp://" + ip + ":" + port

    session = qi.Session()
    try:
        # Initialize qi framework.

        session.connect(connection_url)
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + ip + "\" on port " + port +".\n")
        sys.exit(1) 

    gestion_tab(session)

def gestion_tab(session): #permet d'executer la tablette

        # Get the service ALTabletService.

    try:
        tabletService = session.service("ALTabletService")
        tabletService.loadApplication("SimpleWebPython")
        tabletService.showWebview()

    except Exception, e:
        print "Error was: ", e

# Getting the service ALDialog
    try:
        ALDialog = session.service("ALDialog")
        ALDialog.resetAll()
        ALDialog.setLanguage("English")

        # Loading the topics directly as text strings
        #topic_name = ALDialog.loadTopic("/home/nao/.local/share/PackageManager/apps/SimpleWebPython/simple_en.top")
    	#WARNING TO CHANGE YOUR PATH  
    	topic_name = ALDialog.loadTopic("/home/tp/softbankRobotics/apps/SimpleWebPython/simpled_en.top")

        # Activating the loaded topics
        ALDialog.activateTopic(topic_name)


        # Starting the dialog engine - we need to type an arbitrary string as the identifier
        # We subscribe only ONCE, regardless of the number of topics we have activated
        ALDialog.subscribe('simpled')

    except Exception, e:
        print "Error was: ", e

    try:
        memoryService=session.service("ALMemory")

    except Exception, e:
        print "Error was: ", e

    try: 
    
    #memoryService.insertData("Simpleweb/Page2")
    #memoryService.suscriber("Simpleweb/Page2")

        
        sub = memoryService.subscriber("SimpleWeb/Page2")
        objet=memoryService.getData("SimpleWeb/Page2")
        sub.signal.connect(mycallback)

    #memoryService.insertData("Simpleweb/Page3")
    #memoryService.suscriber("Simpleweb/Page3")


    except Exception, e:
        print "Error was: ", e

    try: 
        sub1 = memoryService.subscriber("SimpleWeb/Page3")
        panier=memoryService.getData("SimpleWeb/Page3")
        print "test"
        sub1.signal.connect(mycallback1)
    


    except Exception, e:
        print "Error was: ", e


    try:
        raw_input("\n Press Enter when finished:")
    finally:
        # stopping the dialog engine
        ALDialog.unsubscribe('simpled')

        # Deactivating the topic
        ALDialog.deactivateTopic(topic_name)

        # now that the dialog engine is stopped and there are no more activated topics,
        # we can unload our topic and free the associated memory
        ALDialog.unloadTopic(topic_name)


#----------------------------FONCTION LOAD OBJET-------------------------------    
"Ici on charge tous les objets de l'environnement dans lequel le robot va évoluer"
def Environnement(clientEnv): 
    
    coord_y = [-0.8,0.0,0.8]
    liste_coord_y = random.sample(coord_y,3)
    

    pybullet.loadURDF(
        "table2.urdf",
        basePosition=[2.3, 0, 0.3],
        globalScaling=17,
        physicsClientId=clientEnv)
        
    pybullet.loadURDF(
        "totem_Tortue.urdf",
        basePosition=[1.95, liste_coord_y[0], 0.7],
        globalScaling=1,
        physicsClientId=clientEnv)
        
    pybullet.loadURDF(
        "totem_Parrot.urdf",
        basePosition=[1.95, liste_coord_y[1], 0.7],
        globalScaling=1.5,
        physicsClientId=clientEnv)
        
    pybullet.loadURDF(
        "totem_Cat.urdf",
        basePosition=[1.95, liste_coord_y[2], 0.7],
        globalScaling=1.5,
        physicsClientId=clientEnv)

    pybullet.loadURDF(
        "caisse.urdf",
        basePosition=[0.0, 2.5, 0.01],
        globalScaling=0.2,
        physicsClientId=clientEnv)

    pybullet.loadURDF(
        "caisse.urdf",
        basePosition=[-0.1, -2.5, 0.01],
        globalScaling=0.2,
        physicsClientId=clientEnv)

    pybullet.loadURDF(
        "caisse.urdf",
        basePosition=[-1.8,-0.05, 0.01],
        globalScaling=0.2,
        physicsClientId=clientEnv)

    pybullet.loadURDF(
        "mur1.urdf",
        basePosition=[3.5,0, 0.2],
        globalScaling=1,
        physicsClientId=clientEnv)

    pybullet.loadURDF(
        "mur2.urdf",
        basePosition=[0.175,-3.75, 0.2],
        globalScaling=1,
        physicsClientId=clientEnv)

    pybullet.loadURDF(
        "mur2.urdf",
        basePosition=[0.175,3.75, 0.2],
        globalScaling=1,
        physicsClientId=clientEnv)
    
    pybullet.loadURDF(
        "mur1.urdf",
        basePosition=[-3.15,0, 0.2],
        globalScaling=1,
        physicsClientId=clientEnv)

    pybullet.loadURDF(
        "sol.urdf",
        basePosition=[-3.15,0, 0.001],
        globalScaling=5,
        physicsClientId=clientEnv)

    pybullet.loadURDF(
        "tableau.urdf",
        basePosition=[0.275,3.72, 0.25],
        globalScaling=2,
        physicsClientId=clientEnv)
    
    pybullet.loadURDF(
        "tableau2.urdf",
        basePosition=[-1.8 ,3.72, 0.25],
        globalScaling=2,
        physicsClientId=clientEnv)
        
    pybullet.loadURDF(
        "tableau3.urdf",
        basePosition=[2.2, 3.72, 0.25],
        globalScaling=2,
        physicsClientId=clientEnv)
        
    pybullet.loadURDF(
        "tableau.urdf",
        basePosition=[0.275,-3.74, 0.25],
        globalScaling=2,
        physicsClientId=clientEnv)
    
    pybullet.loadURDF(
        "tableau2.urdf",
        basePosition=[-1.8 ,-3.74, 0.25],
        globalScaling=2,
        physicsClientId=clientEnv)
        
    pybullet.loadURDF(
        "tableau3.urdf",
        basePosition=[2.2, -3.74, 0.25],
        globalScaling=2,
        physicsClientId=clientEnv)
        
    pybullet.loadURDF(
        "animalerie.urdf",
        basePosition=[-3.15, 0, 0.25],
        globalScaling=2,
        physicsClientId=clientEnv)

#----------------------------FONCTION_Prise_Photos-----------------------------
"Ici on donne les instructions de mouvement pour que le robot prenne tous les animaux en photo"

def Placement(pepper): #on avance vers une distance suffisante pour prendre les photos
    pepper.moveTo(0.9,0,0) 
    pepper.moveTo(0,-0.8,0)
    
def Retour_Depart(pepper): #on revient à la position de départ selon la position à laquelle on est
    global PositionObjetTrouve

    if PositionObjetTrouve == 1: #a gauche
        print("position 1")
        pepper.moveTo(0,+0.8,0) 
        pepper.moveTo(-0.9,0,0)
    elif PositionObjetTrouve == 2: #au milieu
        print("position 2")
        pepper.moveTo(-0.9,0,0)
    else : #a droite
        print(" position 3")
        pepper.moveTo(0,-0.8,0) 
        pepper.moveTo(-0.9,0,0)

    PositionObjetTrouve = 0  #on réinitialise 

def Init_camera(pepper): #permet d'orienter la caméra
    print("Initialisation")
    pepper.goToPosture("Stand", 0.6)
    pepper.setAngles("HeadPitch",-1.0, 1.0) #le robot lève la tête pour avoir le bon angle

def Prise_Photo(pepper, objet_recherche): #permet de capturer des images tant que l'objet n'a pas été trouvé

    global PositionObjetTrouve
    global flagObjetTrouve
    pepper.subscribeCamera(PepperVirtual.ID_CAMERA_BOTTOM)

    print("Etalonnage en cours...")
    for loop in range(5): #on boucle pour que la fenetre camera s'affiche bien
        img = pepper.getCameraFrame()
        cv2.imshow("bottom camera", img) #on affiche l'image dans la fênetre crée grâce à cv2
        cv2.waitKey(1)

    pepper.unsubscribeCamera(PepperVirtual.ID_CAMERA_BOTTOM) #pour éviter la prise de RAM 
    cv2.imwrite('/home/tp/image_detect.jpg', img) #on enregistre l'image en local
    cv2.waitKey(1)
    label = imageDetection(0.2) #renvoi le résultat de l'analyse
    if label == objet_recherche :
        flagObjetTrouve = 1
        print("Objet trouvé !")

    PositionObjetTrouve+=1 #permet de savoir à quelle position on est ( 1, 2 ou 3)
    

def imageDetection(min_score): #permet la reconnaissance d'objet à partir d'une image

    clientAlgorithmia = Algorithmia.client('sim8VSFz8+/cjSk7Cl83Rt/3KVi1')

    monfichier = clientAlgorithmia.dir("data://joachimhgg/Projet_majeur/") #on stocke l'image et le résultat sur le cloud d'algorithmia

    image_detect = "data://joachimhgg/Projet_majeur/image_detect.png"

    # Upload local file
    print("Processing image detection...")
    clientAlgorithmia.file(image_detect).putFile("/home/tp/image_detect.jpg")

    input = {
        "image": image_detect,
        "output": "data://joachimhgg/Projet_majeur/result.png",
        "min_score": min_score,
        "model": "ssd_mobilenet_v1"
    }

    algoObject = clientAlgorithmia.algo('deeplearning/ObjectDetectionCOCO/0.2.1')
    algoObject.set_options(timeout=300) # si jamais ça dépasse 300sec on quitte

    #on pourrait enlever le for ici mais on le conserve en vu d'amélioration
    for i in range(len(algoObject.pipe(input).result['boxes'])): #on boucle pour chaque objet détecté

        confidence = algoObject.pipe(input).result['boxes'][i]['confidence']
        label = algoObject.pipe(input).result['boxes'][i]['label']
        coordinates = algoObject.pipe(input).result['boxes'][i]['coordinates']
        print ("label : "+ str(label)+ "\ncoordonnées : "+ str(coordinates))
        return label #on retourne le premier label renvoyé

    if len(algoObject.pipe(input).result['boxes']) == 0: 
        print ("Warning #1: image non détectée")
        #return imageDetection(0.1) #si il n'y a rien on retente avec un min_score plus faible

#----------------- Partie Catch du totem -----------------
def Catch_Objet(pepper): #permet au pepper d'attraper l'objet

    if PositionObjetTrouve == 1:
        pepper.moveTo(0,0.02,0) #objet droit
    elif PositionObjetTrouve == 3:
        pepper.moveTo(0,0.02,0) #objet gauche

    pepper.moveTo(0.3,0,0) #on s'approche de l'objet 
    pepper.setAngles("RElbowRoll", 0.0, 1.0) 
    pepper.setAngles("RShoulderPitch", 0.15, 1.0) 
    pepper.setAngles("RHand", 1.5, 1.0) 
    pepper.moveTo(0.4,0,0)
    pepper.moveTo(0,0.185,0)
    time.sleep(4) #étape délicate donc on attend un peu 
    pepper.setAngles("RHand", 0.00, 1.0) 
    time.sleep(4)
    

    #on se replace pour reculer selon la position de l'objet pris
    if PositionObjetTrouve == 1: 
        pepper.moveTo(0,-0.02,0) #objet droit
    elif PositionObjetTrouve == 3:
        pepper.moveTo(0,-0.03,0) #objet gauche
    pepper.moveTo(-0.7,0,0)
    pepper.moveTo(0,-0.185,0)

def Lacher_Objet(pepper, panier): #permet de lacher un objet dans un des paniers
    if panier == 'Left box': #information envoyé par la tablette
        pepper.moveTo(0,-1.80,0)
        pepper.moveTo(0,0,-1.57)
        pepper.setAngles("RHand", 1.5, 1.0) 
    elif panier == 'Center box':
        pepper.moveTo(-0.9,0,0)
        pepper.moveTo(0,0,3.14)
        pepper.setAngles("RElbowRoll", -0.3, 1.0) 
        pepper.setAngles("RHand", 1.5, 1.0) 
        time.sleep(1)
    elif panier == 'Right box':
        pepper.moveTo(0,1.80,0)
        pepper.moveTo(0,0,1.57)
        pepper.setAngles("RHand", 1.5, 1.0) 
    else:
        print ("Error #1: panier inconnu")
    
def detectionLaser(objet): #fonction non utilisée dans le programme mais permet de se placer par laser sans connaitre les coordonnées mais juste la taille de la table et des caisses

    #laser_list = pepper.getRightLaserValue()
    #laser_list.extend(pepper.getFrontLaserValue())
    #laser_list.extend(pepper.getLeftLaserValue())
    #laser_list= pepper.getFrontLaserValue()

    a=0
    ok=0
    #on tourne jusqu'à ce qu'on soit bien en face de l'objet
    laser_list= pepper.getFrontLaserValue() 
    print(laser_list)
    if objet == 'table' : #on choisi les lasers qui ne détecte pas la table (les lasers verts) #à mettre dans l'odre décroissant
        list_i = []#[14,13,0] 
    elif objet == 'panier':
        list_i = [14,13,12,2,1,0]

    while (a==0):
        
        for i in list_i:   #on parcourt la liste des lasers qui doivent être vert et on regarde si il le sont
            if (laser_list[i]==3.0):
                ok+=1
        print(ok)
        print(len(list_i))
        if ok == len(list_i): #si tous les lasers choisit dans la list_i sont verts
            
            ok=0
            
            for i in list_i: #on enlève de la liste les lasers verts
                laser_list.pop(i)
                
            print ("nouvelle liste", laser_list)
            
            for laser in laser_list : # et on regarde si les autres lasers sont bien rouges
                if laser < 3.0 :
                    ok+=1
            if ok == len(laser_list): #si ils sont bien rouges, on met a=1
                a=1
                print("objet trouvé")
        else:
            ok=0
            
        if a==0: #tant que a==0 on tourne le robot
            pepper.moveTo(0,0,0.1)
            laser_list= pepper.getFrontLaserValue()
            print(laser_list)

    print("Objet detecté !")
    
    #se code permet de déplacer le robot jusqu'à une distance de laser
    """while laser_list[7] < 2.5: #on s'approche à 1.3 mètres de la table
        pepper.moveTo(-0.1,0,0)
        laser_list= pepper.getFrontLaserValue()
        print(laser_list[7])"""

if __name__ == "__main__":
    main() #programme principal
