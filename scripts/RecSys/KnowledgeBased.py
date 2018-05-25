from v2.scripts.RecSys import RecSysEngine
from v2.scripts import QueryRunner
from random import randint

class KnowledgeBased(RecSysEngine.RecSysEngine):

	def __init__(self):
		super().__init__()

		print("creating new instance of Knowledge Based")
		self.bpm = 0
		self.min_bpm = 0
		self.max_bpm = 0
		self.key = "A"


	def GetRecommendation(self, profileId=None, key=None, bpm=None, instrumentID=None, section=None):
		if bpm is not None:
			self._calculateBPMranges(bpm)
		if key is not None:
			self._setValidKeys(key)

		songList = None
		if section is "A":
			songList = self._getLowIntenseTracks(bpm, key, instrumentID)
		elif section is "B":
			songList = self._getMediumIntenseTracks(bpm, key, instrumentID)
		elif section is "C":
			songList = self._getHighIntenseTracks(bpm, key, instrumentID)
		else:
			songList = self._getAllTracks(bpm, key, instrumentID)

		if songList is []:
			return None

		length = len(songList) - 1
		randomIndex = randint(0, length)
		result = songList[randomIndex][0]
		return result

	def _getAllTracks(self, bpm, key, instrumentID):
		songList = QueryRunner.getSongsWithBPMKeyAndInstrumentId(bpm, key, instrumentID)
		return songList

	def _getLowIntenseTracks(self, bpm, key, instrumentID):
		songList1 = QueryRunner.GetSongsWithBPMandKeyAndInstrumentAndInstense(bpm=bpm, key=key, instrumentId=instrumentID, intense=1)
		songList2 = QueryRunner.GetSongsWithBPMandKeyAndInstrumentAndInstense(bpm=bpm, key=key, instrumentId=instrumentID, intense=2)
		for item in songList2:
			songList1.append(item)
		return songList1

	def _getMediumIntenseTracks(self, bpm, key, instrumentID):
		songList1 = QueryRunner.GetSongsWithBPMandKeyAndInstrumentAndInstense(bpm=bpm, key=key, instrumentId=instrumentID, intense=3)
		songList2 = QueryRunner.GetSongsWithBPMandKeyAndInstrumentAndInstense(bpm=bpm, key=key, instrumentId=instrumentID, intense=4)
		for item in songList2:
			songList1.append(item)
		return songList1

	def _getHighIntenseTracks(self, bpm, key, instrumentID):
		songList1 = QueryRunner.GetSongsWithBPMandKeyAndInstrumentAndInstense(bpm=bpm, key=key, instrumentId=instrumentID, intense=4)
		songList2 = QueryRunner.GetSongsWithBPMandKeyAndInstrumentAndInstense(bpm=bpm, key=key, instrumentId=instrumentID, intense=5)
		for item in songList2:
			songList1.append(item)
		return songList1


	def _calculateBPMranges(self, bpm):
		intBpm = int(bpm)
		self.bpm = intBpm
		self.min_bpm = intBpm / 2
		self.max_bpm = intBpm * 2


	def _setValidKeys(self, key):
		self.key = str(key)

		if key is not "None":
			self.keyFifth = QueryRunner.getFifthFromKey(key)


