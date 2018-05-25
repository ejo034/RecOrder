import unittest
from v2.scripts import QueryRunner

class QueryRunnerTester(unittest.TestCase):

	def testGetFifth(self):
		key = "A"
		answer = "E"
		result = QueryRunner.getFifthFromKey(key)
		self.assertEqual(answer, result)

	def testGetFifthWrongInput(self):
		key = "W"
		answer = "None"
		result = QueryRunner.getFifthFromKey(key)
		self.assertEqual(answer, result)

	def testGetFifthNone(self):
		key = "None"
		answer = "None"
		result = QueryRunner.getFifthFromKey(key)
		self.assertEqual(answer, result)

