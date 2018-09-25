import json
import csv
import requests
import requests
import time
import pandas
import argparse



details = {}

#this function gets the IDs for the Researcher Observations and the Image Observations from the database
#it will only work on an SI computer that has access to solr
def getPID(dep_names):#returns a dict of deployment names with documents and their PIDs
    deployments = {}
    for deployment in dep_names:
        print(deployment)
        deployments[deployment] = {}
        request_id = requests.get("http://oris-srv04.si.edu:8090/solr/gsearch_sianct/select?q=ctLabel%3A"+deployment+"&wt=json&indent=true")#creates a URL to search for the deployment
        response = json.loads(request_id.text)
        docs = response['response']['docs']
        for doc in docs:#makes a dictionary of document names and their PIDs
            deployments[deployment][doc['datasetLabel']] = doc["PID"]
            print(doc['datasetLabel'])
    return deployments

def getDeploymentctPID(baseurl, depid):
	params = {"wt":"json"}
	params["q"] = "cameraCiteinfo:"+str(depid)
	request = requests.get(baseurl, params)
	print(request.url)
	returnedobject = json.loads(request.text)
	return returnedobject["response"]["docs"][0]["ctPID"].encode('utf-8')
    
def getCSV(deployments):#downloads CSVs of observations, expects dict formatted as getPID() response
    cookie = input("Paste the session cookie from your workbench session. In chrome hit f12 click network, load a page, select the first row, go to request headers and copy the cookie string.\n\n")
    payload = {"Host": "workbench.sidora.si.edu"
    ,"Connection": "keep-alive"
    ,"Accept": "application/json, text/javascript, */*; q=0.01"
    ,"X-Requested-With": "XMLHttpRequest"
    ,"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
    ,"Referer": "https://workbench.sidora.si.edu/sidora/workbench/"
    ,"Accept-Encoding": "gzip, deflate, br"
    ,"Accept-Language": "en-US,en;q=0.9"
    ,"Cookie": cookie}
    for deployment in deployments:
        for doc in deployments[deployment]:
            csv_response = requests.get("https://workbench.sidora.si.edu/sidora/info/"+str(deployments[deployment][doc])+"/meta/OBJ/download", headers=payload)
            if csv_response.status_code == 200:
                file = open(doc+deployment+".csv","w")
                print(type(csv_response.text))
                file.write(csv_response.text)
            else:
                print(str(deployment) + "Error :: " + str(csv_response.status_code))

def getDepStatus(df):#takes a row of a dataframe, finds a column named Deployments, and returns True or False
    request_id = requests.get("http://oris-srv04.si.edu:8090/solr/gsearch_sianct/select?q=ctLabel%3A"+df['Deployments']+"&wt=json&indent=true")#creates a URL to search for the deployment
    response = json.loads(request_id.text)
    if request_id.status_code == 200:
        docs = response['response']['docs']
        if len(docs)>1:
            return True
        else:
            return False
    else:
        print(request_id.status_code)
        print(df['Deployments'])

if __name__ == '__main__':#this allows this file to be run as a script or imported as a package
    parser = argparse.ArgumentParser()
    parser.add_argument('--getcsvs', help='True if you want to download the CSVs from workbench')
    parser.add_argument('--fromcsv', help='a path to a CSV containing a column named Deployments, returns results to <this file>_results.csv')#specify in order to fill a field in a CSV
    args = parser.parse_args()
    if args.fromcsv:
        df = pandas.read_csv(args.fromcsv)
        df['Uploaded'] = df.apply(getDepStatus, axis=1)
        df.to_csv(args.fromcsv+'_results.csv')
    else:
        deps = input("paste a list of deployment names split by spaces").split()
        print(deps)
        details = getPID(deps)#creates a list of deployments from user input
        print(details)
        output = input('Give a filename to export the deployments to: ')
        pandas.DataFrame.from_dict(details,orient='index').to_csv(output)
        if args.getcsvs:
            getCSV(details)