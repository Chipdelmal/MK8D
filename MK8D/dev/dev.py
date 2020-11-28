
import MK8D as mk
from os import path
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go


###############################################################################
# Generate and export one dataframe
###############################################################################
(PT_FL, FILENAME, OUT) = (
    './data/',
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
    'Mario Kart 8 Deluxe - 48 Tracks (200cc, Cartridge, No Items).lss'
)
OUT = 'MK8D_Full.csv'
FILEPATHS = [path.join(PT_FL, i) for i in FILENAMES]
data = mk.compileRunsDataframeFromFiles(FILEPATHS, prependID=True)
data.to_csv(path.join(PT_FL, OUT), index=False)

###############################################################################
# Filter for finished runs
###############################################################################
tracksFltr = mk.TRACKS
fshdRunsIDs = sorted(list(mk.getFinishedRunsID(data, tracksFltr)))
fshdRuns = mk.getFinishedRuns(data, tracksFltr)
runsCTimes = mk.convertFinishedRunsToCTimes(fshdRuns, fshdRunsIDs, tracksFltr)

###############################################################################
# Traces plot
###############################################################################
fig = px.line(runsCTimes, x="Track", y="Time", color='ID')
fig

###############################################################################
# Center CTimes around value
###############################################################################
data = runsCTimes
centerFunction = np.min

ids = list(runsCTimes['ID'].unique())
tracks = list(data['Track'].unique())

track = tracks[0]
trackTimes = [mk.getTrackTime(data, i, track) for i in ids]
mk.centerTrackTimes(trackTimes, centerFunction=np.min)



