# eMammal Legacy Data Converter  
## Unified Scripts  
  
For proper formatting, I recommend you read this file on github at https://github.com/smithsonian/eMammal_tools  
  
  
  
  
## /controller.R  
  
Use this script to go from the three csvs, images, deployment and project described at  

    X:\1 eMammal\Legacy Data\0_Legacy Data Converter\Metadata_Templates\Metadata_templates.xlsx  

to the final zipped folders for ingest into eMammal.  
  
The scripts folder of this repository also includes other scripts and tools to simplify some eMammal tasks.  
Navigate to the readme in that folder for more details.  

### Known Issues:  

Make sure all input files are formatted in UTF-8 and don't have any strange character codes(0x65, etc). This can be an issues when copying text from the website. Return characters may be copied unpredictably and cause issues. Returns and extra spaces should be removed from text copied from the website.
   

Switching the encoding in notepad++ and then switching it back to UTF-8 may fix this in some cases.





## General Instructions for Legacy Data Processing

Preparing data for the controller from the existing legacy projects:   
  
	X:\1 eMammal\Legacy Data\0READMELegacyProjectSummaries_MW.docx
  
Processing data with the Controller, or manually:

	X:\1 eMammal\Legacy Data\0_Legacy Data Converter\Batch Process eMammal Legacy Data 2.0.docx
  
Or from the notes in the controller.r file here.


## Using the legacy data scripts:

https://github.com/smithsonian/eMammal_tools/tree/master/Scripts

