
import numpy as np
import pandas as pd
import MK8D.constants as cnst


def getFinishedRunsID(data, tracks):
    runsIds = []
    for i in cnst.TRACKS:
        filtr = (data['Track']== i)
        runsIds.append(set(data['ID'][filtr]))
    finishedRuns = set.intersection(*runsIds)
    return finishedRuns


def getFinishedRuns(data, tracks):
    fshdRuns = getFinishedRunsID(data, cnst.TRACKS)
    fltr = data['ID'].isin(fshdRuns)
    return data[fltr]


def getTrackTime(data, rid, track):
    row = data[data['ID'] == rid]
    return float(row[data['Track'] == track]['Time'])


def getRunByID(data, rid):
    return data[(data['ID'] == rid)]


def convertRunCTime(runData, tracks=cnst.TRACKS):
    rid = list(runData['ID'])[0]
    runData['Track'] = pd.Categorical(
        runData.Track, categories=tracks, ordered=True
    )
    runData.sort_values(by='Track')
    cTime = np.cumsum([getTrackTime(runData, rid, track) for track in tracks])
    runData['Time'] = cTime
    return runData


def convertFinishedRunsToCTimes(data, fshdRIds):
    fshdRunsIDList = list(fshdRIds)
    runsCTimesDataList = []
    for rid in fshdRunsIDList:
        runData = getRunByID(data, rid)
        runDataCTime = convertRunCTime(runData, tracks=cnst.TRACKS)
        runsCTimesDataList.append(runDataCTime)
    runsCTimes = pd.concat(runsCTimesDataList)
    return runsCTimes