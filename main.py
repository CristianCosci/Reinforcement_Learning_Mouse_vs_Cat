
#-------------------------Run this to test the agents----------------------------------------------#
import pygame
import pickle
import time
import random
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

display_width, display_height = 800, 900

pygame.init()
pygame.display.set_caption('Grid environment')
gameDisplay = pygame.display.set_mode((display_width,display_height))
clock = pygame.time.Clock()

game_matrix = Matrix(rows=10, columns=10)
env = Env(gameDisplay, game_matrix)

#initialising our agents
cat = Agent(env, possibleActions = 4)
mouse = Agent(env, possibleActions = 4)

#load the policy
'''cat.change_policy('Policies/policy 6/policy_cat_6.pickle')
mouse.change_policy('Policies/policy 6/policy_mouse_6.pickle')'''

#helpful function
def show_info(cheese, mouse):
    pygame.draw.rect(gameDisplay, BLACK, [0, 600, 600, 5])
    font = pygame.font.SysFont(None, 40)
    text1 = font.render("Total Cheese Eaten: "+str(cheese), True, GREEN)
    text2 = font.render("Total Mouse Caught: "+str(mouse), True, RED)
    
    gameDisplay.blit(text1,(50,610))
    gameDisplay.blit(text2,(50,655))	

#indicative rectangle to show cheese eaten or mouse caught
def draw_rect(color, x, y, width, height):
    pygame.draw.rect(gameDisplay, color, [x*width, y*height, width, height], 10)
    pygame.display.update()
    time.sleep(2)

total_mouse_caught = 0
total_cheese_eaten = 0


num_episodes = 5

# loop over episodes
for i_episode in range(1, num_episodes+1):
   
    state = env.reset()
    '''action_mouse = mouse.take_action(state['mouse'])
    action_cat = cat.take_action(state['cat'])'''
    
    #render the environment         
    env.render(i_episode)

    

    while True:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()   #close the window
                quit() 

        #next_state, reward, done, info = env.step(action_mouse, action_cat)
        
        #render the environment
        gameDisplay.fill(WHITE)         
        env.render(i_episode)
        #show_info(total_cheese_eaten, total_mouse_caught)

        #updating the display
        pygame.display.update()
        clock.tick(5)
        
        '''if done:
            if info['cheese_eaten']:
                total_cheese_eaten += 1
                draw_rect(GREEN, info['x'], info['y'], info['width'], info['height'])       
            
            if info['mouse_caught']:
                total_mouse_caught += 1
                draw_rect(RED, info['x'], info['y'], info['width'], info['height'])    
            #finish this episode    
            break'''
       
        #update state and action
        #state = next_state
        #action_mouse = mouse.take_action(state['mouse'])
        #action_cat = cat.take_action(state['cat'])
        
time.sleep(2)
pygame.quit()

        

