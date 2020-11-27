
import MK8D as mk
from os import path
import pandas as pd
import plotly.graph_objects as go


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
# Concatenate and export one dataframe from files list
###############################################################################
FILENAMES = (
    'Mario Kart 8 Deluxe - 48 Tracks (200cc, Digital, No Items).lss', 
    # 'Mario Kart 8 Deluxe - 48 Tracks (200cc, Cartridge, No Items).lss'
)
OUT = 'MK8D_Full.csv'
FILEPATHS = [path.join(PT_FL, i) for i in FILENAMES]
data = mk.compileRunsDataframeFromFiles(FILEPATHS)
data.to_csv(path.join(PT_FL, OUT), index=False)

###############################################################################
# Traces Plot
###############################################################################
fshdRunsIDs = sorted(list(mk.getFinishedRunsID(data, mk.TRACKS)))
fshdRuns = mk.getFinishedRuns(data, mk.TRACKS)
runsCTimes = mk.convertFinishedRunsToCTimes(fshdRuns, fshdRunsIDs)
runsCTimes