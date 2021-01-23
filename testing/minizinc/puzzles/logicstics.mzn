
% Wallace, Mark. Building Decision Support Systems: Using MiniZinc. Springer Nature, 2020.
% 6.4.3 Linear Expressions and Constraints
% example called 'Transportation Model'
% solution in: 8.5.4 Linear Expressions and Constraints

% Each client has a demand which has to be satisfied, and each plant has a capacity
% which it cannot exceed. Finally there is a (different) cost in going from each plant
% to each client. To model this problem we introduce a decision variable for each link
% from a plant to a client, whose value is the flow down that link. The constraints say
% that the total flow out from each plant must be less than its capacity, and the total
% flow into each client must satisfy its demand. (We allow this flow to be greater than
% or equal to the demand.)

% Parameters:
% - Array of demands dem = [2.0, 3.8, 3.0, 1.2]
% - Array of capacities cap = [5.5, 3.8, 4.2]
% - 4 by 3 matrix recording the cost of delivering to each client from
% each plant:

% cost  1     2       3
% 1   10.0    7.0     11.0
% 2   8.0     5.0     11.0
% 3   5.0     5.0     8.0
% 4   9.0     3.0     7.0

array [1..4] of float : dem = [2.0, 3.8, 3.0, 1.2];
array [1..3] of float : cap = [5.5, 3.8, 4.2];

array [1..4,1..3] of float : costs = 
    array2d(1..4,1..3,
    [
        10.0,7.0 ,11.0,
        8.0 ,5.0 ,11.0,
        5.0 ,5.0 ,8.0,
        9.0 ,3.0 ,7.0,
    ]);

array [1..4,1..3] of var 0.0..max(cap) : supply ;

% supply has to be non negative
constraint forall (i in 1..4, j in 1..3)(
    supply[i,j] >= 0.0
);

% the clients demand have to be satisfied
constraint forall (i in 1..4)(
    sum(j in 1..3)(supply[i,j]) >= dem[i]
);

% the plant cannot provide more than its capacity
constraint forall (j in 1..3)(
    sum(i in 1..4)(supply[i,j]) <= cap[j]
);

solve minimize sum(i in 1..4, j in 1..3)(costs[i,j]*supply[i,j]);

output [ show(supply[i,j]) ++ " " ++ 
    if j == 3 then "\n" else "" endif | 
    i in 1..4, j in 1..3 ];