from v2.scripts.RecSys import RecommenderSelector as recSelect
from v2.scripts.Utility import Util
from v2.scripts import QueryRunner

class Slice:
	def __init__(self,bpm, key):
		self.bpm = bpm
		self.key = key
		self.elements = []
	def addElement(self, newElement):
		if self.elements is None:
			self.elements = []
		self.elements.append(newElement)
	def getElements(self):
		return self.elements



class SliceBuilder:

	def __init__(self, writer):
		self.engine = None
		self.sliceStructs = QueryRunner.getAllSliceStructures()
		self.generatedSlices = {}
		self.writer = writer


	def buildSlice(self, part, bpm, key, profileId, useItemBased=None):

		if self.engine is None and useItemBased is not None:
			# select rec engine
			self.engine = recSelect.selectRecommendationEngine(profileId, useItemBased, self.writer)

		if part in self.generatedSlices:
			return self.generatedSlices[part]


		#get random sliceStructure for slice
		sliceStructure = self._randomSliceStructure()
		self.writer.PrintAndWrite("slice structure for " + str(part) + " : " + str(sliceStructure))

		slice = Slice(bpm, key)

		dictionaryIndex = 1
		for keyDict in sliceStructure:

			#the instrument track is empty, skip to the next instrument
			if sliceStructure[keyDict] is 0:
				dictionaryIndex += 1
				continue

			tempInstrument = dictionaryIndex
			if tempInstrument is 2:
				tempKey = "None"
			else:
				tempKey = key

			recommend = self.engine.GetRecommendation(
				profileId=profileId,
				key=tempKey,
				bpm=bpm,
				instrumentID=tempInstrument,
				section=part
			)

			if recommend is None:
				#the engine did not manage to get a recommendation
				self.writer.PrintAndWrite("could not make recommendation, picks a random result")

				randomResult = Util.GetRandomClip(bpm, tempKey, tempInstrument)
				if randomResult is None:
					return None
				else:
					recommend = randomResult
					self.writer.PrintAndWrite("** selected result ran", False)
					self.writer.PrintAndWrite(recommend)

			slice.addElement(recommend)
			dictionaryIndex += 1

		self.writer.PrintAndWrite("slice:", False)
		self.writer.PrintAndWrite(slice.getElements(), False)
		self.writer.PrintAndWrite("", False)

		self.generatedSlices[part] = slice

		return slice



	def _randomSliceStructure(self):
		if self.sliceStructs is None:
			self.sliceStructs = QueryRunner.getAllSliceStructures()

		randomSelection = Util.GetRandomElementFromList(self.sliceStructs)

		return randomSelection