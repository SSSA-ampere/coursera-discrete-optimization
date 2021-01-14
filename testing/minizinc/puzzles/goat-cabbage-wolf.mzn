% the problem description:
% - https://en.wikipedia.org/wiki/Wolf,_goat_and_cabbage_problem
% solution:
% - https://stackoverflow.com/questions/8138775/fox-goat-cabbage-transportation
% - [goat, cabbage, wolf problem with minizinc](https://youtu.be/kiX1FOw1GUU?t=2076)
% similar problems:
%  - This is +- similat to the job shop problem since both have the notion of time minimization
%    https://www.minizinc.org/doc-2.5.3/en/modelling2.html#ex-jobshop

% SOLUTIONS assuming maxstep = 8
% Farmer  = [Left, Right, Left, Right, Left, Right, Left, Right]
% Goat    = [Left, Right, Right, Right, Left, Left, Left, Right]
% Cabbage = [Left, Left, Left, Right, Right, Right, Right, Right]
% Wolf    = [Left, Left, Left, Left, Left, Right, Right, Right]
% 1  FGCW -- ....
% 2  ..CW -- FG..
% 3  F.CW -- .G..
% 4  ...W -- FGC.
% 5  FG.W -- ..C.
% 6  .G.. -- F.CW
% 7  FG.. -- ..CW
% 8  .... -- FGCW
% ----------
% Farmer  = [Left, Right, Left, Right, Left, Right, Left, Right]
% Goat    = [Left, Right, Right, Right, Left, Left, Left, Right]
% Cabbage = [Left, Left, Left, Left, Left, Right, Right, Right]
% Wolf    = [Left, Left, Left, Right, Right, Right, Right, Right]
% 1  FGCW -- ....
% 2  ..CW -- FG..
% 3  F.CW -- .G..
% 4  ..C. -- FG.W
% 5  FGC. -- ...W
% 6  .G.. -- F.CW
% 7  FG.. -- ..CW
% 8  .... -- FGCW
% ----------
% ==========

% if maxstep increases, then there are more solutions, possible with cycles

int: maxstep = 8;
set of int: STEP = 1..maxstep;
enum POS = {Left, Right};

array [STEP] of var POS: farmer;
array [STEP] of var POS: goat;
array [STEP] of var POS: cabbage;
array [STEP] of var POS: wolf;

% if the cabbage and the goat are in the same side, then must also be the farmer
constraint forall(i in STEP)(
  cabbage[i] = goat[i] -> farmer[i] = cabbage[i]
  );
  
% if the wolf and the goat are in the same side, then must also be the farmer
constraint forall(i in STEP)(
  wolf[i] = goat[i] -> farmer[i] = wolf[i]
  );

% the boat can only transport the farmer + one assuming both are in the same side of the river
predicate moves(array [STEP] of var 1..maxstep-1: item,  1..maxstep-1: s) =
  item[s] != item[s+1];

predicate stays(array [STEP] of var 1..maxstep-1: item, 1..maxstep-1: s) =
  item[s] = item[s+1];

constraint forall(s in 1..maxstep-1) (
  moves(wolf,s) -> wolf[s] = farmer[s] /\ moves(farmer,s) /\  stays(cabbage,s) /\  stays(goat,s)
);

constraint forall(s in 1..maxstep-1) (
  moves(cabbage,s) ->  cabbage[s] = farmer[s] /\ moves(farmer,s) /\  stays(wolf,s) /\  stays(goat,s)
);

constraint forall(s in 1..maxstep-1) (
  moves(goat,s) -> goat[s] = farmer[s] /\ moves(farmer,s) /\  stays(wolf,s) /\  stays(cabbage,s)
);

% the initial position
constraint farmer[1] = Left /\ goat[1] = Left /\ cabbage[1] = Left /\ wolf[1] = Left ;


% the goal
constraint farmer[maxstep] = Right /\ goat[maxstep] = Right /\ cabbage[maxstep] = Right /\ wolf[maxstep] = Right ;



output ["Farmer  = \(farmer)\n"];
output ["Goat    = \(goat)\n"];
output ["Cabbage = \(cabbage)\n"];
output ["Wolf    = \(wolf)\n"];
output [ "\(s)  "
  ++ if fix(farmer[s]  = Left) then "F" else "." endif
  ++ if fix(goat[s]    = Left) then "G" else "." endif
  ++ if fix(cabbage[s] = Left) then "C" else "." endif
  ++ if fix(wolf[s]    = Left) then "W" else "." endif
  ++ " -- "
  ++ if fix(farmer[s]  = Right) then "F" else "." endif
  ++ if fix(goat[s]    = Right) then "G" else "." endif
  ++ if fix(cabbage[s] = Right) then "C" else "." endif
  ++ if fix(wolf[s]    = Right) then "W" else "." endif
  ++ "\n"
  | s in STEP
]