import subprocess
import pdb
def generateMP3(inputpath, outputpath, fontpath):
    subprocess.call(["fluidsynth", "-F","output.wav",fontpath, inputpath])
    pdb.set_trace()
    subprocess.call(["lame", "output.wav", outputpath])
    subprocess.call(["rm","output.wav"])
generateMP3("output.mid","output.mp3","Gort\'s-DoubleDecker_J1.SF2")
