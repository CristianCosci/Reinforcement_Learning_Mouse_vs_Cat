
#-------------------------Run this to test the agents----------------------------------------------#
import pygame
import time

from Agent import Agent
from Environment import Env, Matrix 

# Definizione colori
ORANGE = (255, 165, 0)
GREEN = (0, 150, 0)
WHITE = (255,255,255)
RED = (255, 0, 0)
BLACK = (0,0,0)

display_width, display_height = 800, 900

pygame.init()
pygame.display.set_caption('Tom & Jerry AI Agents')
gameDisplay = pygame.display.set_mode((display_width,display_height))
clock = pygame.time.Clock()

grid_matrix = Matrix(rows=10, columns=10)
env = Env(gameDisplay, grid_matrix)

# Inizializzazione agenti
cat = Agent(env, possibleActions = 4, alpha=0.1)
mouse = Agent(env, possibleActions = 4, alpha=0.1)

# Load della policy
dir = 'policy_gattoIntelligente/AllRandom/evitaMuri'
mouse.load_policy(dir+'/mouse2.pickle')
cat.load_policy(dir+'/cat2.pickle')

# Funzioni di comodo
def show_info(cheese, mouse):
    pygame.draw.rect(gameDisplay, BLACK, [0, 800, 800, 5])
    font = pygame.font.SysFont(None, 40)
    text1 = font.render("Total Cheese Eaten: "+str(cheese), True, GREEN)
    text2 = font.render("Total Mouse Caught: "+str(mouse), True, RED)
    
    gameDisplay.blit(text1,(50,810))
    gameDisplay.blit(text2,(50,855))	

# Barra delle statistiche
def draw_rect(color, x, y, width, height):
    pygame.draw.rect(gameDisplay, color, [x*width, y*height, width, height], 10)
    pygame.display.update()
    time.sleep(2)

total_mouse_caught = 0
total_cheese_eaten = 0

num_episodes = 100

toccatemuro = 0
toccate_ostacolo = 0

# loop over episodes
for i_episode in range(1, num_episodes+1):
   
    state = env.reset()
    action_mouse = mouse.take_action(state['mouse'])
    action_cat = cat.take_action(state['cat'])
    
    # Render dell'environment
    env.render(i_episode)

    while True:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()   # Close window
                quit() 

        next_state, reward, done, info, toccatemuro, toccate_ostacolo = env.step(action_mouse, action_cat, toccatemuro, toccate_ostacolo)
        
        # Render dell'environment
        gameDisplay.fill(WHITE)         
        env.render(i_episode)
        show_info(total_cheese_eaten, total_mouse_caught)

        # Updating the display
        pygame.display.update()
        clock.tick(12)
        
        if done:
            if info['cheese_eaten']:
                total_cheese_eaten += 1
                draw_rect(GREEN, info['x'], info['y'], info['width'], info['height'])       
            
            if info['mouse_caught']:
                total_mouse_caught += 1
                draw_rect(RED, info['x'], info['y'], info['width'], info['height'])    
            # Terminazione episodio    
            break
       
        # Update state and action
        state = next_state
        action_mouse = mouse.take_action(state['mouse'])
        action_cat = cat.take_action(state['cat'])
       
        
print(toccatemuro)
print(total_cheese_eaten)
print(total_mouse_caught)
time.sleep(2)
pygame.quit()

        

