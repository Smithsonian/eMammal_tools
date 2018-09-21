from bs4 import UnicodeDammit
import requests
from bs4 import BeautifulSoup
import pandas
import json
import math
import numpy

token = '2103c15b0319ba05e7de13619aa6b7afaa68037ab347c19591a3854fb3380a5f'

def get_IUCN_id_status(name,token):
    url = 'http://apiv3.iucnredlist.org/api/v3/species/'+name+'?token='+token
    request = requests.get(url)
    if request.status_code == 200:
        response = json.loads(request.text)
        if 'result' in response:
            if(len(response['result'])>0):
                index = 0
                if len(response['result']) > 1:
                    for i in response:
                        print(i+' : '+response['result'][i]['taxonid'])
                    index  = input("Which one?")
                IUCNid = response['result'][index]['taxonid']
                IUCNstatus = response['result'][index]['category']
                return {'IUCNid':IUCNid,'IUCNstatus':IUCNstatus}
    else:
        return({'error':request.status_code})

def get_IUCN_country(id,token):
    print(id)
    url = 'http://apiv3.iucnredlist.org/api/v3/species/countries/id/'+id+'?token='+token
    print(url)
    request = requests.get(url)
    if request.status_code == 200:
        response = json.loads(request.text)
        if 'result' in response:
            if(len(response['result'])>0):
                countries = []
                for i in response['result']:
                    print(i)
                    countries.append(i['code'])
                    print(i['country'])
                return countries
        else:
            return('no results')
    else:
        return('error')

def build_species_IUCN_keys(observations):
    species = {}
    for index, row in observations.iterrows():
        if type(row["Genus.Species"]) == str:
            if row["Genus.Species"] not in species:
                print(row["Genus.Species"])
                species[row["Genus.Species"]] = get_IUCN_id_status(row["Genus.Species"],token)
    return species

if __name__ == '__main__':
    wanglang['IUCN.ID'] = wanglang.apply(set_IUCN_id,axis=1,args=(species,))
    wanglang['IUCN.Status'] = wanglang.apply(set_IUCN_status,axis=1,args=(species,))
    mammalmisdet['Country'] = mammalmisdet['IUCN_ID:'].apply(get_IUCN_country,args=(token,))
