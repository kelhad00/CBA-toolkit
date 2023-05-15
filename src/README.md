## src

This folder contains :

**1) snl_stats_extraction_data.py :**
This file contains all extraction functions for the statistics.

**2) snl_stats_visualization.py :**
This file contains all the vizualisation functions to vizualise the statistics.

**3) preprocessing.py :**
This file contains functions that help to extract data from eaf files coming from the datasets.
setup_label_database() and divide_seq_to_frames() are the main functions used.

**4) settings.py :**
This file contains somes variables used in the other python files of this folder.

**5) ml_stats.py :**
This file contains the functions that make the necessary statistics.

**6) ml_stats_vizusalisation.py :**
This file contains the function to vizualise the statistics.

**7) tests.py :**
This file has a function test(). This function is there just to help try out functions inside other files.

**8) to_improve.py :**
This file contains the functions to be improved in order to succeed in certain specific actions.

**9) json_creation.py :**
This file generates a JSON file from the directory data containing EAF files.

**10) data.json :**
This file contains a dictionnary where you can find some parameters you need to work with.
Here are precisions you need to know to understand the parameters. This is the explanation of how you need to manage directories.

 **In FOLDER_PATHS :**
 - DIR is the path where we have all databases. 
     This directory is called "data" and it has to be in the same folder as the repository (snlstats) you cloned.

 - ROOT1 is the path for ccdb database. This directory is inside data directory.
 - ROOT2 is the path for ifadv database. This directory is inside data directory.
 - ROOT3 is the path for ndc database. This directory is inside data directory.
 - ROOTX is the path for your database and so on. This directory is inside data directory

 **In DATABASES_PATHS :**
 You find the paths of files of each database.

 **In DATABASES_PAIR_PATHS :**
 You find the paths of the pair files of each database.

 **In TIER_LISTS :**
 Here are tiers and annotations values present in the EAF files.
 
 **TO IMPROVE**

 **In the previous JSON : parameters.json**
 **In _databasename_IN_OUT:**
 - PATH_IN_databasename : path of all person 1 in the database pairs
 - PATH_OUT_databasename : path of all person 2 in the database pairs

 Here we have paths for video pairs from each database. 
 Create a folder "data_in_out" (it has to be in the same folder as the repository (snlstats) you cloned.)
 Inside this folder, create three folders according to this notation "databasename_in_out".
 Inside each databasename_in_out folder, create two folders named "In" and "Out"

