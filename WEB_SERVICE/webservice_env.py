#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon May 27 09:08:19 2019

@author: yorm
"""
import cv2
import time
import pybullet
import pybullet_data
from qibullet import PepperVirtual
from qibullet import SimulationManager
import Algorithmia

#----------------------INITIALISATION-----------------------------------------


flagMove=0
def main():
    global flagMove

    flagPriseImg =0
    flagDetectionObjet =0

    simulation_manager = SimulationManager()
    clientEnv = simulation_manager.launchSimulation(gui=True)
    pepper = simulation_manager.spawnPepper(clientEnv, spawn_ground_plane=True)

    pybullet.setAdditionalSearchPath(pybullet_data.getDataPath())

    totem1= [2, 0, 0.5]
    totem2= [2.5, 0, 0.5]
    totem3= [3, 0, 0.5]
#-----------------------------------------------------------------------------

#----------------------------FONCTION LOAD OBJET-------------------------------
    pybullet.loadURDF(
        "table.urdf",
        basePosition=[2.5, 0, 0],
        globalScaling=0.7,
        physicsClientId=clientEnv)

    pybullet.loadURDF(
        "Corona.urdf",
        basePosition=totem1,
        globalScaling=0.2,
        physicsClientId=clientEnv)
    pybullet.loadURDF(
        "Corona.urdf",
        basePosition=totem2,
        globalScaling=0.2,
        physicsClientId=clientEnv)
    pybullet.loadURDF(
        "Corona.urdf",
        basePosition=totem3,
        globalScaling=0.2,
        physicsClientId=clientEnv)
 #----------------------------------------------------------------------------

    pepper.showLaser(True)
    pepper.subscribeLaser()
    pepper.goToPosture("Stand", 0.6)
    cv2.waitKey(0)

    pepper.subscribeCamera(PepperVirtual.ID_CAMERA_BOTTOM)

    #pepper.moveTo(2.5,2.,0.) 
    a=0
    b=0
    ok=0
    #on tourne jusqu'à ce qu'on soit bien en face de la table
    laser_list= pepper.getFrontLaserValue()
    print(laser_list)
    list_i = [0,13] #on choisi les lasers qui ne détecte pas la table

    while ((b==0) or (a==0) ):
        

        for i in list_i:   
            if (laser_list[i]==3.0):
                ok+=1
            laser_list.pop(i)
        if ok == len(list_i): #len(list_i)
            b=1
        else:
            ok=0

        pepper.moveTo(0,0,0.1)

        if all(laser_list < 3.0 for laser in laser_list):
            a=1
        else:
            a=0
        print(a)

        laser_list= pepper.getFrontLaserValue()
        print(laser_list)


    while True:

        #laser_list = pepper.getRightLaserValue()
        #laser_list.extend(pepper.getFrontLaserValue())
        #laser_list.extend(pepper.getLeftLaserValue())
        laser_list= pepper.getFrontLaserValue()
        print(laser_list)

        if all(laser == 5.6 for laser in laser_list):
            print("Nothing detected")
            flagMove=1
        else:
            if flagPriseImg == 70000:
                print("Detected")
                flagPriseImg =0
                img = pepper.getCameraFrame()
                cv2.imshow("bottom camera", img)
                cv2.imwrite('/home/yorm/Documents/pepper/Projet_majeur/WEB_SERVICE/image_detect.jpg', img)
                cv2.waitKey(1)

                if flagDetectionObjet == 5:
                    flagDetectionObjet=0
                    imageDetection()

                flagDetectionObjet+=1
            else:
                flagPriseImg+=1
            pass
        if flagMove ==1:
            flagMove=0
            #pepper.moveTo(pepper, posX,posY, 0)


def imageDetection():
    global flagMove

    clientAlgorithmia = Algorithmia.client('sim8VSFz8+/cjSk7Cl83Rt/3KVi1')

    monfichier = clientAlgorithmia.dir("data://joachimhgg/Projet_majeur/")

    image_detect = "data://joachimhgg/Projet_majeur/image_detect.png"#"https://img.20mn.fr/9LwkkaTHRhWX31xJkaTB-Q/1200x768_chardonneret-elegant-espece-oiseau-protegee.jpg"

    # Upload local file
    print("Image detection")
    clientAlgorithmia.file(image_detect).putFile("/home/yorm/Documents/pepper/Projet_majeur/WEB_SERVICE/image_detect.jpg")

    """    # Download contents of file as a string
    if clientAlgorithmia.file(image_detect).exists() is True:
        clientAlgorithmia.file(image_detect).putFile("/home/yorm/Documents/pepper/Projet_majeur/WEB_SERVICE/image_detect.jpg")
    """
     

    #image_detect = "https://img.20mn.fr/9LwkkaTHRhWX31xJkaTB-Q/1200x768_chardonneret-elegant-espece-oiseau-protegee.jpg"
    input = {
        "image": image_detect,
        "output": "data://joachimhgg/Projet_majeur/result.png",
        "min_score": 0.1,
        "model": "ssd_mobilenet_v1"
    }

    algoObject = clientAlgorithmia.algo('deeplearning/ObjectDetectionCOCO/0.2.1')
    algoObject.set_options(timeout=300) # si jamais ça dépasse 300sec on quitte

    if len(algoObject.pipe(input).result['boxes']) == 1:
        flagMove=1

    for i in range(len(algoObject.pipe(input).result['boxes'])): #on boucle pour chaque objet détecté

        confidence = algoObject.pipe(input).result['boxes'][i]['confidence']
        label = algoObject.pipe(input).result['boxes'][i]['label']
        coordinates = algoObject.pipe(input).result['boxes'][i]['coordinates']
        print ("label : "+ str(label)+ "\ncoordonnées : "+ str(coordinates))

if __name__ == "__main__":
    #imageDetection()
    main()
