
import pandas as pd
from xmltodict import parse
from collections import OrderedDict
import MK8D.auxiliary as aux


def getDictFromXMLFile(filePath):
    with open(filePath) as fd:
        doc = parse(fd.read())
    return doc


def getSegments(doc):
    return doc['Run']['Segments']['Segment']


def getSpeed(doc):
    sp = doc['Run']['Metadata']['SpeedrunComVariables']['Variable'][0]['#text']
    return sp


def getVersion(doc):
    vs = doc['Run']['Metadata']['SpeedrunComVariables']['Variable'][1]['#text']
    return vs


def getItems(doc):
    it = doc['Run']['Metadata']['SpeedrunComVariables']['Variable'][2]['#text']
    return it


def getCategory(doc):
    ct = doc['Run']['CategoryName']
    return ct

    

def parseRunsFromFile(filePath, metadata=True):
    # Load file into dictionary and get segments
    doc = getDictFromXMLFile(filePath)
    segments = getSegments(doc)
    # Get metadata
    (speed, version, category, items) = [None] * 4
    if metadata:
        (speed, version, items, category) = (
            getSpeed(doc), getVersion(doc),
            getItems(doc), getCategory(doc)
        )
    # Assemble output dictionary
    runs = {
        'category': category,
        'version': version,
        'speed': speed,
        'items': items,
        'segments': segments
    }
    return runs


def getSegmentsNames(segments):
    return [i['Name'] for i in segments]


def getRunsDict(runs):
    (nms, tracks) = (getSegmentsNames(runs['segments']), OrderedDict())
    for (ix, track) in enumerate(runs['segments']):
        tHist = track['SegmentHistory']['Time']
        tEntry = {int(i['@id']): aux.tStrToSecs(i['RealTime']) for i in tHist}
        tracks.update({nms[ix]: tEntry})
    return tracks



def getTrackList(runs, tracks, name):
    # Constant data and track info
    (spd, itm, cat, ver) = (
        runs['speed'], runs['items'], runs['category'], runs['version']
    )
    track = tracks[name]
    # Run ID with timings
    (ids, times) = (list(track.keys()), list(track.values()))
    trackList = [
        (name, time, int(key), ver, itm, spd, cat)
        for (key, time) in zip(ids, times)
    ] 
    return trackList



def getRunsDataframe(runs, tracks):
    tracksNames = list(tracks.keys())
    tracksList = []
    for i in tracksNames:
        tracksList.extend(getTrackList(runs, tracks, i))
    columns = ['Track', 'Time', 'ID', 'Version', 'Items', 'Speed', 'Category']
    runsDataframe = pd.DataFrame(tracksList, columns=columns)
    return runsDataframe