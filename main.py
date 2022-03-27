
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

# Definizione env, griglia e agenti
map = Matrix(rows=10, columns=10)
env = Env(gameDisplay, map)
# Inizializzazione agenti
cat = Agent(env, possibleActions = 4)
mouse = Agent(env, possibleActions = 4)

# Numero di epoche 
num_episodes = 10000

# Load della policy
dir = '/'
mouse.load_policy(dir+'mouse.pickle')
cat.load_policy(dir+'cat.pickle')

# Statistiche
total_mouse_caught = 0
total_cheese_eaten = 0
total_toccatemuro_mouse = 0
total_toccatemuro_cat = 0
total_roccateostacolo_mouse = 0
total_roccateostacolo_cat = 0

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

        next_state, reward, done, info, toccate_muro_mouse, toccate_muro_cat, toccate_ostacolo_mouse, toccate_ostacolo_cat = env.step(action_mouse, action_cat)
        
        total_toccatemuro_mouse += toccate_muro_mouse
        total_toccatemuro_cat += toccate_muro_cat
        total_roccateostacolo_mouse += toccate_ostacolo_mouse
        total_roccateostacolo_cat += toccate_ostacolo_cat

        # Render dell'environment
        gameDisplay.fill(WHITE)         
        env.render(i_episode)
        show_info(total_cheese_eaten, total_mouse_caught)

        # Updating the display
        pygame.display.update()
        clock.tick(999999999)
        
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
       
        
print('muro topo: ', total_toccatemuro_mouse)
print('ostacolo topo: ', total_roccateostacolo_mouse)
print('muro gatto: ', total_toccatemuro_cat)
print('ostacolo gatto: ', total_roccateostacolo_cat)
print('topo: ', total_cheese_eaten)
print('gatto: ', total_mouse_caught)
time.sleep(2)
pygame.quit()