include "globals.mzn";

% model used to test the heuristics solutions
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
array [NODES] of var int: colors;

% neighbor nodes cannot have the same color
constraint forall(i in EDGES)(colors[edges1[i]] != colors[edges2[i]]);

% list of clique alldifferent constraints for the cliques
% PUT_CLIQUES_HERE

solve satisfy;

output [show(colors)];
