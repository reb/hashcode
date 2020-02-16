def read(text):
    lines = text.split('\n')
    [max_slices, different_pizzas] = [int(i) for i in lines[0].split(' ')]
    pizza_sizes = [int(size) for size in lines[1].split(' ')]
    return {
        "max_slices": max_slices,
        "different_pizzas": different_pizzas,
        "pizza_sizes": pizza_sizes,
    }


def write(solution):
    amount_of_pizzas = str(len(solution))
    pizzas = " ".join([str(size) for size in solution])
    return "\n".join((amount_of_pizzas, pizzas))
