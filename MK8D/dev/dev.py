
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
centerFunction = np.max

(ids, tracks) = (
    list(runsCTimes['ID'].unique()), 
    list(data['Track'].unique())
)

runsCTimesC = runsCTimes.copy()

for track in tracks:
    trackTimes = [mk.getTrackTime(data, i, track) for i in ids]
    centered = mk.centerTrackTimes(trackTimes, centerFunction=centerFunction)
    # Replace centered time in the copied dataframe
    for (j, time) in enumerate(centered):
        fltr = (runsCTimesC['Track'] == track, runsCTimes['ID'] == ids[j])
        selector = [all(i) for i in zip(*fltr)]
        runsCTimesC[selector]['Time'] = ids[j]
        runsCTimesC.loc[selector, 'Time'] = time

fig = px.line(runsCTimesC, x="Track", y="Time", color='ID')
fig


