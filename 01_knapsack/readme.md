# Knapsack Solutions

This folder has the following solutions to the Knapsack challenge:

- sorted_value_per_weight.py: an extremely fast (less than 0.04s for the largest and about 0.3s for all) and simple heuristics that gives pretty good results with typically with more than 99.99% of knapsack occupation.
- bb_heap.py: a reeealy fast (less than 0.1s for the largest and about 0.8s for all) [Branch & Bound algorigthm](https://www.coursera.org/learn/discrete-optimization/lecture/66OlO/knapsack-5-relaxation-branch-and-bound) using a heap. Optimal results with very low memory usage (less than 20 nodes kept in memory!!!). Perhaps this could be more elegant if rewritten recursively. 
- bb_tree.py: Branch & Bound algorithm using a binary tree. Still under construction. It plots the search tree for debugging purposes.

All solutions have a *debug* flag that can be turned on or off.

# The expected values for the 6 problems

                                                   Expected   Obtained
./data/ks_30_0, solver.py, Knapsack Problem 1      92000      90000
./data/ks_50_0, solver.py, Knapsack Problem 2      142156     141956
./data/ks_200_0, solver.py, Knapsack Problem 3     100236     100062
./data/ks_400_0, solver.py, Knapsack Problem 4     3967028    3966813
./data/ks_1000_0, solver.py, Knapsack Problem 5    109899     109869
./data/ks_10000_0, solver.py, Knapsack Problem 6   1099881    1099870

# The expected values from other Students

Edward Kandrot's Solution

```
Input	      Time(s)	   Output   Score
ks_30_0       0.016	       99798    10
ks_50_0   	  0.004	      142156    10
ks_200_0	  0.594	      100236    10
ks_400_0	  0.099	     3967180    10
ks_1000_0	  0.029	      109899    10
ks_10000_0	  0.212	     1099893    10

Input	       Time(s)	    Output
ks_40_0		    0.008	     99924
ks_45_0		    0.003	     23974
ks_50_1		    0.005	      5345
ks_60_0		    0.024	     99837
ks_82_0		      NA	       NA
ks_100_0	    0.074	     99837
ks_100_1	    0.003	   1333930
ks_100_2	    0.001	     10892
ks_200_1	    0.012	   1103604
ks_300_0	    0.068	   1688692
ks_500_0	    0.009	     54939
```

Jacky's results
```
Input	  Algorithm	    Time(s)	    Output  Score
Ks_30_0	         BB	       0.05	     99798     10
Ks_50_0   	     BB	      0.006	    142156	   10
Ks_200_0	     BB	       0.37	    100236	   10
Ks_400_0	   	 BB        0.52	   3967180	   10
Ks_1000_0	     BB	       0.14	    109899	   10
Ks_10000_0	     BB        3.49	   1099893	   10
```

Jiayi Wei's solution with A*.

```
Problem     | Time(s)  |     Score
ks_19_0     | 4.489e-2 |     12248
ks_30_0     | 1.992e-1 |     99798
ks_40_0     | 4.289e+0 |     99672
ks_45_0     | 2.087e-3 |     23974
ks_50_0     | 1.057e-3 |    142156
ks_50_1     | 1.299e-3 |      5345
ks_60_0     | 9.496e-1 |     99837
ks_82_0     | 1.897e+1 | 104720112
ks_100_0    | 1.292e+0 |     99837
ks_100_1    | 2.750e-3 |   1333930
ks_100_2    | 1.122e-3 |     10892
ks_106_0    | 3.220e+1 | 106923168
ks_200_0    | 6.094e+0 |    100236
ks_200_1    | 1.871e-2 |   1103604
ks_300_0    | 4.835e-1 |   1688692
ks_400_0    | 5.663e-1 |   3967180
ks_500_0    | 6.875e-3 |     54939
ks_1000_0   | 1.834e-2 |    109899
ks_10000_0  | 2.486e-1 |   1099893
```

# Usage

```
$ python solutions/bb_heap.py data/ks_1000_0
$ python solutions/sorted_value_per_weight.py data/ks_1000_0
```

# Profiling

## Using FlameGraph
### Requirements

 - perf tools
 - https://github.com/brendangregg/FlameGraph

### Running 

```
$ sudo perf record -F 99 -a -g -- python solutions/bb_heap.py data/ks_1000_0 | stackcollapse-perf.pl out.perf | flamegraph.pl --color=java --hash > example-perf.svg
```

## Using SnakeViz


### Requirements

- https://jiffyclub.github.io/snakeviz/

### Running 

```
$ python -m cProfile -o program.prof solutions/bb_heap.py data/ks_1000_0
$ snakeviz program.prof
```

## Other Profiling Options

- https://github.com/nvdv/vprof
- https://github.com/uber/pyflame
- https://github.com/Netflix/flamescope
- https://github.com/jlfwong/speedscope
- https://github.com/NERSC/timemory
- http://pramodkumbhar.com/2017/04/summary-of-profiling-tools/

