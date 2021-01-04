# -*- coding: utf-8 -*-
"""
Created on Mon May 27 13:52:16 2019

@author: nicolas
"""
import random
import pybullet
import pybullet_data
from qibullet import PepperVirtual
from qibullet import SimulationManager

#----------------------INITIALISATION-----------------------------------------
def main():
    simulation_manager = SimulationManager()        
    client = simulation_manager.launchSimulation(gui=True)
    pepper = simulation_manager.spawnPepper(client, spawn_ground_plane=True)
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
        physicsClientId=client)
        
    pybullet.loadURDF(
        "totem_Tortue.urdf",
        basePosition=[2.0, liste_coord_y[0], 0.7],
        globalScaling=2.0,
        physicsClientId=client)
        
    pybullet.loadURDF(
        "totem_Parrot.urdf",
        basePosition=[2.0, liste_coord_y[1], 0.7],
        globalScaling=2.0,
        physicsClientId=client)
        
    pybullet.loadURDF(
        "totem_Cat.urdf",
        basePosition=[2.0, liste_coord_y[2], 0.7],
        globalScaling=2.0,
        physicsClientId=client)

    pybullet.loadURDF(
        "caisse.urdf",
        basePosition=[0.5, 2, 0.1],
        globalScaling=0.2,
        physicsClientId=client)

    pybullet.loadURDF(
        "cage.urdf",
        basePosition=[0.5, -2, 0.4],
        globalScaling=0.9,
        physicsClientId=client)

    pybullet.loadURDF(
        "panier.urdf",
        basePosition=[-1.5, -0.05, 0.1],
        globalScaling=0.45,
        physicsClientId=client)
        
 #----------------------------------------------------------------------------

    pepper.showLaser(True)
    pepper.subscribeLaser()
    pepper.goToPosture("Stand", 0.6)

    while True:
        laser_list = pepper.getRightLaserValue()
        laser_list.extend(pepper.getFrontLaserValue())
        laser_list.extend(pepper.getLeftLaserValue())

        if all(laser == 5.6 for laser in laser_list):
            print("Nothing detected")
        else:
            print("Detected")
            pass


if __name__ == "__main__":
    main()

