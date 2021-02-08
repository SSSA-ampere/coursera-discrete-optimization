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

% how many nodes for each color
array [1..ubc] of var NODES: nodes_per_color;

% the total number of different 'colors' in the array colors
var lbc..ubc: nbColors;

% neighbor nodes cannot have the same color
constraint forall(i in EDGES)(colors[edges1[i]] != colors[edges2[i]]);

% count the different numbers in colors
constraint nbColors = card({ colors[i] | i in NODES});

% symmetry breaking constraint
% the number of nodes with color i must be >= than the number of nodes with color i+1
% from: A survey on vertex coloring problems. 2009
%constraint forall(i in 1..ubc-1) (
%    count([ colors[j] = i | j in NODES]) >= count([ colors[j] = i+1 | j in NODES])
%);

%function var int: among(array [int] of var int: x, set of int: v)
%Returns the number of variables in x that take one of the values in v .
%count the number of occurences of i in colors and assign it to nodes_per_color[i]
constraint forall(i in 1..ubc) (
    %trace("nodes_per_color[\(i)] \n" ,
    nodes_per_color[i] = among(colors, i..i)
    %)
);

%predicate decreasing(array [$X] of var set of int: x)
%Requires that the array x is in decreasing order (duplicates are allowed).
%strictly_decreasing
constraint decreasing (nodes_per_color);

%constraint forall(i in 1..ubc) (
%    nodes_per_color[i] = count([ colors[j] = i | j in NODES])
%);


% symmetry breaking constraint
% color i+1 can be assigned to a vertex only if color i is assigned to some other vertex
% from: A survey on vertex coloring problems. 2009
% constraint forall(i in 1..ubc-1)(
%     count([ colors[j] = i+1 | j in NODES]) > 0  ->  count([ colors[j] = i | j in NODES]) > 0
% );
constraint forall (i,j in 1..ubc where i < j)(nodes_per_color[j] > 0 /\  nodes_per_color[i] > 0);


% list of clique alldifferent constraints for the cliques
% PUT_CLIQUES_HERE

%solve minimize maxC;
solve minimize nbColors;

output ["\(nbColors)\n"];
output [show(colors)];
output ["\n"];
output [show(nodes_per_color)];
