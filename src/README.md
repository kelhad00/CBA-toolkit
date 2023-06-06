## src

This folder contains:

**1) snl_stats_extraction_data.py:**
This file contains all extraction functions for the statistics.

**2) preprocessing.py:**
This file contains functions that help to extract data from eaf files coming from the datasets for the machine learning part.
setup_label_database() and divide_seq_to_frames() are the main functions used.

**3) settings.py:**
This file contains somes variables used in the other python files of this folder.

**4) ml_stats.py:**
This file contains the functions that make the necessary statistics for machine learning part.

**5) ml_stats_vizusalisation.py:**
This file contains the function to vizualise the statistics for machine learning part.

**6) tests.py:**
This file has a function test(). This function is there just to help try out functions inside other files.

**7) to_improve.py:**
This file contains the functions to be improved in order to succeed in certain specific actions.

**8) json_creation.py:**
This file generates a JSON file from the directory data containing EAF files.

**9) page2:**
This folder contains the scripts for the second page of the Streamlit interface:
* snl_stats_visualization_page2.py : This file contains the functions to display the statistics of the expressions in the second page of the Streamlit interface.
* function_thread_page2.py : This file contains the functions to display in multi-threading the statistics of the expressions in the second page of the Streamlit interface.

**10) page3:**
This folder contains the scripts for the third page of the Streamlit interface:
* snl_stats_visualization_page3.py : This file contains the functions to display the statistics of the expressions in the third page of the Streamlit interface.
* function_thread_page3.py : This file contains the functions to display in multi-threading the statistics of the expressions in the third page of the Streamlit interface.

**11) page4:**
This folder contains the scripts for the fourth page of the Streamlit interface:
* snl_stats_visualization_page4.py : This file contains the functions to display the statistics of the expressions in the fourth page of the Streamlit interface.

**12) page6:**
This folder contains the scripts for the sixth page of the Streamlit interface:
* snl_stats_visualization_page6.py : This file contains the functions to display the statistics of the expressions in the sixth page of the Streamlit interface.
* snl_stats_visualization_database.py : This file contains the functions to display informations about the database in the sixth page of the Streamlit interface.


