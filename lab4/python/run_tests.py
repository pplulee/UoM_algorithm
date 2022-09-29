import sys
import os

structure = sys.argv[1]

command =  'python3 tests_'+structure+'.py'

for i in range(21):
    command_input = command+' '+str(i)
    os.system(command_input)
    

