from v2.scripts import QueryRunner
import operator

def findAllTracksNotUsed():
	clipsUsed = {}
	instrumentUsed = {}
	cursor, connection = QueryRunner._createcursorandconnection()

	allTracks = QueryRunner.getAllTracks()
	for track in allTracks:
		trackId = track[0]
		instrument = track[1]

		if trackId not in clipsUsed.keys():
			clipsUsed[trackId] = 0

		if instrument not in instrumentUsed.keys():
			instrumentUsed[instrument] = 0

	allUsersPref = QueryRunner.getAllUsersPreferenceFull(cursor=cursor)

	for rating in allUsersPref:

		item1 = rating[1]
		item2 = rating[2]

		clipsUsed[item1] += 1

		item1Inst = QueryRunner.getInstrumentIDFromInstrumentKey(item1, cursor=cursor)
		instrumentUsed[item1Inst] += 1

		if item1 != item2:
			clipsUsed[item2] += 1

			item2Inst = QueryRunner.getInstrumentIDFromInstrumentKey(item2,cursor=cursor)
			instrumentUsed[item2Inst] += 1


	sorted_mostused = sorted(clipsUsed.items(), key=operator.itemgetter(1), reverse=True)
	print(sorted_mostused)

	print()

	sorted_inst = sorted(instrumentUsed.items(), key=operator.itemgetter(1), reverse=True)
	print(sorted_inst)




findAllTracksNotUsed()