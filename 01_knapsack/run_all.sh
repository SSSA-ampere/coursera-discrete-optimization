echo "" > results.out
for file in ./data/*
do
  echo "####################################" >> results.out
  echo "solutions/bb_heap.py $file" >> results.out 
  echo "####################################" >> results.out
  #solutions/bb_heap.py "$file" >> results.out
  solutions/sorted_value_per_weight.py "$file" >> results.out
done
