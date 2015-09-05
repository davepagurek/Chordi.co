import midi
import music21

class Song:
    chordMap = {
        "M0": 0,
        "m0": 1,
        "o2": 2,
        "m2": 3,
        "m4": 4,
        "M4": 5,
        "m5": 6,
        "M5": 7,
        "m7": 8,
        "M7": 9,
        "M7^7": 10,
        "m9": 11,
        "M9": 12,
        "o11": 13

        # "M1": 0,
        # "m1": 1,
        # "o2": 2,
        # "m2": 3,
        # "m3": 4,
        # "M3": 5,
        # "m4": 6,
        # "M4": 7,
        # "m5": 8,
        # "M5": 9,
        # "M5^7": 10,
        # "m6": 11,
        # "M6": 12,
        # "o7": 13
    }

    def __init__(self, filename, key):
        pattern = midi.read_midifile("midi/"+filename)

        self.key = music21.key.Key(key)
        self.song = []
        self.tempo = 120
        self.quarterNote = pattern.resolution
        self.name = filename

        #print self.quarterNote

        for track in pattern:
            quarterBegin = 0
            quarterEnd = self.quarterNote - 1
            endTick = 0

            for event in track:
                    endTick += event.tick
                    if type(event) is midi.SetTempoEvent:
                        self.setTempo(event.data)
                    if type(event) is midi.EndOfTrackEvent:
                        break

            currentTick = 0

            while quarterBegin <= endTick:
                currentTick = 0
                currentNotes = set()
                noteEnds = set()
                for event in track:
                    currentTick += event.tick
                    if currentTick > quarterEnd:
                            break

                    if currentTick >= quarterBegin and currentTick <= quarterEnd:
                        if type(event) is midi.NoteOnEvent:
                            currentNotes.add(event.data[0])
                            #print currentNotes

                        if type(event) is midi.NoteOffEvent:
                            noteEnds.add(event.data[0])

                if len(currentNotes) > 0:
                    chord = music21.chord.Chord(currentNotes)
                    self.song.append({"from": quarterBegin, "to": quarterEnd, "chord": self.chordNumber(chord)})
                elif len(noteEnds) > 0:
                    chord = music21.chord.Chord(noteEnds)
                    self.song.append({"from": quarterBegin, "to": quarterEnd, "chord": self.chordNumber(chord)})

                quarterBegin += self.quarterNote
                quarterEnd = quarterBegin + self.quarterNote - 1


                    #if type(event) is midi.NoteOnEvent:
                        #currentNotes.add(event.data[0])

                    #if type(event) is midi.NoteOffEvent:
                        #if event.data[0] in currentNotes:
                            #currentNotes.remove(event.data[0])

    def dataString(self):
        string = "-1"
        for chord in self.song:
            string += " " + str(chord.get("chord"))
        string += " 14"
        return string

    def chordNumber(self, chord):
        #print chord.pitchedCommonName
        name = chord.commonName

        stream = music21.stream.Stream()
        stream.append(self.key)
        stream.append(chord)

        print chord.findRoot().midi%12
        chordNumber = (chord.findRoot().midi + 3)%12
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

        return Song.chordMap.get(chordName, 0)

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
    def save(self):
        f = open("training/"+self.name+".txt",'w')
        f.write(self.dataString())
        f.close()

twinkle = Song("thing4.mid", "A")
print twinkle.dataString()

