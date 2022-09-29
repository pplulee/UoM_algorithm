#!/bin/bash

# This script can be used to use an existing dictionary to produce a pair of dictionary and query files that have certain properties
# The are 7 fixed required inputs in order are:
#   path to existing dictionary file
#   name of output dictionary file (will be overwritten)
#   name of output query file (will be overwritten)
#   length of desired output dictionary
#   length of desired number of queries
#   sorting option; one of 'sorted', 'reverse', or 'random'
#   the percentage of queries that should be in the dictionary
# For the last 4 options you can write '-' for the default value
#
# Note that his creates a temporary file that 'explodes' the dictionary to one word per line
#
# You may modify this file in any way that you wish to update the way in which it generates output files
#
# Hint: for a fully automated experiment you probably want to write another script that calls this script with multiple
#       inputs, executes the necessary tests, and records all the running times
#
# author: Giles, 2019

if [ $# -ne 7 ]
then
  echo "Call with dictionary input file, dictionary output file, query output file, dictionary length, query length, sorting option, query hit percent option"
  exit
fi

dict=$1
dict_out=$2
query_out=$3
dict_len=$4
query_len=$5
dict_sorting=$6
query_hit_percent=$7

exploded_dict="${dict}_exploded"

echo "Exploding dictionary to put one word on each line"
xargs -n 1 < $dict | sort -u > $exploded_dict

read actual_dict_len f <<< $(wc -l $exploded_dict)

echo "$actual_dict_len words in dictionary"

if [ $dict_len = "-" ]
then
  dict_len=$actual_dict_len
fi

if (( $dict_len > $actual_dict_len ))
then
  echo "We cannot create new words, dictionary length must be less than actual"
  exit
fi

if (( $query_hit_percent < 0 )) || (( $query_hit_percent > 100 )) 
then
  echo "query hit percent must be between 0 and 100" 
  exit
fi

query_hit=$(( $query_hit_percent * $query_len / 100 ))
query_miss=$(( $query_len - query_hit ))
echo "$query_hit query hits required"

if (( $query_hit < 100 )) && [ $dict_len -eq $actual_dict_len ]
then
  echo "to get a query hit percentage less than 100 we need some words not selected from the dictionary to use for the misses. Set required dictionary length to less than actual length."
  exit
fi

if [[ $dict_sorting = "sorted" ]]
then
  echo "Sorting dictionary"
  head -n $dict_len $exploded_dict | sort -d > $dict_out
elif [[ $dict_sorting = "reverse" ]]
then
  echo "Reverse sorting dictionary"
  head -n $dict_len $exploded_dict | sort -dr > $dict_out
elif [[ $dict_sorting = "random" ]]
then
  echo "Randomising dictionary"
  head -n $dict_len $exploded_dict |  awk 'BEGIN{srand()}{printf "%06d %s\n", rand()*1000000, $0;}' | sort -n | cut -c8- > $dict_out
else
  echo "No sorting performed"
  head -n $dict_len $exploded_dict > $dict_out
fi

rm -r $query_out

echo "Computing query hits"
while (( $query_hit > 0 ))
do
  take=$(( $query_hit > $dict_len ? $dict_len : $query_hit ))
  head -n $take $dict_out >> $query_out
  query_hit=$(( $query_hit - $take ))
done

echo "Computing query misses"
leftover=$(( $actual_dict_len - $dict_len ))
while (( $query_miss > 0 ))
do
  take=$(( $query_miss > $leftover ? $leftover : $query_miss ))
  tail -n $take $exploded_dict >> $query_out
  query_miss=$(( $query_miss - $take ))
done



