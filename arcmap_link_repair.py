#!python2
#expects to run in python 2.7 with ArcPy

import os
import arcpy
import json

def find_maps(top):#takes a folder and recursively findas all the .mxd files contained
    maps = []
    for root, dirs, files in os.walk(top):
        for f in files:
            if ".mxd" in f:
                print f
                maps.append(os.path.join(root,f))
    return maps
    
def replace_path(maps,ogPath,newPath):
    stillMissing = {'total':0}
    i=0
    for map in maps:
        i+=1
        print(i)
        document = arcpy.mapping.MapDocument(map)
        document.findAndReplaceWorkspacePaths(ogPath,newPath)
        docMissing = arcpy.mapping.ListBrokenDataSources(document)
        stillMissing[map] = [j.dataSource for j in docMissing]
        stillMissing['total'] += len(stillMissing[map])
        document.save()
    return stillMissing
    
def find_GIS_Files(maps,ogPath,newPath):
    stillMissing = {'total':0}
    i=0
    for map in maps:
        i+=1
        print(i)
        document = arcpy.mapping.MapDocument(map)
        document.findAndReplaceWorkspacePaths(ogPath,newPath)
        docMissing = arcpy.mapping.ListBrokenDataSources(document)
        stillMissing[map] = [j.dataSource for j in docMissing]
        stillMissing['total'] += len(stillMissing[map])
        document.save()
    return stillMissing

if __name__ == '__main__':
    top = raw_input("Paste the path to the top level directory you would like to repair:\n")
    maps = find_maps(top)
    print("Found "+str(len(maps))+" MXD files.")
    old_path = raw_input("Paste the old path that you would like to replace, e.g. 'V:\<folderA>'")
    print(old_path)
    new_path = raw_input("Paste the new path that you would like to replace, e.g. 'T:\<folder>\<folderA>'")
    print(new_path)
    #missed = replace_path(maps,"V:\\","T:\\")
    #missed = replace_path(maps,"O:\\Field Ecology\\Lovely, Deer","T:\\Lovely, Deer")
    #missed = replace_path(maps,r"V:\Lovely, Deer\GIS_Data\Rappahannock County",r"T:\Lovely, Deer\GIS_Data\Rappahannock County\Old Files")
    #missed = replace_path(maps,r"O:\Field Ecology\Lovely, Deer\GIS_Data\Frederick County",r"T:\Lovely, Deer\GIS_Data\Frederick County\Old Shapefiles")
    missed = replace_path(maps,old_path,new_path)
    logfile = raw_input("Where would you like to save the summary of remaining broken data sources?")
    with open(logfile,'w') as f:
        f.write(json.dumps(missed))
    print('Any remaining broken sources have been saved as '+str(os.path.realpath(logfile)))
    print('Read this JSON file by copy and pasting in in an online tool such as https://jsonformatter.org/')