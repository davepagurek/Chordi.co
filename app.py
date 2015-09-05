from flask import Flask, render_template, send_from_directory

from learn import Learn
from tomidi import toMidi
from midi2mp3 import generateMP3

import json

MIDI_TEMP_PATH = 'songs/output.mid'
MP3_TEMP_PATH = 'songs/output.mp3'
FONT_PATH = 'Gort\'s-DoubleDecker_J1.SF2'
BASE_URL = 'http://127.0.0.1:5000/'
app = Flask(__name__)
@app.route('/')
def server():
	return render_template("index.html")

@app.route('/music')
def music_function():
    learner = Learn()
    learner.loadFromFile()
    song = learner.getSong(getStartSequence())
    toMidi(song, MIDI_TEMP_PATH)
    generateMP3(MIDI_TEMP_PATH, MP3_TEMP_PATH, FONT_PATH)
    return BASE_URL + MP3_TEMP_PATH

@app.route('/train')
def train_function():
    learner = Learn()
    learner.train()
    learner.saveToFile()
    return server()

def getStartSequence():
    return [0, 7, 9, 0]

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

if __name__ == "__main__":
    app.run(debug = True)
