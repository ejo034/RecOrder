import unittest

from v2.scripts.Utility import Util


class UtilTesting(unittest.TestCase):

	#Random element from list testing

	def testRandomElementFromList_NormalUse(self):
		list = ["A", "B", "C"]

		element = Util.GetRandomElementFromList(list)
		self.assertIn(element, list)

	def testRandomElementFromList_OneElement(self):
		soloList = ["D"]

		soloElement = Util.GetRandomElementFromList(soloList)
		self.assertEqual(soloElement, "D")


	def testRandomElementFromList_LastElement(self):
		list = ["A", "B", "C"]

		element = ""
		while element is not "C":
			element = Util.GetRandomElementFromList(list)

		self.assertEqual(element, "C")



	#TESTING CLEAN RETURNED LIST

	def testCleanReturnedList_Empty(self):
		list = []
		retList, retListLength = Util.CleanReturnedList(list)

		self.assertEqual(retList, [])
		self.assertEqual(retListLength, 0)

	def testCleanReturnedList_One(self):
		list = (('element1',),)

		retList, retLength = Util.CleanReturnedList(list)

		self.assertEqual(retList, "element1")
		self.assertEqual(retLength, 1)


	def testCleanReturnedList_Multiple(self):
		list = (('element1',), ('element2',))
		listTest = ["element1", "element2"]

		retList, retLength = Util.CleanReturnedList(list)

		self.assertEqual(retList, listTest)
		self.assertEqual(retLength, 2)






if __name__ == '__main__':
	unittest.main()