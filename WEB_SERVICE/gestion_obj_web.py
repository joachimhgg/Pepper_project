#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon May 27 09:08:19 2019

@author: yorm
"""

import random
import cv2
import time
import pybullet
import pybullet_data
from qibullet import PepperVirtual
from qibullet import SimulationManager
import Algorithmia
import pepper_kinematics as pk
import numpy as np
import time

#----------------------INITIALISATION-----------------------------------------
simulation_manager = SimulationManager()
clientEnv = simulation_manager.launchSimulation(gui=True)
pepper = simulation_manager.spawnPepper(clientEnv, spawn_ground_plane=True)


#flagMove=0

def main():
    #global flagMove

    pybullet.setAdditionalSearchPath(pybullet_data.getDataPath())

#-----------------------------------------------------------------------------

#---------------------------Déclaration coord aléatoire-----------------------------

    coord_y = [-0.8,0.0,0.8]
    liste_coord_y = random.sample(coord_y,3)


#----------------------------FONCTION LOAD OBJET-------------------------------
    pybullet.loadURDF(
        "table2.urdf",
        basePosition=[2.3, 0, 0.3],
        globalScaling=17,
        physicsClientId=clientEnv)
        
    pybullet.loadURDF(
        "totem_Tortue.urdf",
        basePosition=[2.0, liste_coord_y[0], 0.7],
        globalScaling=2.0,
        physicsClientId=clientEnv)
        
    pybullet.loadURDF(
        "totem_Parrot.urdf",
        basePosition=[2.0, liste_coord_y[1], 0.7],
        globalScaling=2.0,
        physicsClientId=clientEnv)
        
    pybullet.loadURDF(
        "totem_Cat.urdf",
        basePosition=[2.0, liste_coord_y[2], 0.7],
        globalScaling=2.0,
        physicsClientId=clientEnv)

    pybullet.loadURDF(
        "caisse.urdf",
        basePosition=[0.5, 2, 0.1],
        globalScaling=0.2,
        physicsClientId=clientEnv)

    pybullet.loadURDF(
        "cage.urdf",
        basePosition=[0.5, -2, 0.4],
        globalScaling=0.9,
        physicsClientId=clientEnv)

    pybullet.loadURDF(
        "panier.urdf",
        basePosition=[-1.5, -0.05, 0.1],
        globalScaling=0.45,
        physicsClientId=clientEnv)
        
 #----------------------------------------------------------------------------


    pepper.showLaser(True)
    pepper.subscribeLaser()
    pepper.goToPosture("Stand", 0.6)
    #cv2.waitKey(0) #permet de mettre le programme en pause jusqu'à l'appuie d'une touche

    pepper.subscribeCamera(PepperVirtual.ID_CAMERA_BOTTOM)

     
    detectionLaser('table') #on chercher la table
    pepper.moveTo(-0.55,0,0) #on recule 

    catch_obj(2) #on attrape l'objet au milieu

    while True:

        
        #if all(laser == 3.0 for laser in laser_list):
            print("Etalonnage en cours...")
            for loop in range(10): #on boucle pour que la fenetre camera s'affiche bien
                img = pepper.getCameraFrame()
                cv2.imshow("bottom camera", img)
                cv2.waitKey(1)

            
            cv2.imwrite('/home/yorm/Documents/pepper/Projet_majeur/WEB_SERVICE/image_detect.jpg', img)
            cv2.waitKey(1)
            time.sleep(2.0)
            imageDetection()
    pass

def detectionLaser(objet):

    pepper.setAngles('HeadPitch', -0.6,1) #on monte un peu la tête


    #laser_list = pepper.getRightLaserValue()
    #laser_list.extend(pepper.getFrontLaserValue())
    #laser_list.extend(pepper.getLeftLaserValue())
    #laser_list= pepper.getFrontLaserValue()

    a=0
    ok=0
    #on tourne jusqu'à ce qu'on soit bien en face de l'objet
    laser_list= pepper.getFrontLaserValue() 
    print(laser_list)
    if objet == 'table' : 
        list_i = []#[14,1,0] #on choisi les lasers qui ne détecte pas la table (les lasers verts) #à mettre dans l'odre décroissant
    elif objet == 'caisse':
        list_i = [14,1,0]
    elif objet == 'cagette':
        list_i = [14,1,0]
    elif objet == 'panier':
        list_i = [14,1,0]

    while (a==0):
        

        for i in list_i:   
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

    print("table detected !")
    
    #se code permet de déplacer le robot jusqu'à une distance de laser
    """while laser_list[7] < 2.5: #on s'approche à 1.3 mètres de la table
        pepper.moveTo(-0.1,0,0)
        laser_list= pepper.getFrontLaserValue()
        print(laser_list[7])"""

    


def imageDetection():
    #global flagMove

    clientAlgorithmia = Algorithmia.client('sim8VSFz8+/cjSk7Cl83Rt/3KVi1')

    monfichier = clientAlgorithmia.dir("data://joachimhgg/Projet_majeur/")

    image_detect = "data://joachimhgg/Projet_majeur/image_detect.png"#"https://img.20mn.fr/9LwkkaTHRhWX31xJkaTB-Q/1200x768_chardonneret-elegant-espece-oiseau-protegee.jpg"

    # Upload local file
    print("Processing image detection...")
    clientAlgorithmia.file(image_detect).putFile("/home/yorm/Documents/pepper/Projet_majeur/WEB_SERVICE/image_detect.jpg")

    input = {
        "image": image_detect,
        "output": "data://joachimhgg/Projet_majeur/result.png",
        "min_score": 0.3,
        "model": "ssd_mobilenet_v1"
    }

    algoObject = clientAlgorithmia.algo('deeplearning/ObjectDetectionCOCO/0.2.1')
    algoObject.set_options(timeout=300) # si jamais ça dépasse 300sec on quitte

    """if len(algoObject.pipe(input).result['boxes']) == 1:
        flagMove=1"""

    for i in range(len(algoObject.pipe(input).result['boxes'])): #on boucle pour chaque objet détecté

        confidence = algoObject.pipe(input).result['boxes'][i]['confidence']
        label = algoObject.pipe(input).result['boxes'][i]['label']
        coordinates = algoObject.pipe(input).result['boxes'][i]['coordinates']
        print ("label : "+ str(label)+ "\ncoordonnées : "+ str(coordinates))

def catch_obj(totem):

    if totem == 2 : #pour prendre le totem du milieu

        pepper.setAngles(pk.left_arm_tags, pk.left_arm_work_pose, 1.0)

        print pk.left_arm_work_pose[1]
        print "--------------------------"
            
        time.sleep(1.0)
        
        current_angles = pepper.getAnglesPosition(pk.left_arm_tags)
        current_position, current_orientation = pk.right_arm_get_position(current_angles)
        print(current_position,current_orientation)
        target_position = current_position
        target_position[1] = target_position[1] + 0.05 # 5 cm toward left
        target_orientation = current_orientation # This is not supported yet
        
        target_angles = pk.right_arm_set_position(current_angles, target_position, target_orientation)
        print (target_angles.tolist())
        if target_angles.any():
            pepper.setAngles(pk.left_arm_tags, target_angles.tolist(), 1.0)

if __name__ == "__main__":
    #imageDetection()
    main()
