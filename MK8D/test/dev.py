
import MK8D as mk
from os import path
import pandas as pd


###############################################################################
# Generate and export one dataframe
###############################################################################
(PT_FL, FILENAME, OUT) = (
    '/home/chipdelmal/Documents/GitHub/mk8dLivesplit/dta/',
    'Mario Kart 8 Deluxe - 48 Tracks (200cc, Digital, No Items).lss',
    'MK8D.csv'
)
FILEPATH = path.join(PT_FL, FILENAME)
data = mk.getRunsDataframeFromFile(FILEPATH, metadata=True)
data.to_csv(path.join(PT_FL, OUT), index=False)

###############################################################################
# Generate and export one dataframe
###############################################################################
FILENAMES = (
    'Mario Kart 8 Deluxe - 48 Tracks (200cc, Digital, No Items).lss',
    'Mario Kart 8 Deluxe - 48 Tracks (200cc, Cartridge, No Items).lss'
)
OUT = 'MK8D_Full.csv'
FILEPATHS = [path.join(PT_FL, i) for i in FILENAMES]
data = mk.compileRunsDataframeFromFiles(FILEPATHS)
data.to_csv(path.join(PT_FL, OUT), index=False)

