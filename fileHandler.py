import json

def saveLineToFile(lne):
    lneFile = open("line.json", 'w')
    lneFile.truncate()
    lneFile.write(json.dumps(lne))
    lneFile.close()

def savePtsToFile(pts):
    ptsFile = open("points.json", 'w')
    ptsFile.truncate()
    ptsFile.write(json.dumps(pts))
    ptsFile.close()

def saveShipsToFile(sps):
    spsFile = open("ships.json", 'w')
    spsFile.truncate()
    spsFile.write(json.dumps(sps))
    spsFile.close()

def saveStateToFile(stt):
    sttFile = open("state.json", 'w')
    sttFile.truncate()
    sttFile.write(json.dumps(stt))
    sttFile.close()


def loadJsonFromFile(file):
    f = open(file, 'r')
    fstr = f.read()
    dict = json.loads(fstr)
    return dict