import sys
import os
import glob

structure = sys.argv[1]
app = sys.argv[2]

if app == "concat":
    command =  'python3 apps/concat_finder_'+structure+'.py' + ' < ../data/' + app + '_data'
else:
    command = 'python3 apps/sorting_'+structure+'.py' + ' < ../data/' + app + '_data'
    
os.system(command)


