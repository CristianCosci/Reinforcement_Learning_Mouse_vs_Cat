import numpy as np
import random
from collections import defaultdict
import pickle
import os

class Agent:

    def __init__(self, env, possibleActions, alpha, gamma=1.0, eps_start=1.0, eps_decay=0.9999, eps_min=0.05):
        self.env = env
        self.possibleActions = possibleActions
        self.eps_start = eps_start
        self.gamma = gamma
        self.alpha = alpha
        self.eps_decay = eps_decay
        self.eps_min = eps_min
        self.Q = defaultdict(lambda: np.zeros(self.possibleActions))  # Q-TABLE


    def get_action(self, state, epsilon):
        '''
            Sceglie l'azione da eseguire:
                - viene scelta la migliore mossa dalla Q-table con una probabilità di 1-epsilon
                - altrimenti sceglie un'azione casuale
        '''
        bias = random.random()
        if bias > epsilon:
            return np.argmax(self.Q[state])
        else:
            return np.random.choice(np.arange(self.possibleActions))


    def Q_learn(self, state, action, reward, next_state):
        '''
            aggiorna la Q-table
        ''' 
        self.Q[state][action] += self.alpha*(reward + self.gamma*np.max(self.Q[next_state]) - self.Q[state][action])

    
    def set_policy(self):
        '''
            setta la policy ottimale per l'agente
        '''
        policy = defaultdict(lambda: 0)
        for state, action in self.Q.items():
            policy[state] = np.argmax(action)
        self.policy = policy
    
        
    def take_action(self,state):
        '''
            sceglie un'azione secondo la policy
        '''
        return self.policy[state]

    
    def load_policy(self, directory):
        '''
            carica una policy esistente
        '''
        dir = 'policies/'+directory
        with open(dir, 'rb') as f:
            policy_new = pickle.load(f)
        self.policy = defaultdict(lambda:0, policy_new)  # Salvata come defaultdict
        print('policy Loaded')


    def save_policy(self, dir, name):
        '''
            salva una policy in seguito alla creazione (allenamento)
        '''
        try:
            policy = dict(self.policy)
            directory = "policies/"+ dir
            if not os.path.exists(directory):
                os.makedirs(directory)
                print('non esiste')
            else:
                print('esiste')
                
            with open(f'{directory}/{name}.pickle','wb') as f:
                pickle.dump(policy, f)
        except :
            print('not saved')