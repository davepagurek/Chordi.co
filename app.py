from flask import Flask, render_template, send_from_directory
from os import listdir

from learn import Learn
from tomidi import toMidi
from midi2mp3 import generateMP3

import random
import json

MIDI_BASE_PATH = 'songs/output'
FONT_PATH = "GeneralUser GS MuseScore v1.442.sf2"
MP3_BASE_PATH = 'songs/output'
app = Flask(__name__)
@app.route('/')
def server():
	return render_template("index.html")

@app.route('/music/<int:instrument>/<string:mode>')
def music_function(instrument, mode):
    learner = Learn(mode)
    learner.loadFromFile()
    song = learner.getSong(getStartSequence())
    midiPath = getPath(MIDI_BASE_PATH, '.mid')
    toMidi(song, midiPath, instrument)
    mp3Path = getPath(MP3_BASE_PATH, '.mp3')
    generateMP3(midiPath, mp3Path, FONT_PATH)
    return mp3Path

@app.route('/train/<string:mode>')
def train_function(mode):
    learner = Learn(mode)
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

@app.route('/font-awesome/<path:path>')
def send_fonts(path):
    return send_from_directory('font-awesome',path)

def getStartSequence():
    niceChords = [0, 0, 0, 1, 4, 5, 7, 9, 10, 11]
    start = []
    for i in range(0, 4):
        start.append(random.choice(niceChords))
    print start
    return start

def getPath(basePath, ext):
    files = listdir('songs')
    files = [('songs/' + x) for x in files]
    i = 0
    while True:
        songName = basePath + str(i) + ext
        if not songName in files:
            return songName
        i += 1

if __name__ == "__main__":
    app.run(debug = True, threaded=True)
