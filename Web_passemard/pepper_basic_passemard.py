# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 10:04:31 2019
@author: nicolas
"""

import random
import pybullet
import pybullet_data
import cv2
import time
from qibullet import SimulationManager
from qibullet import PepperVirtual

liste_choix = ["cat","turtle","parrot"]
choix = liste_choix[2]

#-----------------------------Initialisation-----------------------------------
def main(): 
    "Initialisation des variables"
    simulation_manager = SimulationManager()        
    client = simulation_manager.launchSimulation(gui=True)
    pepper = simulation_manager.spawnPepper(client, spawn_ground_plane=True)
    pybullet.setAdditionalSearchPath(pybullet_data.getDataPath())
    
    
    "Appel des fonctions"
    Environnement(client)
    pepper.goToPosture("Stand", 0.6)
    time.sleep(1)
    Catch_Objet_Milieu(pepper)
    """for i in range(2): 
        Prise_Photo(pepper)"""
    Retour_Depart_Milieu(pepper)
    Lacher_Objet(pepper,choix)
        
    while True:
        cv2.waitKey(1)
    
    
#----------------------------FONCTION LOAD OBJET-------------------------------    
"Ici on charge tous les objets de l'environnement dans lequel le robot va évoluer"
def Environnement(client): 
    
    coord_y = [-0.8,0.0,0.8]
    liste_coord_y = random.sample(coord_y,3)
    
    pybullet.loadURDF(
        "table2.urdf",
        basePosition=[2.3, 0, 0.3],
        globalScaling=17,
        physicsClientId=client)
        
    pybullet.loadURDF(
        "totem_Tortue.urdf",
        basePosition=[1.95, liste_coord_y[0], 0.7],
        globalScaling=1.5,
        physicsClientId=client)
        
    pybullet.loadURDF(
        "totem_Parrot.urdf",
        basePosition=[1.95, liste_coord_y[1], 0.7],
        globalScaling=1.5,
        physicsClientId=client)
        
    pybullet.loadURDF(
        "totem_Cat.urdf",
        basePosition=[1.95, liste_coord_y[2], 0.7],
        globalScaling=1.5,
        physicsClientId=client)

    pybullet.loadURDF(
        "caisse.urdf",
        basePosition=[0.0, 2.5, 0.1],
        globalScaling=0.2,
        physicsClientId=client)

    pybullet.loadURDF(
        "cage.urdf",
        basePosition=[-0.1, -2.5, 0.4],
        globalScaling=0.9,
        physicsClientId=client)

    pybullet.loadURDF(
        "panier.urdf",
        basePosition=[-1.5, -0.05, 0.1],
        globalScaling=0.55,
        physicsClientId=client)


#----------------------------FONCTION_Prise_Photos-----------------------------
"Ici on donne les instructions de mouvement pour que le robot prenne tous les animaux en photo"

    
def Retour_Depart_Milieu(pepper):
    #pepper.moveTo(0,-0.8,0) 
    #time.sleep(1)
    pepper.moveTo(-0.9,0,0)
    time.sleep(1)
    
def Catch_Objet_Milieu(pepper):
#-----------------Partie Catch du totem  
    #pepper.moveTo(0,-0.77,0)
    pepper.moveTo(0,0.82,0)
    pepper.moveTo(1.2,0,0) #on avance 
    pepper.setAngles("RElbowRoll", 0.0, 1.0) 
    pepper.setAngles("RShoulderPitch", 0.15, 1.0) 
    pepper.setAngles("RHand", 1.5, 1.0) 
    pepper.moveTo(0.4,0,0)
    pepper.moveTo(0,0.185,0)
    time.sleep(4)
    pepper.setAngles("RHand", 0.00, 1.0) 
    time.sleep(4)
    pepper.moveTo(-0.42,0,0)

    
def Prise_Photo(pepper):
    pepper.setAngles("HeadPitch",-1.0, 1.0) #le robot lève la tête pour avoir le bon angle
    pepper.subscribeCamera(PepperVirtual.ID_CAMERA_BOTTOM)
    img = pepper.getCameraFrame() #prise de photo
    cv2.imshow("bottom camera", img) #affichage de la photo
    time.sleep(5)
    pepper.moveTo(0,0.8,0)
    time.sleep(1)     
    
def Lacher_Objet(pepper, choix):
    if choix == "cat":
        pepper.moveTo(-0.9,0,0)
        time.sleep(1)
        pepper.moveTo(0,0,3.14)
        time.sleep(1)
        pepper.setAngles("RElbowRoll", -0.3, 1.0) 
        time.sleep(1)
        pepper.setAngles("RHand", 1.5, 1.0) 
        time.sleep(1)
    elif choix == "parrot":
        pepper.moveTo(0,1.65,0)
        time.sleep(1)
        pepper.moveTo(0,0,1.57)
        time.sleep(1)
        pepper.setAngles("RHand", 1.5, 1.0) 
        time.sleep(1)
    elif choix == "turtle":
        pepper.moveTo(0,-1.65,0)
        time.sleep(1)
        pepper.moveTo(0,0,1.5-7)
        time.sleep(1)
        time.sleep(1)
        pepper.setAngles("RHand", 1.5, 1.0) 
        time.sleep(1)
    

if __name__ == "__main__":
      main()

