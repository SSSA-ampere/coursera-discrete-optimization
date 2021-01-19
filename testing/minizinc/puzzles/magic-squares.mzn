% Source: Krzysztof Apt. Principles of Constraint Programming. Chapter 2. 2003

% Exercise 2.3 Magic Squares.

% A magic square of order n is defined to be an n × n matrix made out
% of the integers from [1..n 2 ] arranged in such a way that the sum of every
% row, column, and the two main diagonals is the same. For example

% 1 15 24 8 17
% 23 7 16 5 14
% 20 4 13 22 6
% 12 21 10 19 3
% 9 18 2 11 25

% is a magic square of order 5, because each row, column and main diagonal
% sums up to 65. Formulate the problem of finding a magic square of order n
% as a task of finding a solution to a CSP.

% the obtained result for n=4 is 
% sums  = [34, 34, 34, 34, 34, 34, 34, 34, 34, 34]
% 4 9 7 14 
% 5 16 2 11 
% 10 3 13 8 
% 15 6 12 1

% the obtained result for n=5 is 
% sums  = [65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65]
% 21 3 13 5 23 
% 6 17 15 19 8 
% 9 25 1 10 20 
% 11 4 14 24 12 
% 18 16 22 7 2 

% for n>5, the execution time becomes too big, i.e. more than 2 min

include "alldifferent.mzn";

int: n=6;

% the max value cannot be bigger than pow(n,2)*n, i.e., all values having the max value
array [1..n,1..n] of var 1..pow(n,2): m;
array [1..2*n+2] of var 1..pow(n,2)*n: s;

constraint alldifferent(m);

% the sum of the lines is stored in s[1..n]
constraint forall (i in 1..n)(
    s[i] = sum(j in 1..n)(m[i,j])
);

% the sum of the cols is stored in s[n+1..2*n]
constraint forall (i in 1..n)(
    s[n+i] = sum(j in 1..n)(m[j,i])
);

% the lower diagonal
constraint s[2*n+1] = sum(i in 1..n)(m[i,i]);


% the upper diagonal
constraint s[2*n+2] = sum(i in 1..n)(m[n-i+1,i]);


% all positions of s must be equal
constraint forall (
    [s[i] = s[j] | i,j in 1..2*n+2 where i < j]
);

output ["sums  = \(s)\n"];
output [ show(m[i,j]) ++ " " ++ 
    if j == n then "\n" else "" endif | 
    i in 1..n, j in 1..n ];


