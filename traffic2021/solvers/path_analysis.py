from typing import List, Dict
import logging

from traffic2021.problem import (
    Problem,
    Solution,
    Vehicle,
    Intersection,
    fast_score,
    GreenLight,
)

logger = logging.getLogger(__name__)


def solve(problem: Problem) -> Solution:

    # count all street occurences
    street_counts = count_streets(problem.vehicles)

    # try all cycle lengths
    best_solution = None
    best_score = 0
    no_improvement = 0
    for cycle_length in range(1, problem.duration + 1):
        solution = cycle_length_solution(problem, street_counts, cycle_length)
        score = fast_score(problem, solution)
        logger.info(
            "Solution for cycle length: %s has a score of %s", cycle_length, score
        )
        if score > best_score:
            best_score = score
            best_solution = solution
            no_improvement = 0
        else:
            no_improvement += 1
        if no_improvement > (problem.duration / 100):
            logger.info("Found no improvement for 1% of the duration now, stopping")
            break

    return best_solution


def cycle_length_solution(
    problem: Problem, street_counts: Dict[str, int], cycle_length: int
) -> Solution:
    solution = Solution(problem)
    for intersection in problem.intersections:
        intersection_street_counts = []
        for street in intersection.streets:
            intersection_street_counts.append(street_counts.get(street, 0))
        total_street_counts = sum(intersection_street_counts)

        light_schedule = []
        for street, count in zip(intersection.streets, intersection_street_counts):
            if count != 0:
                duration = round(cycle_length / total_street_counts * count)
                if duration != 0:
                    light_schedule.append(GreenLight(street, duration))
        solution.schedule[intersection.id].set_street_schedule(light_schedule)

    return solution


def count_streets(vehicles: List[Vehicle]) -> Dict[str, int]:
    # count all street occurences
    street_counts = {}

    for vehicle in vehicles:
        # do not count the last street
        for street in vehicle.path[:-1]:
            try:
                street_counts[street] += 1
            except KeyError:
                street_counts[street] = 1

    return street_counts
