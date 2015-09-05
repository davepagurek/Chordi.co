import midi

quarterNote = 96

chords = {
    "0": [midi.C_4, midi.E_4, midi.G_4],
    "1": [midi.C_4, midi.Ds_4, midi.G_4],
    # "2": [midi.D_4, midi.E_4, midi.A_5],
    "2": [midi.D_4, midi.F_4, midi.A_5],
    "3": [midi.D_4, midi.F_4, midi.A_5],
    "4": [midi.E_4, midi.G_4, midi.B_5],
    "5": [midi.E_4, midi.Gs_4, midi.B_5],
    "6": [midi.F_4, midi.Gs_4, midi.C_5],
    "7": [midi.F_4, midi.A_5, midi.C_5],
    # "8": [midi.G_4, midi.As_5, midi.D_5],
    "8": [midi.G_4, midi.B_5, midi.D_5],
    "9": [midi.G_4, midi.B_5, midi.D_5],
    "10": [midi.G_4, midi.B_5, midi.D_5, midi.F_5],
    "11": [midi.A_5, midi.C_5, midi.E_5],
    "12": [midi.A_5, midi.Cs_5, midi.E_5],
    "13": [midi.B_4, midi.D_4, midi.F_4]
}

chordInput = []
<<<<<<< HEAD
with open ("output.txt", "r") as data:
=======
with open ("training/life.mid.txt", "r") as data:
>>>>>>> 59c1173ddd5de4362ac0e66ffa22a6546c45bd29
    chordInput = data.read().replace("-1", "").replace("14", "").split(' ')

pattern = midi.Pattern(resolution=quarterNote)
track = midi.Track()
pattern.append(track)
midi.SetTempoEvent(tick=0, data=[7, 161, 32])

for index, chord in enumerate(chordInput):
    if index > 0 and chord == chordInput[index-1]:
        continue
    if chords.get(chord) != None:
        hold = 1
        while index+hold < len(chordInput) and chord == chordInput[index+hold]:
            hold = hold+1
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
                track.append(midi.NoteOffEvent(tick=quarterNote*hold-1, pitch=note))
                first = False
            else:
                track.append(midi.NoteOffEvent(tick=0, pitch=note))


track.append(midi.EndOfTrackEvent(tick=quarterNote))

drums = midi.Track()
pattern.append(drums)
drums.append(midi.TrackNameEvent(tick=0, text='Channel #10 10'))
for i in range(0, len(chordInput)):
    note = 42
    if i % 4 == 0:
        note = 36
    elif i % 4 == 2:
        note = 38
    drums.append(midi.NoteOnEvent(tick=1, channel=9, velocity=100, pitch=note))
    drums.append(midi.NoteOffEvent(tick=quarterNote-1, channel=9, pitch=note))
drums.append(midi.EndOfTrackEvent(tick=quarterNote, channel=9))


print pattern

midi.write_midifile("output.mid", pattern)

