

from pizza2021.problem import Solution, Problem
import numpy as np
N = 50
A = np.random.randint(0,100,size=(N, N))
pizza_compatibility_array =  A + A.T
for j in range(N):
    pizza_compatibility_array[j, j] = 0


def score_pizza(*pizzas):
    """Return a score for a delivery consisting of these pizzas"""
    return len(set.union(*pizzas))