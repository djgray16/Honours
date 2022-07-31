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

    """ This is the PGG model I am using """
    


    def setup(self, **kwargs):

        self.gtype = self.p.gtype #what graph type for this model

        self.atype = self.p.atype #what agent type

        

        
        
        self.agents = ap.AgentList(self,self.p.agent_n, self.atype) #initialise agents
        #self.agents += ap.AgentList(self, self.p.agent2_n, self.a2type)#
        # line above is for adding multiple agents in one model
        
        
        
        n = len(self.agents) #this is useful as counts all agents,
        
        m = self.p.graph_m
               
        ### setup graph here###
        
        if self.gtype == 'WS':
            ## we have a connected-watts strogatz graph
            ## check the right parameters are given
            graph = nx.connected_watts_strogatz_graph(n,m,0.5)
        elif self.gtype == 'BA':
            
            ## we have a BA graph
            graph=nx.generators.random_graphs.barabasi_albert_graph(n, m,
                                                                    seed=None, 
                                                                    initial_graph=None)
        
            
        elif self.gtype == 'TAG':
            
            ## we have a tomassani antonioni graph
            graph = TAG(n,m,self.p.graph_alpha)
        else:
            print('no idea what graph you want')
            return
        if self.p.plot_G: #plotting tool
            plot_G(graph)
        
        

        
        self.network = self.agents.network = ap.Network(self, graph)
        self.network.add_agents(self.agents, self.network.nodes)# puts agents on nodes
           
        
        

    def step(self): #process that happens in order for every timestep
        
        self.agents.host_game()
        self.agents.calculate_pi()
        
        self.agents.contribute_choice()
        self.agents.update_contribute()

    def update(self): #happens after every timestep


        self.record('Cooperation_Level', adequate_coop(self.agents.contribute))
       
        self.agents.record('contribute')
        self.agents.record('last_give')
        self.agents.record('last_receive')

        self.agents.record('agent_class')

    def end(self): #end of experiment
        self.report('Final_Cooperation', adequate_coop(self.agents.contribute))
        #self.record('Current_Cooperation2',adequate_coop(self.agents.contribute) )
        pass

