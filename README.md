# Evaluating the psychological plausibility of word2vec and GloVe distributional semantic models
Author: Ivana Kajić (i2kajic@uwaterloo.ca)

This repository contains instructions on how to reproduce results, figures and
tables from the paper *Evaluating the psychological plausibility of word2vec and
GloVe distributional semantic models*.
Some of the steps are computationally involved (e.g, computing the similarity
matrices, calculating average shortest path lengths) so they will take a bit
longer to complete, but this depends on the machine.
The instructions also explain how to download the necessary files, two of which are over 1.5 GB each.

The repository contains the following directories:
- `data` all files used to generate the semantic networks are stored here (they need to be downloaded manually, as explained below)
- `notebooks` most of the analysis and data processing code is stored as Jupyter Notebooks
- `semnet_compare` a set of scripts for doing graph-theoretic analyses and performing the goodness-of-fit test

The instructions assume a fair amount of familiarity with the Python
programming language, the Jupyter Notebook environment, and minimal command of git and the command line.

The project has been developed with Python 3.6.3 and has not been tested with
other versions.

## Steps
1. Clone this repository with `git clone` and install necessary Python
packages with `pip install -r requirements.txt`.
Then, install the `semnet_compare` package by running `pip install -e .` from the `semnet_compare` directory, 
where the `setup.py` script is located 

2. Now, we need to manually download a few fairly large files and place
them in the corresponding directories within `data`.
- Download the [University of South Florida Free Association Norms](http://w3.usf.edu/FreeAssociation/AppendixA/index.html) (all `Cue_Target_Pairs*`, < 10MB in total) into the `./data/fan` directory
- Download the [word2vec](https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM/edit?usp=sharing) vectors and place the extracted files in the `./data/word2vec` directory (1.5 GB)
- Download the `glove.840B.300d.zip` file from the [GloVe](https://nlp.stanford.edu/projects/glove/) project page and unzip the file in the `./data/glove` directory (2.03 GB)

3. After downloading all the files, we can create networks by running the following Jupyter notebooks:
- `get-graph-norms.ipynb`
- `get-graph-w2v.ipynb`
- `get-graph-glove.ipynb`

The notebooks will load downloaded files and create `*pkl` files containing graph edges. Those will be stored in the `./data/{word2vec,glove}` directories.
To create graphs, similarity matrices are computed by multiplying vectors, and this step can take some time.

3. After this, we need to run a few scripts to calculate network statistics. This also takes some time...

Run the following scripts from the command line in the `semnet_compare` directory:

```bash
$ ipython goodness_of_fit.py
$ python analyze_undirected.py
$ python analyze_directed.py
```

They do not depend on each other, so to speed things up those can be executed in three different terminals.

4. At this point we have everything needed start analysing the data. All analyses are done and explained in the Jupyter notebooks:
- To reproduce results from the `Network statistics` section, refer to the `analysis1-networks-stats.ipynb` notebook
- To reproduce results from the `Degree distributions` section, refer to the `analysis2-plot-degree-distr.ipynb` notebook
- To reproduce results from the `Hierarchical topology` section, refer to the `analysis3-explore-local-clustering.ipynb` notebook

