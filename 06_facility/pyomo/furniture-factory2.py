#  ___________________________________________________________________________
# version with multiple solutions 
# introducing the 2nd furniture factory problem
# https://youtu.be/kGs32O2rhx8?t=171

# Solution 1:
# Profit =  2250.0  per week
# c =  24.0  chairs per week
# t =  14.0  tables per week

# Solution 2:
# Profit =  2250.0  per week
# c =  45.0  chairs per week
# t =  0.0  tables per week

#  ___________________________________________________________________________

#
# Imports
#
import pyomo.environ as pyo

model = pyo.ConcreteModel()

# decision variables:
# number of chairs
# number of tables
model.c = pyo.Var(domain=pyo.NonNegativeIntegers)
model.t = pyo.Var(domain=pyo.NonNegativeIntegers)
# model.c = pyo.Var(domain=pyo.NonNegativeReals)
# model.t = pyo.Var(domain=pyo.NonNegativeReals)


# maximize the profit
model.OBJ = pyo.Objective(expr = 50*model.c + 75*model.t, sense=pyo.maximize)

# weekly material/wood constraint
model.wood = pyo.Constraint(expr = 5*model.c + 20*model.t <= 400)
# weekly labor constraint
model.labor = pyo.Constraint(expr = 10*model.c + 15*model.t <= 450)


pyo.SolverFactory('glpk').solve(model)

# model.pprint()
print("Profit = ", model.OBJ(), " per week")
print("c = ", model.c(), " chairs per week")
print("t = ", model.t(), " tables per week")