import subprocess
def generateMP3(inputpath, outputpath, fontpath):
    subprocess.call(["fluidsynth", "-F","output.wav",fontpath, inputpath])
    subprocess.call(["lame", "output.wav", outputpath])
    subprocess.call(["rm","output.wav"])

if __name__ == "__main__":
    generateMP3("output.mid","output.mp3","GeneralUser GS MuseScore v1.442.sf2")
