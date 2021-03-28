#  ___________________________________________________________________________
#
# introducing the furniture factory problem
# https://www.youtube.com/watch?v=pSm1jONu2G8

# model in pygurobi
# https://www.youtube.com/watch?v=Copxhl2FShg
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
#model.c = pyo.Var(domain=pyo.NonNegativeReals)
#model.t = pyo.Var(domain=pyo.NonNegativeReals)


# maximize the profit
model.OBJ = pyo.Objective(expr = 45*model.c + 80*model.t, sense=pyo.maximize)

# weekly material/wood constraint
model.wood = pyo.Constraint(expr = 5*model.c + 20*model.t <= 400)
# weekly labor constraint
model.labor = pyo.Constraint(expr = 10*model.c + 15*model.t <= 450)


pyo.SolverFactory('glpk').solve(model)

# model.pprint()
print("Profit = ", model.OBJ(), " per week")
print("c = ", model.c(), " chairs per week")
print("t = ", model.t(), " tables per week")