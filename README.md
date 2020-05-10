This toolkit is still under development...


# CBA
The Conversation Behavior Analysis toolkit aims at offering the means for analyzing phenomena occurring in conversations such as mimicry, overlapping expressions, expressions timing, etc.


## Content

* /annotations: contains ELAN Template Files (etf) for annotation to use in your own projects.
* CBA/extract_data.py : general functions to read/extract data.
* CBA/db.py : interface specific to the different datasets.
* CBA/interaction_analysis.py : functions for analysing interaction behaviors (ex. counting mimicry).
* CBA/interaction_model.py : object oriented models of interactions.
* CBA/visualization.py : visualization functions.
* CBA/utils.py : utility functions.
* /examples: example code on using the CBA-toolkit

## Examples

To print corresponding pairs of interlocutors in the ccdb, ifadv or ndc datasets, run the following from the examples directory:

```python
python 
image = face_recognition.load_image_file("your_file.jpg")
face_landmarks_list = face_recognition.face_landmarks(image)
```
