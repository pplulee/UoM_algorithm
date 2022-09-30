# This script is designed to help you test the Knapsack lab automatically
#
# It is meant to run in the top directory that has c, java, python, and data as subdirectories
#
# Run as (for exmaple)
#
# bash test.sh java
#
# This script requires bash 4.0 so if you're on a Mac then you'll need to upgrade your version of
# bash e.g. using macports or homebrew
# 
# You can edit the script to change the time limit to use on each input problem.
# Just edit the times array below
#
# IF YOU ARE USING PYTHON then you will definitely need to increase the time limits
#
# You may want to edit the algs and inputs arrays to run a subset of the experiments.
#
# If your code is failing the tests then check that QUIET is not 1 in your code e.g. that it is
# printing things out. This script greps the output.
#
# For branch-and-bound you want the script to capture the best solution found 'so far'. To do this 
# you shoould print using printf("Current best solution=%d\n", current_best) or similar as the script
# is matching against output of this form
#
# You will get one of four outputs from the correctnes checks:
# Yes means it was correct 
# No means it was incorrect
# ?  means that we are not expecting an optimal solution so cannot check that we've got one.
# - means that it timed out. Sometimes this is the expected behaviouor.
#
# When might you get ?
# Branch and bound will only give a `best-effort' on the hard problems within any realistic time limit. 
# Part of the exercise involves explaining why the greedy approach always has a ‘?‘
#
# Author: Giles Reger

function timeout() { perl -e 'alarm shift; exec @ARGV' "$@"; }

function for_c { 
  echo "c/$1" 
}
function for_java { 
  echo "java -cp java comp26120.$1_kp"
}
function for_python { 
  echo "python3 python/$1_kp.py" 
}
function get {
  if [[ $1 == "c" ]]; then for_c $2; fi
  if [[ $1 == "java" ]]; then for_java $2; fi
  if [[ $1 == "python" ]]; then for_python $2; fi
}


lang="c"
if [ $# -eq 1 ]
then
  lang=$1
fi
if [[ "$lang" != "c"  &&  "$lang" != "java"  &&  "$lang" != "python" ]]
then
  echo "Supply either c, java, or python as the language"
  exit
fi

algs=( enum bnb dp greedy )
inputs=( 'easy.20.txt' 'easy.200.txt' 'hard.200.txt' 'hard.2000.txt' ) 
declare -A times=( 
  ['easy.20.txt']=5
  ['easy.200.txt']=5
  ['hard.200.txt']=60
  ['hard.2000.txt']=60
)
declare -A solutions=(
  ['easy.20.txt enum']=377
  ['easy.20.txt bnb']=377
  ['easy.20.txt dp']=377
  ['easy.200.txt bnb']=4077
  ['easy.200.txt dp']=4077
  ['hard.200.txt dp']=126968
  ['hard.2000.txt dp']=1205259
)


for FILE in ${inputs[@]}
do
  LIMIT="${times[$FILE]}"
#  echo "==========================================="
#  echo "Running on $FILE for $LIMIT seconds"
#  echo "==========================================="
#  echo
#  echo "Algorithm |      Optimal Value       | Time Taken  | Result"
  #  echo "----------------------------------------------------------------"
  echo "Running on $FILE for $LIMIT seconds"
  echo
  echo "\begin{tabular}{|l|l|l|l|} \hline"
  echo "Algorithm & Optimal Value & Time Taken & Result \\\\ \hline"
  for alg in ${algs[@]}
  do
    RUN=$(get $lang $alg)
    TIME=$({ time timeout ${LIMIT}s ${RUN} data/$FILE > ${alg}_${FILE}_out ; } 2>&1 | grep real | grep -o '[0-9].*')
    LAST=$(grep -o '\(Current best solution\|value\)=[0-9]*' ${alg}_${FILE}_out | tail -1) 
    VALUE=$(echo $LAST | sed -n -e 's/.*=//g' -e 'p')
    CORRECT="?"
    if [ -z $VALUE ]
    then
      VALUE="-"
      CORRECT="-"
    fi
    if [[ "$LAST" == *Current* ]] 
    then
      VALUE="$VALUE (after ${LIMIT}s)"
    fi
    key="$FILE $alg"
    if [ ${solutions[$key]+abc} ]
    then
      ANSWER=${solutions[$key]}
      if [ $ANSWER == $VALUE ]
      then
        CORRECT="Yes"
      else
        CORRECT="No"
      fi
    fi
    printf -v alg %-10.10s $alg 
    printf -v VALUE %-25.25s "$VALUE"
    #    echo "$alg| $VALUE| ${TIME}    | $CORRECT"
    echo "$alg & $VALUE & ${TIME} & $CORRECT  \\\\"
  done
  echo "\hline \end{tabular}"
  echo
  echo
done

