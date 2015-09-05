import midi
import music21

class Song:
    chordMap = {
        "M1": 0,
        "m1": 1,
        "o2": 2,
        "m2": 3,
        "m3": 4,
        "M3": 5,
        "m4": 6,
        "M4": 7,
        "m5": 8,
        "M5": 9,
        "M5^7": 10,
        "m6": 11,
        "M6": 12,
        "o7": 13
    }

    def __init__(self, filename, key):
        pattern = midi.read_midifile("Midi Thingies/twinkle.mid")

        self.key = music21.key.Key("C")
        self.song = []
        self.tempo = 120
        self.quarterNote = pattern.resolution
        self.name = filename

        for track in pattern:
            lastTick = -1
            currentTick = 0
            currentNotes = set()
            for event in track:
                if type(event) is midi.SetTempoEvent:
                    self.setTempo(event.data)

                if type(event) is midi.NoteOffEvent:
                    currentTick += event.tick

                if currentTick - lastTick >= self.quarterNote and len(currentNotes) > 0:
                    chord = music21.chord.Chord(currentNotes)
                    self.song.append({"from": lastTick+1, "to": currentTick, "chord": self.chordNumber(chord)})
                    lastTick = currentTick

                if type(event) is midi.NoteOnEvent:
                    currentNotes.add(event.data[0])

                if type(event) is midi.NoteOffEvent:
                    if event.data[0] in currentNotes:
                        currentNotes.remove(event.data[0])

    def dataString(self):
        string = "-1"
        for chord in self.song:
            string += " " + str(chord.get("chord"))
        string += " 14"
        return string

    def chordNumber(self, chord):
        name = chord.commonName

        stream = music21.stream.Stream()
        stream.append(self.key)
        stream.append(chord)

        chordNumber = chord.scaleDegrees[0][0]
        chordName = ""
        if name == "major triad":
            chordName = "M" + str(chordNumber)
        elif name == "minor triad":
            chordName = "m" + str(chordNumber)
        elif name == "dominant seventh chord":
            chordName = "M" + str(chordNumber) + "^7"
        else:
            print "Couldn't find: ", name
            chordName = "M" + str(chordNumber)

        return Song.chordMap.get(chordName, 1)

    def setTempo(self, data):
        timePerQuarter = ""
        for digit in data:
            timePerQuarter += hex(digit)[2:]
        self.tempo = 60000000/self.quarterNote

    def noteFromMidi(self, num):
        index = ((num-21)%12 - 3) % 12
        if 0 <= index < len(Song.notes):
            return Song.notes[index]
        else:
            return "undef: " + str(index)
    def save(self, songData):
        f = open(self.name,'w')
        f.write(self.dataString())
        f.close()




twinkle = Song("Midi Thingies/thing2.mid", "C")
print twinkle.dataString()

