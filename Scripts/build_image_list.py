import pandas
import csv
import os
import re
import subprocess
import sys

def summarizeImages(path,csv=False):
    deployments = pandas.DataFrame(columns=['path','deployment'])
    images = pandas.DataFrame(columns=['path','deployment','datetime','size','image'])
    for dirName, subdirList, fileList in os.walk(path):
        if '.jpg' in '\t'.join(fileList).lower() and "$RECYCLE.BIN" not in dirName:
            print(dirName, subdirList)
            match = re.match(".*\\\\(.*)$",dirName)
            deployment = match.group(1)
            deployments = deployments.append({'path':dirName,'deployment':deployment},ignore_index=True)
            os.chdir(dirName)
            output = subprocess.check_output('dir /s',shell=True)
            out_list = output.decode("utf-8").split('\r\n')
            for file in out_list:
                try:
                    details = re.match("(\S*  \S* \S*)\s*(\S*) (\S*).JPG$", file)
                    datetime = details.group(1)
                    size = details.group(2)
                    file = details.group(3)
                    #print([dirName,deployment,datetime,size,file])
                    images = images.append({'path':dirName,'deployment':deployment,'datetime':datetime,'size':size,'image':file},ignore_index=True)
                except Exception as err:
                    #print(err)
                    #print(file)
                    output = open(path+'errors.csv', 'a')
                    output.write(dirName+','+deployment+','+'\n')
                    output.close()
    if csv:
        outpath = os.path.join(path,'images.csv')
        images.to_csv(outpath,index=False)
        deployments.to_csv(os.path.join(path,'deployments.csv'),index=False)
        return outpath
    return(images)
                
def summarizeDeployments(path,csv=False):
    deployments = pandas.DataFrame(columns=['path','deployment'])
    for dirName, subdirList, fileList in os.walk(path):
        if '.jpg' in '\t'.join(fileList).lower() and "$RECYCLE.BIN" not in dirName:
            print(dirName, subdirList)
            match = re.match(".*\\\\(.*)$",dirName)
            deployment = match.group(1)
            deployments = deployments.append({'path':dirName,'deployment':deployment},ignore_index=True)
    if csv:
        outpath = os.path.join(path,'deployments.csv')
        deployments.to_csv(outpath,index=False)
        return(outpath)
    return(deployments)
    
if __name__ =="__main__":

    path = input("Where?")
    type = input("deployments or images?")
    if type == 'images':
        print(summarizeImages(path,csv=True))
    else:
        print(summarizeDeployments(path,csv=True))
    

#path = 'C:\\Users\\HoffordC\\Documents\\Peru_Pagoreni\\NEWeMam_Pag_GD'