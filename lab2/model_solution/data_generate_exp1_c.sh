STATES="sorted reverse none"
SIZES="10000 20000 30000 40000 50000"

rm data/sorted_data_c.dat
rm data/reverse_data_c.dat
rm data/none_data_c.dat
rm data/sorted_data_c.csv
rm data/reverse_data_c.csv
rm data/none_data_c.csv

for STATE in $STATES
do

for SIZE in $SIZES
do

for COUNT in 1 2 3 4 5
do

    # Debugging statement to check program calls working as expected
    ../../search_and_sort_lab/c/speller_darray -d ../dictionaries_and_queries/dict_${SIZE}_${STATE}_$COUNT -m 1 -s ${SIZE} ../dictionaries_and_queries/query_${SIZE}_${STATE}_$COUNT

    ALL_TIME=`(time -p  ../../search_and_sort_lab/c/speller_darray -d ../dictionaries_and_queries/dict_${SIZE}_${STATE}_$COUNT -m 1 -s ${SIZE} ../dictionaries_and_queries/query_${SIZE}_${STATE}_$COUNT) 2>&1 | grep -E "user|sys" | sed s/[a-z]//g`
    
    RUNTIME=0
    for i in $ALL_TIME;
    do RUNTIME=`echo $RUNTIME + $i|bc`;
    done
    echo $SIZE $RUNTIME >> data/${STATE}_data_c.dat
    echo $SIZE, $RUNTIME >> data/${STATE}_data_c.csv
    
done

done

done
