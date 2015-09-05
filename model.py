class SongModel:
	def __init__(self, songString, preChords = 5):

		# list that contains enumerated chords
		chords = songString.split(' ')
		if len(chords) < preChords + 1:
			print 'Not enough chords in song'

		i = 0
		self.model = list()

		while(finalChords <= 13):
			finalChord = chords[i + preChords]
			dataPoint = tuple(x for x in chord[i : i + preChords])

			self.model.append([dataPoint, (finalChord,)])
			i += 1

		self.printModel()

	def printModel(self):
		print self.model