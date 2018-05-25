from v2.scripts.SongCreation import SliceBuilder, SongStructureSelector
from v2.scripts.Utility import Util
from v2.scripts.InOut import AudioMerger, FeedbackRecorder, PrimeMover, Writer
from v2.scripts import QueryRunner



class SongCreator:

	def __init__(self, bpm, key, length, profileKey):
		self.bpm = bpm
		self.key = key
		self.length = length
		self.profileKey = profileKey
		self.clipclipRelation = []
		self.writer = Writer.Writer(self.profileKey)
		self.sliceBuilder = SliceBuilder.SliceBuilder(self.writer)



	def CreateSong(self):
		self.writer.PrintAndWrite("")
		self.writer.PrintAndWrite("__________________________________")
		self.writer.PrintAndWrite("_* CREATING SONG", False)
		elementDict = {}

		# song structure
		self.writer.PrintAndWrite("__* SELECTING STRUCTURE ", False)
		structure = SongStructureSelector.SelectSongStructure(self.length)

		self.writer.PrintAndWrite("Selected Structure: " + structure, False)

		# split song structure into parts
		elementList = Util.SplitStructureIntoParts(structure)

		# for each element in the list, get a slice for it
		for element in elementList:
			sliceID, slice = self._getSlice(element)
			elementDict[sliceID] = slice

		# moving old files
		PrimeMover.moveOldAudioFiles(self.writer)

		# creating song audiofile
		self._putSongToghether(structure, elementDict)

		# regestering ccrelations
		self._registerClipRelations(elementDict)

		# feedback
		self.writer.PrintAndWrite("", False)
		self.writer.PrintAndWrite("** TIME TO GIVE FEEDBACK** ", False)
		self.writer.PrintAndWrite("", False)
		#FeedbackRecorder.GetNumOfRandomFromClipRelations(self.profileKey, self.clipclipRelation, writer=self.writer, numRandom=3)
		FeedbackRecorder.GetFeedbackOnSong(self.profileKey, elementDict, writer=self.writer)
		FeedbackRecorder.GetFeedbackForKNumberOfSlices(self.profileKey, elementDict, writer=self.writer, numRandom=3)

		self.writer.PrintAndWrite("", False)
		self.writer.PrintAndWrite("** DONE ** ", False)


	def _getSlice(self, part):
		self.writer.PrintAndWrite("generating slice for " + str(part))

		slice = self.sliceBuilder.buildSlice(
			part=part,
			bpm=self.bpm,
			key=self.key,
			profileId=self.profileKey,
			useItemBased=True
		)

		if slice is None:
			self.writer.PrintAndWrite("slice returned none")
			self.writer.PrintAndWrite("")

			slice = self.sliceBuilder.buildSlice(
				part=part,
				bpm=self.bpm,
				key=self.key,
				profileId=self.profileKey,
				useItemBased=False
			)

		self.writer.PrintAndWrite("")
		return part, slice



	def _putSongToghether(self, structure, elementDict):
		self.writer.PrintAndWrite("", False)
		self.writer.PrintAndWrite("** PUTTING SONG TOGETHER ** ", False)

		song = None

		for element in structure:

			if element is None or elementDict[element] is None:
				self.writer.PrintAndWrite("The song had missing parts, or parts that were None. Stopped.")
				return None

			elements = elementDict[element].getElements()
			audioclip = None

			if len(elements) is 3:
				audioclip = AudioMerger.mergeClipsFromList(elements)

			elif len(elements) is 2:
				audioclip = AudioMerger.mergeClips(clipId1=elements[0], clipId2=elements[1])
			else:
				return None

			if audioclip is None:
				return None

			if song is None:
				song = audioclip
			else:
				song = AudioMerger.AppendClip2ToClip1(song, audioclip)

		filename = Util.GeneratePathAndFileNameForAudiofile(isSong=True)
		exportSuccess = AudioMerger.exportAudio(song, filename=filename)
		if not exportSuccess:
			return None



	def _registerClipRelations(self, elementDictionary):
		self.writer.PrintAndWrite("", False)
		self.writer.PrintAndWrite("** REGISTERING CLIP RELATIONS **", False)

		for i in range(0, 3):
			currentItem = None
			previousItem = None
			for element in elementDictionary:
				previousItem = currentItem
				temp = elementDictionary[element].getElements()

				if len(temp) < 3:
					previousItem = None
					currentItem = None
					break

				currentItem = temp[i]
				if previousItem is None:
					continue

				self.clipclipRelation.append([previousItem,currentItem])
				insertSuccess = QueryRunner.InsertClipClipRelation(previousItem, currentItem)
				if insertSuccess:
					continue
				else:
					print("insert fail")
					break

