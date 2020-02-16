
def binarysearch(intList, n):
    """find largest value in sorted list smaller than n"""

    if len(intList) == 1:
        return intList[0]

    midpoint = len(intList) // 2
    if intList[midpoint] == n:
        return n
    else:
        if n <= intList[midpoint]:
            return binarysearch(intList[:midpoint], n)
        else:
            return binarysearch(intList[midpoint:], n)


def partialsumfromlargest(sumList, candidateList, threshold, maxSum):
    """Return the smallest values from the list and the sum of the largest values which surpasses the threshold ratio"""

    if len(candidateList) == 0 or maxSum < candidateList[0]:
        return sumList
    elif maxSum == candidateList[0]:
        sumList.append(candidateList[0])
        return sumList

    largeSumSize = maxSum*threshold  # identify target to reach with large array values only.
    cutoffSize = binarysearch(candidateList, int(largeSumSize))  # largest candidate size which is smaller than target.
    cutoffIndex = candidateList.index(cutoffSize)
    numLargeElements = int(largeSumSize/cutoffSize)
    largeElements = candidateList[cutoffIndex:cutoffIndex - numLargeElements:-1]
    sumList.extend(largeElements)
    newSum = maxSum - sum(largeElements)  # new max sum for recursion
    newCandidateList = candidateList[0:cutoffIndex + 1 - numLargeElements]
    return partialsumfromlargest(sumList, newCandidateList, threshold, newSum)


def solve(problem):
    selected_sizes = partialsumfromlargest([], problem["pizza_sizes"], 0.85, problem["max_slices"])

    return [problem["pizza_sizes"].index(size) for size in selected_sizes]


if __name__ == "__main__":
    M = 100
    pizzaList = [4, 14, 15, 18, 29, 32, 36, 82, 95, 95]
    pizzasoln = partialsumfromlargest([], pizzaList, .99, M)
    allsolns = [partialsumfromlargest([], pizzaList, 0.6 + j*0.01, M) for j in range(40)]