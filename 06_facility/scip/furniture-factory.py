
"""
introducing the furniture factory problem
https://www.youtube.com/watch?v=pSm1jONu2G8

model in pygurobi
https://www.youtube.com/watch?v=Copxhl2FShg
"""
from pyscipopt import Model

model = Model("furniture")
c = model.addVar(vtype="I", name="chair")
t = model.addVar(vtype="I", name="tables")
# c = model.addVar(name="chair")
# t = model.addVar(name="tables")

# Set up constraint for the weekly amount of wood 
model.addCons(5*c + 20*t <= 400, name="wood")

# Set up constraint for weekly labor hours 
model.addCons(10*c + 15*t <= 450, name="labor")

# Set objective function
model.setObjective(45*c + 80*t, "maximize")

model.hideOutput()
model.optimize()

#solution = model.getBestSol()

print("Optimal value:", model.getObjVal())
print((c.name, t.name), " = ", (model.getVal(c), model.getVal(t)))

