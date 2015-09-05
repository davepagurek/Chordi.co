import midi
import music21

class Song:
    notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

    def __init__(self, filename):
        pattern = midi.read_midifile("Midi Thingies/twinkle.mid")

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

                if type(event) is midi.NoteOnEvent or type(event) is midi.NoteOffEvent:
                    currentTick += event.tick

                if currentTick - lastTick >= self.quarterNote:
                    self.song.append({"from": lastTick+1, "to": currentTick, "notes": music21.chord.Chord(currentNotes).pitchedCommonName})
                    lastTick = currentTick

                if type(event) is midi.NoteOnEvent:
                    currentNotes.add(event.data[0])

                if type(event) is midi.NoteOffEvent:
                    if event.data[0] in currentNotes:
                        currentNotes.remove(event.data[0])

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
        dataString = ""
        for x in songData:
            dataString += " " + x
        f.write(dataString)
        f.close()
