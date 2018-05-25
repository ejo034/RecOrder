import os
from pydub import AudioSegment
from v2.scripts import QueryRunner


def _getClipFromId(id):
	directory = str(os.getcwd())
	path = "Audio/all/"

	#replace this with a call to the database for the path
	if id < 0:
		id = 1

	idString = str(id)
	filetype = ".wav"
	fullPath = str(path + idString + filetype)

	audio = None

	if os.path.isfile(fullPath):
		audio = AudioSegment.from_wav(fullPath)

	return audio



def mergeClips(clipId1, clipId2, shouldLoop=True):
	clip1 = _getClipFromId(clipId1)
	clip2 = _getClipFromId(clipId2)

	if clip1 is None or clip2 is None:
		return None

	firstIsLongestOrEqual = _checkIfFirstTrackIsLongerOrEqual(clipId1, clipId2)

	if firstIsLongestOrEqual:
		combined = clip1.overlay(clip2, loop=shouldLoop)
	else:
		combined = clip2.overlay(clip1, loop=shouldLoop)

	return combined



def chainClips(clipId1, clipId2):
	clip1 = _getClipFromId(clipId1)
	clip2 = _getClipFromId(clipId2)

	if clip1 is None or clip2 is None:
		return None

	chained = AppendClip2ToClip1(clip1,clip2)

	return  chained



def mergeClipsFromList(listOfClipId):
	print("merging from list")
	print(listOfClipId)

	merged = None
	index = 0

	for id in listOfClipId:

		clip = _getClipFromId(id)
		if clip is None:
			merged = None
			break

		if index is 0:
			merged = clip
		else:
			#need a length check here
			merged = merged.overlay(clip, loop=True)

		index += 1

	return merged



def AppendClip2ToClip1(song, clip):
	appendedSong = song.append(clip, crossfade=100)
	return appendedSong



def _checkIfFirstTrackIsLongerOrEqual(clipId1, clipId2):
	track1Len = QueryRunner.getTrackLength(clipId1)
	track2Len = QueryRunner.getTrackLength(clipId2)

	if track1Len == track2Len or track1Len > track2Len:
		return True
	else:
		return False



def exportAudio(audio, filename):
	print("path and name: {0}".format(filename))

	try:
		audio.export(filename, format="wav")
		return True

	except:
		print("Export could not be made")
		return False