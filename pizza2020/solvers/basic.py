def solve(problem):
    total_slices = 0
    selected_pizzas = []
    pizza_sizes = list(enumerate(problem["pizza_sizes"]))
    while pizza_sizes:
        index, size = pizza_sizes.pop(0)
        if (size + total_slices) > problem["max_slices"]:
            return selected_pizzas
        selected_pizzas.append(index)
        total_slices += size

    return selected_pizzas
