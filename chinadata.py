from bs4 import UnicodeDammit
import requests
from bs4 import BeautifulSoup
import pandas
import json
import math
import numpy
import re

token = '2103c15b0319ba05e7de13619aa6b7afaa68037ab347c19591a3854fb3380a5f'

input = ''
    
def reorganize_images():#this function takes in data specifically from HongLiangs china dataset to reorder with pandas.
    columnsrenamed = {'Scientific_Name':'Genus.Species','Class':'Species.Common.Name','Number.of.Individuals':'Count'}
    rename = observations.rename(columnsrenamed,axis=1)
    newcolumns = ['Deployment.ID1','Image.Sequence.ID','Location','Photo.Type','Photo.Type.Identified.by','TSN.ID','IUCN.ID','IUCN.Status','Date_Time','Interest.Rank','Age','Individual.ID','Animal.recognizable','Individual.Animal.Notes','Digital.Origin','Embargo.Period','Restrictions.on.Access','Image.Use.Restrictions']
    for column in newcolumns:
        rename[column] = numpy.NaN
    rename['Date_Time'] = rename['Date'] +' '+ rename['Time']
    columnordering = ['Deployment.ID1','Deployment.ID','Image.Sequence.ID','Image.ID','Location','Image.File.Name','Photo.Type','Photo.Type.Identified.by','Genus.Species','Species.Common.Name','TSN.ID','IUCN.ID','IUCN.Status','Date_Time','Interest.Rank','Age','Sex','Individual.ID','Count','Animal.recognizable','Individual.Animal.Notes','Digital.Origin','Embargo.Period','Restrictions.on.Access','Image.Use.Restrictions']
    rename_reshape = rename[columnordering]
    return rename_reshape

def reorganize_deployments():#this function is incomplete but could be completed like reorganize_images
    df.combine(df2,axis=1)
    renaming = {'Camera Deployment ID':'Camera.Deployment.ID','Latitude':'Actual.Latitude', 'Longitude':'Actual.Longitude','Camera Deployment Begin Date':'Camera.Deployment.Begin.Date', 'Camera Deployment End Date':'Camera.Deployment.End.Date','Camera ID':'Camera.ID', 'Quiet Period Setting':'Quiet.Period.Setting', 'Sensitivity Setting':'Sensitivity.Setting','Bait Description':'Bait.Description','Feature Description':'Feature.Methodology','Quiet Period Setting':'Quiet.Period.Setting','Sensitivity Setting':'Sensitivity.Setting'}
    targetcolumns = ['Camera.Deployment.ID1', 'Camera.Deployment.ID', 'Camera.Site.Name', 'Camera.Deployment.Begin.Date', 'Camera.Deployment.End.Date', 'Actual.Latitude', 'Actual.Longitude', 'Camera.Failure.Details', 'Bait', 'Bait.Description', 'Feature', 'Feature.Methodology', 'Camera.ID', 'Quiet.Period.Setting', 'Sensitivity.Setting']
    newcolumns = ['Camera.Site.Name','Camera.Failure.Details']


def find_id_matches(data,payload):#takes a dataframe and HTTP headers and returns a dictionary of old deploymentids paired with new deploymentids
    deployments = {}
    for index, row in data.iterrows():
        if row["Deployment.ID"] not in deployments:
            deployments[row["Deployment.ID"]] = extract_deploymentid(row["Deployment.ID"],payload)
    return deployments

def add_deploymentids():
    returns

def get_deployment_ids(row,idpairs):
    return idpairs[row['Deployment.ID']]

def set_IUCN_status(row):
    if pandas.notnull(row["Genus.Species"]):
        if type(species[row["Genus.Species"]]) == dict:
            return species[row["Genus.Species"]]["IUCNstatus"]
        else:
            return None
    else:
        return None

def set_IUCN_id(row):
    if pandas.notnull(row["Genus.Species"]):
        if type(species[row["Genus.Species"]]) == dict:
            return species[row["Genus.Species"]]["IUCNid"]
        else:
            return None
    else:
        return None

def set_tsn(row,tsniucn):
    if not math.isnan(row['IUCN.ID']):
        if int(row['IUCN.ID']) in tsniucn:
            print('success:::::'+str(row['IUCN.ID']))
            return masterindexed.loc[int(row['IUCN.ID'])]['TSN']
        else:
            if not math.isnan(row['IUCN.ID']):
                print('Error on ::'+str(row['Genus.Species'])+' :: '+str(row['IUCN.ID']))
                errors[row['Genus.Species']] = row['IUCN.ID']
    else:
        return None

def set_start_date(row,image_df):
    deploy_name = row["Camera.Deployment.ID"]
    return iamge_df[image_df["Deployment.ID"] == deploy_name]["Date.Time"].min()

def set_end_date(row,image_df):
    deploy_name = row["Camera.Deployment.ID"]
    return iamge_df[image_df["Deployment.ID"] == deploy_name]["Date.Time"].max()

def replaceUnknownBirds(row, matches):
    if row['Genus.Species'] in matches:
        print("FOUNDIT")
        row['Individual.Animal.Notes'] = row['Genus.Species']
        row['Genus.Species'] = "Unknown Bird"
        row['Species.Common.Name'] = "Unknown Bird"
        print(row)
    return row

#if __name__ == '__main__':
#    observations = pandas.read_csv(input)
#    master_indexed = pandas.read_csv(emammalmaster).set_index('IUCN_ID')
#    errors = {}
#    wanglang['IUCN.ID'] = wanglang.apply(set_IUCN_id,axis=1,args=(species,))
#    wanglang['IUCN.Status'] = wanglang.apply(set_IUCN_status,axis=1,args=(species,))
#    wanglang = wanglang.apply(func=replaceUnknownBirds,axis=1,args=(birds,))

#wanglang = pandas.read_csv("Wanglang NR_2014-2017-utf-8.csv")
#wanglang['Deployment.ID1'] = wanglang.apply(get_value,axis=1,args=(idpairs,))
