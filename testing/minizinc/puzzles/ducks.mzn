% source: programming with constraints: an introduction. 1998

% exercise 1.7: Huey, Dewey and Louie are being questioned by their uncle. These are the statments they make:
%  Huey: "Dewey and Louie had equal share in it; if one is guilty, so is the other."
%  Dewey: "If Huey is guilty, then so am I."
%  Louie: "Dewey and I are not both guilty."

% Their uncle,  knowing that they are cub scouts, realises that they cannot tell a lie. Has he got sufficient infromation to decide who (if any) are guilty ? Model the problem as Boolean constratins, and decide.

% solution: none of the is guilty
% 0, 0, 0

% 0 is not guilty, 1 is guilty
var 0..1: h;
var 0..1: d;
var 0..1: l;

constraint d = l;
constraint h = 1 -> d = 1;
%constraint d = l <-> l = 0;
constraint d+l < 2;

output ["\(h), \(d), \(l)\n"];

