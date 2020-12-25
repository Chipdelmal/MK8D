# MK8D

Python package for "Mario Kart 8 Deluxe" livesplit data analysis.  It processes Livesplit *LSS* files (*XML* format) to provide a cleaner way to analyze the data by re-shaping it to a dataframe. 


This package is an improvement upon the [mk8dLivesplit](https://github.com/Chipdelmal/mk8dLivesplit) implementation. The main change is that it handles runs in a dataframe for easier parsing and filtering (sacrificing a bit of processing speed).
 
## Features

* Streamlined conversion from *LSS* to *CSV* dataframe
* Combine different *LSS* files into one dataframe automatically
* Plot and compare runs 
  * Full run
  * Individual Tracks

## Basic Usage

Install the package with:

```bash
pip install MK8D
```

To convert an LSS file into a CSV dataframe, run:

```bash
MK8D_lss2csv INPUT_FOLDER OUTPUT_FOLDER OUTPUT_FILENAME
```

where **INPUT_FOLDER** is the path to the directory where the *LSS* files are stored, **OUTPUT_FOLDER** is the location in which we want our files to be exported to, and **OUTPUT_FILENAME** is the name of the *CSV* file to be exported.

For example, if run from the repository directory:

```bash
MK8D_lss2csv ./MK8D/dev/data ./dev/data MK8D.csv
```

would take every *LSS* file found in the `./MK8D/dev/data` and compile a dataframe to a *CSV* file, which would be exported to the same folder.

## Dependencies

* Pandas
* Numpy
* Plotly
* Plotly Express
* Matplotlib
* Colour
* XMLToDict

## To do

- [x] Fix bug with tracks sorting
- [x] Add attempt date support
- [x] Create command line tool
- [ ] Auto-export plots
- [ ] Highlight PB
- [ ] Add stats to plots
- [ ] Add "start" state to traces plot