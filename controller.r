########################################################################################################################################
########################################################################################################################################
# This script relies on the python files located at X:\1 eMammal\Legacy Data\0_Legacy Data Converter\Integrated Scripts\Scripts
# If the scripts are moved, modify scriptsdir
# A backup of all of these scripts is at https://github.com/caseyhofford/eMammal_tools
# This script takes three files, images.csv, deployment.csv and project.csv, as inputs. They must be in the same directory.
# These files must all be encoded in UTF-8 (not UTF-8 BOM), use the encoding menu of notepad++ to convert to UTF-8 if you are encountering errors.
########################################################################################################################################
########################################################################################################################################

########################################################################################################################################
########################################################################################################################################
# Requirements
# 
# 1) Install anaconda python in your home directory. This can be installed without administrator priveleges by selecting "Just Me" for the installation. 
#   https://www.anaconda.com/download/
#
# 2) Have access to the X:\\ drive.
#
# 3) The images.csv, deployment.csv and project.csv should be in one folder together. They should be formatted as described here "X:\1 eMammal\Legacy Data\0_Legacy Data Converter\Metadata_Templates\Metadata_templates.xlsx"
#
# 4) The images should be in folders named as the deployment names, with only jpg images inside, no subfolders.
#
########################################################################################################################################
########################################################################################################################################
#
# How to use this file 
#
# The sections of this code are organized into blocks, contained withing curly brackets. Hit ctl+return on the start of each of these and check the output to make sure it has been succesful.
# These blocks are preceded by a comment like this one describing what the block does. Some of the blocks require user input.
###############################################################
## setting paths
###############################################################
#
#Note: the pypath variable is set to an installation of Anaconda python that lives on the X: drive.
#This is a fairly slow way to run pyton.
#Manually installing anaconda and then uncommenting line 43 and commenting line 44 is suggested to get this to run substantially faster
{
  #set scripts dir to the directory countaining the python scripts and the eMammal_Legacy_Data_Converter folder, should be automatically set
  scriptsdir = "X:\\1 eMammal\\Legacy Data\\0_Legacy Data Converter\\Integrated Scripts\\Scripts"
  
  #set the python path, this can be set manually if needed, but is currently set to the default installation directory for the current user.
  username = Sys.getenv("USERNAME")
  pypath = paste("C:\\Users",username,"AppData\\Local\\Continuum\\anaconda3\\python.exe",sep = "\\")
  #the path below can be used to use an installation of Anaconda on the server. It is VERY slow. Installing anaconda locally is recommended
  #pypath = "X:/1 eMammal/Legacy Data/0_Legacy Data Converter/Integrated Scripts/anaconda3/python.exe"
  
  #the path below should be set to the correct version of the legacy data coverter. 
  #Alternatively the correct version should be at https://github.com/caseyhofford/eMammalXMLConverter
  converterpath = paste(scriptsdir,"eMammal_Legacy_Data_Converter", sep = "\\")
  
  #Ask the user where the csv files and the image files are stored
  projpath = readline(prompt = "Enter the path to the folder containing the csvs for the project: ")
  imagespath = readline(prompt = "Enter the path to the parent folder containing the photos: ")
  outputpath = paste(projpath,"output",sep = "\\")
}
###############################################################
## importing and installing dependencies and functions
###############################################################

{
  #R packages
  library(reticulate)
  library(lubridate)
  
  #set correct python installation
  use_python(pypath, required = TRUE)
  
  #install two python packages needed for the chinadata scripts
  #should not be necessary if anaconda is installed
  #py_install("pandas")
  #py_install("requests")
  
  #initialize functions from python scripts, scriptsdir is set above in the Setting Paths section
  ###import from path imports the whole python file as a Module, with functions called on the module. 
  #source_python(paste(scriptsdir,"\\chinadata.py", sep = ""))
  validator <- import_from_path("validate_data", scriptsdir, convert = TRUE)
  zip <- import_from_path("zip", scriptsdir, convert = TRUE)
  
  #initialize the R functions
  #***************************
  source(file = paste(scriptsdir,"make_deployments.r", sep = "\\"))
}

##################################
#
# run prevalidation
#
##################################
{
  setwd(projpath)
  image_values = validator$validate_images_csv('./images.csv')
  writeLines("******************* \n READ \n*******************\nThe list value$errors lists any errors the python validator caught. \nA column that lists NaN means there is a NaN(not a number, a null value) in a column where there SHOULD NOT BE a null value")
  if(length(image_values$errors) > 0) {
    View(image_values$errors)
    print('Errors exist in your image CSV, look at the output above or run View(image_values$errors) to find out more')
  } else {
    writeLines("******************* \n READ \n*******************\n
               Please take a look at the output printed above. It should list all of the columns with errors, with 
               a summary of their values followed by a list of errors. This validator does not know everything! 
               Please take a quick look at each of the column summaries to make sure the output makes sense.")
    View(image_values)
  }
  
  dep_values = validator$validate_deployments_csv('deployment.csv')
  if(length(dep_values$errors) > 0){
    View(dep_values$errors)
  }else{
    View(dep_values)
  }
  
  #Add validation of project CSV to verify it doesnt contain a BOM, 0xA0 or any other non unicode characters.
}
####################################################################################################################
##
## Functions have been set, time to run the code!
## Make sure your working directory (projpath) has three files, images.csv, project.csv, and deployment.csv
## These csvs should be formatted as described in the metadata templates and manual for submitting legacy data to eMammal
##
####################################################################################################################
#
# Import the csvs
# create the deployment level csvs in <projpath>/output
# Create the XML files from the CSVs
#
###################################################################
{
  #setwd to the location that contains your project, image and deployment CSV
  setwd(projpath)
  
  #import the csvs
  #****************
  image = read.csv("./images.csv")
  project = read.csv("project.csv")
  deployment = read.csv("deployment.csv")
  #sequence = read.csv("sequence.csv")#this csv is created

  #*****************************************************
  #run the SplitDeployments method to create your deployments folder. 
  SplitDeployments(project, deployment, image)
  #now we set the working directory to the output folder created by SplitDeployments
  setwd(outputpath)
  # All these functions take the same argument, which is the folder path of your deployment folders, which should now be your working directory
  # It will raise warnings about setting 'append' these can be ignored
  ImageSequence("./")
  #Be aware, the sequence.csv function can run extrememly slowly. Multi-species sequence checking could be removed to improve performance.
  sequence.csv("./")
  DeploymentID("./")
  
  #create the deployment_manifest.xml files
  #*****************************************
  writeLines("Creating XMLs")
  setwd(converterpath) #working directory needs to be in the converters folder for it to run correctly
  outputpath_qu = paste("\"",outputpath,"\"",sep = "") #this creates a quoted version of the output path to be sent to the command line where it can be run
  pypath_qu = paste("\"",pypath,"\"",sep = "")
  system(paste(pypath_qu,"create_manifest.py",outputpath_qu,outputpath_qu,"1",sep = " "), intern = TRUE) #this runs the xml converter in a seperate process. It cannot be easily imported into R because it uses command line arguments to set variables
  print("The XMLs are duplicated. 
        The xmls folder in your ./output directory exists to run the XML verifier. 
        The XMLs are also stored in the folders for each deployment, these are used to create the zip files.
        These two sets of XMLs are exactly the same.")
}

######################################################################################################################################################
######************************************************************************************************************************************************
######* 
######*   You MUST run the XML validator now to check the manifests
######*
######*   To start, run block below
######*
######*   "X:\1 eMammal\Legacy Data\0_Legacy Data Converter\eMammal Manifest Validators\Jar Files\eMammal-xmlVerifier-1.0.3.jar"
######*
######************************************************************************************************************************************************
######################################################################################################################################################

{
  setwd(projpath)
  system("java -jar \"X:\\1 eMammal\\Legacy Data\\0_Legacy Data Converter\\eMammal Manifest Validators\\Jar Files\\eMammal-xmlVerifier-1.0.3.jar\"", intern=TRUE)
}
  

#copy the xmls to the image folders, verify their contents and zip them
#**********************************************************************

#zip_files takes two paths, the parent of the folders containing XMLs and the parent of the folders containing each deployments images
#it will raise errors if there is anything else in the folder
#it will check that the xml's first and last filename match a file in the folder
#the function will not overwrite existing zip folders, if you would like to recreate the zips, manually delete them before running below.

zip$zip_files(outputpath, imagespath)

