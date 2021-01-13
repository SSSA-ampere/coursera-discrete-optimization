from minizinc import Instance, Model, Solver

gecode = Solver.lookup("gecode")

nqueens = Model("./queens.mzn")
instance = Instance(gecode, nqueens)
instance["n"] = 8

# Find and print all possible solutions
result = instance.solve(all_solutions=True)
for i in range(len(result)):
    print(result[i, "q"])