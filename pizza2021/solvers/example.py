from pizza2021.problem import Solution, Problem


def solve(problem: Problem) -> Solution:
    solution = Solution()

    pizzas = problem.pizzas
    for team_size in (2, 3, 4):
        if len(pizzas) > team_size:
            solution.add_delivery(team_size, [p.id for p in pizzas[:team_size]])
            pizzas = pizzas[team_size:]

    return solution
