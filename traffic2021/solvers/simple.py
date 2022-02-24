from traffic2021.problem import Problem, Solution, GreenLight, fast_score, score
import time
import logging


logger = logging.getLogger(__name__)


def solve(problem: Problem) -> Solution:
    solution = Solution(problem)

    for intersection in problem.intersections:
        street_schedule = [
            GreenLight(street_name, 1) for street_name in intersection.streets
        ]
        solution.schedule[intersection.id].set_street_schedule(street_schedule)

    tic = time.perf_counter()
    logger.info(f"Score for this solution is: {score(problem, solution)}")
    toc = time.perf_counter()
    logger.info(f"Score took {toc - tic:0.4f} seconds")
    return solution


def solve2(problem: Problem) -> Solution:
    n_lights = number_of_lights(problem)
    solution_vector = np.random.randint(0, high=10, size=n_lights)
    solution_vector_int = np.rint(solution_vector).astype("int")
    return array_to_sol(solution_vector_int, problem)
