% The Zebra Puzzle https://en.wikipedia.org/wiki/Zebra_Puzzle
% solution:
% zebra = 4 Japan
% water = 1 Norway
% 1 - Norway, sculptor, snail, blue, water
% 2 - Italian, diplomat, fox, yellow, tea
% 3 - English, doctor, horse, red, milk
% 4 - Japan, painter, zebra, green, coffee
% 5 - Spain, violinist, dog, white, juice

include "alldifferent.mzn";

enum color = {red, yellow, green, white, blue};
enum nationality = {English, Spain, Japan, Italian, Norway};
enum pet = {dog, snail, fox, horse, zebra};
enum drink = {tea, coffee, milk, juice, water};
enum profession = {painter, sculptor, diplomat, violinist, doctor};

%var 1..5: house;
%array [1..5] of var 1..5: house_pos;
array [1..5] of var color: colors;
array [1..5] of var nationality: nationalities;
array [1..5] of var pet: pets;
array [1..5] of var drink: drinks;
array [1..5] of var profession: professions;

%The Englishman lives in the red house.
constraint forall (h in 1..5)(
  nationalities[h] = English -> colors[h] = red
);

%The Spaniard has a dog.
constraint forall (h in 1..5)(
  nationalities[h] = Spain -> pets[h] = dog
);

%The Japanese is a painter.
constraint forall (h in 1..5)(
  nationalities[h] = Japan -> professions[h] = painter
);

%The Italian drinks tea.
constraint forall (h in 1..5)(
  nationalities[h] = Italian -> drinks[h] = tea
);

%The Norwegian lives in the first house on the left.
constraint nationalities[1] = Norway;

%The owner of the green house drinks coffee.
constraint forall (h in 1..5)(
  colors[h] = green -> drinks[h] = coffee
);

%The green house is on the right of the white house.
constraint forall (h in 1..4)(
  colors[h] = white -> colors[h+1] = green
);

%The sculptor breeds snails.
constraint forall (h in 1..5)(
  professions[h] = sculptor -> pets[h] = snail
);

% The diplomat lives in the yellow house.
constraint forall (h in 1..5)(
  professions[h] = diplomat -> colors[h] = yellow
);

% They drink milk in the middle house.
constraint drinks[3] = milk;

% The Norwegian lives next door to the blue house.
constraint forall (h in 2..4)(
  colors[h] = blue -> nationalities[h-1] = Norway \/ nationalities[h+1] = Norway
);

% The violinist drinks fruit juice.
constraint forall (h in 1..5)(
  professions[h] = violinist -> drinks[h] = juice
);

% The fox is in the house next to the doctor’s.
constraint forall (h in 2..4)(
  professions[h] = doctor -> pets[h-1] = fox \/ pets[h+1] = fox
);

% The horse is in the house next to the diplomat’s.
constraint forall (h in 2..4)(
  professions[h] = diplomat -> pets[h-1] = horse \/ pets[h+1] = horse
);

constraint alldifferent(pets);
constraint alldifferent(professions);
constraint alldifferent(colors);
constraint alldifferent(drinks);
constraint alldifferent(nationalities);

%solve satisfy;

output [ if fix(pets[h]  = zebra)   then "zebra = \(h) \(nationalities[h])\n" else "" endif | h in 1..5  ];
output [ if fix(drinks[h]  = water) then "water = \(h) \(nationalities[h])\n" else "" endif | h in 1..5 ];
output [ "\(h) - "
  ++ "\(nationalities[h]), "
  ++ "\(professions[h]), "
  ++ "\(pets[h]), "
  ++ "\(colors[h]), "
  ++ "\(drinks[h])\n"
  | h in 1..5
]