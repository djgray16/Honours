# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 17:54:41 2022

@author: djgra
"""

'''to do

make a sampling algorithm for exp and power law graphs, with minimum degree
I think throwback is best
Then just sample from that, add graph with nodes '''

import agentpy as ap
import numpy as np
import random as random
import networkx as nx
import time
from TAG import *
from Agents import *
import math as math
import pandas as pd

n=1000

target_min = 3
target_avg = 9
def sf(n, target_min, target_avg):

    G = nx.scale_free_graph(n )
    
    #G = nx.barabasi_albert_graph(1000,4)
    
    G.remove_edges_from(nx.selfloop_edges(G))
    
    G = G.to_undirected()
    
    
    plot_G(G)
    
    
    degree_vals = [i[1] for i in list(G.degree)]
    print(min(degree_vals))
    
    print(sum(degree_vals)/len(degree_vals))
    
    
    while min(degree_vals)<target_min:
        to_be_removed = [x for  x in G.nodes() if G.degree(x) <= target_min]
        for i in to_be_removed:
            j = random.choice(list(G.nodes))
            G.add_edge(i,j)
            
        degree_vals =  [i[1] for i in list(G.degree)]
        print(min(degree_vals))
    
        print(sum(degree_vals)/len(degree_vals))
        print('run around')
        
    to_add = (target_avg - sum(degree_vals)/len(degree_vals))*n
    to_add  = int(to_add/2)
    print(to_add)
    i = 0
    while i<to_add:
        i+=1
        j = random.choice(list(G.nodes))
        k = random.choice(list(G.nodes))
        G.add_edge(j,k)
        
    G.remove_edges_from(nx.selfloop_edges(G))
        
    
        
    degree_vals =  [i[1] for i in list(G.degree)]
    print(min(degree_vals))
    
    print(sum(degree_vals)/len(degree_vals))
    print('run around')
    return G
def BA2(n,target_min,target_avg):
    G = nx.barabasi_albert_graph(n = n, m = int(target_avg/2))
    
    degree_vals = [i[1] for i in list(G.degree)]
    print(min(degree_vals))
    
    print(sum(degree_vals)/len(degree_vals))
    while min(degree_vals)<target_min:
        to_be_removed = [x for  x in G.nodes() if G.degree(x) < target_min]
        for i in to_be_removed:
            G.remove_node(i)
        degree_vals =  [i[1] for i in list(G.degree)]
        print(min(degree_vals))
    
        print(sum(degree_vals)/len(degree_vals))
        new_n = len(to_be_removed)
        target_m = (sum(degree_vals)/len(degree_vals) - target_avg)*n/(2*new_n)
        target_m = int(target_m)
        G = nx.barabsi_albert_graph(n = new_n, m = target_m)
        
        degree_vals = [i[1] for i in list(G.degree)]
        print(min(degree_vals))
    
        print(sum(degree_vals)/len(degree_vals))

    
    return G

BA2(n,target_min, target_avg)
            


