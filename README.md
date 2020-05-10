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
* pair_data.py : example code

## Examples

To print corresponding pairs of interlocutors in the ccdb, ifadv or ndc datasets, run the following from the examples directory:

To print pairs from CCDB, IFADV or NDC-ME.
```python
python pair_data.py --path_ccdb <path to the CCDB audio, video or eaf files>
python pair_data.py --path_ifadv <path to the IFADV audio, video or eaf files>
python pair_data.py --path_ndc <path to the NDC-ME audio, video or eaf files>

```
