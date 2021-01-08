# Knapsack Solutions


This folder has the following solutions to the Knapsack challenge:

- sorted_value_per_weight.py: an extremely fast (less than 0.04s for the largest and about 0.3s for all) and simple heuristics that gives pretty good results with typically with more than 99.99% of knapsack occupation.
- bb_heap.py: a fast (about 6 min for all problems) [Branch & Bound algorithm](https://www.coursera.org/learn/discrete-optimization/lecture/66OlO/knapsack-5-relaxation-branch-and-bound) using a stack. Got the optimal result for all the datasets, except for ks_100_0, ks_106_0, ks_200_0, ks_82_0. It has very low memory footprint since it only keep in memory the not visited nodes, about 2*N nodes. Check the source code to see the detailed documentation. 
- bb_tree.py: Branch & Bound algorithm using a binary tree. Still under construction. It plots the search tree for debugging purposes.

All solutions have a *debug* flag that can be turned on or off.

# Coursera's problems
## The obtained results for bb_heap.py

The six mandatory problems resulted in these results:

```
                    Obtained  Optimal
./data/ks_30_0      99798     y
./data/ks_50_0      142156    y
./data/ks_200_0     100236    n
./data/ks_400_0     3967180   y
./data/ks_1000_0    109899    y
./data/ks_10000_0   1099893   y
```

bb_heap.py has an abortion strategy to avoid long runs. This way, it was not possible to 
guarantee the optimal solution for *./data/ks_200_0*. However, looking at Coursera's forum,
it seems that the obtained value is indeed the optimal value.

The solutions for the entire dataset can be found in the file *results.out*.

## The expected values from other Students

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
ks_40_0     | 4.289e+0 |     99672 -- 99924
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

The problem with ks_82_0 and ks_106_0 are some of the hardest cases. Their profits and weights are equal, or close to equal. For a Branch and Bound algorithm, it 'kills' the LP relaxation since
almost all the tree must be visited.

# Usage

```
$ python solutions/bb_heap.py data/ks_1000_0
$ python solutions/sorted_value_per_weight.py data/ks_1000_0
```

# Plotting the tree

bb_head.py as an attribute called *build_tree* that, when it's True, it saves the tree in Pickle format while performing the search. Then, two additional scripts can be used for plotting the tree:

 - *tree_convert.py*: converts the generated Pickle file into several other formats, including dot graphviz.
 - *tree_plot.py*: plot the tree using Networkx. In the future it will also plot an interactive tree with plotly. 

# Profiling

## Using FlameGraph
### Requirements

 - perf tools
 - https://github.com/brendangregg/FlameGraph

### Running 

```
$ sudo perf record -F 99 -a -g -- python solutions/bb_heap.py data/ks_1000_0 | stackcollapse-perf.pl out.perf | flamegraph.pl --color=java --hash > example-perf.svg
```

## Using Py-Spy

### Requirements

 - https://github.com/benfred/py-spy
 - https://github.com/jlfwong/speedscope

### Running 

```
$ py-spy record -f speedscope -o profile.speed --  python ./solutions/bb_heap.py ./data/ks_40_0
$ speedscope profile.speed
```

## Using Snakeviz

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


# References

 - Martello, S. & Toth, P. [Knapsack problems: algorithms and computer implementations](http://www.or.deis.unibo.it/knapsack.html). John Wiley & Sons, 1990.
 - Ghassan Shobaki. ["Algorithms Lecture 20: Backtracking and Branch-and-Bound (Part 1)"](https://www.youtube.com/watch?v=WW5u8RTu44Y&list=PL6KMWPQP_DM8t5pQmuLlarpmVc47DVXWd&index=20).
 - Kellerer, H., Pferschy, U., & Pisinger, D. (2004). Knapsack Problems. Sec 2.4 
 

# To go even further

 - Pisinger, David. "Where are the hard knapsack problems?." Computers & Operations Research 32.9 (2005): 2271-2284.
