STATES="sorted reverse none"
SIZES="10000 20000 30000 40000 50000 60000 70000 80000 90000 100000"

for STATE in $STATES
do

for SIZE in $SIZES
do

echo $SIZE

for COUNT in 1 2 3 4 5
do

    python3 generate.py random dict_${SIZE}_${STATE}_$COUNT query_${SIZE}_${STATE}_$COUNT $SIZE 1 $STATE 0
    
done

done

done
