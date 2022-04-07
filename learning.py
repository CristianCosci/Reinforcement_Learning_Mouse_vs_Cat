import pygame
import time
import sys
import numpy as np
import matplotlib.pyplot as plt

from Agent import Agent
from Environment import Env, Matrix

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
pct_obstacles = 0.07
cat_mode = 'knowCheese'
map = Matrix(rows=10, columns=10, max_pct_obstacles=pct_obstacles)
env = Env(display, map, cat_mode)
mouse = Agent(env, possibleActions=4, alpha = 0.1, gamma = 0.85)
cat = Agent(env, possibleActions=4, alpha = 0.1, gamma = 0.85)


# Qlearning params
epsilon, eps_decay, eps_min = 1.0, 0.99995, 0.05

# Train epoch
num_episodes = 80000

# Stas for plot
info_plot = True
total_rewards_mouse = np.zeros(num_episodes)
total_rewards_cat = np.zeros(num_episodes)
total_toccateMuro_mouse = np.zeros(num_episodes)
total_toccateMuro_cat = np.zeros(num_episodes)
total_toccate_ostacolo_mouse = np.zeros(num_episodes)
total_toccate_ostacolo_cat = np.zeros(num_episodes)
total_mouse_caught = np.zeros(num_episodes)
total_cheese_eaten = np.zeros(num_episodes)

mouse_caught = 0
cheese_eaten = 0

# Learning effettivo
for i_episode in range(1, num_episodes+1):
    env.set_obstacles(env.load_obstacles(map.OBSTACLES,pct_obstacles)) # Load different obstacles at each epoch
    if i_episode % 100 == 0:
        print("\rEpisode {}/{}".format(i_episode, num_episodes), end="")
        print()
        #print("Muri toccati: {},    Ostacoli toccati: {}".format(toccatemuro,toccate_ostacolo))
        #toccatemuro = 0
        sys.stdout.flush()
    
    epsilon = max(epsilon*eps_decay, eps_min)

    state = env.reset()
    action_mouse = mouse.get_action(state['mouse'], epsilon)
    action_cat = cat.get_action(state['cat'], epsilon)

    ep_rewards_mouse = 0
    ep_rewards_cat = 0
    ep_toccateMuro_mouse = 0
    ep_toccateMuro_cat = 0
    ep_toccate_ostacolo_mouse = 0
    ep_toccate_ostacolo_cat = 0

    # Render the environment        
    env.render(i_episode)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        next_state, reward, done, info, toccate_muro_mouse, toccate_muro_cat, toccate_ostacolo_mouse, toccate_ostacolo_cat  = env.step(action_mouse, action_cat)

        ep_rewards_mouse += reward['mouse']
        ep_rewards_cat += reward['cat']
        ep_toccateMuro_mouse += toccate_muro_mouse
        ep_toccateMuro_cat += toccate_muro_cat
        ep_toccate_ostacolo_mouse += toccate_ostacolo_mouse
        ep_toccate_ostacolo_cat += toccate_ostacolo_cat

        mouse.Q_learn(state['mouse'], action_mouse, reward['mouse'], next_state['mouse'])
        cat.Q_learn(state['cat'], action_cat, reward['cat'], next_state['cat'])

        # Render the environment
        display.fill(WHITE)         
        env.render(i_episode)
        show_stats(cheese_eaten, mouse_caught)

        pygame.display.update()
        clock.tick(99999999999999)

        if done:
            if info['cheese_eaten']:
                cheese_eaten += 1
                draw_stats_pannel(GREEN, info['x'], info['y'], info['width'], info['height'])       
            
            if info['mouse_caught']:
                mouse_caught += 1
                draw_stats_pannel(RED, info['x'], info['y'], info['width'], info['height'])    
            # Terminazione episodio  
            break
       
        # Update state and action
        state = next_state
        action_mouse = mouse.get_action(state['mouse'], epsilon)
        action_cat = cat.get_action(state['cat'], epsilon)

    total_mouse_caught[i_episode-1] = mouse_caught
    total_cheese_eaten[i_episode-1] = cheese_eaten
    total_rewards_mouse[i_episode-1] = ep_rewards_mouse
    total_rewards_cat[i_episode-1] = ep_rewards_cat
    total_toccateMuro_mouse[i_episode-1] = ep_toccateMuro_mouse
    total_toccateMuro_cat[i_episode-1] = ep_toccateMuro_cat
    total_toccate_ostacolo_mouse[i_episode-1] = ep_toccate_ostacolo_mouse
    total_toccate_ostacolo_cat[i_episode-1] = ep_toccate_ostacolo_cat


dir = 'policies/gattoIntelligente/'
dir += (cat_mode + '/' + 'prova80k/')
# Plot stats
if info_plot:
    plt.plot(total_rewards_mouse)
    plt.title('Reward')
    plt.savefig(dir+'reward_mouse.png')
    plt.show()
    plt.plot(total_rewards_cat)
    plt.title('Reward')
    plt.savefig(dir+'reward_cat.png')
    plt.show()
    plt.plot(total_toccate_ostacolo_mouse)
    plt.savefig(dir+'toccateOstacolo_mouse.png')
    plt.show()
    plt.plot(total_toccate_ostacolo_cat)
    plt.savefig(dir+'toccateOstacolo_cat.png')
    plt.show()
    plt.plot(total_toccateMuro_mouse)
    plt.savefig(dir+'toccateMuro_mouse.png')
    plt.show()
    plt.plot(total_toccateMuro_cat)
    plt.savefig(dir+'toccateMuro_cat.png')
    plt.show()
    plt.title('Mouse vs cat')
    plt.plot(total_mouse_caught, label='topo catturato', color='orange')
    plt.plot(total_cheese_eaten, label='formaggio mangiato', color='green')
    plt.legend()
    plt.savefig(dir+'mouse_vs_cat.png')
    plt.show()

print(mouse_caught)
print(cheese_eaten)

cat.set_policy(saveQtable=True, dir=dir)
mouse.set_policy(saveQtable=True, dir=dir)
# Save the policy
cat.save_policy(dir, 'cat', savePolicytable=True)
mouse.save_policy(dir, 'mouse', savePolicytable=True)