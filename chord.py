from music21 import *

c = chord.Chord([58, 66, 61])
print c.pitchedCommonName

c.sortDiatonicAscending()

print c.pitches
print c.pitchedCommonName