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