import numpy as np
import random

#l = [(np.random.randint(0, 50), np.random.randint) for i in range(10)]
#print(l)

l = ((random.randrange(0, 50), random.randrange(0, 20)) for i in range(10))
print(type(l))

l = [3,3], [4,4], [4,2]#[3,0], [3,3], [3,6], [3,9], [5,1], [5,4], [5,7]
print(type(l))


N = 5
  
# initializing Tuple element range 
R = 10
res = [divmod(ele, R + 1) for ele in random.sample(range((R + 1) * (R + 1)), N)]
res = tuple(res)
print(type(res))

print(res)
print(l)

for obs in res:
    print(obs[1])

print(int(100 / 100 * 0.75 * 100))