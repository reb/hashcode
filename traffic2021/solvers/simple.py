from traffic2021.problem import *#Problem, Solution, GreenLight
import numpy as np


def solve2(problem: Problem) -> Solution:
    solution = Solution(problem)

    for intersection in problem.intersections:
        street_schedule = [
            GreenLight(street_name, 1) for street_name in intersection.streets
        ]
        solution.schedule[intersection.id].set_street_schedule(street_schedule)

    return solution


def solve(problem: Problem) -> Solution:
    n_lights = number_of_lights(problem)
    solution_vector = np.random.randint(0, high=10, size=n_lights)
    solution_vector_int = np.rint(solution_vector).astype('int')
    return array_to_sol(solution_vector_int, problem)

