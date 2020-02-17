import logging
import sys

logger = logging.getLogger("dynamic.py")

cache = {}


def solve(problem):
    sys.setrecursionlimit(10**6)
    selected_sizes, _ = best_selection(problem["pizza_sizes"], problem["max_slices"])
    logger.info(f"Found a solution with {sum(selected_sizes)} slices")
    return translate(problem["pizza_sizes"], selected_sizes)


def translate(pizza_sizes, selected):
    solution = []
    for i, size in enumerate(pizza_sizes):
        if size in selected:
            solution.append(i)
            selected.remove(size)
    return solution


def best_selection(possible_sizes, allowed):
    """Find the best possible selection given a max amount"""
    logger.debug("best_solution(%s, %s)", possible_sizes, allowed)

    if len(possible_sizes) == 0:
        logger.debug("No sizes to pick from")
        return [], allowed


    # ignoring the biggest size
    logger.debug("Grabbing best without the biggest")
    without_selection, without_allowed = best_selection(
        possible_sizes[:-1], allowed
    )

    biggest_size = possible_sizes[-1]

    # return already if the biggest_size doesn't fit into the allowed_size
    if allowed < biggest_size:
        logger.debug("Selecting without %s, because only %s is allowed", biggest_size, allowed)
        cache[(len(possible_sizes), allowed)] = (
            without_selection,
            without_allowed,
        )
        return without_selection, without_allowed

    logger.debug("Grabbing best with the biggest selected")
    with_selection, with_allowed = best_selection(
        possible_sizes[:-1], allowed - biggest_size
    )
    with_selection += [biggest_size]
    with_allowed -= biggest_size

    if sum(without_selection) > sum(with_selection):
        logger.debug("Selecting without %s, because the without amount is better", biggest_size)
        cache[(len(possible_sizes), allowed)] = (
            without_selection,
            without_allowed,
        )
        return without_selection, without_allowed
    else:
        logger.debug("Selecting with %s", biggest_size)
        cache[(len(possible_sizes), allowed)] = (with_selection, with_allowed)
        return with_selection, with_allowed
