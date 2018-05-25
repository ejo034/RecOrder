

def normalizeRating(rating, minR=1, maxR=5):
	print("Normalizing")
	maxMinusMin = maxR - minR
	twoTimesRatingMinusMin = (2*rating) - (2*minR)
	topPart = twoTimesRatingMinusMin - maxMinusMin
	solution = topPart / maxMinusMin
	return solution



def deNormalizeRating(normRating, minR=1, maxR=5):
	print("deNormalizing")
	maxMinusMin = maxR - minR
	normRatingPlussOne = (normRating + 1 )
	normRatingTimesMaxMin = normRatingPlussOne * maxMinusMin
	solution = 1/2 * normRatingTimesMaxMin
	solution = solution + 1
	return solution