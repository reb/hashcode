def read(text):
    lines = text.split("\n")
    [_, T2, T3, T4] = [int(i) for i in lines[0].split()]
    pizzas = [p.split()[1:] for p in lines[1:]]
    return {"T2": T2, "T3": T3, "T4": T4, "pizzas": pizzas}


def write(deliveries):
    """
    Write out the deliveries
    
    Format: {team_size: [pizza_id, ...]}
    """

    output_lines = f"{len(deliveries)}"
    for team_size, pizzas in deliveries.items():
        output_lines.append(f"{team_size} {' '.join(pizzas)}")
    return "\n".join((output_lines))
