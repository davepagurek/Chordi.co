import sys
import subprocess
def generateMP3(inputpath, outputpath, fontpath):
    command = "fluidsynth -F output.wav %s  %s && lame output.wav %s && rm output.wav" % (fontpath,inputpath,outputpath)
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    process.wait()
