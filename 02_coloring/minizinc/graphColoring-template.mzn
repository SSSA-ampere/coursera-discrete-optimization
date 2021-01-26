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

% neighbor nodes cannot have the same color
constraint forall(i in EDGES)(colors[edges1[i]] != colors[edges2[i]]);

% count the different numbers in colors
constraint nbColors = card({ colors[i] | i in NODES});

% symmetry breaking constraint
% the number of nodes with color i must be >= than the number of nodes with color i+1
% from: A survey on vertex coloring problems. 2009
constraint forall(i in 1..ubc-1) (
    count([ colors[j] = i | j in NODES]) >= count([ colors[j] = i+1 | j in NODES])
);

% symmetry breaking constraint
% color i+1 can be assigned to a vertex only if color i is assigned to some other vertex
% from: A survey on vertex coloring problems. 2009
constraint forall(i in 1..ubc-1)(
    count([ colors[j] = i+1 | j in NODES]) > 0  ->  count([ colors[j] = i | j in NODES]) > 0
);

% list of clique alldifferent constraints for the cliques
% PUT_CLIQUES_HERE

%solve minimize maxC;
solve minimize nbColors;

output ["\(nbColors)\n"];
output [show(colors)];
