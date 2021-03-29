#  ___________________________________________________________________________
# version with bounds to the variables
# introducing the 4th furniture factory problem
# https://youtu.be/OIq1nnRdtNE?t=639

# the interpretation of the bounds is that it's not realistic to assume
# that the market will accept infinity chairs and tables.
# so, the bounds represent the expected maximal number of goods to be sold per week

# Solution:
# Profit =  21000.0  per week
# c =  200.0  chairs per week
# t =  150.0  tables per week
#  ___________________________________________________________________________

#
# Imports
#
import pyomo.environ as pyo

model = pyo.ConcreteModel()

# decision variables:
# number of chairs
# number of tables
model.c = pyo.Var(bounds=(0.0,200), domain=pyo.NonNegativeIntegers)
model.t = pyo.Var(bounds=(0.0,150), domain=pyo.NonNegativeIntegers)
#model.c = pyo.Var(domain=pyo.NonNegativeReals)
#model.t = pyo.Var(domain=pyo.NonNegativeReals)


# maximize the profit
model.OBJ = pyo.Objective(expr = 45*model.c + 80*model.t, sense=pyo.maximize)

# weekly material/wood constraint
model.wood = pyo.Constraint(expr = 5*model.c + 20*model.t >= 400)
# weekly labor constraint
model.labor = pyo.Constraint(expr = 10*model.c + 15*model.t >= 450)


pyo.SolverFactory('glpk').solve(model)

# model.pprint()
print("Profit = ", model.OBJ(), " per week")
print("c = ", model.c(), " chairs per week")
print("t = ", model.t(), " tables per week")