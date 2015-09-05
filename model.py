import static

class SongModel:
	def __init__(self, songString, preChords = static.NUM_OF_INPUTS):

		# list that contains enumerated chords
		numbers = songString.split(' ')
		chords = [int(x) for x in numbers]
		if len(chords) < preChords + 1:
			print 'Not enough chords in song'

		i = 0
		self.model = list()
		finalChord = -1

		while True:
			finalChord = chords[i + preChords]
			dataPoint = tuple(x for x in chords[i : i + preChords])
			self.model.append([dataPoint, (finalChord,)])

			if (finalChord > 13):
				break

			i += 1