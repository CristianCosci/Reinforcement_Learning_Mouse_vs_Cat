import matplotlib.pyplot as plt
import numpy as np

eps_start = 1.0
eps_min = 0.05
eps_decay = 0.999868
epochs = 30000
pct = 0
stop = 0
df = np.zeros(epochs)
for i in range(epochs):
    if i == 0:
        df[i] = eps_start
    else:
        df[i] = df[i-1] * eps_decay
        if df[i] <= eps_min:
            print(i)
            stop = i
            break

print("With this parameter you will stop epsilon decay after {}% of training".format(stop/epochs*100))
plt.plot(df)
plt.show()