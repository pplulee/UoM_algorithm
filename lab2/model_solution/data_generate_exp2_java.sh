SIZES="10000 20000 30000 40000 50000"
QUERY_SIZES="0.1 0.5 1 5 10"


for SIZE in $SIZES
do

rm data/${SIZE}_amortised_data_linear_java.dat
rm data/${SIZE}_amortised_data_binary_java.dat
rm data/${SIZE}_amortised_data_linear_java.csv
rm data/${SIZE}_amortised_data_binary_java.csv

for QSIZE in $QUERY_SIZES
do

QUERY_SIZE=$( echo "$SIZE * $QSIZE/1" | bc)


for COUNT in 1 2 3 4 5
do

    # Debugging command to check program call actually works
    java -cp ../../search_and_sort_lab/java comp26120.speller_darray -d ../dictionaries_and_queries/dict_${SIZE}_${QUERY_SIZE}_$COUNT -m 0 -s ${SIZE} ../dictionaries_and_queries/query_${SIZE}_${QUERY_SIZE}_$COUNT

    ALL_TIME=`(time -p java -cp ../../search_and_sort_lab/java comp26120.speller_darray -d ../dictionaries_and_queries/dict_${SIZE}_${QUERY_SIZE}_$COUNT -m 0 -s ${SIZE} ../dictionaries_and_queries/query_${SIZE}_${QUERY_SIZE}_$COUNT) 2>&1 | grep -E "user |sys " | sed s/[a-z]//g`
    
    RUNTIME=0
    for i in $ALL_TIME;
    do RUNTIME=`echo $RUNTIME + $i|bc`;
    done
    
    echo $QSIZE $RUNTIME >> data/${SIZE}_amortised_data_linear_java.dat
    echo $QSIZE, $RUNTIME >> data/${SIZE}_amortised_data_linear_java.csv
    
    # Debugging command to check program call actually works
    java -cp ../../search_and_sort_lab/java comp26120.speller_darray -d ../dictionaries_and_queries/dict_${SIZE}_${QUERY_SIZE}_$COUNT -m 1 -s ${SIZE} ../dictionaries_and_queries/query_${SIZE}_${QUERY_SIZE}_$COUNT

    ALL_TIME2=`(time -p java -cp ../../search_and_sort_lab/java comp26120.speller_darray -d ../dictionaries_and_queries/dict_${SIZE}_${QUERY_SIZE}_$COUNT -m 1 -s ${SIZE} ../dictionaries_and_queries/query_${SIZE}_${QUERY_SIZE}_$COUNT) 2>&1 | grep -E "user |sys " | sed s/[a-z]//g`
    
    
    RUNTIME2=0
    for i in $ALL_TIME2;
    do RUNTIME2=`echo $RUNTIME2 + $i|bc`;
    done
    
    echo $QSIZE $RUNTIME2 >> data/${SIZE}_amortised_data_binary_java.dat
    echo $QSIZE, $RUNTIME2 >> data/${SIZE}_amortised_data_binary_java.csv
    
done

done

done
