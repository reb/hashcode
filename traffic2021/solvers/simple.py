from traffic2021.problem import Problem, Solution, GreenLight


def solve(problem: Problem) -> Solution:
    solution = Solution(problem)

    for intersection in problem.intersections:
        street_schedule = [
            GreenLight(street_name, 1) for street_name in intersection.streets
        ]
        solution.schedule[intersection.id].set_street_schedule(street_schedule)

    return solution
