#!python2
#expects to run in python 2.7 with ArcPy

import os
import arcpy
import json
import sys
import re

include={"V:\\GIS_Data\\SIGEO Camera Trapping\\Final_SCBI_SIGEOCameraSamplingGrid.shp": 4, "V:\\GIS_Data\\Dragon 2011\\janpoints.csv": 14, "V:\\GIS_Data\\CRC\\BasicLayers\\natural studies area\\Natural_studies_area.shp": 1, "V:\\GIS_Data\\Dragon 2011\\rapproadclip.shp": 3, "V:\\GIS_Data\\Dragon 2011\\fred_oct_spotlight.shp": 14, "V:\\GIS_Data\\Dragon 2011\\50mfromroadselection.shp": 7, "V:\\GIS_Data\\Dragon 2011\\jantestpoints2.csv": 7, "V:\\GIS_Data\\CRC\\BasicLayers\\NAD83\\Buildings_NAD83.shp": 5, "V:\\GIS_Data\\CRC\\BasicLayers\\NAD83\\roads_nad83.shp": 11, "V:\\GIS_Data\\CRC\\BasicLayers\\NAD83\\Fence_NAD83.shp": 14, "V:\\GIS_Data\\SIGEO Camera Trapping\\Final_SCBI_SIGEOCameraSamplingGrid_label.shp": 4, "V:\\GIS_Data\\Dragon 2011\\RCL.shp": 3, "V:\\GIS_Data\\Land cover_US\\nlcd92mosaic.img": 4, "V:\\GIS_Data\\CRC\\BasicLayers\\NAD27\\100x100_meter_veg_plots.shp": 2, "V:\\GIS_Data\\Regional\\Virginia\\VAoutline.shp": 4, "V:\\GIS_Data\\Dragon 2011\\Octspotlightpoints.shp": 7, "V:\\GIS_Data\\SIGEO Camera Trapping\\SCBI_SIGEOCameraSampling24haGrid.shp": 4, "total": 0, "V:\\GIS_Data\\CRC\\BasicLayers\\NAD27\\200x200_meter_grids.shp": 1, "V:\\GIS_Data\\CRC\\BasicLayers\\NAD27\\landuse06.shp": 5, "V:\\GIS_Data\\Dragon 2011\\rappsurveyroadsshp.shp": 3, "V:\\GIS_Data\\CRC\\BasicLayers\\NAD27\\roads(best).shp": 14, "V:\\GIS_Data\\Dragon 2011\\eastparcels.shp": 3, "V:\\GIS_Data\\CRC\\crcvegmap\\centralgrid": 1, "V:\\GIS_Data\\CRC\\BasicLayers\\NAD83\\stream_NAD83.shp": 16, "V:\\GIS_Data\\CRC\\BasicLayers\\NAD27\\fence.shp": 12, "V:\\GIS_Data\\Dragon 2011\\jantestpoints.csv": 7, "V:\\GIS_Data\\National_Parks\\nps_boundary\\nps_boundary.shp": 4, "V:\\GIS_Data\\Land cover_US\\NLCD2006_landcover_4-20-11_se5\\nlcd2006_landcover_4-20-11_se5.img": 45, "V:\\GIS_Data\\SIGEO Camera Trapping\\Final_SCBI_SIGEOCameraSampling24haGrid_label.shp": 4, "V:\\GIS_Data\\Land cover_US\\NLCD2011\\nlcd_2011_landcover_2011_edition_2014_03_31.img": 16, "V:\\GIS_Data\\Regional\\statesp020\\statesp020.shp": 4, "V:\\GIS_Data\\Dragon 2011\\deergisaddrappaltered.csv": 3, "V:\\GIS_Data\\Dragon 2011\\rappsurveyclipped.shp": 6, "V:\\GIS_Data\\CRC\\BasicLayers\\NAD27\\boundary.shp": 16, "V:\\GIS_Data\\DEM\\DEM10m\\dem-crc.img": 1, "V:\\GIS_Data\\CRC\\BasicLayers\\NAD83\\roads_posey.shp": 6, "V:\\GIS_Data\\CRC\\BasicLayers\\NAD27\\hab_TM.shp": 5, "V:\\GIS_Data\\Dragon 2011\\spotlight272.csv": 7, "V:\\GIS_Data\\CRC\\posey\\posey.shp": 1, "V:\\GIS_Data\\CRC\\BasicLayers\\NAD27\\STREAMS.shp": 2, "V:\\GIS_Data\\DEM\\DEM10m\\dem-sigeo": 2, "V:\\GIS_Data\\DEM\\DEM30mStates\\Merged.tif": 8, "V:\\GIS_Data\\Dragon 2011\\deergisaddrapp.csv": 3, "V:\\GIS_Data\\Dragon 2011\\surveyroadsfred.shp": 7, "V:\\GIS_Data\\Dragon 2011\\westparcels.shp": 3}

def find_maps(top):#takes a folder and recursively findas all the .mxd files contained
    maps = []
    for root, dirs, files in os.walk(top):
        for f in files:
            if re.search("\.mxd$",f):
                print f
                maps.append(os.path.join(root,f))
    return maps

def ignore_old_files(directory,files):
    ignore = []
    pathlist = [os.path.normpath(key) for key in include]
    for item in files:
        fp = os.path.join(directory,item)
        time = os.path.getmtime(fp)
        if not os.path.isdir(fp):
            if time < 1451606400.0:
                if os.path.normpath(fp) not in pathlist:
                    ignore.append(item)
        elif len(os.listdir(fp)) == 0:
            ignore.append(item)
    return ignore

#takes a list of paths to map document files, and two strings, first to match, second to replace.    
def replace_path(maps,ogPath,newPath):
    stillMissing = {'total':0}
    i=0
    for map in maps:
        try:
            i+=1
            print(str(i)+" :: "+map)
            document = arcpy.mapping.MapDocument(map)
            try:
                document.findAndReplaceWorkspacePaths(ogPath,newPath)
                document.save()
            except IOError as e:
                print(e)
                print(map)
                stillMissing[map] = "Error :: "+str(e)
            docMissing = arcpy.mapping.ListBrokenDataSources(document)
            stillMissing[map] = []
            for j in docMissing:
                stillMissing['total'] += 1
                try:
                    stillMissing[map].append(j.dataSource)
                except:
                    e = sys.exc_info()[0]
                    print(e)
                    print(j.name + "in" + map)
                    stillMissing[map] = "Error :: "+str(e)
        except:
            e = sys.exc_info()[0]
            print(e)
            print(map)
            stillMissing[map] = "Error :: "+str(e)
    return stillMissing

def find_GIS_Files(maps,files={},root="V:\GIS_Data"):
    i=0
    for map in maps:
        i+=1
        print(str(i)+" :: "+map)
        document = arcpy.mapping.MapDocument(map)
        try:
            for lyr in arcpy.mapping.ListLayers(document):
                if lyr.supports("DATASOURCE"):
                    if root in lyr.dataSource:
                        files[lyr.dataSource] = 1 if not lyr.dataSource in files else files[lyr.dataSource]+1
        except:
            e = sys.exc_info()[0]
            print(e)
            print(map)
    return files

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
    logfile = logfile if (os.path.isdir(os.path.normpath(logfile)) and logfile != '') else os.path.join(top,"missing.json")
    with open(logfile,'w') as f:
        f.write(json.dumps(missed))
    print('Any remaining broken sources have been saved as '+str(os.path.realpath(logfile)))
    print('Read this JSON file by copy and pasting in in an online tool such as https://jsonformatter.org/')