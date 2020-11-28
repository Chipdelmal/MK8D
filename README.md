# MK8D

Python package for "Mario Kart 8 Deluxe" livesplit data analysis.  It processes Livesplit *lss* files (*XML* format) to provide a cleaner way to analyze the data by re-shaping it to a dataframe. 


This package is an improvement upon the [mk8dLivesplit](https://github.com/Chipdelmal/mk8dLivesplit) implementation. The main change is that it handles runs in a dataframe for easier parsing and filtering (sacrificing a bit of processing speed).
 
## Features

* Streamlined conversion from *lss* to *csv*
* Combine different *lss* files into one dataframe automatically

## Dependencies

* Pandas
* Numpy
* Plotly
* Matplotlib

## To do

- [x] Fix bug with tracks sorting
- [ ] Add attempt date support