# Knapsack Solutions

This folder has the following solutions to the Knapsack challenge:

- sorted_value_per_weight.py: extremely fast and simple heuristics that gives pretty good results with typically with more than 99% of knapsack occupation.
- bb_heap.py: fast Branch & Bound algorigthm using a heap. Optimal results with very low memory usage. Still craching in ks_100_1, ks_400_0, ks_500_0, ks_10000_0.
- bb_tree.py: Branch & Bound algorithm using a binary tree. Still under construction. It plots the search tree for debugging purposes.

All solutions have a *debug* flag that can be turned on or off.

# Usage

```
$ python solutions/bb_heap.py data/ks_1000_0
$ $ python solutions/sorted_value_per_weight.py data/ks_1000_0
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
