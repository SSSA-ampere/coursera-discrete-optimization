# Installing pyomo

```
conda create -n pyomo python=3.9
conda activate pyomo
conda install -c conda-forge ipopt glpk coincbc
pyomo solve --solver=glpk diet.py diet.dat
```

