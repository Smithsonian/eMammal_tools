import os
import subprocess
from shutil import copyfile
import re
import validate_data
import csv

def zip_files(in_path, out_path):#In path is a directory with many folders as <depname>/deployment_manifest.xml and out_path is a directory with <depname>/<filenames>.JPG
    os.chdir(in_path)
    for x in os.listdir('.'):
        if os.path.isdir(x):
            if not os.path.isfile(out_path+'\\zip\\'+x+'.zip'):
                xml = open(x+'\\deployment_manifest.xml','r').read()
                actualfiles = os.listdir(out_path+"\\"+x)
                errors = validate_data.validate_filenames(xml, actualfiles, verbose=True)
                if errors['valid']:
                    copyfile(x+'\\deployment_manifest.xml', out_path+'\\'+x+'\\deployment_manifest.xml')
                    command = '"C:\\Program Files\\7-Zip\\7z.exe" a '+'"'+out_path+'\\zip\\'+x+'.zip"'+' "'+out_path+'\\'+x+'\\*'+'"'
                    print(command)
                    subprocess.call(command)#subprocess.run() would be better
                else:
                    print("there are errors with your data\n")
                    if not os.path.isfile('errors.csv'):
                        with open('errors.csv','a', newline='') as errorscsv:
                            errorwriter = csv.writer(errorscsv, dialect='excel')
                            errorwriter.writerow(['error','image','species'])
                    for key, value in errors.items():
                        if value:
                            with open('errors.csv','a', newline='') as errorscsv:
                                errorwriter = csv.writer(errorscsv, dialect='excel')
                                for image in value:
                                    list = [key]
                                    list.extend(image)
                                    print(list)
                                    errorwriter.writerow(list)
                    if errors['typeerrors']:
                        print(str(errors['typeerrors'])+'\n'+x+'\nFolders must contain only jpgs or xmls, please remove files listed above.')
                    if errors['imageerrors']:
                        print(str(errors['imageerrors'])+'\n'+x+'\nfolder contains images not in XML, they are listed above and output to output/errors.csv.')
                        if delete_list(errors['imageerrors'],out_path+'\\'+x):
                            print("files deleted")
                            copyfile(x+'\\deployment_manifest.xml', out_path+'\\'+x+'\\deployment_manifest.xml')
                            command = '"C:\\Program Files\\7-Zip\\7z.exe" a '+'"'+out_path+'\\zip\\'+x+'.zip"'+' "'+out_path+'\\'+x+'\\*'+'"'
                            print(command)
                            subprocess.call(command)#subprocess.run() would be better
                    if errors['xmlerrors']: 
                        print(str(errors['xmlerrors'])+'\n'+x+'\nXML contains files not in the folder. Those are listed above and in output/errors.csv, along with the associated species IDs.')

def delete_list(list,path):
    conf = input('you are about to delete '+str(len(list))+' images from '+path+'. Is there a backup of this folder somewhere?: (Y/N)').lower()
    if conf == 'y':
        for file in list:
            os.remove(path+'\\'+file)
        return True
    else:
        print('backup not confirmed, deletion canceled')
        return False

if __name__ == '__main__':
    #allows the file to be run as a standalone script
    print('this script expects XML files in folders with the deployment names and photos in folders with the same name, these can be two different locations')
    in_path = input("XML Parent Input Path:")
    out_path = input("Photos Parent Output Path:")