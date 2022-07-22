# -*- coding: utf-8 -*-
"""
Created on Sun Mar 27 19:53:37 2022

@author: djgra
"""
import agentpy as ap
import numpy as np
import random as random
import networkx as nx

from Agents import *
from TAG import *
class WealthModel(ap.Model):

    """ A simple model of random wealth transfers """
    
    def __init__(self,graphType,**kwargs):
        super().__init__(**kwargs)
        print(graphType)

    def setup(self):
        
        
        self.agents = ap.AgentList(self,self.p.AT, AT)
        #self.agents +=ap.AgentList(self, self.p.selfish_agents, Selfish)
        #self.current_coffers = 0
        #self.per_agent = 0
        self.prop_contributors = sum(agent.contribute for agent in self.agents)
        
        n = len(self.agents)
        m = self.p.graph_m
        #graph=nx.generators.random_graphs.barabasi_albert_graph(n, m, seed=None, initial_graph=None)
        
        #graph = TAG(n,m,self.p.graph_alpha) ##this is the line to change to change graphs
        #nx.draw(graph)
        #graph = nx.star_graph(n)
        #graph = nx.gnm_random_graph(n,m*n/2)
        graph = nx.connected_watts_strogatz_graph(n,m,0.5)
        self.network = self.agents.network = ap.Network(self, graph)
        self.network.add_agents(self.agents, self.network.nodes)
        
    def wealth_calculation(self):
        contribution = sum(agent.contribute for agent in self.agents)
        
        count_contributors = sum(agent.contribute>0.1 for agent in self.agents)
        self.prop_contributors = count_contributors/len(self.agents)
        contribution = contribution*self.p.phi
        self.current_coffers = contribution
        agent_payment = contribution/len(self.agents)
        self.per_agent = agent_payment
        
        
        
        

    def step(self):
        self.agents.games = 0
        self.agents.host_game()
        self.agents.contribute_choice()

        
        
        
        

    def update(self):

        #self.record('Gini Coefficient', gini(self.agents.wealth))
        self.record('Cooperation_Level', adequate_coop(self.agents.contribute))
        #self.record('per_agent')
        #self.record('Number Cooperators', self.agents.)
        #self.agents.record('wealth')
        #self.report('Current_Cooperation',adequate_coop(self.agents.contribute) )        
        self.agents.record('contribute')
        self.agents.record('last_give')
        self.agents.record('last_receive')

        self.agents.record('agent_class')

    def end(self):
        self.report('Final_Cooperation', adequate_coop(self.agents.contribute))
        #self.record('Current_Cooperation2',adequate_coop(self.agents.contribute) )
        pass

