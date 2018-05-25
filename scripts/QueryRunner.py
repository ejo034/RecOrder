import sys
from v2 import AppCreator
from v2.scripts import EncodeDecode
from v2.scripts.Utility import Util, ErrorPrinter

appClass = AppCreator.App()
mysql = appClass.mysql


def _createcursorandconnection():
	try:
		conn = mysql.connect()
	except:
		ErrorPrinter.databaseConnectionError()
		sys.exit()
	cursor = conn.cursor()

	return cursor, conn


def _createcursor():
	cursor, conn = _createcursorandconnection()
	return cursor






# ********* GET calls ***************

def getTrackLength(trackId):
	cursor = _createcursor()
	cursor.callproc("getTrackLength", (trackId, ))
	data = cursor.fetchall()

	if data is ():
		return 0

	else:
		return data[0][0]


def getSongStructureList(songLength):
	if songLength == None or songLength == "":
		ErrorPrinter.invalidDBCallInput("Song structure")
		return None

	cursor = _createcursor()

	cursor.callproc("GetStructuresWithLength", (songLength,))
	data = cursor.fetchall()

	cleanData, datalength = Util.CleanReturnedList(data)
	
	return cleanData, datalength


def GetFinishedSongStructure(index):
	if index == None or index < 0:
		ErrorPrinter.invalidDBCallInput("Finished song structure")
		return None

	cursor = _createcursor()

	cursor.callproc("GetSongStructureHash", (index,))
	data = cursor.fetchall()

	if data == ():
		ErrorPrinter.databaseReturnedNothing("Finished song structure")
		return ""

	cleanData, _ = Util.CleanReturnedList(data)

	#decode
	decoded = EncodeDecode.decodeMessage(cleanData)
	if decoded == None:
		print("unable to decode")
		return ""

	return decoded


def getAllUserProfileIds(cursor=None):
	if cursor is None:
		cursor = _createcursor()

	cursor.callproc("GetAllUserProfileIds",())
	data = cursor.fetchall()


	cleanData, datalength = Util.CleanReturnedList(data)

	if datalength is 0:
		return None
	if datalength is 1:
		return [cleanData]

	return cleanData


def getAllTracks():
	cursor = _createcursor()
	cursor.callproc("GetAllTracks",())
	data = cursor.fetchall()
	return data


def getAllSliceStructures():
	cursor = _createcursor()
	cursor.callproc("GetAllSliceStructures", ())
	data = cursor.fetchall()

	if data != ():
		cleanData = []
		for item in data:
			itemList = {"hasGuitar" : item[1], "hasDrums" : item[3], "hasBass" : item[2]}
			cleanData.append(itemList)

		return cleanData

	else:
		return None


def getFifthFromKey(key):
	cursor = _createcursor()
	cursor.callproc("GetFifthFromKey", (key,))
	data = cursor.fetchall()

	if data is not ():
		cleanData = data[0][0]
		return cleanData

	else:
		return "None"


def getInstrumentIDFromInstrumentKey(key, cursor = None):
	if cursor is None:
		cursor = _createcursor()

	cursor.callproc("GetInstrumentFromTrack",(key,))
	data = cursor.fetchall()

	return data[0][1]


def getSongsWithBPMKeyAndInstrumentId(bpm, key, instrumentId, fifth=None ):
	cursor = _createcursor()

	if fifth is not None:
		#cursor.callproc("getTracksWithBpmKeyAndFifth", (bpm, key, fifth))
		print("fifth is not yet implemented")

	cursor.callproc("getTracksWithBpmKeyAndInstrument",(bpm, key, instrumentId,))
	data = cursor.fetchall()
	cleanList = []
	if data is not ():
		for item in data:
			cleanList.append(item)
	return cleanList


def getAllUsersPreferenceFull(cursor=None):
	if cursor is None:
		cursor = _createcursor()
	cursor.callproc("getAllUsersPreferences",())
	data = cursor.fetchall()

	if data is ():
		print("*** no user preferences found")
		return None

	return data


def getUserFullPreference(userid, cursor=None, splitCCId=True):
	if cursor is None:
		cursor = _createcursor()
	if splitCCId is True:
		cursor.callproc("getUserFullPreference",(userid,))
	else:
		cursor.callproc("getUserFullPreference2",(userid,))

	data = cursor.fetchall()

	if data is ():
		return None

	return data


def GetAllClipClipRelations(cursor=None):
	if cursor is None:
		cursor = _createcursor()

	cursor.callproc("getAllClipClipRelations", ())
	data = cursor.fetchall()

	if data is ():
		return None

	return data


def getClipsFromClipClipLinkId(id):
	cursor = _createcursor()
	cursor.callproc("GetClipClipLinkFromId",(id,))
	data = cursor.fetchall()
	if data is ():
		return None

	return data[0]


def getClipClipIdFromClips(clip1, clip2, cursor=None):
	if cursor is None:
		cursor = _createcursor()

	cursor.callproc("GetClipClipIdFromClips", (clip1, clip2,))
	data = cursor.fetchall()

	if data is ():
		return None

	return data[0][0]


def GetAllClipClipRelationsThatUserHasNotRated(userid, relevantIdList, writer, cursor=None):
	if cursor is None:
		cursor = _createcursor()

	ratedClipClipIds = []
	notSeenList = []
	relevantCCids = []

	userpreference = getUserFullPreference(userid=userid, cursor=cursor, splitCCId=False)
	if userpreference is None:
		userpreference = []

	for item in userpreference:
		ccid = item[1]
		ratedClipClipIds.append(ccid)


	for item in relevantIdList:
		item1 = item[0]
		item2 = item[1]
		ccId = getClipClipIdFromClips(item1, item2, cursor=cursor)
		relevantCCids.append(ccId)

	writer.PrintAndWrite("rated")
	writer.PrintAndWrite(ratedClipClipIds)

	writer.PrintAndWrite("relevant ccid")
	writer.PrintAndWrite(relevantCCids)

	for relevantCCid in relevantCCids:
		if relevantCCid not in ratedClipClipIds:
			notSeenList.append(relevantCCid)

	writer.PrintAndWrite("not seen")
	writer.PrintAndWrite(notSeenList)

	return notSeenList


def GetSongsWithBPMandKeyAndInstrumentAndInstense(bpm, key, instrumentId, intense):
	cursor = _createcursor()
	cursor.callproc('getTracksWithBpmKeyInstrumentAndScale', (bpm, key, instrumentId, intense, ))
	data = cursor.fetchall()
	cleanList = []
	if data is not ():
		for item in data:
			cleanList.append(item)
	return cleanList

# ********* POST ***************

def InsertFinishedSongStructure(structure):

	#encode
	encoded = EncodeDecode.encodeMessage(structure)
	if encoded is None:
		pass

	cursor, conn = _createcursorandconnection()

	cursor.callproc("InsertSongStructureHash", (encoded,))
	data = cursor.fetchall()

	if len(data) is 0:
		conn.commit()
		print("successful insertion ")

	else:
		print("something went wrong")
		print(data[0])



def insertUserPreferenceFromClips(userId, clip1, clip2, rating):
	'''
	:param userId:
	:param clip1:
	:param clip2:
	:return: boolean based on success of insertion
	'''

	#this method is clunky and could probably be done in one proc,
	#but i hate working with mysql workbench
	#so this is how it is


	if (userId is None) or (clip1 is None) or (clip2 is None) or (rating is None):
		return False

	cursor, conn = _createcursorandconnection()

	insertSuccess1 = InsertClipClipRelation(clip1, clip2, cursor=cursor, conn=conn)

	clipClipId = getClipClipIdFromClips(clip1, clip2)

	insertSuccess2 = InsertUserPreferenceFromCCid(userId, clipClipId, rating, cursor, conn)


	if insertSuccess1 and insertSuccess2:
		conn.commit()
		print("successful insertion ")
		return True

	else:
		return False


def InsertClipClipRelation(clip1, clip2, cursor=None, conn=None, ):
	if clip1 is None or clip2 is None:
		return False

	if cursor is None or conn is None:
		cursor, conn = _createcursorandconnection()

	cursor.callproc("InsertClipClipLink",(clip1, clip2,))
	data = cursor.fetchall()


	if len(data) is not 0:
		print("something went wrong")
		print(data[0])
		return False

	return True


def InsertUserPreferenceFromCCid(userId, clipclipID, rating, cursor=None, conn=None):
	if cursor is None or conn is None:
		cursor, conn = _createcursorandconnection()

	cursor.callproc("InsertUserPreference", (userId, clipclipID, rating))
	data = cursor.fetchall()

	if len(data) is not 0:
		print("something went wrong")
		print(data[0])
		return False

	return True


def InsertUserPreferenceFromSlice(userid, sliceList, rating):
	cursor, conn = _createcursorandconnection()

	length = len(sliceList)

	for i in range(0, length):
		clip1 = sliceList[i]
		clip2 = None

		if i + 1 >= length:
			clip2 = sliceList[0]
		else:
			clip2 = sliceList[i+1]

		insertSuccess1 = InsertClipClipRelation(clip1, clip2, cursor=cursor, conn=conn)
		clipClipId = getClipClipIdFromClips(clip1, clip2)
		insertSuccess2 = InsertUserPreferenceFromCCid(userId=userid, clipclipID=clipClipId, rating=rating, cursor=cursor, conn=conn)

	try:
		conn.commit()
	except:
		print("inserting went wrong")
		return False

	return True