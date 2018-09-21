################################################################
##This function creates folders and CSVs for each deployment
################################################################
SplitDeployments <- function(project, deployment, image){
  #Create output folder
  dir.create("output")
  
  #Get the list of unique values
  for (name in levels(deployment$Camera.Deployment.ID)){
    #Create deployment dir
    folder = paste("output/", name , sep = "")
    dir.create(folder)
    
    #Subset the data by field
    dep = subset(deployment, Camera.Deployment.ID==name)
    #seq = subset(sequence, Deployment.ID==name)
    img = subset(image, Deployment.ID==name)
    
    #Build paths
    fn1 = paste("output/", name, "/Project.csv" , sep = "")
    fn2 = paste("output/", name, "/Deployment.csv" , sep = "")
    #fn3 = paste("output/", name, "/Sequence.csv" , sep = "")
    fn4 = paste("output/", name, "/Image.csv" , sep = "")
    
    # Get minimum Image.Sequence.ID and take one off to find subtract value
    #subtractvalue = min(seq$Image.Sequence.ID) - 1
    #if (subtractvalue == Inf){ print( name ) }
    
    #Subtract value from column Image.Sequence.ID to start with 1
    #seq$Image.Sequence.ID = seq$Image.Sequence.ID - subtractvalue
    #img$Image.Sequence.ID = img$Image.Sequence.ID - subtractvalue
    
    #Save the CSV files
    write.csv(project, fn1, row.names=FALSE, quote=TRUE, na="")
    write.csv(dep, fn2, row.names=FALSE, quote=TRUE, na="")
    #write.csv(seq, fn3, row.names=FALSE, quote=FALSE, na="")
    write.csv(img, fn4, row.names=FALSE, quote=TRUE, na="")
  }
  message ("Spliting deployments succesfully completed!")
}


####################################################################
# Function "ImageSequence()" is used to calculate sequence data
# and fill the "Image.Sequence.ID" column in the "Image.csv" file
# for each deployment
####################################################################
ImageSequence <- function(pat){
  # The only argument "pat" here is the folder path of the deployments folders
  # load packages
  require(lubridate)
  # Set work directory
  setwd(pat)
  deploy <- list.files()
  for (i in deploy){
    if (length(dir(path = paste(pat, "\\", i, sep = "", collapse = ""),
                   pattern = "Image.csv")) == 0){
      next
    }
    imagecsvPath <- paste(pat, "\\", i, "\\", "Image.csv",
                          sep = "", collapse = "")
    
    #Make emergency copy if image data copied wrong
    #imagecsvCopy <- paste(pat, "/", i, "/", "ImageCopybyJenny.csv",
    #                      sep = "", collapse = "")
    #file.copy(imagecsvPath, imagecsvCopy)
    
    #If you want to add a value across all csvs, put it here (eg. interest rank)
    imagecsv <- read.csv(file = imagecsvPath, header = TRUE, check.names = FALSE)
    imagecsv <- subset(imagecsv, imagecsv$`Deployment.ID` != "")
    imagecsv$Date_Time <- parse_date_time(x = as.character(imagecsv$Date_Time),
                                          orders = c("%m-%d-%y %h:%M"))
    imagecsv <- imagecsv[order(imagecsv$Date_Time),]
    if(dim(imagecsv)[1] == 1){
      imagecsv[,"Image.Sequence.ID"][1] = 1
    }
    else {
      imagecsv[,"Image.Sequence.ID"][1] = 1
      for (j in 2:dim(imagecsv)[1]){
        if (difftime(time1 = imagecsv$Date_Time[j],
                     time2 = imagecsv$Date_Time[j-1],units = "mins") >=2){
          imagecsv[,"Image.Sequence.ID"][j] = imagecsv[,"Image.Sequence.ID"][j-1] + 1
        }
        else{
          imagecsv[,"Image.Sequence.ID"][j] = imagecsv[,"Image.Sequence.ID"][j-1]
        }
      }
    }
    
    write.csv(imagecsv, file = imagecsvPath, append = FALSE,
              row.names = FALSE, na = "")
  }
  message ("ImageSequence function complete!")
}

####################################################################
# Function "sequence.csv" is to generate the Sequence.csv file
####################################################################
sequence.csv <- function(pat){
  # Set work directory
  setwd(pat)
  # Load packages
  require(lubridate)
  deploy <- list.files()
  for (i in deploy){
    if (length(dir(path = paste(pat, "/", i, sep = "", collapse = ""),
                   pattern = "Image.csv")) == 0){
      next
    }
    imagecsvPath <- paste(pat, "/", i, "/", "Image.csv",
                          sep = "", collapse = "")
    imagecsv <- read.csv(file = imagecsvPath, header = TRUE, check.names = FALSE)
    
    
    # Duplicates and reorders the image csv so that sequences with no animal and
    #   animal images are generated with the animal listed
    
    imagetosequence <- imagecsv
    imagetosequence <- imagetosequence[order(imagetosequence[,'Image.Sequence.ID'], -imagetosequence[,'IUCN.ID']),]
    imagetosequence <- subset(imagetosequence, !duplicated(imagetosequence$Image.Sequence.ID))
    
    imagecsv$Date_Time <- parse_date_time(x = as.character(imagecsv$Date_Time),
                                          orders = c("%m-%d-%y %H:%M","%y-%m-%d %H:%M:%S"))
    maxseq <- max(imagecsv[,"Image.Sequence.ID"])
    
    # Create the sequence.csv df
    sequencecsv <- data.frame(matrix(data = NA, nrow = maxseq, ncol = 16))
    colnames(sequencecsv) <- c("Observation.Type",
                               "Deployment.ID",
                               "Image.Sequence.ID",
                               "Date_Time.Begin",
                               "Date_Time.End",
                               "Genus.species",
                               "Species.Common.Name",
                               "Age",
                               "Sex",
                               "Individual.ID",
                               "Count",
                               "Animal.recognizable",
                               "Individual.Animal.Notes",
                               "TSN.ID",
                               "IUCN.ID",
                               "IUCN.Status")
    
    # Fill in the sequence information from image.csv
    sequencecsv[,"Observation.Type"] <- rep("Researcher", times = maxseq)
    sequencecsv[,"Image.Sequence.ID"] <- seq(from = 1, to = maxseq, by = 1)
    sequencecsv[,"Count"] <- rep(imagetosequence$Count)
    sequencecsv$Count[is.na(sequencecsv$Count)] <- 1        #Adds count of 1 for null values
    sequencecsv[,"Genus.species"] <- rep(imagetosequence$Genus.Species)
    sequencecsv[,"Animal.recognizable"] <- rep(imagetosequence$Animal.recognizable)
    sequencecsv[,"Species.Common.Name"] <- rep(imagetosequence$Species.Common.Name)
    sequencecsv[,"Individual.Animal.Notes"] <- rep(imagetosequence$Individual.Animal.Notes)
    sequencecsv[,"Individual.ID"] <- rep(imagetosequence$Individual.ID)
    sequencecsv[,"TSN.ID"] <- rep(imagetosequence$TSN.ID)
    sequencecsv[,"IUCN.ID"] <- rep(imagetosequence$IUCN.ID)
    sequencecsv[,"IUCN.Status"] <- rep(imagetosequence$IUCN.Status)
    sequencecsv[,"Age"] <- rep(imagetosequence$Age)
    sequencecsv[,"Sex"] <- rep(imagetosequence$Sex)
    #return(imagecsv)
    
    # Set time range of sequence
    for(j in 1:maxseq){
      dtseq <- subset(imagecsv$Date_Time, imagecsv[,"Image.Sequence.ID"] == j)
      #View(dtseq)
      sequencecsv[,"Date_Time.Begin"][j] = as.character(min(dtseq))
      sequencecsv[,"Date_Time.End"][j] = as.character(max(dtseq))
    }
    
    # Looks for sequences with two species, returns a csv with deployment name and
    #   sequence number so you can edit the XML
    for (j in 1:maxseq){
      imagecsv1 = subset(imagecsv, imagecsv$Species.Common.Name != "No Animal")
      dupes = aggregate(Species.Common.Name ~ Image.Sequence.ID, imagecsv1, function(x) length(unique(x)))
      if (any(dupes$Species.Common.Name > 1)){
        write.csv(x = dupes,
                  file = paste(pat, "/Duplicates_", i,".csv",
                               sep = "", collapse = ""),
                  append = FALSE, na = "", row.names = FALSE)
      }
      
      write.csv(x = sequencecsv,
                file = paste(pat, "/", i, "/", "Sequence.csv",
                             sep = "", collapse = ""),
                append = FALSE, na = "", row.names = FALSE)
    }
  }
  message ("Sequence.csv files created!")
}

####################################################################
# Function "DeploymentID" adds the eMammal deployment ID to the
# image, sequence, and deployment csvs
####################################################################
DeploymentID <- function(pat){
  # The only argument "pat" here is the folder path of the deployments folders
  # Set work directory
  setwd(pat)
  deploy <- list.files()
  
  # Series of loops that insert the deployment IDs and image.sequence.ids necessary
  #   for ingest of the deployment manifests. Be aware that these loops use column
  #   numbers rather than names so just double check your csv formats before you
  #   run these
  ##
  ##Why is this editing the image CSV if it is pulling the deployment ID from there in the first place? Is this first for loop doing anything useful?
  for (i in deploy){
    if (length(dir(path = paste(pat, "/", i, sep = "", collapse = ""),
                   pattern = "Image.csv")) == 0){
      next
    }
    imagecsvPath <- paste(pat, "/", i, "/", "Image.csv",
                          sep = "", collapse = "")
    imagecsv <- read.csv(file = imagecsvPath, header = TRUE, check.names = FALSE)
    deploy.id <- paste(imagecsv[1,1])
    imagecsv[,2] <- paste(deploy.id)
    imagecsv <- imagecsv[,2:ncol(imagecsv)]
    
    write.csv(imagecsv, file = imagecsvPath, append = FALSE,
              row.names = FALSE, na = "")
  }
  for (i in deploy){
    if (length(dir(path = paste(pat, "/", i, sep = "", collapse = ""),
                   pattern = "Sequence.csv")) == 0){
      next
    }
    imagecsvPath <- paste(pat, "/", i, "/", "Image.csv",
                          sep = "", collapse = "")
    imagecsv <- read.csv(file = imagecsvPath, header = TRUE, check.names = FALSE)
    deploy.id <- paste(imagecsv[1,1])
    deploy.id1 <- paste(imagecsv[1,1], "s", sep = "")
    sequencecsvPath <- paste(pat, "/", i, "/", "Sequence.csv",
                             sep = "", collapse = "")
    sequencecsv <- read.csv(file = sequencecsvPath, header = TRUE, check.names = FALSE)
    sequencecsv[,2] <- imagecsv[1,1]
    sequencecsv[,3] <- paste(deploy.id1, sequencecsv[,3], sep = "")
    
    write.csv(sequencecsv, file = sequencecsvPath, append = FALSE,
              row.names = FALSE, na = "")
  }
  for (i in deploy){
    if (length(dir(path = paste(pat, "/", i, sep = "", collapse = ""),
                   pattern = "Deployment.csv")) == 0){
      next
    }
    imagecsvPath <- paste(pat, "/", i, "/", "Image.csv",
                          sep = "", collapse = "")
    imagecsv <- read.csv(file = imagecsvPath, header = TRUE, check.names = FALSE)
    deploycsvPath <- paste(pat, "/", i, "/", "Deployment.csv",
                           sep = "", collapse = "")
    deploycsv <- read.csv(file = deploycsvPath, header = TRUE, check.names = FALSE)
    deploycsv <- deploycsv[,2:17]
    deploy.id <- paste(imagecsv[1,1])
    deploycsv[,1] <- paste(deploy.id)
    
    write.csv(deploycsv, file = deploycsvPath, append = FALSE,
              row.names = FALSE, na = "")
  }
  message ("Deployment IDs added to sequence IDs")
}