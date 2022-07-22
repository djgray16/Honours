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

    """ An agent with wealth  who can choose to contribute. Other agents are 
    built off this"""

    def setup(self):

        self.last_receive = 1 #how much they last received
        self.last_give = 1 #how much they last gave



        
        
class AT(BaseAgent):
    
    '''This is the agent described in Antonioni and Tomassini papers. 
    They make a choice dependent initially, then adapt in steps of 0.25'''
    def setup(self):
        super().setup()
        self.agent_class =5
        self.games = 0
        self.choices = [0,0.25,0.5,0.75,1] #initial choice
        self.contribute = random.choice(self.choices)
        self.last_give = self.contribute
        self.last_receive = 0
        self.receipts = []
        
    def host_game(self):
        players = self.network.neighbors(self).to_list()

        players.append(self)

        contribution = sum(a.contribute for a in players)
        payout = self.model.p.phi*contribution/len(players)
        
        
        for a in players:
            a.record_game(payout)
        #nx.draw(self.network)
        
    def record_game(self,payout):
        self.games +=1
        self.receipts.append(payout)
        
        
    def contribute_choice(self):
        self.last_receive = sum(self.receipts)
        
        games = len(self.receipts)

        if games != self.games:
            print('number of games error', self.games, games)

        #this is the updated profit from correspondance
        self.pi = self.last_receive

        if self.pi>=2*games*self.contribute:
            
            #happy to increase or stay the same
            if random.random()>0.5:
                self.last_give = self.contribute
                self.contribute = min(self.contribute+0.25, 1.0)
                self.receipts = []
                #print('went up', self.last_give, self.contribute)
            
                
            else:
                self.last_give = self.contribute
                self.contribute = self.contribute
                self.receipts = []
                #print('held', self.last_give, self.contribute)
        else:
            #unhappy
            self.last_give = self.contribute
            self.contribute = max(0,self.contribute-0.25)
            self.receipts = []
            #print('down', self.last_give, self.contribute)