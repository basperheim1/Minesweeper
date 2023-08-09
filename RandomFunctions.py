import random

def product(args):
    # product('ABCD', 'xy') --> Ax Ay Bx By Cx Cy Dx Dy
    # product(range(2), repeat=3) --> 000 001 010 011 100 101 110 111
    pools = [tuple(pool) for pool in args]
    result = [[]]
    for pool in pools:
        result = [x+[y] for x in result for y in pool]
    for prod in result:
        yield tuple(prod)

def random_sample_with_exclusion(start_range, end_range, exclude_num, sample_size):
    # Create a list of numbers within the specified range, excluding the excluded number
    numbers = [num for num in range(start_range, end_range+1) if num != exclude_num]

    # Randomly sample without replacement from the numbers list
    random_sample = [-1] + quickSort(random.sample(numbers, sample_size))
    return random_sample

def partition(aList, first, last):
    pivotValue = aList[first]

    left_mark = first+1
    right_mark = last

    done = False
    while not done:
        while left_mark <= right_mark and aList[left_mark] >= pivotValue:
            left_mark += 1

        while right_mark >= left_mark and aList[right_mark] <= pivotValue:
            right_mark -= 1

        if right_mark < left_mark:
            done = True
        else:
            temp = aList[left_mark]
            aList[left_mark] = aList[right_mark]
            aList[right_mark] = temp

    temp = aList[first]
    aList[first] = aList[right_mark]
    aList[right_mark] = temp

    return right_mark

def quickSortHelper(aList, first, last):
    if first < last:
        splitpoint = partition(aList, first, last)

        quickSortHelper(aList, first, splitpoint-1)
        quickSortHelper(aList, splitpoint+1, last)


def quickSort(aList):
    quickSortHelper(aList, 0, len(aList)-1)
    return aList

def combinations(iterable, r):
    # combinations('ABCD', 2) --> AB AC AD BC BD CD
    # combinations(range(4), 3) --> 012 013 023 123
    pool = tuple(iterable)
    n = len(pool)
    if r > n:
        return
    indices = list(range(r))
    yield list(pool[i] for i in indices)
    while True:
        for i in reversed(range(r)):
            if indices[i] != i + n - r:
                break
        else:
            return
        indices[i] += 1
        for j in range(i+1, r):
            indices[j] = indices[j-1] + 1
        yield list(pool[i] for i in indices)