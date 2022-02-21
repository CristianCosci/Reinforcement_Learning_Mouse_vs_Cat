import numpy as np
import random
from collections import defaultdict
import pickle


class Agent:

    def __init__(self, env, possibleActions):
        self.env = env
        self.possibleActions = possibleActions
        self.Q = defaultdict(lambda: np.zeros(self.nA))  #Q-TABLE


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
        with open(directory, 'rb') as f:
            policy_new = pickle.load(f)
        self.policy = defaultdict(lambda:0, policy_new)  #salvata come defaultdict
        print('policy Loaded')


    def save_policy(self,i):
        '''
            salva una policy in seguito alla creazione (allenamento)
        '''
        try:
            policy = dict(self.policy)
            with open(f'policy{i}.pickle','wb') as f:
                pickle.dump(policy, f)
        except :
            print('not saved')