# <Maciej> <Wieloch>, <303080>
from typing import List, Tuple


def quicksort(data: List[int]) -> List[int]:

    data_copy = data[:]
    start = 0
    stop = len(data) - 1

    def _quicksort(data_copy: List[int], start: int, stop: int):

        i = start
        j = stop
        pivot = data_copy[int(start + (stop - start) / 2)]

        while i < j:

            if data_copy[i] < pivot:
                i = i + 1

            if data_copy[j] > pivot:
                j = j - 1

            if i <= j:
                data_copy[i], data_copy[j] = data_copy[j], data_copy[i]
                i = i + 1
                j = j - 1

        if start < j:
            _quicksort(data_copy, start, j)

        if i < stop:
            _quicksort(data_copy, i, stop)

        return data_copy

    return _quicksort(data_copy, start, stop)


def bubblesort(data: List[int]) -> Tuple[List[int], int]:

    crossing = 0
    data_copy = data[:]

    for j in range(len(data)):

        for i in range(1, len(data) - j):

            crossing = crossing + 1

            if data_copy[i - 1] > data_copy[i]:
                data_copy[i - 1], data_copy[i] = data_copy[i], data_copy[i - 1]

    return data_copy, crossing


my_list = [2, 25, 9, 14, 1]
print(bubblesort(my_list))