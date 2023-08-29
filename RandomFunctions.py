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
    random_sample = (random.sample(numbers, sample_size))
    random_sample.sort(reverse=True)

    # Adds a -1 to the first index so the list never has length 0, and therefore always has a -1th index
    random_sample_w_negative_one = [-1] + random_sample
    return random_sample_w_negative_one


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