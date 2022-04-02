import numpy as np
import random

n = 10
possible_obstacles = []
print(type(possible_obstacles))
# Initialize lists
for x in range(n):
    if x == 4:
        pass
    else:
        for y in range(n):
            possible_obstacles.append((x, y))
obstacle_list = list()
print(range(len(possible_obstacles)))
numeri = random.sample(range(len(possible_obstacles)), n)
for i in numeri:
    obstacle_list.append(possible_obstacles[i])
