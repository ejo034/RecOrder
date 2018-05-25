import os
import shutil


def moveOldAudioFiles(writer):
	writer.PrintAndWrite("")
	writer.PrintAndWrite("** ENTER PRIME MOVER! ** ", False)
	writer.PrintAndWrite("moving old files")

	path = "Audio/generated/"
	oldpath = "Audio/generated/old/"

	files = os.listdir(path)
	if len(files) is 1:
		return True


	for file in files:

		if file.endswith(".wav"):
			shutil.move(path+file, oldpath)


	writer.PrintAndWrite("moving done")
