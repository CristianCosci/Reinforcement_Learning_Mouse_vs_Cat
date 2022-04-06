import pygame
import time
import sys
import numpy as np
import matplotlib.pyplot as plt

from Agent_GattoSentinella import Agent
from Environment_GattoSentinella import Env, Matrix

#colours
ORANGE = (255, 165, 0)
GREEN = (0, 150, 0)
WHITE = (255,255,255)
RED = (255, 0, 0)
BLACK = (0,0,0)

def show_stats(cheese_eaten, mouse_caugth):
    pygame.draw.rect(display, BLACK, [0, 800, 800, 5])
    font = pygame.font.SysFont(None, 40)
    text1 = font.render('Totale formaggio mangiato: '+str(cheese_eaten), True, GREEN)
    text2 = font.render('Totale topo catturato: '+str(mouse_caugth), True, RED)
    display.blit(text1,(50, 810))
    display.blit(text2,(50, 855))

def draw_stats_pannel(color, x, y, width, height):
    pygame.draw.rect(display, color, [x * width, y * height, width, height], 10)
    pygame.display.update()
    #time.sleep(2)

#-------------------------------------------------------------------------------------------------------------------------------------------------#
# Pygame
displayWidth = 800
displayHeight = 900
pygame.init()
pygame.display.set_caption('Tom & Jerry AI Agents')
display = pygame.display.set_mode((displayWidth, displayHeight))
clock = pygame.time.Clock()

# env, grid and agent definitions
pct_obstacles = 0.04
cat2_mode = 'misto'
map = Matrix(rows=10, columns=10, max_pct_obstacles=pct_obstacles, cat2_mode=cat2_mode)
env = Env(display, map, cat2_mode)
mouse = Agent(env, possibleActions=4, alpha = 0.1, gamma = 0.85)

# Parametri di Qlearning
epsilon, eps_decay, eps_min = 1.0, 0.9999, 0.05

# Train epoch
num_episodes = 40000

# Stas for plot
info_plot = True
total_rewards = np.zeros(num_episodes)
total_toccateMuro = np.zeros(num_episodes)
total_toccate_ostacolo = np.zeros(num_episodes)
total_mouse_caught = np.zeros(num_episodes)
total_cheese_eaten = np.zeros(num_episodes)

mouse_caught = 0
cheese_eaten = 0

# Learning
for i_episode in range(1, num_episodes+1):
    env.set_obstacles(env.load_obstacles(map.OBSTACLES,pct_obstacles)) # Load different obstacles at each epoch
    if i_episode % 100 == 0:
        print("\rEpisode {}/{}".format(i_episode, num_episodes), end="")
        print()
        sys.stdout.flush()
    
    epsilon = max(epsilon*eps_decay, eps_min)

    state = env.reset()
    action_mouse = mouse.get_action(state['mouse'], epsilon)

    # Gatto sentinella doppio
    cat1_direction = 2
    if cat2_mode == 'verticale':
        cat2_direction = 2
    elif cat2_mode == 'misto':
        cat2_direction = 0

    ep_rewards = 0
    ep_toccateMuro = 0
    ep_toccate_ostacolo = 0

    #render the environment         
    env.render(i_episode)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()


        next_state, reward, done, info, cat1_direction, cat2_direction, toccate_muro, toccate_ostacolo = env.step(action_mouse, cat1_direction, cat2_direction)

        ep_rewards += reward['mouse']
        ep_toccateMuro += toccate_muro
        ep_toccate_ostacolo += toccate_ostacolo
        
        mouse.Q_learn(state['mouse'], action_mouse, reward['mouse'], next_state['mouse'])

        # Render the environment
        display.fill(WHITE)         
        env.render(i_episode)
        show_stats(cheese_eaten, mouse_caught)

        pygame.display.update()
        clock.tick(99999999999999999999)

        if done:
            if info['cheese_eaten']:
                cheese_eaten += 1
                draw_stats_pannel(GREEN, info['x'], info['y'], info['width'], info['height'])       
            
            if info['mouse_caught']:
                mouse_caught += 1
                draw_stats_pannel(RED, info['x'], info['y'], info['width'], info['height'])    
            # Episode termination
            break
       
        # Update state and action
        state = next_state
        action_mouse = mouse.get_action(state['mouse'], epsilon)
    
    total_mouse_caught[i_episode-1] = mouse_caught
    total_cheese_eaten[i_episode-1] = cheese_eaten
    total_rewards[i_episode-1] = ep_rewards
    total_toccateMuro[i_episode-1] = ep_toccateMuro
    total_toccate_ostacolo[i_episode-1] = ep_toccate_ostacolo


dir = 'policies/gattoSentinella/gattoDoppio/'
dir += (cat2_mode + '/')
# Plot stats
if info_plot:
    plt.plot(total_rewards)
    plt.title('Reward')
    plt.savefig(dir+'reward.png')
    plt.show()
    plt.plot(total_toccate_ostacolo)
    plt.savefig(dir+'toccateOstacolo.png')
    plt.show()
    plt.plot(total_toccateMuro)
    plt.savefig(dir+'toccateMuro.png')
    plt.show()
    plt.title('Mouse vs cat')
    plt.plot(total_mouse_caught, label='topo catturato', color='orange')
    plt.plot(total_cheese_eaten, label='formaggio mangiato', color='green')
    plt.legend()
    plt.savefig(dir+'mouse_vs_cat.png')
    plt.show()

print(mouse_caught)
print(cheese_eaten)

mouse.set_policy(saveQtable=True, dir=dir)
# Save the policy
mouse.save_policy(dir, 'mouse', savePolicytable=True)