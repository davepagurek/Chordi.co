from flask import Flask, render_template, send_from_directory
from os import listdir

from learn import Learn
from tomidi import toMidi
from midi2mp3 import generateMP3

MIDI_TEMP_PATH = 'songs/output.mid'
FONT_PATH = "GeneralUser GS MuseScore v1.442.sf2"
MP3_BASE_PATH = 'songs/output'
BASE_URL = 'http://127.0.0.1:5000/'
app = Flask(__name__)
@app.route('/')
def server():
	return render_template("index.html")

@app.route('/music/<int:param>')
def music_function(param):
    learner = Learn()
    learner.loadFromFile()
    song = learner.getSong(getStartSequence())
    toMidi(song, MIDI_TEMP_PATH, param)
    mp3Path = getMP3Path()
    generateMP3(MIDI_TEMP_PATH, mp3Path, FONT_PATH)
    return BASE_URL + mp3Path

@app.route('/train')
def train_function():
    learner = Learn()
    learner.train()
    learner.saveToFile()
    return server()

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)

@app.route('/images/<path:path>')
def send_images(path):
    return send_from_directory('images', path)

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)

@app.route('/songs/<path:path>')
def send_songs(path):
    return send_from_directory('songs', path)

def getStartSequence():
    return [0, 7, 9, 0]

def getMP3Path():
    files = listdir('songs')
    files = [('songs/' + x) for x in files]
    i = 0
    while True:
        songName = MP3_BASE_PATH + str(i) + '.mp3'
        if not songName in files:
            return songName
        i += 1

if __name__ == "__main__":
    app.run(debug = True)
