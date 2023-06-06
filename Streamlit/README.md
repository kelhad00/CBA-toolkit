## Streamlit

This file presents the work done in the other folder of the repository in an interactive web page.
To load it, you need to install streamlit in the python environment you work on.
Check this link to know how to do that : https://docs.streamlit.io/library/get-started/installation

This folder contains:
 
**1) Affichage_pattern.py:**
This file is a display function that uses the Streamlit library to configure and customize the appearance of a web page.

**2) MainPage.py:**
This file defines the home page of the Streamlit interface which displays the title of the study and a brief description of the database and the statistics to be displayed.

**3) 2-Descriptive Analysis.py:**
This file presents descriptive statistics on expressions in a database in the form of graphs.

**4) 3-Non Verbal Expressions Analysis.py:**
This file is dedicated to the analysis of the absolute and relative durations of different expressions, both at the individual level and at the level of interactions in the form of graphs.

**5) 4-Non Verbal Expressions Effects.py:**
This file allows to visualize the effects within and between expressions, including the capacity for mimicry.

**6) 5-ML Statistics.py:**
This file uses various functions to display machine learning statistics. It allows you to select a database, fill in some parameters, and then display graphs based on that database's data.

**7) 6-Other.py:**
This file allows you to explore different description areas and view database data.

**8) data.json:**
This file contains a dynamic dictionnary where you can find parameters of your database.

 **In FOLDER_PATHS:**
 - DIR is the path where we have all databases. 
     This directory is called "data" and it will be created at the same level than the other folders of the project.

 - ROOT1 is the path for ccdb dataset. This directory is inside data directory.
 - ROOT2 is the path for ifadv dataset. This directory is inside data directory.
 - ROOT3 is the path for ndc dataset. This directory is inside data directory.
 - ROOTX is the path for your dataset and so on. This directory is inside data directory

 **In DATABASES_PATHS:**
 You find the paths of files of each dataset.

 **In DATABASES_PAIR_PATHS:**
 You find the paths of the pair files of each dataset.

 **In TIER_LISTS:**
 Here are tiers and annotations values present in the EAF files.
 
 **TO IMPROVE**

 **In the previous JSON: parameters.json**
 **In _databasename_IN_OUT:**
 - PATH_IN_databasename: path of all person 1 in the database pairs
 - PATH_OUT_databasename: path of all person 2 in the database pairs

 Here we have paths for video pairs from each database. 
 Create a folder "data_in_out" (it has to be in the same folder as the repository (snlstats) you cloned).
 Inside this folder, create three folders according to this notation "databasename_in_out".
 Inside each databasename_in_out folder, create two folders named "In" and "Out"
 
 
To run the file, you write in your executive python interface: streamlit run MainPage.py
 
For more informations about streamlit or for a better understanding: https://docs.streamlit.io
