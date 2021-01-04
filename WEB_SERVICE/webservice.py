#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon May 27 09:08:19 2019

@author: yorm
"""



import Algorithmia

client = Algorithmia.client('sim8VSFz8+/cjSk7Cl83Rt/3KVi1') #objet client

# -*- coding: utf-8 -*-

"""
input = {
  "image": "https://img.20mn.fr/9LwkkaTHRhWX31xJkaTB-Q/1200x768_chardonneret-elegant-espece-oiseau-protegee.jpg",
  "output": "data://joachimhgg/Projet_majeur/result1.json"
}

algoSalNet = client.algo('deeplearning/SalNet/0.2.2')
algoSalNet.set_options(timeout=300) # optional
print(algoSalNet.pipe(input).result)

input = {
  "file": "data://media/videos/2016-10-31_11-28-11.mp4",
  "confidence": 0.5,
  "fps": 1
}
algoVideo = client.algo('media/DetectVideoObjects/0.1.1')
algoVideo.set_options(timeout=300) # optional
print(algoVideo.pipe(input).result)
"""

#client.dir("data://joachimhgg/Projet_majeur/").create() #pour créer un dossier
monfichier = client.dir("data://joachimhgg/Projet_majeur/")

image_detect = "data://joachimhgg/Projet_majeur/image_detect.png"#"https://img.20mn.fr/9LwkkaTHRhWX31xJkaTB-Q/1200x768_chardonneret-elegant-espece-oiseau-protegee.jpg"
# Upload local file
if client.file(image_detect).exists() is False:
    client.file(image_detect).putFile("/home/yorm/Documents/pepper/Projet_majeur/WEB_SERVICE/image_detect.jpg")

# Download contents of file as a string
if client.file(image_detect).exists() is True:
    input = client.file(image_detect).getString()

input = {
  "image": image_detect,
  "output": "data://joachimhgg/Projet_majeur/result.png",
  "min_score": 0.7,
  "model": "ssd_mobilenet_v1"
}

algoObject = client.algo('deeplearning/ObjectDetectionCOCO/0.2.1')
algoObject.set_options(timeout=300) # si jamais ça dépasse 300sec on quitte

for i in range(len(algoObject.pipe(input).result['boxes'])): #on boucle pour chaque objet détecté
	
	confidence = algoObject.pipe(input).result['boxes'][i]['confidence']
	label = algoObject.pipe(input).result['boxes'][i]['label']
	coordinates = algoObject.pipe(input).result['boxes'][i]['coordinates']
	print ("label : "+ str(label)+ "\ncoordonnées : "+ str(coordinates))



