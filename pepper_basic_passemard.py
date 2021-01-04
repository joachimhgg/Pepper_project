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


#-----------------------------Initialisation-----------------------------------
def main():
    simulation_manager = SimulationManager()
    client = simulation_manager.launchSimulation(gui=True)
    pepper = simulation_manager.spawnPepper(client, spawn_ground_plane=True)
    "pybullet.setAdditionalSearchPath(pybullet_data.getDataPath())"
    pybullet.setAdditionalSearchPath("/home/tp/.local/lib/python2.7/site-packages/pybullet_data/")
    print(pybullet_data.getDataPath())
    
#---------------------------Déclaration coord aléatoire------------------------

    coord_y = [-0.8,0.0,0.8]
    liste_coord_y = random.sample(coord_y,3)


#----------------------------FONCTION LOAD OBJET-------------------------------
    
#Ici on charge tous les objets de l'environnement dans lequel le robot va évoluer
    
    pybullet.loadURDF(
        "table2.urdf",
        basePosition=[2.3, 0, 0.3],
        globalScaling=17,
        physicsClientId=client)
        
    pybullet.loadURDF(
        "totem_Tortue.urdf",
        basePosition=[1.95, -0.8, 0.7],
        globalScaling=1.5,
        physicsClientId=client)
        
    pybullet.loadURDF(
        "totem_Parrot.urdf",
        basePosition=[1.95, 0.8, 0.7],
        globalScaling=1.5,
        physicsClientId=client)
        
    pybullet.loadURDF(
        "totem_Cat.urdf",
        basePosition=[1.95, 0, 0.7],
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
        globalScaling=0.45,
        physicsClientId=client)
        

 #-----------------------------------------------------------------------------

#----------------------------Instruction---------------------------------------

#Ici on donne toutes les instructions que le robot doit réaliser
    pepper.goToPosture("Stand", 0.6)
    time.sleep(1)

#-----------------Partie Catch du totem  
  
    pepper.moveTo(1.2,0,0) #on avance 
    pepper.setAngles("RElbowRoll", 0.0, 1.0) 
    pepper.setAngles("RShoulderPitch", 0.15, 1.0) 
    pepper.setAngles("RHand", 1.0, 1.0) 
    pepper.moveTo(0.4,0,0)
    pepper.moveTo(0,0.175,0)
    pepper.setAngles("RHand", 0.00, 1.0) 
    time.sleep(4)
    pepper.moveTo(-0.42,0,0)

    
    
#-------------------------------------
    
    pepper.subscribeCamera(PepperVirtual.ID_CAMERA_BOTTOM)

    while True:
        #img = pepper.getCameraFrame()
        #cv2.imshow("bottom camera", img)
        cv2.waitKey(1)

#------------------------------------------------------------------------------
if __name__ == "__main__":
	main()