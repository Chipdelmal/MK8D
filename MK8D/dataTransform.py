
import numpy as np
import pandas as pd
import MK8D.constants as cnst


def getFinishedRunsID(data, tracks=cnst.TRACKS):
    runsIds = []
    for i in tracks:
        filtr = (data['Track']== i)
        runsIds.append(set(data['ID'][filtr]))
    finishedRuns = set.intersection(*runsIds)
    return finishedRuns


def getFinishedRuns(data, tracks=cnst.TRACKS):
    fshdRuns = getFinishedRunsID(data, tracks)
    fltr = (data['ID'].isin(fshdRuns), data['Track'].isin(set(tracks)))
    fltrBool = [all(i) for i in zip(*fltr)]
    return data[fltrBool]


def getTrackTime(data, rid, track):
    row = data[data['ID'] == rid]
    return float(row[row['Track'] == track]['Time'])


def getRunByID(data, rid):
    return data[(data['ID'] == rid)]


def convertRunCTime(runData, tracks=cnst.TRACKS):
    rid = list(runData['ID'])[0]
    runData['Track'] = pd.Categorical(
        runData.Track, categories=tracks, ordered=True
    )
    runData = runData.sort_values(by='Track')
    cTime = np.cumsum([getTrackTime(runData, rid, track) for track in tracks])
    runData['Time'] = cTime
    return runData


def convertFinishedRunsToCTimes(data, fshdRIds, tracks=cnst.TRACKS):
    fshdRunsIDList = list(fshdRIds)
    runsCTimesDataList = []
    for rid in fshdRunsIDList:
        runData = getRunByID(data, rid)
        runDataCTime = convertRunCTime(runData, tracks=tracks)
        runsCTimesDataList.append(runDataCTime)
    runsCTimes = pd.concat(runsCTimesDataList)
    return runsCTimes


def centerTrackTimes(times, centerFunction=np.mean):
    offset = centerFunction(times)
    offsetTimes = [(i - offset) for i in times]
    return (offsetTimes, offset)


def centerRunsCTimes(runsCTimes, centerFunction=np.mean):
    cName = centerFunction.__name__
    # Get unique run ID and tracks names 
    (ids, tracks) = (
        list(runsCTimes['ID'].unique()), 
        list(runsCTimes['Track'].unique())
    )
    # Create copy to store modified dataframe
    runsCTimesC = runsCTimes.copy()
    offsets = []
    # Iterate through tracks to get the "center" and shift times around it
    for track in tracks:
        trackTimes = [getTrackTime(runsCTimes, i, track) for i in ids]
        (centered, center) = centerTrackTimes(
            trackTimes, centerFunction=centerFunction
        )
        offsets.append(center)
        # Replace centered time in the copied dataframe
        for (j, time) in enumerate(centered):
            fltr = (runsCTimesC['Track'] == track, runsCTimes['ID'] == ids[j])
            selector = [all(i) for i in zip(*fltr)]
            runsCTimesC[selector]['Time'] = ids[j]
            runsCTimesC.loc[selector, cName+' offset'] = time
            runsCTimesC.loc[selector, cName] = center
    return runsCTimesC


def convertTimeFromSec(data, timeTarget='Hours'):
    dataTemp = data.copy()
    if timeTarget == 'Hours':
        timeFun = lambda x: x / (60 * 60)
    elif timeTarget == 'Minutes':
        timeFun = lambda x: x / 60
    else:
        return 'Available options are: Hours and Minutes'
    dataTemp['Time'] = dataTemp['Time'].apply(lambda x: timeFun(x))
    return dataTemp
