import sys
import os
import glob

app = sys.argv[1]
if app=="concat":
    filename_start = 'apps/concat_finder_'
else:
    filename_start = 'apps/sorting_'
    
filenames_list = glob.glob(filename_start+'*.py')

for filename in filenames_list:
    print(filename)
    command = 'time python3 ' + filename + ' < ../data/' + app + '_data > /dev/null'
    os.system(command)


