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
% sums  = [39, 39, 39, 39, 39, 39, 39, 39, 39, 39]
% 18 2 7 12 
% 10 1 13 15 
% 6 9 16 8 
% 5 27 3 4 

% the obtained result for n=5 is 
% sums  = [77, 77, 77, 77, 77, 77, 77, 77, 77, 77, 77, 77]
% 3 5 35 4 30 
% 13 31 11 10 12 
% 17 18 1 14 27 
% 16 8 7 40 6 
% 28 15 23 9 2 

% the obtained result for n=6 is 
% sums  = [165, 165, 165, 165, 165, 165, 165, 165, 165, 165, 165, 165, 165, 165]
% 104 16 14 9 4 18 
% 15 42 20 61 2 25 
% 13 22 7 6 59 58 
% 12 23 88 8 5 29 
% 11 41 19 57 3 34 
% 10 21 17 24 92 1 

% for n>7, the execution time becomes too big

include "alldifferent.mzn";

int: n=5;

% the max value cannot be bigger than pow(n,2)*n, i.e., all values having the max value
array [1..n,1..n] of var 1..pow(n,2)*n: m;
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
constraint forall (i,j in 1..2*n+2)(
    s[i] = s[j]
);

output ["sums  = \(s)\n"];
output [ show(m[i,j]) ++ " " ++ 
    if j == n then "\n" else "" endif | 
    i in 1..n, j in 1..n ];


