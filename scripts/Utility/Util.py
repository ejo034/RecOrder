from datetime import datetime
from random import randint
from v2.scripts import QueryRunner

def GetRandomElementFromList(list):
	listLength = len(list)

	if listLength is 1:
		return list[0]

	randomIndex = randint(0, listLength-1)
	element = list[randomIndex]
	return element


def GetRandomClip(bpm, key, instrumentId):
	songList = QueryRunner.getSongsWithBPMKeyAndInstrumentId(bpm, key, instrumentId)
	if songList is []:
		return None

	length = len(songList) - 1
	randomIndex = randint(0, length)

	return songList[randomIndex][0]




def SplitStructureIntoParts(structure):
	elementList = []

	for char in structure:
		if char not in elementList:
			elementList.append(char)

	return elementList




def CleanReturnedList(retList):
	length = len(retList)

	if length == 0:
		return [], 0

	if length == 1:
		return retList[0][0], 1

	_tempList = []

	for item in retList:
		_tempList.append(item[0])

	return _tempList, length


def GeneratePathAndFileNameForAudiofile(isSong=False, filename=""):
	pathAndName = "Audio/generated/"

	timestamp = GetDatestampForFileName()

	if isSong:
		pathAndName += "generatedSong_" + timestamp
	else:
		if filename != "":
			pathAndName += str(filename) + "_" + timestamp
		else:
			pathAndName += "clip_" + timestamp

	pathAndName += ".wav"

	return pathAndName


def GetDatestampForFileName():
	return str(datetime.now()).replace(":","").replace("-","").replace(".","").replace(" ","")

