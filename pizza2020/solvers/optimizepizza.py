import logging

logger = logging.getLogger("optimizepizza.py")


def binarysearch(intList, n):
    """find largest value in sorted list smaller than n"""

    logger.debug("binarysearch(%s, %s)", intList, n)

    if len(intList) == 1:
        logger.debug("returning intList[0]: %s", intList[0])
        return intList[0]

    midpoint = len(intList) // 2
    if intList[midpoint] == n:
        logger.debug("returning n: %s", n)
        return n
    else:
        if n <= intList[midpoint]:
            logger.debug("going into another recursion with [:midpoint]")
            return binarysearch(intList[:midpoint], n)
        else:
            logger.debug("going into another recursion with [midpoint:]")
            return binarysearch(intList[midpoint:], n)


def partialsumfromlargest(sumList, candidateList, threshold, maxSum):
    """Return the smallest values from the list and the sum of the largest values which surpasses the threshold ratio"""

    logger.debug(
        "partialsumfromlargest(%s, %s, %s, %s)",
        sumList,
        candidateList,
        threshold,
        maxSum,
    )

    if len(candidateList) == 0 or maxSum < candidateList[0]:
        return sumList
    elif maxSum == candidateList[0]:
        sumList.append(candidateList[0])
        return sumList

    largeSumSize = (
        maxSum * threshold
    )  # identify target to reach with large array values only.
    cutoffSize = binarysearch(
        candidateList, int(largeSumSize)
    )  # largest candidate size which is smaller than target.
    cutoffIndex = candidateList.index(cutoffSize)
    numLargeElements = int(largeSumSize / cutoffSize)
    largeElements = candidateList[cutoffIndex : cutoffIndex - numLargeElements : -1]
    sumList.extend(largeElements)
    newSum = maxSum - sum(largeElements)  # new max sum for recursion
    newCandidateList = candidateList[0 : cutoffIndex + 1 - numLargeElements]
    return partialsumfromlargest(sumList, newCandidateList, threshold, newSum)


def solve(problem):
    selected_sizes = partialsumfromlargest(
        [], problem["pizza_sizes"], 0.85, problem["max_slices"]
    )
    logger.info(f"Found a solution with {sum(selected_sizes)} slices")

    return translate(problem["pizza_sizes"], selected_sizes)


def translate(pizza_sizes, selected):
    solution = []
    for i, size in enumerate(pizza_sizes):
        if size in selected:
            solution.append(i)
            selected.remove(size)
    return solution


if __name__ == "__main__":
    M = 100
    pizzaList = [4, 14, 15, 18, 29, 32, 36, 82, 95, 95]
    pizzasoln = partialsumfromlargest([], pizzaList, 0.99, M)
    allsolns = [
        partialsumfromlargest([], pizzaList, 0.6 + j * 0.01, M) for j in range(40)
    ]
