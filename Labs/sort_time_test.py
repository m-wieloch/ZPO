# <Maciej> <Wieloch>, <303080>

import sort
import random
from timeit import timeit

lst_sorted = []
lst_reversed = []
lst_equal = []
lst_random = random.sample(range(0, 1000), 1000)

for i in range(0, 1000):
    lst_sorted.append(i)
for i in reversed(range(0, 1000)):
    lst_reversed.append(i)
for i in range(0, 1000):
    lst_equal.append(6)

t1_bubble = timeit("sort.bubblesort(lst_sorted)", number=1000, globals=globals())
t2_bubble = timeit("sort.bubblesort(lst_reversed)", number=1000, globals=globals())
t3_bubble = timeit("sort.bubblesort(lst_equal)", number=1000, globals=globals())
t4_bubble = timeit("sort.bubblesort(lst_random)", number=1000, globals=globals())

t1_qs = timeit("sort.quicksort(lst_sorted)", number=1000, globals=globals())
t2_qs = timeit("sort.quicksort(lst_reversed)", number=1000, globals=globals())
t3_qs = timeit("sort.quicksort(lst_equal)", number=1000, globals=globals())
t4_qs = timeit("sort.quicksort(lst_random)", number=1000, globals=globals())
