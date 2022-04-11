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
            Choose the action to do:
                - The best move is chosen from the Q-table with a probability of 1-epsilon
                - otherwise he chooses a random action
        '''
        bias = random.random()
        if bias > epsilon:
            return np.argmax(self.Q[state])
        else:
            return np.random.choice(np.arange(self.possibleActions))


    def Q_learn(self, state, action, reward, next_state):
        '''
            Update the Q-table
        ''' 
        self.Q[state][action] += self.alpha*(reward + self.gamma*np.max(self.Q[next_state]) - self.Q[state][action])

    
    def set_policy(self, saveQtable, dir):
        '''
            Set the optimal policy for the agent
        '''
        if saveQtable:
            self.saveQtableToCsv(dir)
        
        policy = defaultdict(lambda: 0)
        for state, action in self.Q.items():
            policy[state] = np.argmax(action)
        self.policy = policy
    

    def save_policy(self, dir, name, savePolicytable):
        '''
            Save a policy after the learning process
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


    def load_policy(self, directory):
        '''
            Load an existing policy
        '''
        with open(directory, 'rb') as f:
            policy_new = pickle.load(f)
        self.policy = defaultdict(lambda:0, policy_new)  #salvata come defaultdict
        print('policy Loaded')

        
    def take_action(self,state):
        '''
            Choose the action to do accordirg to the policy
        '''
        return self.policy[state]