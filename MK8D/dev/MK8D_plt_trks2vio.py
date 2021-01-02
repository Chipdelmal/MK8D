
import time 
from datetime import datetime
from datetime import timedelta
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import MK8D as mk


(PT_DT, PT_PL) = ('./data/MK8D_trks.csv', './plots/Violins.html')
TRACKS = mk.TRACKS
mixed = True

data = pd.read_csv(PT_DT)
data = data[data['Track'] != 'Start']
versions = list(data['Version'].unique())
tracks = list(data['Track'].unique())
###############################################################################
# Violin Plot
###############################################################################
bestTimes = [min(data[data['Track'] == track]['Time']) for track in TRACKS]
worstTimes = [max(data[data['Track'] == track]['Time']) for track in TRACKS]
bestStr = [str(timedelta(seconds=i))[2:mk.TPREC] for i in bestTimes] 
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
            side='negative', points=False, line_color='#2614ED', 
            spanmode='hard', line={'width': .75}
        )
    )
    fig.add_trace(
        go.Violin(
            x=data['Track'][data['Version']==versions[1]],
            y=data['Time'][data['Version']==versions[1]],
            legendgroup=versions[1], scalegroup=versions[1], name=versions[1],
            side='positive', points=False, line_color='#FF006E', 
            spanmode='hard', line={'width': .75}
        )
    )
else:
    # Plot only one violin ----------------------------------------------------
    fig = go.Figure()
    fig.add_trace(
        go.Violin(
            x=data['Track'], y=data['Time'],
            points=False, line_color='#2614ED', 
            spanmode='hard', line={'width': 1.5},
        )
    )
# Update axes -----------------------------------------------------------------
fig.update_traces(meanline_visible=True)
fig.update_layout(violingap=0, violinmode='overlay')
fig.update_xaxes(
    range=[-1, len(TRACKS)], 
    tickvals=TRACKS, tickfont_size=17, tickangle=90
)
fig.update_yaxes(
    range=[min(bestTimes)-15, max(worstTimes)+2], 
)
fig.update_layout(
    # title='Runs Progress',
    font=dict(size=20),
    xaxis=dict(title_text='Track', titlefont=dict(size=30)),
    yaxis=dict(title_text='Time (seconds)', titlefont=dict(size=30))
)
# Add annotation --------------------------------------------------------------
for (i, stat) in enumerate(bestStr):
    fig.add_annotation(
        x=i, y=.01,
        text=stat,
        font={'size': 12.5, 'color': '#233090'},
        showarrow=False,
        yref="paper",
        textangle=90
    )
# Add Separator lines ---------------------------------------------------------
vLines = [
    dict(
        type= 'line',
        yref= 'paper', y0= 0, y1= 1,
        xref= 'x', x0=i-.5, x1=i-.5,
        line=dict(color='#233090', width=.75, dash='dot')
    ) for i in range(0, len(TRACKS)+1, 4)
]
fig.update_layout(shapes=vLines)
# Show and export -------------------------------------------------------------
fig.show()
fig.write_html(PT_PL)