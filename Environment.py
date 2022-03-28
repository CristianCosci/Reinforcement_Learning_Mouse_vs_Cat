from json import load
import pygame
import numpy as np 


# Classe di comodo per rappresentare la griglia (mappa)
class Matrix:
    def __init__(self, rows=5, columns=5):
        self.ROWS = rows 
        self.COLUMNS = columns
        self.OBSTACLES = [3,3], [3,4], [3,5], [3,6], [4,6], [6,6], [6,5], [6,3], [5,3], [4,3], [5,6], [6,4]

    
#----------------------------------classe ambiente---------------------------------------------#
class Env():
    def __init__(self, display, matrix):
        self.HEIGHT = matrix.ROWS
        self.WIDTH = matrix.COLUMNS

        # Setto informazioni finestra pygame
        self.DISPLAY = display  # Inizializzato con pygame nel main
        displayWidth, displayHeight = display.get_size()
        displayHeight -= 100  # Per avere spazio aggiuntivo per mostrare altre informazioni
        self.BLOCK_WIDTH = int(displayWidth/self.WIDTH)
        self.BLOCK_HEIGHT = int(displayHeight/self.HEIGHT)

        # Agenti
        self.CAT = Cat(self.DISPLAY, self.BLOCK_WIDTH, self.BLOCK_HEIGHT)
        self.MOUSE = Mouse(self.DISPLAY, self.BLOCK_WIDTH, self.BLOCK_HEIGHT)
        self.MOVES = {'mouse':100,'cat':100}

        # Ostacoli
        self.OBSTACLES = self.load_obstacles(matrix.OBSTACLES)

        # Cheese
        self.CHEESE_IMG = pygame.transform.scale(pygame.image.load('immagini/cheese.png'),(self.BLOCK_WIDTH, self.BLOCK_HEIGHT))


    def load_obstacles(self, possible_obstacles):
        obstacle_list = list()
        i = 0
        numeri = np.random.randint(0, 2, size=len(possible_obstacles))
        #print(numeri)
        for obs in possible_obstacles:
            if numeri[i] == 1:
                obstacle_list.append(obs)
            i+= 1
        
        return tuple(obstacle_list)


    def set_obstacles(self, obstacles):
        self.OBSTACLES = obstacles
        

    def get_state(self):
        '''
        Lo stato è definito diversamente per il gatto e per il topo:
            - il topo riceve come stato la quadrupla delle 4 distanze (asse verticale e orizzontale) rispetto al gatto e al formaggio
            - il gatto riceve come stato la coppia delle 2 distanze rispetto al topo
        '''
        wall_mouse = self.checkWall('mouse')
        wall_cat = self.checkWall('cat')
        obsacles_mouse = self.checkObstacles(wall_mouse, 'mouse')
        obsacles_cat = self.checkObstacles(wall_cat, 'cat')
        '''self.STATE = {'mouse':(self.MOUSE_X - self.CAT_X, self.MOUSE_Y - self.CAT_Y, self.MOUSE_X - self.CHEESE_X, self.MOUSE_Y -  self.CHEESE_Y),\
                        'cat':(self.CAT_X - self.MOUSE_X, self.CAT_Y - self.MOUSE_Y)}  
        '''
        self.STATE = {'mouse':((self.MOUSE_X - self.CAT_X) + (self.MOUSE_Y - self.CAT_Y), (self.MOUSE_X - self.CHEESE_X) + (self.MOUSE_Y -  self.CHEESE_Y), obsacles_mouse),
                        'cat':((self.MOUSE_X - self.CAT_X) + (self.MOUSE_Y - self.CAT_Y), (self.CAT_X - self.CHEESE_X) + (self.CAT_Y -  self.CHEESE_Y), obsacles_cat)}  
        return self.STATE


    def reset(self):
        '''
        Funzione per resettare l'ambiente alla situazione iniziale
        '''
        self.MOUSE_X, self.MOUSE_Y = (0, np.random.randint(0, self.HEIGHT-1))
        
        self.CAT_X, self.CAT_Y = (self.HEIGHT-1, np.random.randint(0, self.HEIGHT-1))
        
        # Formaggio
        #self.CHEESE_X, self.CHEESE_Y = (np.random.randint(self.WIDTH // 3, self.WIDTH // 3 * 2), np.random.randint(self.HEIGHT // 3, self.HEIGHT // 3 * 2))
        self.CHEESE_X, self.CHEESE_Y = (np.random.randint((self.WIDTH // 3) + 1, (self.WIDTH // 3 * 2)), np.random.randint((self.HEIGHT // 3) + 1, (self.HEIGHT // 3 * 2)))
        
        self.MOVES['mouse'] = 100
        self.MOVES['cat'] = 100
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
        
    
    def step(self, mouse_action, cat_action):
        '''
        Funzione di movimento
        '''
        done = False
        mouse_action_null = False
        cat_action_null = False
        mouse_out_of_bounds = False
        cat_out_of_bounds = False
        reward = {'mouse': -1, 'cat': -1}
        toccate_ostacolo_mouse = 0
        toccate_ostacolo_cat = 0
        toccate_muro_mouse = 0
        toccate_muro_cat = 0
        info = {
            'cheese_eaten': False,
            'mouse_caught': False,
            'x': -1, 'y': -1,\
            'width': self.BLOCK_WIDTH,
            'height': self.BLOCK_HEIGHT
        }

        self.MOVES['cat'] -= 1
        self.MOVES['mouse'] -= 1
        # done if moves = 0
        if self.MOVES['cat'] == 0 or self.MOVES['mouse'] == 0:
            done = True
        
        mouse_towards_obstacle = self.check_towards_obstacle(mouse_action, agent='mouse')
        cat_towards_obstacle = self.check_towards_obstacle(cat_action, agent='cat')
        if mouse_towards_obstacle:
            toccate_ostacolo_mouse +=1
            reward['mouse'] = -20
            mouse_action_null = True
        if cat_towards_obstacle:
            toccate_ostacolo_cat +=1
            reward['cat'] = -20
            cat_action_null = True

        mouse_out_of_bounds = self.check_out_of_bounds(mouse_action, agent='mouse')
        cat_out_of_bounds = self.check_out_of_bounds(cat_action, agent='cat')
        if mouse_out_of_bounds:
            reward['mouse'] = -20
            toccate_muro_mouse +=1
            mouse_action_null = True
        if cat_out_of_bounds:
            reward['cat'] = -20
            toccate_muro_cat +=1
            cat_action_null = True

        self.update_positions(mouse_action, cat_action, mouse_action_null, cat_action_null)

        # Mouse ha mangiato il formaggio
        if self.MOUSE_X == self.CHEESE_X and self.MOUSE_Y == self.CHEESE_Y:
            done = True
            reward['mouse'] = 200
            info['cheese_eaten'], info['x'], info['y'] = True,  self.MOUSE_X, self.MOUSE_Y
        
        # Cat ha mangiato mouse
        if self.CAT_X == self.MOUSE_X and self.CAT_Y == self.MOUSE_Y:
            done = True
            reward['cat'] = 200
            reward['mouse'] = -200
            info['mouse_caught'], info['x'], info['y'] = True,  self.MOUSE_X, self.MOUSE_Y
        
        return self.get_state(), reward, done, info, toccate_muro_mouse, toccate_muro_cat, toccate_ostacolo_mouse, toccate_ostacolo_cat
    

    def check_towards_obstacle(self, action, agent):
        assert agent == 'cat' or agent == 'mouse'
        towards_obstacle = False
        x_change, y_change = self.get_changes(action, action_null=False)
        for obs in self.OBSTACLES:
            if agent == 'cat':
                if ((self.CAT_X + x_change) == obs[0]) and ((self.CAT_Y + y_change) == obs[1]):    
                    towards_obstacle = True
            else:
                if ((self.MOUSE_X + x_change) == obs[0]) and ((self.MOUSE_Y + y_change) == obs[1]):
                    towards_obstacle = True

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
            
    
    def update_positions(self, mouse_action, cat_action, mouse_action_null, cat_action_null):
        x_change_mouse, y_change_mouse = self.get_changes(mouse_action, mouse_action_null)
        x_change_cat, y_change_cat = self.get_changes(cat_action, cat_action_null)

        self.MOUSE_X += x_change_mouse 
        self.MOUSE_Y += y_change_mouse

        self.CAT_X += x_change_cat 
        self.CAT_Y += y_change_cat 
        

    def get_changes(self, action, action_null):
        x_change, y_change = 0, 0
        if not action_null:
            #decide action
            if action == 0:
                x_change = -1  #moving left
            elif action == 1:
                x_change = 1   #moving right
            elif action == 2:
                y_change = -1 #moving upwards
            elif action ==3:
                y_change = 1  #moving downwards
        
        return x_change, y_change

    def getWallDistance(self, agent):
        assert agent == 'cat' or agent == 'mouse'
        distanza_X = 0
        distanza_Y = 0
        if agent == 'cat':
            if self.WIDTH - self.CAT_X < self.CAT_X:
                distanza_X = self.WIDTH - self.CAT_X
            else:
                distanza_X = self.CAT_X
            if self.HEIGHT - self.CAT_Y < self.CAT_Y:
                distanza_Y = self.HEIGHT - self.CAT_Y
            else:
                distanza_Y = self.CAT_Y
        elif agent == 'mouse':
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


    def checkWall(self, agent):
        assert agent == 'cat' or agent == 'mouse'
        if agent == 'cat':
            x, y = self.CAT_X, self.CAT_Y
        else:
            x, y = self.MOUSE_X, self.MOUSE_Y

        wall_position = 0
        if x - 2 < 0:
            wall_position = 1        # wall on the left
        if x + 2 > self.WIDTH-1:
            wall_position = 2       # wall on the rigth
        if y - 2 < 0:
            if wall_position == 1:
                wall_position = 5   # wall on top e left
            elif wall_position == 2:
                wall_position = 6   # wall on top e rigth
            else:
                wall_position = 3   # wall on the top
        if y + 2 > self.HEIGHT-1:
            if wall_position == 1:
                wall_position = 7   # wall on bottom e left
            elif wall_position == 2:
                wall_position = 8   # wall on bottom e right
            else:
                wall_position = 4   # wall on the bottom

        return wall_position


    def checkObstacles(self, wall_position, agent):
        assert agent == 'cat' or agent == 'mouse'
        if agent == 'cat':
            x, y = self.CAT_X, self.CAT_Y
        else:
            x, y = self.MOUSE_X, self.MOUSE_Y

        if wall_position == 0:
            for obs in self.OBSTACLES:
                if (x == obs[0]):
                    if (y + 1) == obs[1]:
                        wall_position = 4   # down
                    elif (y - 1) == obs[1]:
                        wall_position = 3   # up
                elif (y == obs[1]):
                    if (x + 1) == obs[0]:
                        wall_position = 2   # right
                    elif (x- 1) == obs[0]:
                        wall_position = 1   # left
        
        return wall_position


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