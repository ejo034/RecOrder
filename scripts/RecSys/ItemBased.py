from v2.scripts.RecSys import RecSysEngine
from v2.scripts import QueryRunner
from random import randint


class ItemBased(RecSysEngine.RecSysEngine):

	def __init__(self, writer):
		super().__init__()

		# used for slope one
		self.frequencies = {}
		self.deviations = {}
		self.data = {}
		self.instrumentType = 0
		self.writer = writer


	def GetRecommendation(self, profileId=None, key=None, bpm=None, instrumentID=None, section=None):
		if instrumentID is not self.instrumentType:
			self.deviations = {}
			self.frequencies = {}
			self.data = {}

		success = self._getData(key=key, bpm=bpm, instrumentKey=instrumentID)
		if success is False:
			return None

		#if this returns not false it is empty
		if profileId not in self.data.keys():
			print("no user id")
			return None

		if not self.data[profileId]:
			print("empty")
			return None

		result = self.weightedSlopeOne(profileId)

		if result is None or len(result) is 0:
			return None

		#once we have the recommendations, get a random one from them.
		# This way we get some surprising elements
		length = len(result) - 1
		randomIndex = randint(0, length)

		randomItem = result[randomIndex][0]

		self.writer.PrintAndWrite("** selected result", False)
		self.writer.PrintAndWrite(randomItem)

		return randomItem


	def weightedSlopeOne(self, profileId):
		self.writer.PrintAndWrite("** running weighted slope one recommendation")

		self.__computeDeviations()
		#PrinterUtil.prettyDictPrint(self.deviations)

		userData = self.data[profileId]
		self.writer.PrintAndWrite("** user data")
		self.writer.PrintAndWrite(userData)

		recommendation = self.__slopeOneRecommendation(userData)
		self.writer.PrintAndWrite("** recommendations")
		self.writer.PrintAndWrite(recommendation)

		return recommendation


	def __computeDeviations(self):
		#if the dictionary is not empty
		if bool(self.deviations):
			return False

		self.writer.PrintAndWrite("** deviations")

		#for each persons ratings in the relevant data-set, get their ratings
		for ratings in self.data.values():

			# for each item and rating in those ratings
			for (item, rating) in ratings.items():

				# create freq and dev items in their dictionaries
				self.frequencies.setdefault(item, {})
				self.deviations.setdefault(item, {})

				#for each other item and rating, but not the current one
				for (item2, rating2) in ratings.items():
					if item != item2:

						# find the difference / deviation between the two ratings
						# add the difference to dev and freuency to dicts
						self.frequencies[item].setdefault(item2, 0)
						self.deviations[item].setdefault(item2, 0.0)

						self.frequencies[item][item2] += 1
						self.deviations[item][item2] += rating - rating2

		#then, divide each of the deviations by the frequency of the item-item pair
		for (item, ratings) in self.deviations.items():
			for item2 in ratings:
				ratings[item2] /= self.frequencies[item][item2]


	def __slopeOneRecommendation(self, userRatings):
		self.writer.PrintAndWrite("*** calculating slope one recommendation")

		recommendation = {}
		frequency = {}

		userRatingKeys = list(userRatings.keys())

		# For every item (and rating) the user has rated
		for (userItem, userRating) in userRatings.items():

			# For every item (and rating) in the deviations
			for (diffItem, diffRating) in self.deviations.items():

				deviationKeys = list(self.deviations[diffItem].keys())

				# if the user has not rated diffitem
				# and the item exist in the deviations
				if (diffItem not in userRatingKeys) and (userItem in deviationKeys):

					#temporary save the frequency of diffitem and useritem
					freq = self.frequencies[diffItem][userItem]

					recommendation.setdefault(diffItem, 0.0)
					frequency.setdefault(diffItem, 0)

					# add the sum of the deviation of the user
					recommendation[diffItem] += (diffRating[userItem] + userRating) * freq
					frequency[diffItem] += freq

		#divide on frequency
		recommendation = [(k, v / frequency[k]) for (k, v) in recommendation.items()]

		#sort
		recommendation.sort(key=lambda itemtuple : itemtuple[1], reverse=True)

		return recommendation


	def _getData(self, key, bpm, instrumentKey):
		self.writer.PrintAndWrite("** getting data")

		# gets all the songs with the correct bpm, key and instrument
		clipList = QueryRunner.getSongsWithBPMKeyAndInstrumentId(bpm, key, instrumentKey)
		if len(clipList) is 0:
			return False

		idClipList = []

		for item in clipList:
			idClipList.append(item[0])

		# need to have the preference for all users
		preferences = {}
		allPreferences = QueryRunner.getAllUsersPreferenceFull()
		if allPreferences is None:
			return False

		for pref in allPreferences:
			resultDict = {}
			user = pref[0]
			item1 = pref[1]
			item2 = pref[2]
			rating = pref[3]

			if item1 in idClipList:
				if item1 not in resultDict:
					resultDict[item1] = rating
				else:
					resultDict[item1] += rating

			if item2 in idClipList:
				if item2 not in resultDict:
					resultDict[item2] = rating
				else:
					resultDict[item2] += rating

			if user not in preferences:
				# if the user is not known, just add the generated dictionary
				preferences[user] = resultDict

			else:
				# if the user is known, update the existing dictionary with new data
				existingDict = preferences[user]
				for (subkey, subitem) in resultDict.items():
					existingDict[subkey] = subitem
				preferences[user] = existingDict

		self.data = preferences
