## SNL Stats

This folder contains :

**1) snl_stats_extraction_data.py :**
This file contains all extraction functions for the statistics.

**2) snl_stats_visualization.py :**
This file contains all the vizualisation functions to vizualise the statistics.

**3) tests.py :**
This file has a function test(). This function is there just to help try out functions inside other files.

**4) to_improve.py :**
This file contains the functions to be improved in order to succeed in certain specific actions.

**5) parameters.json :**
This file contains a dictionnary where you can find some parameters you need to work with.
Here are precisions you need to know to understand the parameters. This is the explanation of how you need to manage directories.

 **In FOLDER_PATHS :**
 - DIR is the path where we have all databases. 
     This directory is called "data" and it has to be in the same folder as the repository (snlstats) you cloned.

 - ROOT1 is the path for ccdb database. This directory is inside data directory.
 - ROOT2 is the path for ifadv database. This directory is inside data directory.
 - ROOT3 is the path for ndc database. This directory is inside data directory.

 **In DATABASES_PATHS :**
 You find the paths of files of each database.

 **In DATABASES_PAIR_PATHS :**
 You find the paths of the pair files of each database.

 **In INTENSITY_LISTS :**
 Here are intensities for smiles and laughs.

 **In _databasename_IN_OUT:**
 - PATH_IN_databasename : path of all person 1 in the database pairs
 - PAYH_OUT_databasename : path of all person 2 in the database pairs

 Here we have paths for video pairs from each database. 
 Create a folder "data_in_out" (it has to be in the same folder as the repository (snlstats) you cloned.)
 Inside this folder, create three folders according to this notation "databasename_in_out".
 Inside each databasename_in_out folder, create two folders named "In" and "Out"

