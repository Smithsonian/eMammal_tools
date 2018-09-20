## File Descriptions

./arcmap_link_repair.py
    #### Python environment: Arcpy Installation of Python 2.7
    #### How to run:
    Navigate to scripts in explorer, type "cmd"(w/o quotes) in the address bar and hit return.
    In the window that appears, run the command below
    C:\Python27\ArcGIS10.6\python.exe arcmap_link_repair.py
    #### Description
    This file allows you you to go through a directory and find all the map documents and replace their sources to update them when moved (e.g. replace V:\ with T:\ or V:\GIS with T:\Files\GIS). 
    This will not apply substitutions that break links. It will only update sources if the new source is found.
    Make sure you are using paths with single slashes.
    It will output a file in the JSON format that can be used to see what sources are still broken in the map documents in these folders. This can be useful to figure out what folders may have been moved and need to be located. You will have to track them down manually but can then rerun the script to replace the broken path with the corrected path in all documents.
    
./build_image_list.py
    #### Python environment: 
    Python 3.7 Anaconda Distribution (https://www.anaconda.com/download/)
    Intended to find all the images in a folder and return a csv with folder names and image names to summarize a project.
    No promises here.

./categoryfolders.py
    #### Python environment: 
    Python 3.7 Anaconda Distribution (https://www.anaconda.com/download/)
    Intended to sort images into species specific folders for CV training purposes. 
    No promises here.

./check_database.py
    #### Python environment: 
    Python 3.7 Anaconda Distribution, can be installed on your local account easily (https://www.anaconda.com/download/)
    #### How to run:
    Install Anaconda Python in your account.
    Navigate to scripts in explorer, type "cmd"(w/o quotes) in the address bar and hit return.
    In the window that appears, run the command below
    C:\Users\**<YOUR USERNAME HERE>**\AppData\Local\Continuum\anaconda3\python.exe check_database.py 
    
    This script will verify that deployments have been added to the database by querying SOLR. It will return a CSV listing all the documents that it has found. When deployments are not found, they are simply excluded from the csv.
    
    #### Known Issues:
    It does not work with deployments that have spaces in their name.

./chinadata.py
    #### Description:
    This will not run as is.
    It is a whole bunch of little snippets of code from manipulating HongLiang's chinadata for ingest into eMammal. Probably not useful to anyone but me.

./IUCN_client.py
    #### Python environment: 
    Python 3.7 Anaconda Distribution, can be installed on your local account easily (https://www.anaconda.com/download/)
    #### How to run:
    Import functions into IDLE, iPython or a separate program.
    #### Description:
    **get_IUCN_id_status(name,token):** takes a species name and your api token and returns a dictionary - {'IUCNid':IUCNid,'IUCNstatus':IUCNstatus}