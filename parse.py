import midi

class Song:
    notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

    def __init__(self, filename):
        self.song = []
        self.tempo = 120
        self.name = filename
        pattern = midi.read_midifile("Midi Thingies/twinkle.mid")

        for track in pattern:
            lastTick = -1
            currentTick = 0
            currentNotes = set()
            for event in track:
                if type(event) is midi.SetTempoEvent:
                    self.tempo = __dataToBPM(event.data)

                if type(event) is midi.NoteOnEvent:
                    set.add(__noteFromMidi(event.data[0]))
                    currentTick += event.tick

                if type(event) is midi.NoteOffEvent:
                    set.remove(__noteFromMidi(event.data[0]))
                    currentTick += event.tick

                if currentTick != lastTick:
                    self.song += {"from": lastTick+1, "to": currentTick, "notes": currentNotes.copy()}
                    lastTick = currentTick

    def __dataToBPM(data):
        print data
        timePerQuarter = ""
        for digit in data:
            timePerQuarter += hex(digit)[2:]
        return 60000000/int(timePerQuarter, 16)

    def __noteFromMidi(num):
        index = ((num-21)%12 - 3) % 12
        if 0 <= index < len(notes):
            return notes[index]
        else:
            return "undef: " + str(index)
    def save(self, songData):
        f = open(self.name,'w')
        dataString = ""
        for x in songData:
            dataString += x
        f.write(dataString)
        f.close()




twinkle = Song("Midi Thingies/twinkle.mid")
print twinkle.song

