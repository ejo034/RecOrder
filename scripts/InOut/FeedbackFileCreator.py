from v2.scripts.InOut import AudioMerger
from v2.scripts.Utility import Util
from v2.scripts import QueryRunner



def CreateCCRelationAudioFileForEvaluation(ccID, filename=""):
	print("exporting clip-clip relation audio track")

	result = QueryRunner.getClipsFromClipClipLinkId(ccID)

	clip1 = result[0]
	clip2 = result[1]

	audioclip = AudioMerger.chainClips(
		clipId1=clip1,
		clipId2=clip2
	)
	if audioclip is None:
		return False

	print("audioclip: {0}".format(audioclip))

	nameofFile = "ccrel" + str(filename)
	filename = Util.GeneratePathAndFileNameForAudiofile(filename=nameofFile)
	exportSuccess = AudioMerger.exportAudio(
		audio=audioclip,
		filename=filename
	)

	print("export success: {0}".format(exportSuccess))
	print()
	return True





def CreateSliceAudioFileForEvaluation(sliceIdList):
	print("exporting slice audio track")

	audioclip = AudioMerger.mergeClipsFromList(sliceIdList)
	if audioclip is None:
		return False

	print("audioclip: {0}".format(audioclip))

	tempfilename = "slice_" + str(sliceIdList)
	filename = Util.GeneratePathAndFileNameForAudiofile(filename=tempfilename)

	exportSuccess = AudioMerger.exportAudio(
		audio=audioclip,
		filename=filename
	)

	print("export success: {0}".format(exportSuccess))
	print()

	return True