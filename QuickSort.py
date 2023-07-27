# Worst thing about mergesort is because it uses O(n) memory, as you have to make a ton of sublists

# Quicksort:
# Another divide-and-conquer algorithm
# Has running times of O(nlogn) in a typical case
# We'll see how this can also lead to O(n^2) in a worst case scenario
# Idea: We can sort a list by subdividing the list based on a PIVOT value
# Place elements < pivot to left-side of the list
# Place elements > pivot to the right-side of the list
# Recuse for each left/right portion of the list
# When sub list sizes == 1, then the entire list is sorted
# Randomly choose the pivot value unfortunately, could completely fuck us over if we were unlucky
# Choose the first element in the list
# Find an element in the left side using left-mark index
# Starting at the beginning of the list just past hte pivot that will move right
# Find an element in the right side using right=mark index starting at the end of the list moving from right
# to left that's out of place
# Swap out of place elements with each other
# We're just putting them in the correct side of the list
# Continue doing this until the right-mark index < left-mark index

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


