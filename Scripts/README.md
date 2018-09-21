# File Descriptions    
  
## ./arcmap_link_repair.py    
### Python environment:  

Arcpy Installation of Python 2.7    
### How to run:    
Navigate to scripts in explorer, type "cmd"(w/o quotes) in the address bar and hit return.    
In the window that appears, run the command below    
    C:\Python27\ArcGIS10.6\python.exe arcmap_link_repair.py    
### Description    
This file allows you you to go through a directory and find all the map documents and replace their sources to update them when moved (e.g. replace V:\ with T:\ or V:\GIS with T:\Files\GIS).      
This will not apply substitutions that break links. It will only update sources if the new source is found.    
Make sure you are using paths with single slashes.    
It will output a file in the JSON format that can be used to see what sources are still broken in the map documents in these folders. This can be useful to figure out what folders may have been moved and need to be located. You will have to track them down manually but can then rerun the script to replace the broken path with the corrected path in all documents.    
  
## ./build_image_list.py    
### Python environment:    
Python 3.x Anaconda Distribution (https://www.anaconda.com/download/)    
Intended to find all the images in a folder and return a csv with folder names and image names to summarize a project.    
No promises here.    
  
## ./categoryfolders.py    
### Python environment:    
Python 3.x Anaconda Distribution (https://www.anaconda.com/download/)    
Intended to sort images into species specific folders for CV training purposes.     
No promises here.    
  
## ./check_database.py    
### Python environment:    
Python 3.x Anaconda Distribution, can be installed on your local account easily (https://www.anaconda.com/download/)    
### How to run:    
Install Anaconda Python in your account.    
Navigate to scripts in explorer, type "cmd"(w/o quotes) in the address bar and hit return.    
In the window that appears, run the command below    
    C:\Users\<YOUR USERNAME HERE>\AppData\Local\Continuum\anaconda3\python.exe check_database.py    
  
This script will verify that deployments have been added to the database by querying SOLR. It will return a CSV listing all the documents that it has found. When deployments are not found, they are simply excluded from the csv.    
  
### Known Issues:    
It does not work with deployments that have spaces in their name.    
  
## ./chinadata.py    
### Description:    
This will not run as is.    
It is a whole bunch of little snippets of code from manipulating HongLiang's chinadata for ingest into eMammal. Probably not useful to anyone but me.    
  
## ./IUCN_client.py    
### Python environment:    
Python 3.x Anaconda Distribution, can be installed on your local account easily (https://www.anaconda.com/download/)    
### How to run:    
Import functions into IDLE, iPython or a separate program.    
### Description:    
**get_IUCN_id_status(name,token):** takes a species name and your api token and returns a dictionary containing:      {'IUCNid':<IUCNid>,'IUCNstatus':<IUCNstatus>}          ## ./make_deployments.r  #### Environment:  R  #### Description:  This file contains 4 functions that were previously contained in the images_to_sequences.R and split.R files. I have moved these to one file and made images_to_sequences into a function (SplitDeployments()). These are intended to be run from the controller.r function located at:      X:\1 eMammal\Legacy Data\0_Legacy Data Converter\Integrated Scripts    #### Fucntions:  **SplitDeployments(project, deployment, image):** this function takes three arguments, they are the dataframes of project.csv, deployment.csv and images.csv. It returns nothing but prints a message on completion and creates folders for each deployment containing the CSVs of each deployment.  **ImageSequence(pat):** Function "ImageSequence()" is used to calculate sequence data and fill the "Image.Sequence.ID" column in the "Image.csv" file for each deployment.  **sequence.csv(pat):** Function "sequence.csv" is to generate the Sequence.csv file   **DeploymentID(pat):** Function "DeploymentID" adds the eMammal deployment ID to the image, sequence, and deployment csvs   ## ./scrape_site.py  ### Python environment:     Python 3.x Anaconda Distribution, can be installed on your local account easily (https://www.anaconda.com/download/)   ### How to run:    Install Anaconda Python in your account.    Navigate to scripts in explorer, type "cmd"(w/o quotes) in the address bar and hit return.     In the window that appears, run the command below, replacing the csvs with appropriate paths.        C:\Users\<YOUR USERNAME HERE>\AppData\Local\Continuum\anaconda3\python.exe scrape_site.py deployments <output.csv> <input.csv>   The input CSV should contain a column "Deployment.ID" which lists the names of the deployments that you are looking for eMammal IDs for.  You will have to paste your cookie string from your current eMammal browser session into the command line to access any deployment IDs that are not publicly visible. This can be done by inspecting a request in the developer console in your browser (f12). The text in the request header after cookie: is what you need.    #### Description:  This pulls eMammal deployment IDs based on deployment names.  There is also a function intended to build a complete species list from the eMammal content page, however it does not currently work.  ## ./validate_data.py   ### Python environment:    Python 3.x Anaconda Distribution, can be installed on your local account easily (https://www.anaconda.com/download/)  ### How to run:    Install Anaconda Python in your account.  This script can be called by the controller R function. This is how it will normally be used since the R script allows you to go from the initial csvs all the way to the final zipped folders.    Navigate to scripts in explorer, type "cmd"(w/o quotes) in the address bar and hit return.    In the window that appears, run the command below        C:\Users\<YOUR USERNAME HERE>\AppData\Local\Continuum\anaconda3\python.exe validate_data.py <zip or folder> <path to folder of deployments> <path to save the results>    #### Description:  This script looks through a directory full of deployments and validates them. It ensures that the filenames in the XML match the filenames in the folder as well as that there are no extra files or subfolders.  There are also functions in here that check the csvs you start with for value errors. These are run by the controller R script and can not be run from the command line, however the functions can be called from elsewhere.## ./zip.py  #### Environment:   Python 3  ### How to run:    Install Anaconda Python 3 in your account.   This script can be called by the controller R function. This is how it will normally be used since the R script allows you to go from the initial csvs all the way to the final zipped folders.     If you would like to run this on its own, navigate to scripts in explorer, type "cmd"(w/o quotes) in the address bar and hit return.    In the window that appears, run the command below        C:\Users\<YOUR USERNAME HERE>\AppData\Local\Continuum\anaconda3\python.exe zip.py  you will be prompted for the two paths of the folder of deployment folders containing the XML, and the path of the deployment folders containing the images. This makes it easy to copy all of the XMLs from the output of the manifest creator to the corresponding image folders.  Note#### Description:  This script takes the output of the XML creator, as well as a folder of images, validates the contents and then zips the files to prepare them for ingest. It uses validate_data to verify the files.