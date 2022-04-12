
#-------------------------Run this to test the agents----------------------------------------------#
import pygame
import numpy as np
import time

from Agent import Agent
from Environment import Env, Matrix 

# Colors
ORANGE = (255, 165, 0)
GREEN = (0, 150, 0)
WHITE = (255,255,255)
RED = (255, 0, 0)
BLACK = (0,0,0)

def show_info(cheese, mouse):
    pygame.draw.rect(gameDisplay, BLACK, [0, 800, 800, 5])
    font = pygame.font.SysFont(None, 40)
    text1 = font.render("Total Cheese Eaten: "+str(cheese), True, GREEN)
    text2 = font.render("Total Mouse Caught: "+str(mouse), True, RED)
    
    gameDisplay.blit(text1,(50,810))
    gameDisplay.blit(text2,(50,855))	

def draw_rect(color, x, y, width, height):
    pygame.draw.rect(gameDisplay, color, [x*width, y*height, width, height], 10)
    pygame.display.update()
    time.sleep(0)

#-------------------------------------------------------------------------------------------------------------------------------------------------#
# Pygame
display_width, display_height = 800, 900
pygame.init()
pygame.display.set_caption('Tom & Jerry AI Agents')
gameDisplay = pygame.display.set_mode((display_width,display_height))
clock = pygame.time.Clock()

# env, grid e agent definition
gestione_loop = 'break' # break, none, randomize -> It is used to speed the test phase:
                                                        # If is in 'none' there is no control on stalmate and the agent loop over 100 steps also if there is a stalmate
                                                        # If is 'randomize' at each stalmate situation the agent take a random choose on action to exectute
                                                        # If is 'break' when agent enter stalmate the episode will break
                                                        # The stalmate situation is probably caused because the agent prefer to do stalmate instead of losing the game
                                                        # Only when also cat is an intelligent aget because his action are intelligent
cat_mode = 'knowCheese'
map_mode = 'walls'
if map_mode == 'walls':
    pct_obstacles = 0.04
else:
    pct_obstacles = 0.07               
map = Matrix(rows=10, columns=10, max_pct_obstacles=pct_obstacles)
env = Env(gameDisplay, map, cat_mode, map_mode)
cat = Agent(env, possibleActions = 4)
mouse = Agent(env, possibleActions = 4)

# Numero di epoche 
num_episodes = 10000

# Load the policies
dir = 'policies/gattoIntelligente/'
dir += (cat_mode + '/')
mouse.load_policy(dir+'mouse.pickle')
cat.load_policy(dir+'cat.pickle')

# Stats
total_mouse_caught = 0
total_cheese_eaten = 0
total_toccatemuro_mouse = 0
total_toccatemuro_cat = 0
total_roccateostacolo_mouse = 0
total_roccateostacolo_cat = 0

# loop over episodes
for i_episode in range(1, num_episodes+1):
    env.set_obstacles(env.load_obstacles(map.OBSTACLES,pct_obstacles)) # Load different obstacles at each epoch
    state = env.reset()

    loop = False
    if gestione_loop == 'break' or gestione_loop == 'randomize':
        old_state = state.copy()
        check_loop = 0

    action_mouse = mouse.take_action(state['mouse'])
    action_cat = cat.take_action(state['cat'])
    
    # Render the environment
    env.render(i_episode)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()   # Close window
                quit() 

        next_state, reward, done, info, toccate_muro_mouse, toccate_muro_cat, toccate_ostacolo_mouse, toccate_ostacolo_cat = env.step(action_mouse, action_cat)
        
        total_toccatemuro_mouse += toccate_muro_mouse
        total_toccatemuro_cat += toccate_muro_cat
        total_roccateostacolo_mouse += toccate_ostacolo_mouse
        total_roccateostacolo_cat += toccate_ostacolo_cat

        # Render the environment
        gameDisplay.fill(WHITE)         
        env.render(i_episode)
        show_info(total_cheese_eaten, total_mouse_caught)

        # Updating the display
        pygame.display.update()
        clock.tick(9999999999999999999999999)
        
        if done:
            if info['cheese_eaten']:
                total_cheese_eaten += 1
                draw_rect(GREEN, info['x'], info['y'], info['width'], info['height'])       
            
            if info['mouse_caught']:
                total_mouse_caught += 1
                draw_rect(RED, info['x'], info['y'], info['width'], info['height'])  
            break
        
        # Update state and action
        state = next_state
        if loop:
            action_mouse = np.random.randint(0, 5)
            action_cat = np.random.randint(0, 5)
            loop = False
        else:
            action_mouse = mouse.take_action(state['mouse'])
            action_cat = cat.take_action(state['cat'])

        
        # Check if the two agents are in a stalemate
        if gestione_loop == 'break' or gestione_loop == 'randomize':
            if old_state == next_state:
                #print('Loop')
                if gestione_loop == 'break':
                    break
                elif gestione_loop == 'randomize':
                    loop = True
            else:
                if check_loop == 1:
                    old_state = state.copy()
                    check_loop = 0
                else:
                    check_loop = 1
        

print('muro topo: ', total_toccatemuro_mouse)
print('ostacolo topo: ', total_roccateostacolo_mouse)
print('muro gatto: ', total_toccatemuro_cat)
print('ostacolo gatto: ', total_roccateostacolo_cat)
print('topo: ', total_cheese_eaten)
print('gatto: ', total_mouse_caught)
time.sleep(2)
pygame.quit()