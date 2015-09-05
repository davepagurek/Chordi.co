import midi

quarterNote = 96

chords = {
    "0": [midi.C_4, midi.E_4, midi.G_4],
    "1": [midi.C_4, midi.Ds_4, midi.G_4],
    "2": [midi.D_4, midi.E_4, midi.A_5],
    "3": [midi.D_4, midi.F_4, midi.A_5],
    "4": [midi.E_4, midi.Fs_4, midi.B_5],
    "5": [midi.E_4, midi.G_4, midi.B_5],
    "6": [midi.F_4, midi.Gs_4, midi.C_5],
    "7": [midi.F_4, midi.A_5, midi.C_5],
    "8": [midi.G_4, midi.As_5, midi.D_5],
    "9": [midi.G_4, midi.B_5, midi.D_5],
    "10": [midi.G_4, midi.B_5, midi.D_5, midi.F_5],
    "11": [midi.A_5, midi.C_5, midi.E_5],
    "12": [midi.A_5, midi.Cs_5, midi.E_5],
    "13": [midi.B_4, midi.D_4, midi.F_4]
}

chordInput = []
with open ("output.txt", "r") as data:
    chordInput = data.read().replace("-1", "").replace("14", "").split(' ')

pattern = midi.Pattern(resolution=quarterNote)
track = midi.Track()
pattern.append(track)
midi.SetTempoEvent(tick=0, data=[7, 161, 32])

for index, chord in enumerate(chordInput):
    if chords.get(chord) != None:
        first = True
        for note in chords.get(chord):
            if first:
                track.append(midi.NoteOnEvent(tick=1, velocity=100, pitch=note))
                first = False
            else:
                track.append(midi.NoteOnEvent(tick=0, velocity=100, pitch=note))
        first = True
        for note in chords.get(chord):
            if first:
                track.append(midi.NoteOffEvent(tick=quarterNote-1, pitch=note))
                first = False
            else:
                track.append(midi.NoteOffEvent(tick=0, pitch=note))


print pattern

track.append(midi.EndOfTrackEvent(tick=quarterNote*len(chordInput)))
midi.write_midifile("output.mid", pattern)

