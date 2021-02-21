import logging

logger = logging.getLogger("slightly_smarter.py")


def solve(problem):
    target = 0.95 * problem["max_slices"]
    selected_pizzas, slices_taken, pizza_sizes = sub_solve(problem, target)
    logger.debug(f"Solved with {slices_taken} slices taken.")
    return selected_pizzas


def sub_solve(problem, target):
    total_slices = 0
    selected_pizzas = []
    pizza_sizes = list(enumerate(problem["pizza_sizes"]))
    while pizza_sizes:
        index, size = pizza_sizes.pop(-1)
        if (size + total_slices) > target:
            return selected_pizzas, total_slices, pizza_sizes
        selected_pizzas.append(index)
        total_slices += size
    return selected_pizzas, total_slices, pizza_sizes
