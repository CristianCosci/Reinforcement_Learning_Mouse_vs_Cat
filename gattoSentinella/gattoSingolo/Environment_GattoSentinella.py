from cmath import inf
import pygame
import numpy as np 


# classe di comodo per rappresentare la griglia (mappa)
class Matrix:
	def __init__(self, rows=5, columns=5):
		self.ROWS = rows 
		self.COLUMNS = columns
		self.OBSTACLES = []#[[2,2], [3,7], [7,2], [5,7], [6,5]]

    
#----------------------------------classe ambiente---------------------------------------------#
class Env():
    def __init__(self, display, matrix):
        self.HEIGHT = matrix.ROWS
        self.WIDTH = matrix.COLUMNS

        # Setto informazioni finestra pygame
        self.DISPLAY = display  #inizializzato con pygame nel main
        displayWidth, displayHeight = display.get_size()
        displayHeight -= 100    #per avere spazio aggiuntivo per mostrare altre informazioni
        self.BLOCK_WIDTH = int(displayWidth/self.WIDTH)
        self.BLOCK_HEIGHT = int(displayHeight/self.HEIGHT)

        # Agenti
        self.CAT = Cat(self.DISPLAY, self.BLOCK_WIDTH, self.BLOCK_HEIGHT)
        self.MOUSE = Mouse(self.DISPLAY, self.BLOCK_WIDTH, self.BLOCK_HEIGHT)
        self.MOVES = {'mouse':100,'cat':100}
        
        # Ostacoli
        self.OBSTACLES = matrix.OBSTACLES

        # Cheese
        self.CHEESE_IMG = pygame.transform.scale(pygame.image.load('immagini/cheese.png'),(self.BLOCK_WIDTH, self.BLOCK_HEIGHT))


    def get_state(self):
        '''
        Lo stato è definito diversamente per il gatto e per il topo:
            - il topo riceve come stato la quadrupla delle 4 distanze (asse verticale e orizzontale) rispetto al gatto e al formaggio
            - il gatto riceve come stato la coppia delle 2 distanze rispetto al topo
        '''
        distanzaMuro = self.getWallDistance()

        self.STATE = {'mouse':((self.MOUSE_X - self.CAT_X) + (self.MOUSE_Y - self.CAT_Y),
            (self.MOUSE_X - self.CHEESE_X) + (self.MOUSE_Y -  self.CHEESE_Y),
            distanzaMuro)}
    
        return self.STATE


    def reset(self):
        '''
        Funzione per resettare l'ambiente alla situazione iniziale
        '''
        #self.MOUSE_X, self.MOUSE_Y = (0, 0)
        self.MOUSE_X, self.MOUSE_Y = (np.random.randint(0, (self.WIDTH // 3 )-1), np.random.randint(0,9))

        self.CAT_X, self.CAT_Y = ((self.WIDTH / 2) -1 ,np.random.randint(0, 9))
        #self.CAT_X, self.CAT_Y = (self.WIDTH / 2, 0)

        # Formaggio
        #self.CHEESE_X, self.CHEESE_Y = (9, 5)
        self.CHEESE_X, self.CHEESE_Y = (np.random.randint((self.WIDTH // 3 * 2)+1, 9), np.random.randint(0, 9))
        #self.CHEESE_X, self.CHEESE_Y = np.random.randint(0, 9, 2, 'int')

        # Controllo che il formaggio e il topo non possono essere sulla posizione di un ostacolo
        for obs in self.OBSTACLES:
            if self.CHEESE_X == obs[0] and self.CHEESE_Y == obs[1]:
                #then shift it up
                    self.CHEESE_Y -= 1
        
        for obs in self.OBSTACLES:
            if self.MOUSE_X == obs[0] and self.MOUSE_Y == obs[1]:
                #then shift it up
                    self.MOUSE_Y -= 1

        self.MOVES['mouse'] = 100
        return self.get_state()


    def render(self, i_episode = -1):
        '''
            Rendering dell'ambiente a schermo con pygame
        '''
        self.MOUSE.draw(self.MOUSE_X, self.MOUSE_Y)
        self.CAT.draw(self.CAT_X, self.CAT_Y)
        
        self.DISPLAY.blit(self.CHEESE_IMG, (self.CHEESE_X*self.BLOCK_WIDTH, self.CHEESE_Y*self.BLOCK_HEIGHT))

        # Disegno ostacoli
        for pos in self.OBSTACLES:
            pygame.draw.rect(self.DISPLAY, (0,0,255), [pos[0]*self.BLOCK_WIDTH, pos[1]*self.BLOCK_HEIGHT, self.BLOCK_WIDTH, self.BLOCK_HEIGHT])

        if i_episode>=0:
            self.display_episode(i_episode)
        

    def step(self, mouse_action, cat_direction):
        done = False
        mouse_action_null = False
        mouse_out_of_bounds = False
        cat_out_of_bounds = False
        reward = {'mouse': -1}
        toccate_ostacolo = 0
        toccate_muro = 0
        info = {
            'cheese_eaten': False,
            'mouse_caught': False,
            'x': -1, 'y': -1,\
            'width': self.BLOCK_WIDTH,
            'height': self.BLOCK_HEIGHT
        }

        self.MOVES['mouse'] -= 1
        #done if moves = 0
        if self.MOVES['mouse'] == 0:
            done = True
        
        mouse_towards_obstacle = self.check_towards_obstacle(mouse_action, agent='mouse')
        if mouse_towards_obstacle:
            toccate_ostacolo +=1
            reward['mouse'] = -20
            mouse_action_null = True

        mouse_out_of_bounds = self.check_out_of_bounds(mouse_action, agent='mouse')
        cat_out_of_bounds = self.check_out_of_bounds(cat_direction, agent='cat')

        if mouse_out_of_bounds:
            reward['mouse'] = -20
            toccate_muro +=1
            mouse_action_null = True
        if cat_out_of_bounds:
            if cat_direction == 2:
                cat_direction = 3
            else:
                cat_direction = 2

        self.update_positions(mouse_action, cat_direction, mouse_action_null)

        #mouse reached the cheese
        if self.MOUSE_X == self.CHEESE_X and self.MOUSE_Y == self.CHEESE_Y:
            done = True
            reward['mouse'] = 200
            info['cheese_eaten'], info['x'], info['y'] = True,  self.MOUSE_X, self.MOUSE_Y
        
        #cat caught the mouse
        if self.CAT_X == self.MOUSE_X and self.CAT_Y == self.MOUSE_Y:
            done = True
            reward['mouse'] = -200
            info['mouse_caught'], info['x'], info['y'] = True,  self.MOUSE_X, self.MOUSE_Y
        
        return self.get_state(), reward, done, info, cat_direction, toccate_muro, toccate_ostacolo
    

    def check_towards_obstacle(self, action, agent):
        assert agent == 'cat' or agent == 'mouse'
        towards_obstacle = False
        x_change, y_change = self.get_changes(action, action_null=False)
        for obs in self.OBSTACLES:
            if agent == 'cat':
                if ((self.CAT_X + x_change) == obs[0]) and ((self.CAT_Y + y_change) == obs[1]):    
                    towards_obstacle = True
                    #self.CAT_X, self.CAT_Y = (0, self.HEIGHT -1) #riposizionamento
            else:
                if ((self.MOUSE_X + x_change) == obs[0]) and ((self.MOUSE_Y + y_change) == obs[1]):
                    towards_obstacle = True
                    #self.MOUSE_X, self.MOUSE_Y = (0,0)
        
        return towards_obstacle

    
    def check_out_of_bounds(self, action, agent):
        assert agent == 'cat' or agent == 'mouse'
        out_of_bounds = False
        x_change, y_change = self.get_changes(action, action_null=False)
        if agent == 'cat':
            x_change += self.CAT_X
            y_change += self.CAT_Y
        else:
            x_change += self.MOUSE_X
            y_change += self.MOUSE_Y
        
        if x_change < 0:
            out_of_bounds = True
        elif x_change > self.WIDTH-1:
            out_of_bounds = True
        if y_change < 0:
            out_of_bounds = True
        elif y_change > self.HEIGHT -1:
            out_of_bounds = True
        
        return out_of_bounds
    

    def update_positions(self, mouse_action, cat_direction, mouse_action_null):
        x_change_mouse, y_change_mouse = self.get_changes(mouse_action, mouse_action_null)
        x_change_cat, y_change_cat = self.get_changes(cat_direction, False)
        self.MOUSE_X += x_change_mouse 
        self.MOUSE_Y += y_change_mouse
        self.CAT_X += x_change_cat
        self.CAT_Y += y_change_cat
    
    
    def get_changes(self, action, action_null):
        x_change, y_change = 0, 0
        if not action_null:
            #decide action
            if action == 0:
                x_change = -1   #moving left
            elif action == 1:
                x_change = 1    #moving right
            elif action == 2:
                y_change = -1   #moving upwards
            elif action ==3:
                y_change = 1    #moving downwards
        
        return x_change, y_change


    def getWallDistance(self):
        distanza_X = 0
        if self.WIDTH - self.MOUSE_X < self.MOUSE_X:
            distanza_X = self.WIDTH - self.MOUSE_X
        else:
            distanza_X = self.MOUSE_X
        
        distanza_Y = 0
        if self.HEIGHT - self.MOUSE_Y < self.MOUSE_Y:
            distanza_Y = self.HEIGHT - self.MOUSE_Y
        else:
            distanza_Y = self.MOUSE_Y
        
        return min(distanza_X, distanza_Y)

        
    def display_episode(self,epsiode):
        font = pygame.font.SysFont(None, 25)
        text = font.render("Episode: "+str(epsiode), True, (0,0,220))
        self.DISPLAY.blit(text,(1,1))

        
#-----------------------------------------------------------------------------------------------------------------------------------#

class Mouse():

    def __init__(self, gameDisplay, width, height):
        self.DISPLAY = gameDisplay
        self.WIDTH = width 
        self.HEIGHT = height
    
        self.IMG = pygame.image.load('immagini/jerry.png')
        self.IMG = pygame.transform.scale(self.IMG, (self.WIDTH, self.HEIGHT))


    def draw(self, x, y):
        self.DISPLAY.blit(self.IMG, (x*self.WIDTH, y*self.HEIGHT))



class Cat():

    def __init__(self, display, width, height):
        self.DISPLAY = display
        self.WIDTH = width 
        self.HEIGHT = height
        
        self.IMG = pygame.image.load('immagini/tom.png')
        self.IMG = pygame.transform.scale(self.IMG, (self.WIDTH, self.HEIGHT))


    def draw(self, x, y):
        self.DISPLAY.blit(self.IMG, (x*self.WIDTH, y*self.HEIGHT))