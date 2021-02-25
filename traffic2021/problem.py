import logging
from typing import List, Dict

logger = logging.getLogger(__name__)


class Street:
    def __init__(self, begin: int, end: int, name: str, length: int):
        self.begin = begin
        self.end = end
        self.name = name
        self.length = length


class Vehicle:
    def __init__(self, path: List[str]):
        self.path = path


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
        self.total_cycle = 0

    def set_street_schedule(self, light_schedule: List[GreenLight]):
        self.light_schedule = light_schedule
        self.total_cycle = sum(l.duration for l in light_schedule)


class Solution:
    def __init__(self, problem: Problem):
        self.schedule = [
            IntersectionSchedule(intersection.id)
            for intersection in problem.intersections
        ]

    def green_light(self, intersection_id: int, street_name: str, t: int) -> bool:
        t = t % self.schedule[intersection_id].total_cycle
        logger.debug("Checking green light for %s at t=%s", street_name, t)

        for green_light in self.schedule[intersection_id].light_schedule:
            if green_light.street_name == street_name and t < green_light.duration:
                return True
            t -= green_light.duration
            if t < 0:
                return False

        return False


class Simulation:
    def __init__(self, problem: Problem, solution: Solution):
        self.t = 0
        self.streets = problem.streets
        self.bonus = problem.bonus
        self.duration = problem.duration
        self.solution = solution

        self.score = 0

        self.paths = [vehicle.path.copy() for vehicle in problem.vehicles]
        self.arriving_at = {0: list(range(len(self.paths)))}
        self.waiting_at_intersection = []
        for intersection in problem.intersections:
            self.waiting_at_intersection.append(
                {street_name: [] for street_name in intersection.streets}
            )

    def do_tick(self):
        # arrive cars at intersection at time t
        logger.debug("Starting tick %s", self.t)
        for vehicle_arriving in self.arriving_at.get(self.t, []):
            if len(self.paths[vehicle_arriving]) == 1:
                self.score += self.bonus + (self.duration - self.t)
                logger.debug("Vehicle completed path!")
                continue

            street_name = self.paths[vehicle_arriving].pop(0)
            logger.debug(
                "Vehicle %s arriving at the end of %s at t=%s",
                vehicle_arriving,
                street_name,
                self.t,
            )
            intersection = self.streets[street_name].end
            self.waiting_at_intersection[intersection][street_name].append(
                vehicle_arriving
            )

        # cross cars that are first at green lights
        for i_id, streets in enumerate(self.waiting_at_intersection):
            for street_name, vehicles in streets.items():
                if vehicles:
                    logger.debug(
                        "Vehicles %s waiting at intersection %s for street %s",
                        vehicles,
                        i_id,
                        street_name,
                    )
                if vehicles and self.solution.green_light(i_id, street_name, self.t):
                    v_id = vehicles.pop(0)
                    logger.debug("Crossing vehicle %s", v_id)

                    t_arrive = self.streets[self.paths[v_id][0]].length + self.t
                    self.arriving_at.setdefault(t_arrive, []).append(v_id)


def score(problem: Problem, solution: Solution):
    simulation = Simulation(problem, solution)

    # main loop
    while simulation.t <= problem.duration:

        simulation.do_tick()

        # update t
        simulation.t += 1

    return simulation.score


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
    n = 0
    for i in range(len(problem.intersections)):
        n = n + len(problem.intersections[i].streets)
    return n


def read(text: str) -> Problem:
    lines = text.split("\n")
    [d, i, s, v, f] = [int(i) for i in lines[0].split()]

    # streets
    streets = {}
    for line in lines[1 : 1 + s]:
        [b, e, name, l] = line.split()
        streets[name] = Street(int(b), int(e), name, int(l))

    # vehicles
    vehicles = []
    for line in lines[1 + s : 1 + s + v]:
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
