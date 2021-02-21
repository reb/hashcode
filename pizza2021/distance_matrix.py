import logging
import os
from typing import Callable

import numpy as np

from pizza2021.problem import Problem, Pizza

logger = logging.getLogger("main.py")


def create(
    problem: Problem, distance_function: Callable[[Pizza, Pizza], float]
) -> np.array:
    """Create a new distance matrix"""

    matrix = np.zeros((len(problem.pizzas), len(problem.pizzas)))
    for p1 in problem.pizzas:
        for p2 in problem.pizzas[p1.id + 1 :]:
            matrix[p1.id, p2.id] = distance_function(p1, p2)
    matrix = matrix + matrix.T
    return matrix


def load(problem: Problem, distance_function: Callable[[Pizza, Pizza], float]):
    matrix_file = f"{problem.solver_name}-{problem.input_file_name}.distance_matrix.npy"
    if os.path.isfile(matrix_file):
        return np.load(matrix_file)

    matrix = create(problem, distance_function)
    np.save(matrix_file, matrix)
    return matrix
