# -*- coding: utf-8 -*-
"""
Created on Sun Mar 27 19:38:01 2022

@author: djgra
"""

import networkx as nx
import numpy.random as random
import numpy as np
import matplotlib.pyplot as plt
import itertools
import numpy.random as rd
import pandas as pd

def TAG(N,K,alpha):
    ''' N is the number of nodes, K is the required mean degree, and alpha is the proportion of spatial vs degree driven links added. Alpha=1 implies totally degree given (BA). Currently, minor problem is that if there are no nodes that are not neighbors with at least 1 connection, it will fail to take the BA step and pass on that link. At the moment, the fix is to choose from so far unconnected nodes in the non-neighbor set. Other problem is when everything is already neighbors with a point, what to do? '''
    if N<K+1:
        print('Too few nodes, setting N = K+1')
    G = nx.Graph()
    G.add_node(0, pos = random.uniform(0.45,0.55,2))

    for i in range(1,K+1):
        position = random.uniform(0.45, 0.55,2)

        G.add_node(i, pos = position)
        
        #G.add_edge(i,i-1)


    for (a,b) in itertools.combinations(G.nodes,2):
        G.add_edge(a,b)
    for i in range(K+1,N):
        position=random.uniform(0,1,2)
        G.add_node(i, pos = position)    
        links = random.randint(1,K,1)[0]
        for j in range(links):
            if random.uniform(0,1)>alpha:
                #print('Distance style')

                ## distance based graph
                possibilities = [i for i in nx.non_neighbors(G,i)]
                #dist=np.linalg.norm(a-b)
                add_node = min(possibilities, key = lambda d: np.linalg.norm(G.nodes[d]['pos'] - G.nodes[i]['pos']))
                #print(i,add_node)
                G.add_edge(i,add_node)
            else:

                #print('BA style')
                if not nx.non_neighbors(G,i):
                    print('trouble')
                    break
                else:

                    repeated_nodes = [n for n, d in G.degree() for _ in range(d)]
                    #print(len([i for i in nx.non_neighbors(G,i)]))
                    nn = [ii for ii in nx.non_neighbors(G,i)]
                    #print(len(nn))
                    repeated_nodes = [z for z in repeated_nodes if z in nn]
                    if not repeated_nodes:
                        repeated_nodes = nn
                        print('trouble2 but not terrible using unattached neighbours')
                        
                    #print(i, repeated_nodes)
                    add_node = random.choice(repeated_nodes)
                    #print(add_node)
                    G.add_edge(i, add_node)
                ## barabasi albert style
    #degree_sequence = sorted((d for n, d in G.degree()), reverse=True)

    #print('returning', len(G), 'nodes, with mean degree', sum(degree_sequence)/len(degree_sequence))
    return G


            
def adequate_coop(x):
    """The proportion of agents who cooperated. Specifically for a list of agent bool decision variables"""
    tsum = sum(x)
    tprop = tsum/len(x)
    #print(tprop)
    return  tprop 


def plot_G(G, title ='Unnamed',ln = False):


    
    degree_sequence = sorted((d for n, d in G.degree()), reverse=True)
    dmax = max(degree_sequence)
    
    fig = plt.figure("Degree of a random graph", figsize=(8,8))
    # Create a gridspec for adding subplots of different sizes
    axgrid = fig.add_gridspec(5,4)
    

    
    ax1 = fig.add_subplot(axgrid[3:, :2])
    if ln:
        print('warning - dropping 0s')
        degree_sequence = [i for i in degree_sequence if i >0]
        degree_sequence = np.log(degree_sequence)
        
    ax1.plot(degree_sequence, "b-", marker="o")
    ax1.set_title("Degree Rank Plot of" + title + ' Graph')
    ax1.set_ylabel("Degree")
    ax1.set_xlabel("Rank")
    
    ax2 = fig.add_subplot(axgrid[3:, 2:])
    ax2.bar(*np.unique(degree_sequence, return_counts=True))
    ax2.set_title("Degree histogram")
    ax2.set_xlabel("Degree")
    ax2.set_ylabel("# of Nodes")
    
    fig.tight_layout()
    #fig.suptitle(title + str(ln))
    plt.show()
    
    

    
    
    
    
def SF(n, target_min, target_avg):
    '''to do
    make plot with log distribution
    consider if we can overestimate average degree
    can we make a lot and check that the average degree is fair
    when output, say if it is connected/average degree, minimum degree
    KS test to see if it scale-free
    check regression coefficient on log-plot'''
    
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


def make_sf(n,power,minimum,avg):
    

    a =  rd.default_rng().pareto(power-1, n) #making a scale-free distribution
    #with the right scale
    
    scale = (avg-minimum)/(np.mean(a) ) #
    
    a = minimum + scale*a
    a  =[round(i+0.01) for i in a]
    print(len(a))
    print(np.mean(a))
    
    ## adding in poisson rv i/N for each node, to estiamte the number of 
    #selfloops and add them now. 
    
    
    total = sum(a) 
    #params = [(i\total) for i in a]
    
    params = [(2*i/total) for i in range(len(a))]
    print(len(params))
    #params = 5
    poissons = [random.poisson(i) for i in params]
    
    print('estimated number of self-loops is', sum(poissons))
    
    a = [a[i]+poissons[i] for i in range(len(a))]
    print(len(a))
    print('passing degree sequence with mean',np.mean(a))
    if divmod(sum(a),2)[1] >0.5:
        print('trigger 1')
        a[0] +=1
        
    
    G = nx.configuration_model(a)
    G = nx.Graph(G)
    bb = np.mean([i[1] for i in G.degree])
    print(' mean degree, want to get to', avg, bb)
    
    print(', number of self-loops', nx.number_of_selfloops(G))    
    G.remove_edges_from(nx.selfloop_edges(G))
        
    #print('this number should be 0, remaining self-loops',
          #nx.number_of_selfloops(G)) 
    
    
    A = G.to_undirected()
    
    bb = np.mean([i[1] for i in A.degree])
    print(' mean degree, want to get to', avg, bb)
    return A


def make_exp(n, lam, minimum):
    a = rd.exponential(lam, n)
    
    a  =[minimum + round(i) for i in a]
    
    
    #a = [i for i in a if i>minimum-0.5]
    
    #print(a)
    
    if divmod(sum(a),2)[1] >0.5:
        a[0] +=1
    
    
    G = nx.configuration_model(a)
    
    
    #print(nx.number_of_selfloops(G))
    #print(len(list(nx.selfl)))
    for i in nx.selfloop_edges(G):
        G.remove_edge(*i)
        
    #print(nx.number_of_selfloops(G))
    
    A = G.to_undirected()
    
    return A   

    

def est_degree_graph(n, power, minimum, avg, log = False):
    '''
    this is currently the closest, and works well at hitting the targeted aver
    age except for the power law distribution, which needs work I think. 
    '''
        

    a =  rd.default_rng().pareto(power, n)*(power+1)/power
    #a = rd.default_rng().normal(0,power,n)#making a scale-free distribution
    #with the right scale
    
    scale = (avg-minimum)/(np.mean(a) ) #
    
    a = minimum + scale*a
    print(min(a))
    a  =[round(i) for i in a]
    #print(len(a))
    passed_degree_mean = np.mean(a)
    if log:
        print(passed_degree_mean)
    
    
    G = nx.expected_degree_graph(a, selfloops = False)
    
    bb = np.mean([i[1] for i in G.degree])
    if log:
        print(' mean degree, want to get to', avg, bb)
    
    G = nx.Graph(G)
    final = np.mean([i[1] for i in G.degree])
    if log:
        print(', number of self-loops', nx.number_of_selfloops(G)) 
        print(' mean degree, want to get to', avg, final)
    return G
    #return passed_degree_mean, bb, final

'''
sampling = {}

nn = 400
for i in range(nn):
    sampling[i] = est_degree_graph(1000, 2.5, 2, 6)
    
    
df = pd.DataFrame.from_dict(sampling).T

print(df.mean())
'''




