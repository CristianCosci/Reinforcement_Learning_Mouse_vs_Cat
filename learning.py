import pygame
import time
import sys

from Agent import Agent
from Environment import Env, Matrix
from cat import Cat
from mouse import Mouse

#colours
ORANGE = (255, 165, 0)
GREEN = (0, 150, 0)
WHITE = (255,255,255)
RED = (255, 0, 0)
BLACK = (0,0,0)

displayWidth = 800
displayHeight = 900

pygame.init()
pygame.display.set_caption('Tom & Jerry AI Agents')
display = pygame.display.set_mode((displayWidth, displayHeight))
clock = pygame.time.Clock()

map = Matrix(rows=10, columns=10)
env = Env(display, map)

cat = Agent(env, possibleActions=4, alpha = 0.1)
mouse = Agent(env, possibleActions=4, alpha = 0.1)

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
    time.sleep(2)

total_mouse_caught = 0
total_cheese_eaten = 0

epsilon, eps_decay, eps_min = 1.0, 0.99, 0.05
#number of episodes to train
num_episodes = 5

for i_episode in range(1, num_episodes+1):
    if i_episode % 100 == 0:
        print("\rEpisode {}/{}".format(i_episode, num_episodes), end="")
        sys.stdout.flush()
    
    epsilon = max(epsilon*eps_decay, eps_min)

    state = env.reset()
    action_mouse = mouse.get_action(state['mouse'], epsilon)
    action_cat = cat.get_action(state['cat'], epsilon)

    #render the environment         
    env.render(i_episode)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        next_state, reward, done, info = env.step(action_mouse, action_cat)

        mouse.Q_learn(state['mouse'], action_mouse, reward['mouse'], next_state['mouse'])
        cat.Q_learn(state['cat'], action_cat, reward['cat'], next_state['cat'])

        #render the environment
        display.fill(WHITE)         
        env.render(i_episode)
        show_stats(total_cheese_eaten, total_mouse_caught)

        pygame.display.update()
        clock.tick(60)

        if done:
            if info['cheese_eaten']:
                total_cheese_eaten += 1
                draw_stats_pannel(GREEN, info['x'], info['y'], info['width'], info['height'])       
            
            if info['mouse_caught']:
                total_mouse_caught += 1
                draw_stats_pannel(RED, info['x'], info['y'], info['width'], info['height'])    
            #finish this episode    
            break
       
        #update state and action
        state = next_state
        action_mouse = mouse.get_action(state['mouse'], epsilon)
        action_cat = cat.get_action(state['cat'], epsilon)
    
cat.set_policy()
mouse.set_policy()

#to save the policy
cat.save_policy('cat_prova')
mouse.save_policy('mouse_prova')