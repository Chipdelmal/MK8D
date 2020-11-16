

from xmltodict import parse



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
    seg = getSegments(doc)
    # Get metadata
    (sp, vs, ct, it) = [None] * 4
    if metadata:
        sp = getSpeed(doc)
        vs = getVersion(doc)
        it = getItems(doc)
        ct = getCategory(doc)
    # Assemble output dictionary
    runs = {
        'category': ct,
        'version': vs,
        'speed': sp,
        'items': it,
        'segments': seg
    }
    return runs