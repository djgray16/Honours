# -*- coding: utf-8 -*-
"""
Created on Thu Aug 18 11:09:35 2022

@author: djgra
"""
import networkx as nx
import numpy as np
import pandas as pd
## measuring graphs
from TAG import *
tests = 100

graphs_dict = {}
results = {}
graph_choices = ['WS', 'BA', 'RRG', 'TAG']

N = 500

m = 6
WS_p = 0.1
GNP_p = m/(N)
TAG_alpha = 0.3

for i in range(tests):
    for j in graph_choices:
        if j =='WS':
            G= nx.connected_watts_strogatz_graph(N,m,WS_p)
        elif j =='BA':
            G = nx.generators.random_graphs.barabasi_albert_graph(N, int(m/2),
                                                                    seed=None, 
                                                                   initial_graph=None)
        elif j =='RRG':
            G = nx.random_regular_graph(m, N)
        elif j =='TAG':
            G  = TAG(N,m,TAG_alpha)
        elif j =='GNP':
            G = nx.generators.random_graphs.gnp_random_graph(N,GNP_p)
        clus = nx.average_clustering(G)
        if nx.is_connected(G):
            aspl = nx.average_shortest_path_length(G)
        else:
            aspl = 'na'
        dd = [d for n, d in G.degree()]
        degree = np.mean(dd)
        variance = np.var(dd)
        results[(j,i)] = (clus,aspl,degree, variance)
        
df = pd.DataFrame.from_dict(results)

df = df.T

df = df.reset_index()

df['clus'] = df[0]
df['aspl'] = df[1]
df['deg'] = df[2]
df['var'] = df[3]

df = df.drop(['level_1',0,1,2,3], axis = 1)


df =df.set_index('level_0')

df.groupby('level_0').mean()


    


    