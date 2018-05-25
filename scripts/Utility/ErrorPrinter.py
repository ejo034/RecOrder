

def databaseConnectionError():
	print("Something went wrong when connecting to the database")
	print("Check if the Database is running")


def fileOrDirectoryNotFoundError(directory):
	print("!_! File or directory: \"" + str(directory) + "\" not found ")


def invalidDBCallInput(tableName):
	print("!_! Call to " + tableName + " stopped due to invalid input")



def databaseReturnedNothing(tableName):
	print("!_! Call to " + tableName + " returned nothing")


