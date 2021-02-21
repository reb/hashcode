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


def best_pair(pizzas, pizza_compatibility_array):
    """Find the best two team pizza"""
    max_idx = np.where(pizza_compatibility_array == np.max(pizza_compatibility_array))  # find entries which are maximal
    best_pair_candidates = [(i, j) for (i, j) in list(zip(*max_idx)) if i < j]
    pair_scores = [score_pizza(pizzas[i], pizzas[j]) for (i,j) in best_pair_candidates]
    best_score = np.max(pair_scores)
    best_pair_idx = np.where(pair_scores == best_score)[0][0]
    print(best_pair_idx)
    return best_pair_candidates[best_pair_idx], best_score



def score_pizza(*pizzas):
    """Return a score for a delivery consisting of these pizzas"""
    return len(set.union(*pizzas)) ** 2


bp = best_pair(pizzas, pizza_compatibility_array)
print(bp)


def best_triple(pizza_compatibility_array, available_pizzas):
    best_two_pizzas = np.where(pizza_compatibility_array[available_pizzas, available_pizzas]
                               == np.amax(pizza_compatibility_array[available_pizzas, available_pizzas]))
    # best_two_pizzas has format (array([2], dtype=int32), array([0], dtype=int32))
    fitness_row_pizza = np.average(pizza_compatibility_array[best_two_pizzas[1], available_pizzas])
    fitness_column_pizza = np.average(pizza_compatibility_array[available_pizzas, best_two_pizzas[0]])
    two_pizzas = np.array([available_pizzas[best_two_pizzas[:]]])
    if fitness_row_pizza > fitness_column_pizza:
        yummy_pizza = best_two_pizzas[1]
    else:
        yummy_pizza = best_two_pizzas[0]
    np.delete(available_pizzas, np.where(available_pizzas == best_two_pizzas), 1)
    np.delete(available_pizzas, np.where(available_pizzas == best_two_pizzas), 0)
    best_third_pizza = np.where(pizza_compatibility_array[available_pizzas, yummy_pizza] == np.amax(pizza_compatibility_array[available_pizzas, yummy_pizza]))
    three_pizzas = np.concatenate(two_pizzas, np.array(available_pizzas[best_third_pizza]))
    return three_pizzas
