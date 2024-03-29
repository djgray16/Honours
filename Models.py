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

        #self.atype = self.p.atype #what agent type
        if self.p.atype =='ReplicatorLocal':
            self.atype = ReplicatorLocal
        elif self.p.atype =='AT':
            self.atype = AT
        elif self.p.atype =='Nau':
            self.atype = Nau
        elif self.p.atype =='ReplicatorGlobal':
            self.atype = ReplicatorGlobal
        elif self.p.atype =='BaseAgent':
            self.atype  = BaseAgent
        else:
            print('no idea what agent, setting baseagent')
            self.atype = BaseAgent
            return 
        

        

        
        self.agents = ap.AgentList(self,self.p.agent_n, self.atype) 
        #self.agents += ap.AgentList(self, self.p.agent2_n, self.a2type)#
        # line above is for adding multiple agents in one model
        
        
        
        n = self.p.agent_n #this is useful as counts all agents,
        
        m = self.p.graph_m
               
        ### setup graph here###
        
        if self.gtype == 'WS':
            ## we have a connected-watts strogatz graph
            ## check the right parameters are given
            graph = nx.connected_watts_strogatz_graph(n,m,self.p.graph_p)
        elif self.gtype == 'BA':
            
            ## we have a BA graph
            graph=nx.barabasi_albert_graph(n, int(m/2))
        
        elif self.gtype == 'RRG':
            graph = nx.random_regular_graph(m, n)
            
        elif self.gtype == 'CCG': #connected caveman
            l, rem = divmod(n,m+1)
            #print(f'warning, might be changing graph n by at most {rem}')
            graph = nx.connected_caveman_graph(l, m+1)
        elif self.gtype == 'TAG':
            
            ## we have a tomassani antonioni graph
            graph = TAG(n,m,self.p.graph_alpha)
        elif self.gtype =='PL':
            graph =nx.powerlaw_cluster_graph(n,int(m/2),self.p.power_p)
        elif self.gtype =='Star':
            graph = nx.star_graph(n-1)
        elif self.gtype =='Complete':
            graph = nx.complete_graph(n)
            
        else:
            print('no idea what graph you want')
            return
        if self.p.plot_G: #plotting tool
            plot_G(graph, title = self.gtype + str(n))
        
        

        
        self.network = self.agents.network = ap.Network(self, graph)
       #initialise agents
        
        self.network.add_agents(self.agents, self.network.nodes)# puts agents on nodes
        self.agents.network_setup() 
        
        

    def step(self): #process that happens in order for every timestep
        
        self.agents.host_game()
        self.agents.calculate_pi()
        
        self.agents.contribute_choice()
        self.agents.update_contribute()

    def update(self): #happens after every timestep


        self.record('Cooperation_Level', adequate_coop(self.agents.contribute))
        if self.p.step_reporting:
            pass
            self.agents.record('contribute')
            
        #self.agents.record('contribute')
        #self.agents.record('last_give')
        #self.agents.record('last_receive')

        #self.agents.record('agent_class')

    def end(self): #end of experiment
        if self.p.end_reporting:
            self.agents.record('degree')
            self.agents.record('next_contribute')
            #self.agents.record('mean_neighbour')
            #self.agents.record('contribute')
            #self.agents.record('Neighbour_Cooperation', np.mean([i.contribute for i in self.agents.true_neighbours]))
        #self.report('Final_Cooperation', adequate_coop(self.agents.contribute))
        #self.record('Current_Cooperation2',adequate_coop(self.agents.contribute) )
        pass


class LotteryModel(ap.Model):
    def setup(self):
        self.atype = self.p.atype
        self.agents = ap.AgentList(self,self.p.agents, self.atype)
        
    def step(self):
        self.agents.play_game()
        self.agents.contribute_choice()
        self.agents.update_contribute()
        
    def update(self):
        strategy_space = ['SS', 'RR', 'SR', 'RS', 'RwS', 'RwR']
        for i,c in enumerate(strategy_space):
            n_agents = len(self.agents.select(self.agents.strategy == c))
            self[c] = n_agents
            self.record(c)
            
        #self.record('SS', )
    def end(self):
        pass
