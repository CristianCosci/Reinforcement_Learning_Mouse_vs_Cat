import numpy as np
import random
from collections import defaultdict
import pickle
import os

import csv

class Agent:

    def __init__(self, env, possibleActions, alpha=0.1, gamma=0.99):
        self.env = env
        self.possibleActions = possibleActions
        self.gamma = gamma
        self.alpha = alpha
        self.Q = defaultdict(lambda: np.zeros(self.possibleActions))  #Q-TABLE


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

    
    def set_policy(self, saveQtable, dir):
        '''
            setta la policy ottimale per l'agente
        '''
        if saveQtable:
            self.saveQtableToCsv(dir)
        
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


    def save_policy(self, dir, name, savePolicytable):
        '''
            salva una policy in seguito alla creazione (allenamento)
        '''
        if savePolicytable:
            self.savePolicyToCsv(dir)
            
        try:
            policy = dict(self.policy)
            directory = dir
            if not os.path.exists(directory):
                os.makedirs(directory)
                print('non esiste')
            else:
                print('esiste')
                
            with open(f'{directory}{name}.pickle','wb') as f:
                pickle.dump(policy, f)

        except :
            print('not saved')
    

    def saveQtableToCsv(self, dir):
        w = csv.writer(open(dir+"Qtable.csv", "w"))
        
        # loop over dictionary keys and values
        for key, val in self.Q.items():
        
        # write every key and value to file
            w.writerow([key, val])


    def savePolicyToCsv(self, dir):
        policy = dict(self.policy)
        w = csv.writer(open(dir+"Policy.csv", "w"))

        # loop over dictionary keys and values
        for key, val in policy.items():

            # write every key and value to file
            w.writerow([key, val])