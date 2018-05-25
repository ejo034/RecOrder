from v2.scripts import QueryRunner
from v2.scripts.Utility import Util

validTypes = ["short", "medium", "long"]


def SelectSongStructure(songLength):
	inputStr = str(songLength).lower()

	if not _validateInputString(inputStr):
		print("not valid")
		return ""

	list, length = _GetListOfStructuresFromDb(inputStr)

	if length > 1:
		element = Util.GetRandomElementFromList(list)
		return element
	else:
		return list


def _validateInputString(inputStr):
	if inputStr not in validTypes:
		return False
	return True


def _GetListOfStructuresFromDb(inputStr):
	return QueryRunner.getSongStructureList(inputStr)
