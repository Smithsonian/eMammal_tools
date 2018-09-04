import pandas
import csv
import os
import re
import subprocess
import sys

path = input("Where?")

#path = 'C:\\Users\\HoffordC\\Documents\\Peru_Pagoreni\\NEWeMam_Pag_GD'

deployments = pandas.DataFrame()
images = pandas.DataFrame()

for dirName, subdirList, fileList in os.walk(path):
    match = re.match(".*\\\\(.*)\\\\(.*)$",dirName)
    try:
        if match.lastindex == 2:
            deployment = match.group(2)
            print deployment
            os.chdir(dirName)
            output = subprocess.check_output('dir /s',shell=True)
            out_list = output.split('\r\n')
            for file in out_list:
                try:
                    details = re.match("(\S*  \S* \S*)\s*(\S*) (\S*).JPG$", file)
                    datetime = details.group(1)
                    size = details.group(2)
                    file = details.group(3)
                    output = open(path+'\\images.csv', 'a')
                    output.write(dirName+','+deployment+','+datetime+','+size+','+file+'\n')
                    output.close()
                    #row = {'directory' : dirName, 'Deployment.ID' : deployment, 'Date_Time' : datetime, 'size' : size, 'Image.ID': file}
                except Exception as err:
                    output = open(path+'errors.csv', 'a')
                    output.write(dirName+','+deployment+','+'\n')
                    output.close()
            #file.write(deployment+'\n')
            #file.close()
            os.chdir(path)
    except Exception:
        output = open(path+'errors.csv', 'a')
        output.write(dirName+','+str(sys.exc_info()[0])+'\n')
        output.close()
        #print('error on: '+dirName)
        #print(err+'\n')