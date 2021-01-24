include "globals.mzn";

% parameters
int: nbNodes;
int: nbEdges;
set of int: NODES = 0..nbNodes-1;
set of int: EDGES = 1..nbEdges;

% there is no tuple in minizinc, so the nodes of the edge are split into two arrays
array [EDGES] of NODES: edges1;
array [EDGES] of NODES: edges2;

% the color of each node
array [NODES] of var NODES: colors;

% the total number of different 'colors' in the array colors
var NODES: nbColors;

% neighbor nodes cannot have the same color
constraint forall(i in EDGES)(colors[edges1[i]] != colors[edges2[i]]);

% count the different numbers in colors
constraint nbColors = card({ colors[i] | i in NODES});

solve minimize nbColors;

output ["\(nbColors)\n"];
output [show(colors)];
