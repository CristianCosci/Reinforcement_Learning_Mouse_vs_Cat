import numpy as np
possible_obstacles = [3,3], [3,4], [3,5], [3,6], [4,6], [6,6], [6,5], [6,3], [5,3], [4,3], [5,6], [6,4]
obstacle_list = list()
i = 0
numeri = np.random.randint(0, 2, size=len(possible_obstacles))
print(numeri)
for obs in possible_obstacles:
    if numeri[i] == 1:
        obstacle_list.append(obs)
    i+= 1

obstacles = tuple(obstacle_list)