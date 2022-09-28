import sys
import os
import time
from subprocess import Popen, PIPE


# For exmaple, run using python3 ./test.py java simple hashset 1
# The problems are picked up from the data directory. You can edit this yourself,
# either adding extra problems to an existing set or adding a new set altogether.

if len(sys.argv) != 5:
  print("Run as test.py <language> <problems> <structure> <last_mod>")
  sys.exit(0)

language  = sys.argv[1]
problems  = sys.argv[2]
structure = sys.argv[3]
mode = int(sys.argv[4])

# Set up the commands to run the program, which are different for each language
commands = []

if language == "python":
  commands = ['python3','python/speller_'+structure+'.py']
elif language == "java":
  commands = ['java','-cp','java','comp26120.speller_'+structure]
elif language == 'c':
  commands = ['c/speller_'+structure]
else:
  print("Language "+language+" not recognised")
  sys.exit(0)


# Run the tests mode
print("Testing mode "+str(mode)+"...")
# Let's time all the tests
start = time.time()
for test in sorted(os.listdir('data/'+problems)) :
  testdir = 'data/'+problems+'/'+test
  if os.path.isdir(testdir): 
    with open(testdir+'/ans') as ans:
      ans_lines = ans.read().splitlines()

      print("Testing "+test)
      process = Popen(commands+['-d',testdir+'/dict','-m',str(mode),testdir+'/infile'], stdout=PIPE, stderr=PIPE)
      looking = False
      for line in process.stdout.readlines():
        line = line.strip().decode("utf-8").strip('\x00')
        #Skip blank lines in the output
        if len(line) == 0 : 
           continue
        # We depend on particular bits of the output occuring either side of the spelling errors
        if "Spellchecking:" in line:
          looking = True
        elif "Usage statistics:" in line:
          looking = False
        elif looking:
          if len(ans_lines) == 0:
            print("Test failed. Reported "+line+" when no more spelling errors expected")
          elif ans_lines[0] != line:
            print("Test failed. Expected "+ans_lines[0]+" but got "+line)
          else:
            ans_lines = ans_lines[1:]
         
      if len(ans_lines) > 0:
         print("Test failed. Expected more spelling errors") 
         print("First missing line: "+ans_lines[0])
end = time.time()
print("Took "+str(end-start)+" seconds")
