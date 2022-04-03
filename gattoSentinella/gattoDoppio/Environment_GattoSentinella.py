import pygame
import numpy as np 
import random

# Convenience class to represent the grid (map)
class Matrix:
    def __init__(self, rows=5, columns=5, max_pct_obstacles = 0):
        self.ROWS = rows 
        self.COLUMNS = columns
        self.PCT_OBSTACLES = max_pct_obstacles
        if max_pct_obstacles > 0:
            self.OBSTACLES = self.createObstacles(self.ROWS, ((self.ROWS // 2) -1))
        else:
            self.OBSTACLES = []


    def createObstacles(self, n, cat_axis):
        possible_obstacles = []
        for x in range(n):
            if x == cat_axis:
                pass
            else:
                for y in range(n):
                    possible_obstacles.append((x, y))

        return tuple(possible_obstacles)

#----------------------------------classe ambiente---------------------------------------------#
class Env():
    def __init__(self, display, matrix):
        self.HEIGHT = matrix.ROWS
        self.WIDTH = matrix.COLUMNS
        self.PCT_OBS = matrix.PCT_OBSTACLES

        # Setto informazioni finestra pygame
        self.DISPLAY = display  # Inizializzato con pygame nel main
        displayWidth, displayHeight = display.get_size()
        displayHeight -= 100    # Per avere spazio aggiuntivo per mostrare altre informazioni
        self.BLOCK_WIDTH = int(displayWidth/self.WIDTH)
        self.BLOCK_HEIGHT = int(displayHeight/self.HEIGHT)
        
        # Agents
        self.CAT1 = Cat(self.DISPLAY, self.BLOCK_WIDTH, self.BLOCK_HEIGHT)
        self.CAT2 = Cat(self.DISPLAY, self.BLOCK_WIDTH, self.BLOCK_HEIGHT)
        self.MOUSE = Mouse(self.DISPLAY, self.BLOCK_WIDTH, self.BLOCK_HEIGHT)
        self.MOVES = {'mouse':100,'cat':100}

        # Obstacles
        self.OBSTACLES = self.load_obstacles(matrix.OBSTACLES, self.PCT_OBS)

        # Cheese
        self.CHEESE_IMG = pygame.transform.scale(pygame.image.load('immagini/cheese.png'),(self.BLOCK_WIDTH, self.BLOCK_HEIGHT))


    def load_obstacles(self, possible_obstacles, pct_obstacles):
        '''
            Used to random choose n (pct_obstacles*100) obstacles from the possble obstacles
        '''
        n = int(pct_obstacles*100)
        obstacle_list = list()
        numbers = random.sample(range(len(possible_obstacles)), n)
        for i in numbers:
            obstacle_list.append(possible_obstacles[i])
        
        return tuple(obstacle_list)


    def set_obstacles(self, obstacles): # Used to change the obstacles in the map
        self.OBSTACLES = obstacles


    def get_state(self):
        '''
            Return the state for the agent
        '''
        wall = self.checkWall()
        obstacles_first = self.checkDoubleObstacles(wall)
        if wall != obstacles_first:  # Used to avoid worthless operation in case there are not obstacles near the agent
            obstacles_second = self.checkDoubleObstacles(obstacles_first)
            if obstacles_first != obstacles_second:  # Used to avoid worthless operation in case there are not more than 1 obstacle near the agent
                obstacles = self.checkTripleObstacles(obstacles_second)
            else:
                obstacles = obstacles_second
        else:
            obstacles = obstacles_first

        #Doppio gatto sentinella
        self.STATE = {'mouse':((self.MOUSE_X - self.CAT1_X) + (self.MOUSE_Y - self.CAT1_Y),
            (self.MOUSE_X - self.CAT2_X) + (self.MOUSE_Y - self.CAT2_Y),
            (self.MOUSE_X - self.CHEESE_X) + (self.MOUSE_Y -  self.CHEESE_Y), 
            obstacles)}
        
        return self.STATE


    def reset(self):
        '''
            Used to reset all elements position in the environment
        '''
        #self.MOUSE_X, self.MOUSE_Y = (np.random.randint(0, (self.WIDTH // 3 )-1), np.random.randint(0,9)) #doppio gatto verticale SENZA ostacoli
        #self.MOUSE_X, self.MOUSE_Y = (np.random.randint(0, (self.WIDTH // 3 )-2), np.random.randint(0,9)) #doppio gatto verticale e CON ostacoli
        #self.MOUSE_X, self.MOUSE_Y = (np.random.randint(0, (self.WIDTH // 3 )+1), np.random.randint(0, (self.HEIGHT // 3)+1)) #doppio gatto misto SENZA ostacoli
        self.MOUSE_X, self.MOUSE_Y = (np.random.randint(0, (self.WIDTH // 3 )), np.random.randint(0, (self.HEIGHT // 3))) #doppio gatto misto CON ostacoli

        #Gatto sentinella doppio
        #self.CAT1_X, self.CAT1_Y = ((self.WIDTH // 3), np.random.randint(0, 9)) #doppio gatto verticale
        #self.CAT2_X, self.CAT2_Y = ((self.WIDTH // 3 * 2), np.random.randint(0, 9)) #doppio gatto verticale
        self.CAT1_X, self.CAT1_Y = ((self.WIDTH // 3)+2, np.random.randint(0, 9)) #doppio gatto misto SENZA ostacoli
        self.CAT2_X, self.CAT2_Y = (np.random.randint(0, 9), (self.HEIGHT // 3 * 2)-1) #doppio gatto misto SENZA ostacoli

        # Formaggio
        #self.CHEESE_X, self.CHEESE_Y = (np.random.randint((self.WIDTH // 3 * 2)+1, 9), np.random.randint(0, 9)) #doppio gatto verticale SENZA ostacoli
        #self.CHEESE_X, self.CHEESE_Y = (np.random.randint((self.WIDTH // 3 * 2)+2, 9), np.random.randint(0, 9)) #doppio gatto verticale CON ostacoli
        #self.CHEESE_X, self.CHEESE_Y = (np.random.randint((self.WIDTH // 3 * 2), 9), np.random.randint((self.HEIGHT // 3 * 2), 9)) #doppio gatto misto SENZA ostacoli
        self.CHEESE_X, self.CHEESE_Y = (np.random.randint((self.WIDTH // 3 * 2)+1, 9), np.random.randint((self.HEIGHT // 3 * 2)+1, 9)) #doppio gatto misto CON ostacoli

        self.MOVES['mouse'] = 100
        return self.get_state()


    def render(self, i_episode = -1):
        self.MOUSE.draw(self.MOUSE_X, self.MOUSE_Y)
        
        # Gatto sentinella doppio
        self.CAT1.draw(self.CAT1_X, self.CAT1_Y)
        self.CAT2.draw(self.CAT2_X, self.CAT2_Y)
        
        self.DISPLAY.blit(self.CHEESE_IMG, (self.CHEESE_X*self.BLOCK_WIDTH, self.CHEESE_Y*self.BLOCK_HEIGHT))

        # Obstacles
        for pos in self.OBSTACLES:
            pygame.draw.rect(self.DISPLAY, (0,0,255), [pos[0]*self.BLOCK_WIDTH, pos[1]*self.BLOCK_HEIGHT, self.BLOCK_WIDTH, self.BLOCK_HEIGHT])

        if i_episode>=0:
            self.display_episode(i_episode)
        
    
    def step(self, mouse_action, cat1_direction, cat2_direction):
        '''
            Principal method in wich all needed controls are do
        '''
        done = False
        mouse_action_null = False
        mouse_out_of_bounds = False
        cat1_out_of_bounds = False
        cat2_out_of_bounds = False
        reward = {'mouse': -1}
        toccate_ostacolo = 0
        toccate_muro = 0
        info = {    # Dict that contains all the information to keep during the process
            'cheese_eaten': False,
            'mouse_caught': False,
            'x': -1, 'y': -1,\
            'width': self.BLOCK_WIDTH,
            'height': self.BLOCK_HEIGHT
        }

        self.MOVES['mouse'] -= 1
        # done if moves = 0
        if self.MOVES['mouse'] == 0:
            done = True
        
        mouse_towards_obstacle = self.check_towards_obstacle(mouse_action, agent='mouse')
        if mouse_towards_obstacle:
            toccate_ostacolo +=1
            reward['mouse'] = -20
            mouse_action_null = True

        mouse_out_of_bounds = self.check_out_of_bounds(mouse_action, agent='mouse')

        cat1_out_of_bounds = self.check_out_of_bounds(cat1_direction, agent='cat1')
        cat2_out_of_bounds = self.check_out_of_bounds(cat2_direction, agent='cat2')

        if mouse_out_of_bounds:
            reward['mouse'] = -20
            toccate_muro +=1
            mouse_action_null = True

        if cat1_out_of_bounds:
            if cat1_direction == 2:
                cat1_direction = 3
            else:
                cat1_direction = 2
        '''
        #Gatto doppio verticale
        if cat2_out_of_bounds:
            if cat2_direction == 2:
                cat2_direction = 3
            else:
                cat2_direction = 2
        '''
        if cat2_out_of_bounds:
            if cat2_direction == 0:
                cat2_direction = 1
            else:
                cat2_direction = 0
        
        self.update_positions(mouse_action, cat1_direction, cat2_direction, mouse_action_null)

        #mouse reached the cheese
        if self.MOUSE_X == self.CHEESE_X and self.MOUSE_Y == self.CHEESE_Y:
            done = True
            reward['mouse'] = 200
            info['cheese_eaten'], info['x'], info['y'] = True,  self.MOUSE_X, self.MOUSE_Y
        
        #cat caught the mouse
        if self.CAT1_X == self.MOUSE_X and self.CAT1_Y == self.MOUSE_Y:
            done = True
            reward['mouse'] = -200
            info['mouse_caught'], info['x'], info['y'] = True,  self.MOUSE_X, self.MOUSE_Y
        
        if self.CAT2_X == self.MOUSE_X and self.CAT2_Y == self.MOUSE_Y:
            done = True
            reward['mouse'] = -200
            info['mouse_caught'], info['x'], info['y'] = True,  self.MOUSE_X, self.MOUSE_Y
        
        return self.get_state(), reward, done, info, cat1_direction, cat2_direction, toccate_muro, toccate_ostacolo
    

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
        assert agent == 'cat1' or agent == 'cat2' or agent == 'mouse'
        out_of_bounds = False
        x_change, y_change = self.get_changes(action, action_null=False)
        if agent == 'cat1':
            x_change += self.CAT1_X
            y_change += self.CAT1_Y
        elif agent == 'cat2':
            x_change += self.CAT2_X
            y_change += self.CAT2_Y
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
    

    def update_positions(self, mouse_action, cat1_direction, cat2_direction, mouse_action_null):
        x_change_mouse, y_change_mouse = self.get_changes(mouse_action, mouse_action_null)
        x_change_cat1, y_change_cat1 = self.get_changes(cat1_direction, False)
        x_change_cat2, y_change_cat2 = self.get_changes(cat2_direction, False)
        self.MOUSE_X += x_change_mouse 
        self.MOUSE_Y += y_change_mouse
        self.CAT1_X += x_change_cat1
        self.CAT1_Y += y_change_cat1
        self.CAT2_X += x_change_cat2
        self.CAT2_Y += y_change_cat2


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

        
    def checkWall(self):
        visual = 1
        wall_position = 0
        if self.MOUSE_X - visual < 0:
            wall_position = 1        # wall on the LEFT
        if self.MOUSE_X + visual > self.WIDTH-1:
            wall_position = 2       # wall on the RIGHT
        if self.MOUSE_Y - visual < 0:
            if wall_position == 1:
                wall_position = 5   # wall on TOP and LEFT
            elif wall_position == 2:
                wall_position = 6   # wall on TOP and RIGHT
            else:
                wall_position = 3   # wall on the TOP
        if self.MOUSE_Y + visual > self.HEIGHT-1:
            if wall_position == 1:
                wall_position = 7   # wall on DOWN and LEFT
            elif wall_position == 2:
                wall_position = 8   # wall on DOWN e RIGHT
            else:
                wall_position = 4   # wall on the DOWN

        return wall_position


    def checkDoubleObstacles(self, wall_position):
        if wall_position == 0:
            for obs in self.OBSTACLES:
                if (self.MOUSE_X == obs[0]):
                    if (self.MOUSE_Y + 1) == obs[1]:
                        wall_position = 4   # obstacle DOWN
                    elif (self.MOUSE_Y - 1) == obs[1]:
                        wall_position = 3   # obstacle UP
                elif (self.MOUSE_Y == obs[1]):
                    if (self.MOUSE_X + 1) == obs[0]:
                        wall_position = 2   # obstacle RIGHT
                    elif (self.MOUSE_X - 1) == obs[0]:
                        wall_position = 1   # obstacle LEFT
        elif wall_position == 1:
            for obs in self.OBSTACLES:
                if (self.MOUSE_X == obs[0]):
                    if (self.MOUSE_Y + 1) == obs[1]:
                        wall_position = 7   # obstacle DOWN and LEFT
                    elif (self.MOUSE_Y - 1) == obs[1]:
                        wall_position = 5   # obstacle UP and LEFT
                elif (self.MOUSE_Y == obs[1]):
                    if (self.MOUSE_X + 1) == obs[0]:
                        wall_position = 9   # obstacle RIGHT and LEFT
        elif wall_position == 2:
            for obs in self.OBSTACLES:
                if (self.MOUSE_X == obs[0]):
                    if (self.MOUSE_Y + 1) == obs[1]:
                        wall_position = 8   # obstacle DOWN and RIGHT
                    elif (self.MOUSE_Y - 1) == obs[1]:
                        wall_position = 6   # obstacle UP and RIGHT
                elif (self.MOUSE_Y == obs[1]):
                    if (self.MOUSE_X - 1) == obs[0]:
                        wall_position = 9   # obstacle LEFT and RIGHT
        elif wall_position == 3:
            for obs in self.OBSTACLES:
                if (self.MOUSE_X == obs[0]):
                    if (self.MOUSE_Y + 1) == obs[1]:
                        wall_position = 10   # obstacle DOWN and UP
                elif (self.MOUSE_Y == obs[1]):
                    if (self.MOUSE_X + 1) == obs[0]:
                        wall_position = 6   # obstacle RIGHT and UP
                    elif (self.MOUSE_X - 1) == obs[0]:
                        wall_position = 5   # obstacle LEFT and UP
        elif wall_position == 4:
            for obs in self.OBSTACLES:
                if (self.MOUSE_X == obs[0]):
                    if (self.MOUSE_Y - 1) == obs[1]:
                        wall_position = 10   # obstacle UP and DOWN
                elif (self.MOUSE_Y == obs[1]):
                    if (self.MOUSE_X + 1) == obs[0]:
                        wall_position = 8   # obstacle RIGHT and DOWN
                    elif (self.MOUSE_X - 1) == obs[0]:
                        wall_position = 7   # obstacle LEFT and DOWN

        return wall_position
        

    def checkTripleObstacles(self, wall_position):
        if wall_position == 5:
            for obs in self.OBSTACLES:
                if (self.MOUSE_X == obs[0]):
                    if (self.MOUSE_Y + 1) == obs[1]:
                        wall_position = 13   # obstacle DOWN and UP and LEFT
                elif (self.MOUSE_Y == obs[1]):
                    if (self.MOUSE_X + 1) == obs[0]:
                        wall_position = 11  # obstacle RIGHT and UP and LEFT
        elif wall_position == 6:
            for obs in self.OBSTACLES:
                if (self.MOUSE_X == obs[0]):
                    if (self.MOUSE_Y + 1) == obs[1]:
                        wall_position = 14   # obstacle DOWN UP and RIGHT
                elif (self.MOUSE_Y == obs[1]):
                    if (self.MOUSE_X - 1) == obs[0]:
                        wall_position = 11   # obstacle LEFT and UP and RIGHT
        if wall_position == 7:
            for obs in self.OBSTACLES:
                if (self.MOUSE_X == obs[0]):
                    if (self.MOUSE_Y - 1) == obs[1]:
                        wall_position = 13   # obstacle UP and DOWN e LEFT
                elif (self.MOUSE_Y == obs[1]):
                    if (self.MOUSE_X + 1) == obs[0]:
                        wall_position = 12   # obstacle RIGHT and DOWN e LEFT
        if wall_position == 8:
            for obs in self.OBSTACLES:
                if (self.MOUSE_X == obs[0]):
                    if (self.MOUSE_Y - 1) == obs[1]:
                        wall_position = 14   # obstacle UP and RIGHT e DOWN
                elif (self.MOUSE_Y == obs[1]):
                    if (self.MOUSE_X - 1) == obs[0]:
                        wall_position = 12   # obstacle LEFT and RIGHT e DOWN
        if wall_position == 9:
            for obs in self.OBSTACLES:
                if (self.MOUSE_X == obs[0]):
                    if (self.MOUSE_Y + 1) == obs[1]:
                        wall_position = 12   # obstacle DOWN and RIGHT e LEFT
                    elif (self.MOUSE_Y - 1) == obs[1]:
                        wall_position = 11   # obstacle UP and RIGHT e LEFT
        if wall_position == 10:
            for obs in self.OBSTACLES:
                if (self.MOUSE_Y == obs[1]):
                    if (self.MOUSE_X + 1) == obs[0]:
                        wall_position = 14   # obstacle RIGHT and UP e DOWN
                    elif (self.MOUSE_X - 1) == obs[0]:
                        wall_position = 13   # obstacle LEFT and UP e DOWN
        return wall_position


    def checkRegularPosition(self):
        for obs in self.OBSTACLES:
            if self.CHEESE_X == obs[0] and self.CHEESE_Y == obs[1]:
                self.CHEESE_X, self.CHEESE_Y = (np.random.randint((self.WIDTH // 3 * 2)+1, 9), np.random.randint(0, 9))
                self.checkRegularPosition()
        
        for obs in self.OBSTACLES:
            if self.MOUSE_X == obs[0] and self.MOUSE_Y == obs[1]:
                self.MOUSE_X, self.MOUSE_Y = (np.random.randint(0, (self.WIDTH // 3 )-1), np.random.randint(0,9))
                self.checkRegularPosition()

                
    def display_episode(self,epsiode):
        font = pygame.font.SysFont(None, 25)
        text = font.render("Episode: "+str(epsiode), True, (0,0,220))
        self.DISPLAY.blit(text,(1,1))


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