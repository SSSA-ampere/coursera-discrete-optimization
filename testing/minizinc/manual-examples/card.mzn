array[int, int] of int: a = 
  [| 1, 1,
   | 1, 3, 
   | 3, 4 |];

set of int: Rows = index_set_1of2(a);
set of int: Cols = index_set_2of2(a);

int: values = card({ a[r, c] | r in Rows, c in Cols });

output [show(Rows)];
output ["\(values) values in "] ++ 
       [if c == 1 then "\n" else "" endif ++ 
        "\(a[r, c]) " | r in Rows, c in Cols];

