
def prettyDictPrint(dictInn):
	if type(dictInn) is not dict:
		return None

	for (key, item) in dictInn.items():
		temp = str(key)
		if type(item) is dict:
			temp += (" : " + str(list(item.items())))
		else:
			temp += (" : " + str(item))

		print(temp)