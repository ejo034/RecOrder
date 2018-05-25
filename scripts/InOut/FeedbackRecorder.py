from v2.scripts.InOut import Normalizer, FeedbackFileCreator
from v2.scripts import QueryRunner
from random import randint
import random

def GetFeedback(writer, isSong=False):

	if isSong:
		print("")
	else:
		#print("Listen to the clips and come back. I'll be waiting :) ")
		print("...")
		print("Rate the clip from 1 to 5")



	valid = False
	userChoice = 0

	while not valid:

		userChoice = input("> ")

		try:
			userChoice = int(userChoice)
		except:
			print("please write a number between 1 and 5")
			continue


		if int(userChoice) >= 1 and int(userChoice) <= 5:
			valid = True

		else:
			print("not a valid number. It must be between 1 and 5")


	print("you rated it : " + str(userChoice))
	writer.PrintAndWrite("User rated: " + str(userChoice))

	return userChoice





def GetNumOfRandomFromClipRelations(profileKey, clipclipRelation, writer, numRandom=3):
	writer.PrintAndWrite("", False)
	writer.PrintAndWrite("** CLIP CLIP RELATION FEEDBACK ** ", False)

	writer.PrintAndWrite("* getting ratings for {0} number of clips".format(numRandom))

	writer.PrintAndWrite("* getting not rated")
	notRatedList = QueryRunner.GetAllClipClipRelationsThatUserHasNotRated(
		userid=profileKey,
		relevantIdList=clipclipRelation,
		writer=writer
	)

	notRatedListLength = len(notRatedList)
	if notRatedListLength is 0:
		writer.PrintAndWrite("user has rated every item", False)
		writer.PrintAndWrite("Clip-clip realtion aborted", False)
		writer.PrintAndWrite()
		return False

	seenRelationsIndexes = []

	for index in range(0, numRandom):

		randomCCRelIndex = randint(0, notRatedListLength - 1)
		randomChoice = notRatedList[randomCCRelIndex]

		while randomChoice in seenRelationsIndexes:
			randomCCRelIndex = randint(0, notRatedListLength - 1)
			randomChoice = notRatedList[randomCCRelIndex]

		seenRelationsIndexes.append(randomChoice)

		success1 = FeedbackFileCreator.CreateCCRelationAudioFileForEvaluation(
			ccID=randomChoice,
			filename=randomChoice
		)

		if not success1:
			writer.PrintAndWrite("something went wrong with creating the audio file for evaluation", False)
			continue

		writer.PrintAndWrite("", False)
		writer.PrintAndWrite("Clip-clip id: " + str(randomChoice), False)

		writer.PrintAndWrite("Listen to the clips and come back. I'll be waiting :) ")

		feedback = GetFeedback(writer)
		normalizedFeedback = Normalizer.normalizeRating(feedback)

		success2 = QueryRunner.InsertUserPreferenceFromCCid(
			userId=profileKey,
			clipclipID=randomChoice,
			rating=normalizedFeedback
		)

		if success2 is False:
			print("something went wrong with inserting user preference")
			break

	writer.PrintAndWrite("Clip-clip Relation feedback is done",False)
	writer.PrintAndWrite("",False)



def GetFeedbackOnSong(profileKey, elementDict, writer):
	# should get feedback on the three tracks in context of the song
	writer.PrintAndWrite("** Feedback on song ** ",False)


	for i in range(0,3):

		currentInstruments = []

		for j in elementDict:
			current = elementDict[j].getElements()[i]
			currentInstruments.append(current)

		if int(i) == 0:
			writer.PrintAndWrite("Rate the GUITAR track from the generated song ", onlyWrite=False)
		elif i == 1:
			writer.PrintAndWrite("Rate the BASS track from the generated song ", False)
		elif i == 2:
			writer.PrintAndWrite("Rate the DRUM track from the generated song ", False)

		feedbackGuitar = GetFeedback(writer)
		normalizedRating = Normalizer.normalizeRating(feedbackGuitar)
		QueryRunner.InsertUserPreferenceFromSlice(profileKey, currentInstruments, normalizedRating)


def GetFeedbackForKNumberOfSlices(profileKey, elementDictionary, writer, numRandom=3):
	writer.PrintAndWrite("", False)
	writer.PrintAndWrite("** SLICE FEEDBACK ** ", False)

	ratedList = []

	elementDicKeyList = list(elementDictionary.keys())

	loop = 0

	if len(elementDicKeyList) < numRandom:
		loop = len(elementDicKeyList)
	else:
		loop = numRandom


	for i in range(0, loop):

		randomKey = random.choice(elementDicKeyList)

		while randomKey in ratedList:
			randomKey = random.choice(elementDicKeyList)

		ratedList.append(randomKey)

		sliceIdList = elementDictionary[randomKey].getElements()

		success = FeedbackFileCreator.CreateSliceAudioFileForEvaluation(sliceIdList)
		if success is False:
			writer.PrintAndWrite("something went wrong with creating the audio file for evaluation")
			continue

		writer.PrintAndWrite("")
		writer.PrintAndWrite("slice id: " + str(sliceIdList), False)
		writer.PrintAndWrite("Listen to the clips and come back. I'll be waiting :) ")

		feedback = GetFeedback(writer)
		normalizedRating = Normalizer.normalizeRating(feedback)

		QueryRunner.InsertUserPreferenceFromSlice(profileKey, sliceIdList, normalizedRating)

	writer.PrintAndWrite("Slice Feedback done", False)
	writer.PrintAndWrite("")

