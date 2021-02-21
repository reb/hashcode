from typing import List, Set


class Pizza:
    def __init__(self, id: int, ingredients: Set[str]):
        self.id = id
        self.ingredient = ingredients


class Problem:
    def __init__(
        self, pizzas: List[Set[str]], t2: object, t3: object, t4: object,
    ):
        self.pizzas = [Pizza(i, ingredients) for i, ingredients in enumerate(pizzas)]
        self.t2 = t2
        self.t3 = t3
        self.t4 = t4


class Solution:
    def __init__(self):
        self.deliveries = {}

    def add_delivery(self, team_size: int, pizzas: List[int]):
        self.deliveries[team_size] = pizzas


def read(text: str) -> Problem:
    lines = text.split("\n")
    teams = [int(i) for i in lines[0].split()][1:]
    pizzas = [set(p.split()[1:]) for p in lines[1:]]
    return Problem(pizzas, *teams)


def write(solution: Solution) -> str:
    """
    Write out the deliveries

    Format: {team_size: [pizza_id, ...]}
    """

    output_lines = [f"{len(solution.deliveries)}"]
    for team_size, pizzas in solution.deliveries.items():
        output_lines.append(f"{team_size} {' '.join(str(p) for p in pizzas)}")
    return "\n".join((output_lines))
