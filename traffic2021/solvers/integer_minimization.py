from traffic2021.problem import *
import scipy.optimize
import numpy as np

"""
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
sol_integer = np.rint(sol)
"""


def solve(problem: Problem) -> Solution:

    def objective(example_sol):
        return score(array_to_sol(example_sol, problem), problem)

    starting_point = np.ones(number_of_lights(problem))
    optimized_schedule = scipy.optimize.minimize(objective, starting_point, method='nelder-mead')

    if optimized_schedule.success:
        print('Converged to')
        print(optimized_schedule.x)
    else:
        print("failed to converge")
        print(optimized_schedule.message)

    sol = optimized_schedule.x
    solution_vector_int = np.rint(sol).astype('int')
    return array_to_sol(solution_vector_int, problem)