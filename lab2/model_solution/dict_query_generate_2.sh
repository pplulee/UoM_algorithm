SIZES="10000 20000 30000 40000 50000"

QUERY_SIZES="0.1 0.5 1 5 10"

for SIZE in $SIZES
do

for QSIZE in $QUERY_SIZES
do

QUERY_SIZE=$( echo "$SIZE * $QSIZE/1" | bc)

echo $QUERY_SIZE

for COUNT in 1 2 3 4 5
do

     python3 generate.py random dict_${SIZE}_${QUERY_SIZE}_$COUNT query_${SIZE}_${QUERY_SIZE}_$COUNT $SIZE ${QUERY_SIZE} none 99


done

done

done
