import midi
import random

def toMidi(songString, outfile, instrument=27, tempo=0):

    quarterNote = 96

    if tempo == 0:
        tempo = random.choice(range(100, 200))
        print tempo

    chords = {
        0: [midi.C_4, midi.E_4, midi.G_4],
        1: [midi.C_4, midi.Ds_4, midi.G_4],
        # 2: [midi.D_4, midi.E_4, midi.A_5],
        2: [midi.D_4, midi.F_4, midi.A_5],
        3: [midi.D_4, midi.F_4, midi.A_5],
        4: [midi.E_4, midi.G_4, midi.B_5],
        5: [midi.E_4, midi.Gs_4, midi.B_5],
        6: [midi.F_4, midi.Gs_4, midi.C_5],
        7: [midi.F_4, midi.A_5, midi.C_5],
        # "8": [midi.G_4, midi.As_5, midi.D_5],
        8: [midi.G_4, midi.B_5, midi.D_5],
        9: [midi.G_4, midi.B_5, midi.D_5],
        10: [midi.G_4, midi.B_5, midi.D_5, midi.F_5],
        11: [midi.A_5, midi.C_5, midi.E_5],
        12: [midi.A_5, midi.Cs_5, midi.E_5],
        13: [midi.B_4, midi.D_4, midi.F_4]
    }

    chordInput = []
    chordInput = [c for c in songString if 0 <= c <= 13]

    pattern = midi.Pattern(resolution=quarterNote)
    track = midi.Track()
    track.append(midi.ProgramChangeEvent(tick=0, data=[instrument]))
    pattern.append(track)

    tempoString = hex(60000000/tempo).replace("0x", "")
    if len(tempoString) < 6:
        tempoString = "0" + tempoString
    tempoData = map(lambda x: int(x, 16), [tempoString[i:i+2] for i in range(0, len(tempoString), 2)])
    print tempoData
    track.append(midi.SetTempoEvent(tick=0, data=tempoData))

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
    style = 0
    for i in range(0, len(chordInput)):
        if i % 4 == 0:
            if i % 32 == 0:
                drums.append(midi.NoteOnEvent(tick=1, channel=9, velocity=100, pitch=49))
                drums.append(midi.NoteOffEvent(tick=quarterNote-1, channel=9, pitch=49))
            else:
                drums.append(midi.NoteOnEvent(tick=1, channel=9, velocity=100, pitch=36))
                drums.append(midi.NoteOffEvent(tick=quarterNote-1, channel=9, pitch=36))
        elif i % 4 == 2:
            if i % 16 == 14:
                style = 1
            else:
                style = 0
            if style == 1:
                drums.append(midi.NoteOnEvent(tick=1, channel=9, velocity=100, pitch=38))
                drums.append(midi.NoteOffEvent(tick=quarterNote/4-1, channel=9, pitch=38))
                drums.append(midi.NoteOnEvent(tick=1, channel=9, velocity=75, pitch=38))
                drums.append(midi.NoteOffEvent(tick=quarterNote/4-1, channel=9, pitch=38))
                drums.append(midi.NoteOnEvent(tick=1, channel=9, velocity=50, pitch=38))
                drums.append(midi.NoteOffEvent(tick=quarterNote/4-1, channel=9, pitch=38))
                drums.append(midi.NoteOnEvent(tick=1, channel=9, velocity=75, pitch=38))
                drums.append(midi.NoteOffEvent(tick=quarterNote/4-1, channel=9, pitch=38))
            else:
                drums.append(midi.NoteOnEvent(tick=1, channel=9, velocity=80, pitch=38))
                drums.append(midi.NoteOffEvent(tick=quarterNote-1, channel=9, pitch=38))
        elif i % 4 == 3:
            if style == 1:
                drums.append(midi.NoteOnEvent(tick=1, channel=9, velocity=100, pitch=38))
                drums.append(midi.NoteOffEvent(tick=quarterNote/2-1, channel=9, pitch=38))
                drums.append(midi.NoteOnEvent(tick=1, channel=9, velocity=100, pitch=38))
                drums.append(midi.NoteOffEvent(tick=quarterNote/2-1, channel=9, pitch=38))
            else:
                drums.append(midi.NoteOnEvent(tick=1, channel=9, velocity=50, pitch=42))
                drums.append(midi.NoteOffEvent(tick=quarterNote/2-1, channel=9, pitch=42))
                drums.append(midi.NoteOnEvent(tick=1, channel=9, velocity=35, pitch=42))
                drums.append(midi.NoteOffEvent(tick=quarterNote/2-1, channel=9, pitch=42))
        else:
            drums.append(midi.NoteOnEvent(tick=1, channel=9, velocity=75, pitch=42))
            drums.append(midi.NoteOffEvent(tick=quarterNote/2-1, channel=9, pitch=42))
            drums.append(midi.NoteOnEvent(tick=1, channel=9, velocity=55, pitch=42))
            drums.append(midi.NoteOffEvent(tick=quarterNote/2-1, channel=9, pitch=42))

    drums.append(midi.EndOfTrackEvent(tick=quarterNote, channel=9))


    midi.write_midifile(outfile, pattern)

if __name__ == "__main__":
    toMidi([-1, 1, 11, 7, 14], "output.mid")
