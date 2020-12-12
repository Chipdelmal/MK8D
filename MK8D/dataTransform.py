
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
    return offsetTimes