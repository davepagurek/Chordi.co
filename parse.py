import midi

pattern = midi.read_midifile("Midi Thingies/twinkle.mid")
tempo = 120
song = []

notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#"]

def dataToBPM(data):
    print data
    timePerQuarter = ""
    for digit in data:
        timePerQuarter += hex(digit)[2:]
    return 60000000/int(timePerQuarter, 16)

for track in pattern:
    currentNotes = []
    for event in track:
        if type(event) is midi.SetTempoEvent:
            tempo = dataToBPM(event.data)
            print "TEMPO: ", tempo
        if type(event) is midi.NoteOnEvent:
            print ((event.data[0]-21)%12 - 3) % 12
