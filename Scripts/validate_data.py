import pandas
import json
import math
import numpy
import re
import zipfile
import os
import argparse

############################
#pre-manifest validation
#
#the dictionaries list regex rules for fields
#these functions check csv files to make sure the values are allowed for import into eMammal
allowedimg = {
    'Deployment.ID1':'d[0-9]{5}',
    'Deployment.ID' : '.+',
    'Image.Sequence.ID' : '.*',
    'Image.ID' : '.+',
    'Image.File.Name' : '.+\.JPG',
    'Photo.Type' : '.*',
    'Photo.Type.Identified.by' : '.*',
    'Location' : '.*',
    'Genus.Species' : '.*',
    'Species.Common.Name' : '.*',
    'TSN.ID' : '(\d+)',
    'IUCN.ID' : '(\d+)',
    'IUCN.Status' : '(LC|NT|VU|EN|CR|EW|EX|DD|NE|US)',
    'Date_Time' : '.*',
    'Interest.Rank' : '(None|Favorite)',
    'Age' : '(Adult|Juvenile|Unknown|nan)',
    'Sex' : '(Male|Female|Unknown|nan)',
    'Individual.ID' : '.*',
    'Count' : '(nan|\d+)',
    'Animal.recognizable' : '.*',
    'Individual.Animal.Notes' : '.*',
    'Digital.Origin' : '.*',
    'Embargo.Period' : '.*',
    'Restrictions.on.Access' : '.*',
    'Image.Use.Restrictions' : '.*'
    }#this dictionary maps all the columns to a regular expression that validates the column contents

alloweddep = {
    'Camera.Deployment.ID1': 'd[0-9]{5}',
    'Camera.Deployment.ID': '.+',
    'Camera.Site.Name' : '.+',
    'Camera.Deployment.Begin.Date': '\d{1,2}/\d{1,2}/\d{4}',
    'Camera.Deployment.End.Date' : '\d{1,2}/\d{1,2}/\d{4}',
    'Actual.Latitude' : '-?\d{1,3}\.?\d*',
    'Actual.Longitude' : '-?\d{1,3}\.?\d*',
    'Camera.Failure.Details' : '(Camera Functioning|Wildlife Damage|Camera Hardware Failure|Memory Card/Film Failure|Vandalism/Theft|Unknown Failure)',
    'Bait' : '(No Bait|Other Bait|Acoustic|Visual|Meat|Scent)',
    'Bait.Description' : '.*',
    'Feature' : '(Not Entered|Road, paved|Road, dirt|Trail, hiking/people|Trail, game|Road underpass/overpass/bridge|Culvert|Burrow|Nest site|Carcass|Water source/Spring|Fruiting tree|Other)',
    'Feature.Methodology' : '.*',
    'Camera.ID' : '.+',
    'Quiet.Period.Setting' : '(nan|\d+)',
    'Sensitivity.Setting' : '(high|medium|low)',
    'Subproject.Name' : '.+',
    'Subproject.ID' : '\w+\d+'
    }#this dictionary maps deployment fields to regular expressions


def validate_images_csv(file):
    df = pandas.read_csv(file)
    return validate_df(df, allowedimg)

def validate_deployments_csv(file):
    df = pandas.read_csv(file)
    return validate_df(df, alloweddep)

#this will check that most fields of the final dataframe have acceptable values, doesn't check datetime format or if the species match emammal, it returns a dictionary summarizing the fields as well as listing errors. It is recommended that you check all the field summaries for issues this function may not have caught
def validate_df(df, allowed):
    response = {'errors':{}}
    for column in df.columns:#check each column
        #print(column)
        values = df[column].unique().tolist()
        response[column] = values
        for value in values:#check each value in the column
            if column in allowed.keys():
                if not re.match(allowed[column], str(value)):
                    if column in response['errors']:
                        response['errors'][column].append(value)
                    else:
                        response['errors'][column] = [value]
                    #print("Value not allowed in column")
                    #print(column+'::'+str(value))
            else:
                raise ValueError('CSV contains incorrect column')
    return response

##################################
#post manifest creation validation
#
#This is intended to be run on either folders containing images and XMLs or on zips of the same.
#The path should be the directory containing the deployments
#
#The validate_filenames function takes a string containing an emammal XML file and a list of filenames and compares them, looking for errors
def check_folders(path): #verify the integrity of folders that already contain the manifest.
    deployments = {}
    for x in os.listdir(path):
        os.chdir(path)
        if os.path.isdir(x):
            print(x)
            try:
                xml = open(x+'\\deployment_manifest.xml','r').read()
                actualfiles = [x for x in os.listdir(x) if x != 'deployment_manifest.xml']#this list is all files except the deployment manifest
                errors = validate_filenames(xml, actualfiles, verbose=True)
                deployments[x] = errors
            except:
                xml = False
                print("No deployment manifest in "+x)
    return deployments
                    
def check_zip_folders(path): #takes a path to a folder of zipped deployments and validates the contents of the folder and XML
    deployments = {}
    for x in os.listdir(path):
        os.chdir(path)
        if zipfile.is_zipfile(x):
            z = zipfile.ZipFile(x) 
            print(x)
            try:
                xml = z.read('deployment_manifest.xml').decode('latin')
                actualfiles = [x for x in z.namelist() if x != 'deployment_manifest.xml']#this list is all files except the deployment manifest
                errors = validate_filenames(xml, actualfiles, verbose=True)
                deployments[x] = errors
            except IOError:
                xml = False
                print("No deployment manifest in "+x)
            z.close()
        else:
            print(x)
            print("Error")
    return deployments

def validate_filenames(xml, actualfiles, verbose=False):#takes an XML string and list of filenames, returns a dictionary of errors, set verbose to true for a dictionary describing the errors.
    exp = re.compile("<Image>.*?<ImageFileName>(.*?)</ImageFileName>.*?<SpeciesScientificName>(.*?)</SpeciesScientificName>.*?</Image>",re.DOTALL)#use regex to find all images and their species in the xml
    xmlfiles = exp.findall(xml)
    valid = True
    errors = {'typeerrors':[],'imageerrors':[],'xmlerrors':[]}
    for file in actualfiles:#check each file in the folder
        if not re.match('.*(.jpg|.xml)',file, re.IGNORECASE):#check that all files in the folder are allowed
            valid = False
            errors['typeerrors'].append(file)
            #print('--Folders must contain only jpgs or xmls ::: '+x+'\\'+file)
        if file not in [i[0] for i in xmlfiles] and file != 'deployment_manifest.xml':#check that each file is listed in the xml, list comprehension gets file name from (filename, species) tuples 
            valid = False
            errors['imageerrors'].append(file)
            #print('--folder contains images not in XML :: '+file)
    for file in xmlfiles:#check that all files are listed in the XML
        if file[0] not in actualfiles:
            valid = False
            errors['xmlerrors'].append(file)
            #print('--XML contains images not in folder :: '+str(file))
    if len(xmlfiles) != len(actualfiles):#here we check if the xml has the same number of photos as the folder, this fails when there are duplicates in the XML
        valid = False
        errors['lengtherrors'] = [[len(xmlfiles),len(actualfiles)]]
    errors['valid'] = valid
    return errors if verbose else valid

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('type', choices=['zip','folder'], help='Either "zip" or "folder"')
    parser.add_argument('folder', help='What is the path of the parent folder containing the deployments?')
    parser.add_argument('output', help='Where should the summary json file be saved?')
    args = parser.parse_args()
    deployments = {}
    if args.type == 'zip':
        deployments = check_zip_folders(args.folder)
    if args.type == 'folder':
        deployments = check_folders(args.folder)
    output = args.output+'.json'
    errors = {i:deployments[i] for i in deployments if not deployments[i]['valid']}
    try:
        with open(output, 'w') as file:
            file.write(json.dumps(errors))
    except:
        output = 'output.json'
        with open(output, 'w') as file:
            file.write(json.dumps(errors))
    print('The output of invalid files has been saved to '+str(os.path.realpath(output)))
    
if __name__ == "__main__":
    main()