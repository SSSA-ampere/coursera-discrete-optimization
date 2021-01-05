echo "" > results.out
for file in ./data/*
do
  echo "####################################" >> results.out
  echo "solutions/bb_heap.py $file" >> results.out 
  echo "####################################" >> results.out
  # merge the stdout and stderr (used for 'time') into the same output file
  #(time python solver.py "$file") > results.out 2>&1
  python solver.py "$file") >> results.out
  #solutions/sorted_value_per_weight.py "$file" >> results.out
done
