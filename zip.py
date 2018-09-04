import os
import subprocess
from shutil import copyfile
import re
import validate_data

def zip_files(in_path, out_path):#In path is a directory with many folders as <depname>/deployment_manifest.xml and out_path is a directory with <depname>/<filenames>.JPG
    os.chdir(in_path)
    for x in os.listdir('.'):
        if os.path.isdir(x):
            if not os.path.isfile(out_path+'\\zip\\'+x+'.zip'):
                xml = open(x+'\\deployment_manifest.xml','r').read()
                actualfiles = os.listdir(out_path+"\\"+x)
                valid = validate_data.validate_filenames(xml, actualfiles)
                if valid:
                    copyfile(x+'\\deployment_manifest.xml', out_path+'\\'+x+'\\deployment_manifest.xml')
                    command = '"C:\\Program Files\\7-Zip\\7z.exe" a '+'"'+out_path+'\\zip\\'+x+'.zip"'+' "'+out_path+'\\'+x+'\\*'+'"'
                    print(command)
                    subprocess.call(command)#subprocess.run() would be better
                else:
                    print("there are errors with your data")
                    errors = validate_data.validate_filenames(xml, actualfiles, verbose=True)
                    if errors['imageerrors']:
                        delete_list(errors['imageerrors'],out_path+'\\'+x)

def delete_list(list,path):
    conf = input('you are about to delete '+str(len(list))+' images from '+path+'. Is there a backup of this folder somewhere?: (Y/N)').lower()
    if conf == 'y':
        for file in list:
            os.remove(path+'\\'+file)
    else:
        print('backup not confirmed, deletion canceled')

if __name__ == '__main__':
    #allows the file to be run as a standalone script
    print('this script expects XML files in folders with the deployment names and photos in folders with the same name, these can be two different locations')
    in_path = input("XML Parent Input Path:")
    out_path = input("Photos Parent Output Path:")