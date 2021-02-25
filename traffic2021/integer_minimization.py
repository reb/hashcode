"""from gekko import GEKKO

m = GEKKO(remote=False)
x = m.Array(m.Var,9,lb=0,ub=7,integer=True)

def f(x):
    return (481.79/(5+x[0]))+(412.04/(4+x[1]))\
           +(365.54/(3+x[2]))+(375.88/(3+x[3]))\
           +(379.75/(3+x[4]))+(632.92/(5+x[5]))\
           +(127.89/(1+x[6]))+(835.71/(6+x[7]))\
           +(200.21/(1+x[8]))

m.Minimize(f(x))
m.Equation(sum(x)==7)
m.options.SOLVER=1
m.solve()
print(x)"""
import scipy.optimize
import numpy as np


def objective(x):
    return x[0]**2.0 + x[1]**2.0


# define range for input
r_min, r_max = -5.0, 5.0
# define the starting point as a random sample from the domain
pt = r_min + np.random.rand(2) * (r_max - r_min)
# define range for input
r_min, r_max = -5.0, 5.0
# define the starting point as a random sample from the domain
pt = r_min + np.random.rand(2) * (r_max - r_min)
# perform the search
result = scipy.optimize.minimize(objective, pt, method='nelder-mead')

if result.success:
    print('Converged to')
    print(result.x)
else:
    print("failed to converge")
    print(result.message)

sol = result.x
sol_integer = 