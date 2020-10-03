import json


def getJsonFromFile(fileName):
    file = open(fileName, 'r')
    fileText = file.read()
    data = json.loads(fileText)
    return data


def writeToFileAsJSON(data, fileName):
    file = open(fileName, 'w')
    json.dump(data, file)