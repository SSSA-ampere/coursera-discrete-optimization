int: flour;  %no. grams of flour available
int: banana; %no. of bananas available
int: sugar;  %no. grams of sugar available
int: butter; %no. grams of butter available
int: cocoa;  %no. grams of cocoa available

constraint assert(flour >= 0,"Invalid datafile: " ++
                  "Amount of flour should be non-negative");
constraint assert(banana >= 0,"Invalid datafile: " ++
                  "Amount of banana should be non-negative");
constraint assert(sugar >= 0,"Invalid datafile: " ++
                  "Amount of sugar should be non-negative");
constraint assert(butter >= 0,"Invalid datafile: " ++
                  "Amount of butter should be non-negative");
constraint assert(cocoa >= 0,"Invalid datafile: " ++
                  "Amount of cocoa should be non-negative");

var 0..100: b; % no of banana cakes
var 0..100: c; % no of chocolate cackes

%flour
constraint 250*b+200*c <= flour;
%bananas
constraint 2*b <= banana;
% sugar
constraint 75*b + 150*c < sugar;
% butter
constraint 100*b + 150*c <= butter;
% chocolate
constraint 75*c <= cocoa;

%constraint c == b;

% miximize out profit
solve maximize 400*b + 550*c;

output ["no. of banana cakes = \(b)\n",
         "no. of chocolate cakes = \(c)\n",
         "total profit = \(400*b + 550*c)\n",
         "ingredients left:\n",
         " - flour \(flour-(250*b+200*c))\n",
         " - banana \(banana-(2*b))\n",
         " - sugar \(sugar-(75*b + 150*c))\n",
         " - butter \(butter-(100*b + 150*c))\n",
         " - choco \(cocoa-(75*c))\n"];