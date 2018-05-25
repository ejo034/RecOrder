from flask import render_template

from v2 import AppCreator
from v2.scripts.InOut import Writer
from v2.scripts.SongCreation import SongCreator

app = AppCreator.App().app

@app.route('/')
@app.route('/home')
def index():
	return render_template('index.html', title='Home')


@app.route('/createSong')
def createSong():
	bpm = 105
	key = "D"
	length = "short"
	profileKey = 18


	songcreator = SongCreator.SongCreator(
		bpm=bpm,
		key=key,
		length=length,
		profileKey=profileKey
	)

	songcreator.CreateSong()

	return index()


@app.route('/runOfflinePhase')
def runOfflinePhase():
	Writer.WriteScoresToFile()
	#Writer.WriteDeviations()
	return index()



if __name__ == '__main__':
	app.run(host = '0.0.0.0', debug = True)
