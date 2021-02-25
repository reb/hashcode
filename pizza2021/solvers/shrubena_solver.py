from pizza2021.problem import Solution, Problem, read
import numpy as np

problem_data = '''5 1 2 1
3 onion pepper olive
3 mushroom tomato basil
3 chicken mushroom pepper
3 tomato mushroom basil
2 chicken basil
'''
problem = read(problem_data)
pizzas = [pizza.ingredient for pizza in problem.pizzas]

# make a random symmetric matrix to test
N = len(pizzas)
A = np.random.randint(0, 100, size=(N, N))
pizza_compatibility_array = A + A.T
for j in range(N):
    pizza_compatibility_array[j, j] = 0


def best_pair(pizzas, pizza_compatibility_array, index_mask):
    """Find the best two team pizza"""
    available_pizzas = pizza_compatibility_array
    max_idx = np.where(pizza_compatibility_array[np.ix_(index_mask, index_mask)] == np.max(pizza_compatibility_array[
        np.ix_(index_mask, index_mask)]))  # find entries which are maximal
    best_pair_candidates = [(i, j) for (i, j) in list(zip(*max_idx)) if i < j]
    pair_scores = [score_pizza(pizzas[i], pizzas[j]) for (i, j) in best_pair_candidates]
    best_score = np.max(pair_scores)
    best_pair_idx = np.where(pair_scores == best_score)[0][0]
    return best_pair_candidates[best_pair_idx], best_score


def score_pizza(*pizzas):
    """Return a score for a delivery consisting of these pizzas"""
    return len(set.union(*pizzas)) ** 2


bp = best_pair(pizzas, pizza_compatibility_array, tuple(range(N)))
print(bp)


def best_triple(pizza, pizza_compatibility_array, available_pizzas):
    best_two_pizzas_all = best_pair(pizzas, pizza_compatibility_array)
    # best_two_pizzas has format (array([2], dtype=int32), array([0], dtype=int32))
    best_two_pizzas = np.sort(best_two_pizzas_all[0])
    two_pizzas_index = np.array([available_pizzas[best_two_pizzas[0]], available_pizzas[best_two_pizzas[1]]])
    available_pizzas = np.delete(available_pizzas, best_two_pizzas[1])
    available_pizzas = np.delete(available_pizzas, best_two_pizzas[0])
    fitness_row_pizza = pizza_compatibility_array[best_two_pizzas[1], available_pizzas]
    fitness_column_pizza = pizza_compatibility_array[available_pizzas, best_two_pizzas[0]]
    yummy_pizza = np.multiply(fitness_row_pizza, fitness_column_pizza)
    # best_third_pizza_position = np.where(yummy_pizza == np.amax(yummy_pizza))
    best_third_pizza_position = np.unravel_index(np.argmax(yummy_pizza, axis=None), yummy_pizza.shape)
    best_third_pizza = best_third_pizza_position[0]
    index_third_pizza = np.array([available_pizzas[best_third_pizza]])
    three_pizzas = np.concatenate((two_pizzas_index, index_third_pizza))
    score = score_pizza(pizzas[three_pizzas[0]], pizzas[three_pizzas[1]], pizzas[three_pizzas[2]])
    return three_pizzas, score


mask_array = np.array(range(pizza_compatibility_array.shape[0]))
bt = best_triple(pizzas, pizza_compatibility_array, mask_array)
print(bt)