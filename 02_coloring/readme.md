
# Graph Coloring Problem with Constraint Programming and Heuristics

It integrates the minizinc for CP and Networkx heuristics.
Minizinc is used in two modes: to try to get a solution withing a time period; 
to check the satisfiability of the heuritic solutions.
# Results

Not using the results of the heuristics

Coloring Problem 1: ./data/gc_50_3,   colors: 6  ,time: 2.2s,grade: 10;
Coloring Problem 2: ./data/gc_70_7,   colors: 23 ,time: 4s  ,grade: 3 ;
Coloring Problem 3: ./data/gc_100_5,  colors: 20 ,time: 6s  ,grade:   ;
Coloring Problem 4: ./data/gc_250_9,  colors:    ,time: --  ,grade:   ;
Coloring Problem 5: ./data/gc_500_1,  colors: 16 ,time: 45s ,grade:   ;
Coloring Problem 6: ./data/gc_1000_5, colors: 128,time: to  ,grade:   ;

Using the results of the heuristics

Coloring Problem 1: ./data/gc_50_3,   colors: 6  ,time: 2.2s,grade: 10;
Coloring Problem 2: ./data/gc_70_7,   colors: 20 ,time: 4s  ,grade: 7 ;
Coloring Problem 3: ./data/gc_100_5,  colors: 17 ,time: 6s  ,grade: 7 ;
Coloring Problem 4: ./data/gc_250_9,  colors: 90 ,time: --  ,grade: 7 ;
Coloring Problem 5: ./data/gc_500_1,  colors: 16 ,time: 45s ,grade: 10;
Coloring Problem 6: ./data/gc_1000_5, colors: 107,time: to  ,grade: 7 ;


to: timeout; --: could not run


# Best Results

As stated in the [Leaderboard](https://www.coursera.org/learn/discrete-optimization/discussions/weeks/3/threads/oLKvaNbdEeaM2BLvxl_obA), the best results for the 6 problems are:

 - gc1 = 6; 
 - gc2 = 17; 
 - gc3 = 15; 
 - gc4 = 73; 
 - gc5 = 12; 
 - gc6 = 86.

# References

 - Patrick Winston. ["Constraints: Search, Domain Reduction"](https://www.youtube.com/watch?v=d1KyYyLmGpA&list=PLUl4u3cNGP63gFHB6xb-kVBiQHYe_4hSi&index=8). 2010. 
 - Chris Beck. ["Constraint Programming for Planning and Scheduling (part1)"](https://www.youtube.com/watch?v=Di4CvXInmOE). 2016.
 - Chris Beck. ["Constraint Programming for Planning and Scheduling (part1)"](https://www.youtube.com/watch?v=efJcFl3_vk0). 2016.
  - ["Debugging with Minizinc"](https://www.coursera.org/lecture/advanced-modeling/2-1-2-tracing-models-EEbTn)
