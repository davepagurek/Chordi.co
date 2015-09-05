import subprocess
def generateMP3(inputpath, outputpath, fontpath):
    subprocess.call(["fluidsynth", "-F","output.wav",fontpath, inputpath])
    subprocess.call(["lame", "output.wav", outputpath])
    #subprocess.call(["rm","output.wav"])
generateMP3("output.mid","output.mp3","~/Downloads/Gorts_DoubleDecker3/Gort\'s-DoubleDecker_J1.SF2")
