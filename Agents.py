# -*- coding: utf-8 -*-
"""
Created on Sun Mar 27 19:43:13 2022

@author: djgra
"""
import agentpy as ap
import numpy as np
import random as random
import networkx as nx
class BaseAgent(ap.Agent):
    ''' 
    This agent provides the structure for all other agent types. The main attributes
    of the agent are
    
    last_receive: what they received in the last game
    last_give: how much they contributed last time
    agent_class: int for identifying agents
    choices: in the case where discretisation is needed, breaks apart the unit int
    contribute: how much they are contributing in this round
    games: how many games they have played in the round
    receipts: a list of every payout they have received from each game in a round
    pi: revenue from the round
    next_contribute: how much they will give in the next round, and it is 
    changed to contribute after everyone has decided
    '''
    def __str__(self):
        return 'BaseAgent'
    

    def setup(self):
        '''
        parametrising as many values as possible.
        I am not convinced that last_receive, last_give, should start at 1, but 
        it is default for now
        '''

        self.last_receive = 1 #how much they last received
        self.last_give = 1 #how much they last gave
        self.agent_class = 0 # different class for every different type
        self.choices = [0,0.25,0.5,0.75,1] #useful for discretizing
        self.receipts = []
        self.games = 0
        self.contribute = random.choice(self.choices)
        self.next_contribute= self.contribute
        self.profit = 0
        
    def network_setup(self):
        self.neighbours = self.network.neighbors(self).to_list() 
        self.neighbours.append(self)
        self.true_neighbours = self.network.neighbors(self).to_list()
        #print(self.id, [i for i in self.neighbours])
        self.degree = len(self.true_neighbours)
    def host_game(self):
        '''
        finds the players neighbours, sums their contribution and multiplies
        by phi, and then tells each player their payout
        '''
        #players = self.network.neighbors(self).to_list() 

        #players.append(self)
        #print('hosting',self.id, [i.id for i in self.neighbours])
        contribution = sum(a.contribute for a in self.neighbours)
        payout = self.model.p.phi*contribution/(self.degree + 1)
        
        
        for a in self.neighbours:
            a.record_game(payout)
        #nx.draw(self.network)
        

        
    def record_game(self,payout):
        '''
        saves the payout, and updates the game ticker
        '''
        self.games +=1
        self.receipts.append(payout)

    def calculate_pi(self):
        '''
        should be done after each round. Collates receipts and calculates pi, 
        
        '''
        self.last_receive = sum(self.receipts)
        self.pi = self.last_receive
        self.profit = self.pi - self.games*self.contribute
        

    
    def contribute_choice(self):
        '''
        this is where each agent should be different. It is how they decide to
        modify their contribution for next round. For BaseAgent, I have chosen
        random to see if its working. Once they have decided, it is stored in 
        next_contribute.
        
        This is the synchronised method
        
        '''
        #self.last_give = self.contribute
        self.next_contribute = random.choice(self.choices)
        
    def update_contribute(self):
        '''
        now every agent moves to their new contribution, and receipts and 
        games are cleare
        '''
        self.receipts = []
        self.games = 0
        self.last_give = self.contribute
        self.contribute = self.next_contribute
        
        
        
        


class ReplicatorLocal(BaseAgent):
    ''' 
    agent that follows replicator dynamics. Iniitally chooses random contr
    
    This is the replicator dynamics specified by the bipartite graph paper, 
    Pena and Rochat. I couldn't emulate their paper as it is too large in timestep. '
    '''
    def __str__(self):
        return 'Replicator'
    def setup(self):
        super().setup()
        
        self.agent_class = 6  
        self.choices = [0,1]#[0,0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
        self.last_give = random.choice(self.choices)
        self.contribute = self.last_give 
        self.last_receive = 0
    '''
    def contribute_choice(self):
        neighbours = self.network.neighbors(self).to_list()
        neighbours += [self]
        possibilities = [(i.pi - i.contribute*i.games, i.contribute)
                         for i in neighbours if i.]
        assert all(i>0 for i in weights)
        
        draw = random.choices(neighbours, weights = weights)
        self.next_contribute = draw[0].contribute
        #print(self.contribute, self.next_contribute)
    '''
        
      
    def contribute_choice(self):       
        neighbours = self.true_neighbours
        
        #print(self.id, [i.id for i in neighbours])
        #neighbours.remove(self)
        #print(self.pi)
        #print([ i.pi for i in neighbours])
        a =self.model.p.replicator_alpha
        scale= max(i.profit for i in neighbours)
        if self.model.p.extended_reporting:
            mean_neighbour = np.mean([i.contribute for i in neighbours])
            self.mean_neighbour = mean_neighbour
        
        neighbour = random.choice(neighbours)
        #self.last_give = self.contribute
        #self.contribute  = 1

        if neighbour.profit> self.profit:
            ## we are a chance of changing strat
            if scale ==0:
                scale = 1
            prob = ((neighbour.pi - self.pi)/scale)**a
            if prob>random.random():
                self.next_contribute = neighbour.contribute
                
            
                # we need to make a new_contribute, and not change that 
               # until the end of the round, so we are copying properly
                
                #self.contribute = neighbour.contribute
        else:
            self.next_contribute = self.contribute
            
            
class ReplicatorGlobal(BaseAgent):
    ''' 
    agent that follows global replicator dynamics. Iniitally chooses random contr
    
    This is the replicator dynamics specified by the bipartite graph paper, 
    Pena and Rochat. I couldn't emulate their paper as it is too large in timestep. '
    '''
    def __str__(self):
        return 'ReplicatorGlobal'
    def setup(self):
        super().setup()
        
        self.agent_class = 7  
        self.choices = [0,1]#[0,0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
        self.last_give = random.choice(self.choices)
        self.contribute = self.last_give 
        self.last_receive = 0
    '''
    def contribute_choice(self):
        neighbours = self.network.neighbors(self).to_list()
        neighbours += [self]
        possibilities = [(i.pi - i.contribute*i.games, i.contribute)
                         for i in neighbours if i.]
        assert all(i>0 for i in weights)
        
        draw = random.choices(neighbours, weights = weights)
        self.next_contribute = draw[0].contribute
        #print(self.contribute, self.next_contribute)
    '''
        
      
    def contribute_choice(self):       
        #neighbours = self.true_neighbours
        neighbours = self.model.agents
        
        #print(self.id, [i.id for i in neighbours])
        #neighbours.remove(self)
        #print(self.pi)
        #print([ i.pi for i in neighbours])
        a =self.model.p.replicator_alpha
        scale= max(i.profit for i in neighbours)
        
        neighbour = random.choice(neighbours)
        #self.last_give = self.contribute
        #self.contribute  = 1

        if neighbour.profit> self.profit:
            ## we are a chance of changing strat
            prob = ((neighbour.pi - self.pi)/scale)**a
            if prob>random.random():
                self.next_contribute = neighbour.contribute
                
            
                # we need to make a new_contribute, and not change that 
               # until the end of the round, so we are copying properly
                
                #self.contribute = neighbour.contribute
        else:
            self.next_contribute = self.contribute
        
            



        
    
        
        
class AT(BaseAgent):
    
    '''This is the agent described in Antonioni and Tomassini papers. 
    They make a choice dependent initially, then adapt in steps of 0.25'''
    def __repr__(self):
        return 'AT'
    def setup(self):
        super().setup()
        self.agent_class =5
        #self.games = 0
        #self.choices = [0,0.25,0.5,0.75,1] #initial choice
        self.contribute = random.choice(self.choices)
        self.last_give = self.contribute
        self.last_receive = 0
        #self.receipts = []
        

        
        
    def contribute_choice(self):


        if self.pi>=2*self.games*self.contribute:
            
            #happy to increase or stay the same
            if random.random()>0.5:
                #self.last_give = self.contribute
                self.next_contribute = min(self.contribute+0.25, 1.0)
                #self.receipts = []
                #print('went up', self.last_give, self.contribute)
            
                
            else:
                #self.last_give = self.contribute
                self.next_contribute = self.contribute
                #self.receipts = []
                #print('held', self.last_give, self.contribute)
        else:
            #unhappy
            #self.last_give = self.contribute
            self.next_contribute = max(0,self.contribute-0.25)
            #self.receipts = []
            #print('down', self.last_give, self.contribute)
            
            
class Nau(ap.Agent):
    def setup(self):
        d,_ = divmod(self.model.p.agents,3)
        if self.id <=d:
            self.strategy = 'RwS'
        elif self.id <= 2*d:
            self.strategy = 'RS'
        elif self.id<=3*d:
            self.strategy = 'SS'
        elif self.id <=4*d:
            self.strategy = 'RwS'
        elif self.id <=5*d:
            self.strategy = 'SR'
        elif self.id <=6*d:
            self.strategy = 'SS'
        else:
            print('agent id error')
            
            
        
    def play_game(self):
        prob = 1-self.model.p.lottery_p
        if self.strategy == 'SS':
            self.pi = 8
        elif self.strategy == 'RR':
            self.pi = 8*int(random.random()>prob) + 8*int(random.random()>prob)
            return
        elif self.strategy == 'RS':
            self.pi = 8*int(random.random()>prob) + 4
            return
        elif self.strategy == 'SR':
            self.pi = 8*int(random.random()>prob) +4 
            return
        elif self.strategy == 'RwS':
            self.pi = 8*int(random.random()>prob)
            if self.pi>3:
                self.pi +=4
            else:
                self.pi += 8*int(random.random()>prob)
                return
            return
        elif self.strategy == 'RwR':
            self.pi = 8*int(random.random()>prob)
            if self.pi>3:
                self.pi += 8*int(random.random()>prob)
                return
            else:
                self.pi += 4
                return
            return
        else:
            print('screwed up strategies')
            
        
        pass
    def contribute_choice(self):
        delta = 16-self.pi
        delta = 16
        
        if self.pi ==16:
            self.new_strategy = self.strategy
            
        
        observed = random.choice(self.model.agents)
        a = self.model.p.alpha
        q = ((observed.pi - self.pi)/delta)**a
        if (observed.pi - self.pi)>0 and q>=random.random():
            #print('changing strat', self.pi, observed.pi,q,self.strategy, observed.strategy)
            self.new_strategy = observed.strategy
            return
        else:
            self.new_strategy = self.strategy
            return
        
        
        
        
        
    def update_contribute(self):
        self.strategy= self.new_strategy
        self.new_strategy = 0
    