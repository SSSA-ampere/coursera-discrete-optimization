#  ___________________________________________________________________________
# version with multiple solutions plus cost of unsed capacity of labor and wood
# introducing the 3nd furniture factory problem
# https://youtu.be/kGs32O2rhx8?t=739

# Solution 1:
# Profit =  2250.0  per week
# c =  24.0  chairs per week
# t =  14.0  tables per week
# w =  0.0  unused wood cost per week
# l =  0.0  unsued labor cost per week

#  ___________________________________________________________________________

#
# Imports
#
import pyomo.environ as pyo

model = pyo.ConcreteModel()

# decision variables:
# number of chairs
# number of tables
# unused wood
# unused labor
model.c = pyo.Var(domain=pyo.NonNegativeIntegers)
model.t = pyo.Var(domain=pyo.NonNegativeIntegers)
model.w = pyo.Var(domain=pyo.NonNegativeIntegers)
model.l = pyo.Var(domain=pyo.NonNegativeIntegers)
# model.c = pyo.Var(domain=pyo.NonNegativeReals)
# model.t = pyo.Var(domain=pyo.NonNegativeReals)


# maximize the profit
model.OBJ = pyo.Objective(expr = 50*model.c + 75*model.t -1*model.w -2*model.l, sense=pyo.maximize)

# weekly material/wood constraint
model.wood = pyo.Constraint(expr = 5*model.c + 20*model.t + model.w == 400)
# weekly labor constraint
model.labor = pyo.Constraint(expr = 10*model.c + 15*model.t + model.l == 450)


pyo.SolverFactory('glpk').solve(model)

# model.pprint()
print("Profit = ", model.OBJ(), " per week")
print("c = ", model.c(), " chairs per week")
print("t = ", model.t(), " tables per week")
print("w = ", model.w(), " unused wood cost per week")
print("l = ", model.l(), " unsued labor cost per week")