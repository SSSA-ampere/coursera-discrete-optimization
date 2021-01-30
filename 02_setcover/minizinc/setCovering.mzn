

% the the upper and lower bound for number of colors
%int: ubc;
%int: lbc;
int: max_set;
int: max_weight;

% parameters
int: nbItems;
int: nbSets;
set of int: ITEMS = 0..nbItems-1;
set of int: SETS = 1..nbSets;

array [SETS] of 1..max_weight: weights;
array [SETS] of set of ITEMS: sets;

array [SETS] of var 0..1: sel_sets;

var int : sum_sets;

%var set of 1..max_set: set_union;

%constraint forall(s in SETS, j in 1..max_set)(sel_sets[s] = 1 -> set_union = set_union union list_sets[s,j]);
%constraint forall(s in SETS, j in 1..max_set)(sel_sets[s] = 1 -> set_union = set_union union row(list_sets,s));
%constraint set_union = forall(s in SETS)(sel_sets[s] = 1 -> set_union = set_union union sets[s]);
%constraint set_union = forall(s in SETS)([sets[s] where sel_sets[s] = 1]);

% make sure each element is in at least one of the selected sets
%https://github.com/discreteoptimization/setcover/blob/master/minizinc_001/setCovering.mzn
% this one is a bit faster but less intuitive
%constraint forall (i in ITEMS) (
%  sum (s in SETS where i in sets[s]) (sel_sets[s]) >= 1  
%);

constraint forall(i in ITEMS)(
    exists(s in SETS)(sel_sets[s] = 1 /\ i in sets[s])
);

constraint sum_sets = sum(i in SETS)(sel_sets[i] * weights[i]);

solve minimize sum_sets;

output ["\(sum_sets)\n"];
output [show(sel_sets)];