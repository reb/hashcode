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
        return -score(problem, array_to_sol(example_sol, problem))

    n_lights = number_of_lights(problem)
    all_time = problem.duration
    n_roads = len(problem.streets)
    best_time = np.rint(all_time/n_roads * 10)
    best_time_int = best_time.astype('int')
    max_time = np.min([all_time, best_time_int])
    best_point = np.ones(n_lights)
    best_score = score(problem, array_to_sol(best_point, problem))
    for i in range(10):
        other_point = np.random.uniform(0, high=max_time, size=n_lights)
        score_now = score(problem, array_to_sol(other_point, problem))
        if score_now > best_score:
            best_point = other_point
            best_score = score_now
    optimized_schedule = scipy.optimize.minimize(objective, best_point, method='nelder-mead', options={'disp':True})

    if optimized_schedule.success:
        print('Converged to')
        print(optimized_schedule.x)

    else:
        print("failed to converge")
        print(optimized_schedule.message)
    sol = optimized_schedule.x
    solution_vector_int = np.rint(sol).astype('int')

    logger.debug('Starting score')
    logger.debug(score(problem, array_to_sol(starting_point, problem)))
    logger.debug('ending score ')
    logger.debug(score(problem, array_to_sol(solution_vector_int, problem)))
    logger.debug('Solution vector')
    logger.debug(solution_vector_int)
    return array_to_sol(solution_vector_int, problem)