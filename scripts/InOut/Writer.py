from builtins import print

from v2.scripts import QueryRunner
from v2.scripts.InOut import Reader
from v2.scripts.Utility import Util
from v2.scripts.SongCreation import SongCreator




class Writer():
	def __init__(self, userNumber):
		self.usernumber = userNumber


	def PrintAndWrite(self, input, onlyWrite=True):

		if not onlyWrite:
			print(input)

		path = str("data/u{0}.txt".format(self.usernumber))

		with open(path, 'a') as f:

			f.write(str(input) + "\n")




def WriteScoresToFile():
	print("*** WRITING USER PREFERENCES TO FILE ***")

	path = "testData/scores"

	cursor = QueryRunner._createcursor()
	data = QueryRunner.getAllUsersPreferenceFull(cursor = cursor)

	if data is None:
		return False

	print(data)

	with open(path, 'w') as f:

		for row in data:

			user = str(row[0])
			item1 = str(row[1])
			item2 = str(row[2])
			score = str(row[3])

			clips = QueryRunner.getClipClipIdFromClips(clip1=item1, clip2=item2, cursor = cursor)
			if clips is None:
				continue

			strClip = str(clips)

			f.write(user + "\t" + str(strClip) + "\t" + score + "\n")


	print("*** WRITING DONE ***")
	print()

	return True



def WriteDeviations():
	print("*** WRITING DEVIATIONS TO FILE ***")
	outPath = "testData/deviations"
	writtenList = Reader.ReadScoreFileToList()

	if len(writtenList) is 0:
		return

	with open(outPath, "w") as w:
		for row in writtenList:
			print(row)

