import random


rand_list = [random.randint(0, i) for i in range(0, 20)]

list_comprehension_below_10 = [random.randint(0, i) for i in range(0, 20) if i <= 10]

list_comprehension_below_10 = [i for i in filter(lambda number: number < 10, [random.randint(0, i) for i in range(0, 20)])]
