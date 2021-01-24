include "globals.mzn";

% the the upper and lower bound for number of colors
int: ubc;
int: lbc;

% parameters
int: nbNodes;
int: nbEdges;
set of int: NODES = 0..nbNodes-1;
set of int: EDGES = 1..nbEdges;

% there is no tuple in minizinc, so the nodes of the edge are split into two arrays
array [EDGES] of NODES: edges1;
array [EDGES] of NODES: edges2;

% the color of each node
array [NODES] of var 1..ubc: colors;

% the total number of different 'colors' in the array colors
var lbc..ubc: nbColors;
%var NODES: maxC;

% neighbor nodes cannot have the same color
constraint forall(i in EDGES)(colors[edges1[i]] != colors[edges2[i]]);

% count the different numbers in colors
constraint nbColors = card({ colors[i] | i in NODES});
%constraint maxC = max([colors[i] | i in NODES]);

% breaking some color value symmetry by imposing order in the color assignment
%constraint forall(i in NODES, j in 1..nbNodes-2)(colors[i] <= colors[j]);

%constraint forall(i in 1..nbColors, j in 2..nbColors-1)( i < j /\ sum({ colors[k] = i | k in NODES}) >= sum({ colors[k] = j | k in NODES}))

% put bounds in the search
%constraint nbColors >= lbc /\ nbColors <= ubc;
%constraint maxC >= lbc /\ maxC <= ubc;

%solve minimize maxC;
solve minimize nbColors;

output ["\(nbColors)\n"];
%output ["\(maxC)\n"];
output [show(colors)];
