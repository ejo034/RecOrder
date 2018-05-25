scoresPath = "testData/scores"



def ReadScoreFileToList():
	writtenList = []

	with open(scoresPath, "r") as r:
		for line in r.readlines():
			cleanLine = line.strip()
			split = cleanLine.split("\t")

			if len(split) != 3:
				break

			writtenList.append(split)

	return writtenList