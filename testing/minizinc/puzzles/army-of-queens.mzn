% Source: Krzysztof Apt. Principles of Constraint Programming. Chapter 2. 2003

% Exercise 2.8 Peaceable Coexisting Armies of Queens.

% Two armies of queens (black and white) peacefully coexist on a chessboard
% when they are placed upon the board in such a way that no two queens
% from opposing armies can attack each other. The problem is to find the
% maximum two equal-sized armies. Formulate this problem as a constrained
% optimization problem.


% this is the model of the normal 8-queens problem
% int: n; % The number of queens.

% array [1..n] of var 1..n: q;

% include "alldifferent.mzn";

% constraint alldifferent(q);
% constraint alldifferent(i in 1..n)(q[i] + i);
% constraint alldifferent(i in 1..n)(q[i] - i);



int: n = 4;
array [1..n] of var 1..8: posW;
array [1..n] of var 1..8: posB;
array [1..2*n] of var 1..8: pos;

include "alldifferent.mzn";

% combine both arrays
constraint forall(i in 1..n)(pos[i] = posW[i] /\ pos[i+n] = posB[i]);

% the queens cannot be in the same row
constraint alldifferent(pos);

constraint alldifferent(i in 1..2*n)(pos[i] + i);
constraint alldifferent(i in 1..2*n)(pos[i] - i);

output [show(pos) ++ "\n"];
output ["white queens: " ++ show(posW) ++ "\n"];
output ["black queens: " ++ show(posB) ++ "\n"];
