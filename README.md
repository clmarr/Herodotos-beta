# Herodotos-beta
A branch off of the Herodotos Project NER Annotation and Tagger project. 
Exploratory work with NER tagging of other texts for downstream purposes.

This repository includes texts annotated for named entities as part of the [Herodotos Project](https://u.osu.edu/herodotos/) (Ohio State University / Ghent University) and will use a BiLSTM-CRF tagger based on that of ([Lample et al., 2016](https://arxiv.org/abs/1603.01360)) pre-trained on said annotation. 
Please check out the [Humanities Entity Recognizer](https://github.com/alexerdmann/HER) for more details on how it was trained in the prior project.

**All texts are in Latin** taken from the [Latin Library Collection](https://www.thelatinlibrary.com) (collected by [CLTK](https://github.com/cltk/latin_text_latin_library)) or the [Perseus Latin Collection](http://www.perseus.tufts.edu/hopper/collection?collection=Perseus:collection:Greco-Roman).
**Greek may be added soon** 

This project will involve a focus on the ancient ethnography of the Western Roman Empire and adjacent regions, especially, Gaul, Germania, and northwestern Africa. 
While the original Herodotos project (described in Erdmann et al. (2016), "[Challenges and Solutions for Latin Named Entity Recognition](http://www.aclweb.org/anthology/W16-4012)) focused on the Classical Latin of the Late republic and early Principate period, this project will also incorporate works from Late Antiquity.

*Internal structure, and the pipeline*

The first steps in our pipeline is the **data preparation.**

For this we gather texts already existing in the project, as well as a number we are adding. 
Within this repository, all texts will be assigned their own folders (wherein the raw text resides, with subdirectories for matters such as the old tagging results, replication attempts, formation of datasets therefrom, et cetera.).. 
They will all be named in the following format: "<Author>-Title_with_underlines_for_spaces".

We also recruit the NER tagger of Erdmann et al, which is currently undergoing testing for replication of past results. 

The yml file herodotos2016.yml contains the conda environment used to run the tagger. 
If you have anaconda, enable it with the following command: 

> conda env create -f herodotos2016.yml

It can also be handled with methods of the python package yaml. For example: 

> with open("./herodotos2016.yml") as f: 
> 	config = yaml.safe_load(f)

The script preProcess.py is a modified version of the same-named script from the 2016 GitHub repo, that among other things handles the standard NER conventions as concerns punctuation. 

**more details to come.** 

