% Source: Krzysztof Apt. Principles of Constraint Programming. Chapter 2. 2003

% Exercise 2.4 Latin Squares.

% A Latin square of order n is defined to be an n × n matrix made out
% of the integers in [1..n] with the property that each of the these n integers
% occurs exactly once in each row and exactly once in each column of the
% array. For example

% 12345
% 23451
% 34512
% 45123
% 51234

% is a Latin square of order 5. Formulate the problem of finding a Latin square
% of order n as a CSP.

% for n=5, response is
% 3 1 2 4 5 
% 1 2 5 3 4 
% 2 5 4 1 3 
% 4 3 1 5 2 
% 5 4 3 2 1 

% for n=6, response is 
% 3 1 2 4 5 6 
% 2 3 1 6 4 5 
% 1 6 5 2 3 4 
% 4 2 6 5 1 3 
% 5 4 3 1 6 2 
% 6 5 4 3 2 1 

% for n=7, response is 
% 2 3 1 5 4 6 7 
% 4 2 3 1 7 5 6 
% 3 1 7 6 2 4 5 
% 1 7 6 2 5 3 4 
% 5 4 2 7 6 1 3 
% 6 5 4 3 1 7 2 
% 7 6 5 4 3 2 1 

include "alldifferent.mzn";

int: n=7;

array [1..n,1..n] of var 1..n: m;

% all the lines must be different
constraint forall (i in 1..n)(
    alldifferent([m[i,j] | j in 1..n])
);

% all the cols must be different
constraint forall (i in 1..n)(
    alldifferent([m[j,i] | j in 1..n])
);

output [ show(m[i,j]) ++ " " ++ 
    if j == n then "\n" else "" endif | 
    i in 1..n, j in 1..n ];
