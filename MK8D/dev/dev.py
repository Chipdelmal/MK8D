
import MK8D as mk
import numpy as np
from os import path
import pandas as pd
from colour import Color
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
    # 'Mario Kart 8 Deluxe - 48 Tracks (200cc, Cartridge, No Items).lss'
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
fig = px.line(
    mk.convertTimeFromSec(runsCTimes, timeTarget='Hours'),
    x="Track", y="Time", color='ID'
)
fig

###############################################################################
# Center CTimes around value
###############################################################################
runsCTimesC = mk.convertTimeFromSec(
        mk.centerRunsCTimes(runsCTimes, centerFunction=np.mean),
        timeTarget='Minutes'
    )
fig = px.line(
    runsCTimesC, x="Track", y="Time", color='ID',
    color_discrete_sequence=colorsList
)
fig




(alphaOffset, lumaOffset, runsNum) = (.25, .25, len(fshdRunsIDs))
colorsList = [None] * runsNum
for i in range(runsNum):
    c = Color("#233090")
    baseLum = 1 - c.get_luminance()
    print(1 - (baseLum + ((1-baseLum)/runsNum * i)))
    c.set_luminance((baseLum - ((1-baseLum)/runsNum * i)))
    rgb = c.get_rgb()
    colorsList[i] = 'rgba'+ str((rgb[0], rgb[1], rgb[2], alphaOffset + ((1-alphaOffset) * i/runsNum)))
colorsList

