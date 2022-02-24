from cmath import inf


WIDTH = 9
HEIGHT = 9

MOUSE_Y = 5
MOUSE_X = 5

distanza_X = inf
if WIDTH - MOUSE_X < MOUSE_X:
    distanza_X = WIDTH - MOUSE_X
else:
    distanza_X = MOUSE_X

distanza_Y = inf
if HEIGHT - MOUSE_Y < MOUSE_Y:
    distanza_Y = HEIGHT - MOUSE_Y
else:
    distanza_Y = MOUSE_Y

print(min(distanza_X, distanza_Y))