import pygame
from cat import Cat
from mouse import Mouse
from Agent import Agent
import numpy as np 


class Matrix:
	def __init__(self, rows=5, columns=5):
		self.ROWS = rows 
		self.COLUMNS = columns
		self.OBSTACLES = [] #[[2,2], [2,7], [7,2], [7,7], [5,5]]
    

    
class Env():
    def __init__(self, display, matrix):
        self.HEIGHT = matrix.ROWS
        self.WIDTH = matrix.COLUMNS

        #setto informazioni finestra pygame
        self.DISPLAY = display  #inizializzato con pygame nel main
        displayWidth, displayHeight = display.get_size()
        displayHeight -= 100    #per avere spazio aggiuntivo per mostrare altre informazioni
        self.BLOCK_WIDTH = int(displayWidth/self.WIDTH)
        self.BLOCK_HEIGHT = int(displayHeight/self.HEIGHT)

        # agenti
        self.CAT = Cat(self.DISPLAY, self.BLOCK_WIDTH, self.BLOCK_HEIGHT)
        self.MOUSE = Mouse(self.DISPLAY, self.BLOCK_WIDTH, self.BLOCK_HEIGHT)
        self.MOVES = {'mouse':100,'cat':100}

        # ostacoli
        self.OBSTACLES = matrix.OBSTACLES

        # formaggio
        self.CHEESE_IMG = pygame.transform.scale(pygame.image.load('immagini/cheese.png'),(self.BLOCK_WIDTH, self.BLOCK_HEIGHT))



    def get_state(self):
        self.STATE = {'mouse':(self.MOUSE_X - self.CAT_X, self.MOUSE_Y - self.CAT_Y, self.MOUSE_X - self.CHEESE_X, self.MOUSE_Y -  self.CHEESE_Y),\
                        'cat':(self.CAT_X - self.MOUSE_X, self.CAT_Y - self.MOUSE_Y)}  
        return self.STATE
    

    def reset(self):
        self.MOUSE_X, self.MOUSE_Y = (0,0)
        self.CAT_X, self.CAT_Y = (0, self.HEIGHT -1)
        self.CHEESE_X, self.CHEESE_Y = np.random.randint(0, 9, 2, 'int')

        # controllo che cheese non può essere sulla posizione di un ostacolo

        self.MOVES['cat'] = 100
        self.MOVES['cat'] = 100

        return self.get_state()


    def render(self, num_episode = -1):
        '''
            rendering the environment using pygame display
        '''
        #drawing our agents
        self.MOUSE.draw(self.MOUSE_X, self.MOUSE_Y)
        self.CAT.draw(self.CAT_X, self.CAT_Y)
        
        self.DISPLAY.blit(self.CHEESE_IMG, (self.CHEESE_X*self.BLOCK_WIDTH, self.CHEESE_Y*self.BLOCK_HEIGHT))

        #drawing obstacles
        for pos in self.OBSTACLES:
            pygame.draw.rect(self.DISPLAY, (0,0,255), [pos[0]*self.BLOCK_WIDTH, pos[1]*self.BLOCK_HEIGHT, self.BLOCK_WIDTH, self.BLOCK_HEIGHT])

        if num_episode>=0:
            self.display_episode(num_episode)