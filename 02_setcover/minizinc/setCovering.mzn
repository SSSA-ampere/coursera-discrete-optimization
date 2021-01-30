

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

array [ITEMS] of var 1..max_set: set_union;

%constraint forall(s in SETS, j in 1..max_set)(sel_sets[s] = 1 -> set_union = set_union union list_sets[s,j]);
%constraint forall(s in SETS, j in 1..max_set)(sel_sets[s] = 1 -> set_union = set_union union row(list_sets,s));
%constraint set_union = forall(s in SETS, j in 1..max_set)(list_sets[i][j] where sel_sets[i] = 1);
%constraint set_union = [list_sets[i,j] | i in SETS, j in 1..max_set where sel_sets[i] = 1];

constraint forall(i in ITEMS)(
    exists(s in SETS)(sel_sets[s] = 1 /\ i in sets[s])
);

solve minimize sum(i in SETS)(sel_sets[i] * weights[i]);

output [show(sel_sets)];