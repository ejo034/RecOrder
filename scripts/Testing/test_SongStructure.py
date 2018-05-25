import unittest

from v2.scripts.SongCreation import SongStructureSelector as ssSelect


class SongStructureTesting(unittest.TestCase):


	def testSelectSongStructure(self):
		length = "short"

		self._prints(length)

		validReturnList = self._getList(length)
		value = ssSelect.SelectSongStructure(length)

		self.assertIn(value, validReturnList)


	def testMediumSongStructure(self):
		length = "medium"

		self._prints(length)

		validReturnList = self._getList(length)
		value = ssSelect.SelectSongStructure(length)

		self.assertIn(value, validReturnList)


	def testLongSongStructure(self):
		length = "long"

		self._prints(length)

		validReturnList = self._getList(length)
		value = ssSelect.SelectSongStructure(length)

		self.assertIn(value, validReturnList)


	def _getList(self, length):
		validReturnList, validReturnLength = ssSelect._GetListOfStructuresFromDb(length)
		return validReturnList


	def _prints(self,input):
		print("** TESTING " + input + " SONG STRUCTURE ** ")


