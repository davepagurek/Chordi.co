import midi
import music21

class Song:
    majorMap = {
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
        "o11": 13,
        "0": 0,
        "1": 0,
        "2": 3,
        "3": 0,
        "4": 4,
        "5": 7,
        "6": 0,
        "7": 9,
        "8": 0,
        "9": 11,
        "10": 0,
        "11": 13
    }

    minorMap = {
        "M0": 0,
        "m0": 1,
        "o2": 2,
        "m2": 3,
        "m3": 4,
        "M3": 5,
        "m5": 6,
        "M5": 7,
        "m7": 8,
        "M7": 9,
        "M7^7": 10,
        "m8": 11,
        "M8": 12,
        "M10": 13,
        "0": 0,
        "1": 0,
        "2": 2,
        "3": 5,
        "4": 0,
        "5": 6,
        "6": 0,
        "7": 8,
        "8": 12,
        "9": 0,
        "10": 13,
        "11": 0
    }

    def __init__(self, filename):
        pattern = midi.read_midifile("midi/"+filename)
        score = music21.converter.parse("midi/"+filename)

        self.key = score.analyze('key')
        self.song = []
        self.tempo = 120
        self.quarterNote = pattern.resolution
        #print self.quarterNote
        self.name = filename
        counter = 0

        quality = self.key.mode
        interval = self.key.tonic.midi % 12

        previousNotes = set()

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
                            currentNotes.add(event.data[0]%12)
                            #print currentNotes

                        if type(event) is midi.NoteOffEvent:
                            noteEnds.add(event.data[0]%12)

                if len(currentNotes) > 0:
                    #print "start"
                    chord = music21.chord.Chord(currentNotes)
                    self.song.append({"from": quarterBegin, "to": quarterEnd, "chord": self.chordNumber(chord, quality, interval)})
                elif len(noteEnds) > 0 and len(currentNotes) == 0:
                    #print "end"
                    chord = music21.chord.Chord(noteEnds)
                    self.song.append({"from": quarterBegin, "to": quarterEnd, "chord": self.chordNumber(chord, quality, interval)})
                elif len(previousNotes) != 0:
                    #print "carry"
                    chord = music21.chord.Chord(previousNotes)
                    self.song.append({"from": quarterBegin, "to": quarterEnd, "chord": self.chordNumber(chord, quality, interval)})

                if len(currentNotes) != 0:
                    previousNotes = currentNotes
                    counter = 0
                else:
                    counter+=1

                if counter > 8:
                    previousNotes = set()
                    counter = 0

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

    def chordNumber(self, chord, quality, interval):
        #print chord.pitchedCommonName
        name = chord.commonName

        stream = music21.stream.Stream()
        stream.append(self.key)
        stream.append(chord)

        #print chord.findRoot().midi%12
        chordNumber = (chord.findRoot().midi - interval)%12
        chordName = ""
        if name == "major triad":
            chordName = "M" + str(chordNumber)
        elif name == "minor triad":
            chordName = "m" + str(chordNumber)
        elif name == "dominant seventh chord":
            chordName = "M" + str(chordNumber) + "^7"
        else:
            print "Couldn't find: ", name
            chordName = str(chordNumber)

        if quality == 'major':
            return Song.majorMap.get(chordName, 0)
        else:
            return Song.minorMap.get(chordName, 0)

    def setTempo(self, data):
        timePerQuarter = ""
        for digit in data:
            timePerQuarter += hex(digit)[2:]
        timePerQuarter = int(timePerQuarter, 16)
        self.tempo = int(round(60000000.00/timePerQuarter))

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

twinkle = Song("wat.mid")
print twinkle.key
print twinkle.dataString()

