from typing import List, Set, Dict, Tuple


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
    def __init__(self):
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

        self.intersections = []
        for _ in range(amount_of_intersections):
            self.intersections.append(Intersection())

        for street in streets.values():
            self.intersections[street.end].add_street(street.name)


class Solution:
    def __init__(self):

        self.paths = []


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
    output_lines = [f"{0}"]

    return "\n".join((output_lines))
