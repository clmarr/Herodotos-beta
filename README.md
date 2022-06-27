# Herodotos-beta
A branch off of the Herodotos Project NER Annotation and Tagger project. 
Exploratory work with NER tagging of other texts for downstream purposes.

This repository includes texts annotated for named entities as part of the [Herodotos Project](https://u.osu.edu/herodotos/) (Ohio State University / Ghent University) and will use a BiLSTM-CRF tagger based on that of ([Lample et al., 2016](https://arxiv.org/abs/1603.01360)) pre-trained on said annotation. 
Please check out the [Humanities Entity Recognizer](https://github.com/alexerdmann/HER) for more details on how it was trained in the prior project.

**All texts are in Latin** taken from the [Latin Library Collection](https://www.thelatinlibrary.com) (collected by [CLTK](https://github.com/cltk/latin_text_latin_library)) or the [Perseus Latin Collection](http://www.perseus.tufts.edu/hopper/collection?collection=Perseus:collection:Greco-Roman).
**Greek may be added soon** 

This project will involve a focus on the ancient ethnography of the Western Roman Empire and adjacent regions, especially, Gaul, Germania, and northwestern Africa. 
While the original Herodotos project (described in Erdmann et al. (2016), "[Challenges and Solutions for Latin Named Entity Recognition](http://www.aclweb.org/anthology/W16-4012)) focused on the Classical Latin of the Late republic and early Principate period, this project will also incorporate works from Late Antiquity.

## Internal structure and pipeline

The first steps in our pipeline is the **data preparation.**

For this we gather texts already existing in the project, as well as a number we are adding. 
Within this repository, all texts will be assigned their own folders (wherein the raw text resides, with subdirectories for matters such as the old tagging results, replication attempts, formation of datasets therefrom, et cetera.).. 
They will all be named in the following format: "<Author>-Title_with_underlines_for_spaces".

We also recruit the NER tagger of Erdmann et al, which is currently undergoing testing for replication of past results. 

### Python environment 

The yml file herodotos2016.yml contains the conda environment with necessary packages and package versions needed used to run the tagger. 
This was originally necessary because the Erdmann et al 2016 tagger uses theano, which relies on now outdated versions of some core python packages; code has been built subsequently with the assumption that the particularized environment created for it will be used (as remains necessary at present if one wants to use the 2016 tagger to replicate the replication tests.)
If you have anaconda, you can enable it with the following command: 

> conda env create -f herodotos2016.yml

It can also be handled with methods of the python package yaml. For example: 

> with open("./herodotos2016.yml") as f: 
> 	config = yaml.safe_load(f)

### Preprocessing 
The script preProcess.py is a modified version of the same-named script from the 2016 GitHub repo, that among other things handles the standard NER conventions as concerns punctuation. 
The default behavior is a modified version of the original preProcess.py in the Erdmann et al tagger's repo.
It was modified so as to handle punctuation and other such items in a way that is consistent with the input necessary for the Erdmann et al 2016 tagger to produce output that is of a format consistent with that of its test output for Caesar's Gallic Wars (the original script did not, actually, do this -- it had numerous bugs 
**more details to come.** 

## Replication and generalizability testing

Since this project seeks to recruit the Erdmann et al 2016 tagger for downstream purposes such as embedding and analysis thereof, first one must be sure it accurately tags named entities, and especially ethnonyms. 
(Whether ethnonyms are properly 'named entities' is a philosophical question of which there is considerable discourse, with some vexing implications, which we take no position -- cf. Coates 2021 -- but for the purposes of this project, for better or worse, ethnonym-tagging has been done by an NER tagger.) 
Thus, replication testing was done, and the results thereof are to be found in the folder titled "replication" in Caesar's Gallic Wars -- all in all, aside from two errors (insignficant), the same result was attained. 
In order to check for the equivalence of two tagging outputs, each in either CRF or CONLL format, the check_replication.py script was written: all instances of non-replication are noted and printed to a file, as is an error matrix.
Note that there is a difference in notation: the tagger now (rightly) uses BIO notation, but the 2016 training and test outputs were not in this format. 
Thus, GEOF and GEO-B are really the same thing, just as GEOL and GEO-I, and so forth. 

Next is the question of if the results generalize. 
Here, things have been less rosy.
Thus far, results for Gregory of Tours have been vexing, with some analysis about why underway -- even though thet most common ethnonyms are the same, i.e. Gaulish and to a lesser extent Germanic tribes (the most common of all to be mentioned by Gregory are the Arverni, which are mentioned at least 75 times. These are also heavily mentioned by Caesar not least because it was Vercingetorix' tribe. A more thorough breakdown can be found in the file hf_grp_jun23_analysis within the directory for the Gregory of Tours' Historia Francorum.)
Tagging and analysis now ongoing for Sallust, who is much closer to Caesar's time. 
