import numpy as np
import random

n = 10
possible_obstacles = []
for x in range(n):
    if x == 9 or x == 0:
        pass
    else:
        for y in range(n):
            possible_obstacles.append([x, y])

possible_cheese_positions = [4,4], [4,5], [5,4], [5,5]
possible_obstacles_new = possible_obstacles.copy()
for obs in possible_obstacles:
    if obs in possible_cheese_positions:
        possible_obstacles_new.remove(obs)
    
#print(possible_obstacles)
#print(tuple(possible_obstacles_new))

if [4,4][0] == (4,4)[0]:
    print('ok')