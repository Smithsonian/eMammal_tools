import os
import pandas
import re
import shutil

def sort_deps(path):
    deployments = {}
    for x in os.listdir(path):
        os.chdir(path)
        if os.path.isdir(x):
            print(x)
            try:
                xml = open(x+'\\deployment_manifest.xml','r').read()
                actualfiles = os.listdir(x)
                sort_images(xml, x, actualfiles)
            except:
                xml = False
                print("No deployment manifest in "+x)

def sort_images(xml, folder, actualfiles):#takes an XML string and list of filenames, moves the files to folders named by the species in them.
    exp = re.compile("<Image>.*?<ImageFileName>(.*?)</ImageFileName>.*?<SpeciesScientificName>(.*?)</SpeciesScientificName>.*?</Image>",re.DOTALL)
    xmlfiles = exp.findall(xml)
    for file in xmlfiles:
        if file[0] in actualfiles:
            if not os.path.isdir('./'+file[1]):
                print("making directory"+file[1])
                os.mkdir('./'+file[1])
            shutil.copyfile('./'+folder+'/'+file[0], './'+file[1]+'/'+file[0])