% sources: 
%  - https://gwr3n.github.io/presentations/PEPA_2013.pdf
%  - https://youtu.be/Di4CvXInmOE?t=706

% Given a network of 8 nodes a, b, c, d, e,  f, g, h, connected as described by this adjacency matrix:
% a b c d
% b a c e f
% c a b d e f g
% d a c f g
% e b c f h
% f b c d e g h
% g c d f h
% h e f g

% Place numbers 1, . . . , 8 on nodes by making sure that
% - each number appears exactly once
% - consecutive numbers do not appear on adjacent nodes

% solution: 7,4,1,3,6,8,5,2,

include "alldifferent.mzn";


int: a=1;
int: b=2;
int: c=3;
int: d=4;
int: e=5;
int: f=6;
int: g=7;
int: h=8;

array [1..8] of var 1..8: nodes;

predicate next(1..8: n1, 1..8: n2) = 
  n1 = 1 -> nodes[n1] != nodes[n2]+1 \/
  n1 = 8 -> nodes[n1] != nodes[n2]-1 \/
  n1 > 1 /\ n1 < 8 -> nodes[n1] != nodes[n2]+1 /\ nodes[n1] != nodes[n2]-1;

constraint next(a,b);
constraint next(a,c);
constraint next(a,d);
constraint next(b,c);
constraint next(b,e);
constraint next(b,f);
constraint next(c,d);
constraint next(c,e);
constraint next(c,f);
constraint next(c,g);
constraint next(d,f);
constraint next(d,g);
constraint next(e,f);
constraint next(e,h);
constraint next(f,g);
constraint next(f,h);
constraint next(g,h);

constraint alldifferent(nodes);


output ["\(n)," | n in nodes];
output ["\n"];


