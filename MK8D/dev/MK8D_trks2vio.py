
import time 
from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import MK8D as mk


(PT_DT, PT_PL) = ('./data/MK8D_trks.csv', './plots/Violins.html')
tracksFltr = mk.TRACKS
mixed = False

data = pd.read_csv(PT_DT)
versions = list(data['Version'].unique())
tracks = list(data['Track'].unique())
###############################################################################
# Violin Plot
###############################################################################
if (len(versions) == 2) and (not mixed):
    # Plot split violins if Digital/Cartridge ---------------------------------
    fig = go.Figure()
    fig.add_trace(
        go.Violin(
            x=data['Track'][data['Version']==versions[0]],
            y=data['Time'][data['Version']==versions[0]],
            legendgroup=versions[0], scalegroup=versions[0], name=versions[0],
            side='negative', points=False, line_color='blue', spanmode='hard',
            line={'width': .75}
        )
    )
    fig.add_trace(
        go.Violin(
            x=data['Track'][data['Version']==versions[1]],
            y=data['Time'][data['Version']==versions[1]],
            legendgroup=versions[1], scalegroup=versions[1], name=versions[1],
            side='positive', points=False, line_color='red', spanmode='hard',
            line={'width': .75}
        )
    )
else:
    # Plot only one violin ----------------------------------------------------
    fig = go.Figure()
    fig.add_trace(
        go.Violin(
            x=data['Track'], y=data['Time'],
            points=False, line_color='blue', spanmode='hard',
            line={'width': .75}
        )
    )
# Update axes -----------------------------------------------------------------
fig.update_traces(meanline_visible=True)
fig.update_layout(violingap=0, violinmode='overlay')
fig.update_xaxes(
    range=[-1, len(tracks)], tickvals=tracksFltr, 
    tickfont_size=10, tickangle=90
)
fig.show()
fig.write_html(PT_PL)