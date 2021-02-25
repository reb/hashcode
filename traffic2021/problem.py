from typing import List, Dict


class Street:
    def __init__(self, begin: int, end: int, name: str, length: int):
        self.begin = begin
        self.end = end
        self.name = name
        self.length = length


class Vehicle:
    def __init__(self, streets: List[str]):
        self.streets = streets


class Intersection:
    def __init__(self, _id: int):
        self.id = _id
        self.streets = []

    def add_street(self, street_name: str):
        self.streets.append(street_name)


class Problem:
    def __init__(
        self,
        duration: int,
        amount_of_intersections: int,
        bonus: int,
        streets: Dict[str, Street],
        vehicles: List[Vehicle],
    ):
        self.duration = duration
        self.bonus = bonus
        self.streets = streets
        self.vehicles = vehicles

        self.intersections = [Intersection(i) for i in range(amount_of_intersections)]

        for street in streets.values():
            self.intersections[street.end].add_street(street.name)


class GreenLight:
    def __init__(self, street_name: str, duration: int):
        self.street_name = street_name
        self.duration = duration


class IntersectionSchedule:
    def __init__(self, _id: int):
        self.id = _id
        self.light_schedule = []

    def set_street_schedule(self, light_schedule: List[GreenLight]):
        self.light_schedule = light_schedule


class Solution:
    def __init__(self, problem: Problem):
        self.schedule = [
            IntersectionSchedule(intersection.id)
            for intersection in problem.intersections
        ]


def array_to_sol(vec, problem: Problem) -> Solution:
    solution = Solution(problem)
    index = 0
    for intersection in problem.intersections:
        street_schedule = []
        for street_name in intersection.streets:
            street_schedule.append(GreenLight(street_name, vec[index]))
            index = index + 1
        solution.schedule[intersection.id].set_street_schedule(street_schedule)
    return solution


def number_of_lights(problem):
    n = 1
    for i in range(problem.amount_of_intersections):
        n = n * len(problem.intersections(i).streets)
    return n


def read(text: str) -> Problem:
    lines = text.split("\n")
    [d, i, s, _, f] = [int(i) for i in lines[0].split()]

    # streets
    streets = {}
    for line in lines[1 : 1 + s]:
        [b, e, name, l] = line.split()
        streets[name] = Street(int(b), int(e), name, int(l))

    # vehicles
    vehicles = []
    for line in lines[1 + s :]:
        vehicles.append(Vehicle(line.split()[1:]))

    return Problem(d, i, f, streets, vehicles)


def write(solution: Solution) -> str:
    output_lines = [f"{len(solution.schedule)}"]

    for intersection_schedule in solution.schedule:
        output_lines.append(f"{intersection_schedule.id}")
        output_lines.append(f"{len(intersection_schedule.light_schedule)}")
        for green_light in intersection_schedule.light_schedule:
            output_lines.append(f"{green_light.street_name} {green_light.duration}")

    return "\n".join(output_lines)
