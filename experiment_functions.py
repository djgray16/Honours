# -*- coding: utf-8 -*-
"""
Created on Fri Sep  9 12:43:43 2022

@author: s4482670
"""


import agentpy as ap
import numpy as np
import random as random
import networkx as nx

from TAG import *
from Agents import *
from Models import *
import math

# Visualization
#import seaborn as sns

import matplotlib.pyplot as plt



def experiment(parameters, control_board):
    

    ''' needs parameters for the experiment, control board for everything else
    '''
    
    
    run = control_board['run'] 
    #v2 = control_board['v2'] 
    save = control_board['save'] 
    title = control_board['title'] 
    filename = control_board['filename'] 
    reps = control_board['reps']
    CI = control_board['CI']
    MeansOnly = control_board['MeansOnly']
    legend = control_board['legend'] 
    
    assert save*legend <1
    
    
    sample = ap.Sample(
        parameters,
        n=1,
        method='linspace'
        )
    
    exp = ap.Experiment(WealthModel, sample, iterations=reps,
                    record = True)

    if run:
        results = exp.run()
        
        
    ### PLotting 
    
    
    phis = results.parameters.sample.phi
    
    colours = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown',\
               'tab:pink','tab:olive', 'tab:cyan', 'tab:gray' ]
        
    
    markers =['o', '*', 'x', 'p', 's', 'd', 'p', 'h']
    #colours = colours[:len(phis)]
    
    
    coops = results.variables.WealthModel.Cooperation_Level.groupby(['t', 'sample_id']).mean()
    
    pct_up = results.variables.WealthModel.Cooperation_Level.groupby(['t', 'sample_id']).quantile(0.975)
    if CI:
        pct_up = coops + 1/math.sqrt(reps)*1.96*results.variables.WealthModel.Cooperation_Level.groupby(['t', 'sample_id']).std()
    pct_up = pct_up.rename('q_up')
    pct_down = results.variables.WealthModel.Cooperation_Level.groupby(['t', 'sample_id']).quantile(0.025)
    if CI:
        pct_down = coops - 1/math.sqrt(reps)*1.96*results.variables.WealthModel.Cooperation_Level.groupby(['t', 'sample_id']).std()
    
    pct_down = pct_down.rename('q_down')
    
    ts = coops.index
    ts = ts.get_level_values(0).unique()
    
    df = results.parameters.sample
    coops2 = coops.to_frame().join(df).join(pct_up).join(pct_down)
    
    phi_graph = coops2.groupby(['t', 'phi']).mean()

    fig, ax = plt.subplots()
    for i in range(len(phis)):
        #print(i)
        y1 = phi_graph.Cooperation_Level.iloc[phi_graph.index.get_level_values('phi') == phis[i]]
        y2 = phi_graph.q_down.iloc[phi_graph.index.get_level_values('phi') == phis[i]]
        y3 = phi_graph.q_up.iloc[phi_graph.index.get_level_values('phi') == phis[i]]
        x = phis.index
        #plt.legend(phis.unique())
        #print(len(colours), len(markers), len(phis))
        ax.plot(ts,y1, c=colours[i],marker = markers[i], markevery = 0.05,ms = 5,linewidth = 1.75, label = f'r = {phis[i]}') #
        if not MeansOnly:
            ax.plot(ts,y2,  c=colours[i], linestyle = 'dashed', label = f'_5th Percentile of {phis[i]}', markevery = 0.1, alpha = 0.6 )
            ax.plot(ts,y3,  c=colours[i], linestyle =  'dashed', label = f'_95th Percentile of {phis[i]}' ,markevery = 0.1, alpha = 0.6)
        
    if legend:
        ax.legend( loc='lower right')
    ax.set_ylabel('Mean Cooperation')
    ax.set_xlabel('Round')
    ax.set_yticks(ticks = [0,0.2,0.4,0.6,0.8,1.0])
    
    #plt.rcParams["figure.figsize"] = (10,10)
    
    fig.suptitle(f"{title}") #"; N: {parameters['agent_n']} "\
              #f"k: {parameters['graph_m']}, T: {reps}, alpha: {parameters['graph_alpha']} ")
        
    '''   
    plt.title(f' {parameters["agent_n"]} agents,' \
    f'graph: {parameters["gtype"]}, agents: {parameters["atype"]}, graph_alpha: ' \
        f'{parameters["graph_alpha"]}, m: {parameters["graph_m"]}: replicator_alpha:'\
            f' {parameters["replicator_alpha"]}, CI: {CI}'
              )No 
        
    '''   
    
    
    if save: 
        plt.savefig(f'Overleaf/images/{filename}.pdf')
        print(f'saved fig: {title} as {filename}')
        #plt.close(fig)
    return 

def run_compare_two(parameters, control_board):
    run = control_board['run'] 
    v2 = control_board['v2'] 
    save = control_board['save'] 
    title = control_board['title'] 
    filename = control_board['filename'] 
    reps = control_board['reps'] 
    MeansOnly = control_board['MeansOnly']
    CI = control_board['CI']
    legend = control_board['legend']
    
    
    sample = ap.Sample(
        parameters,
        n=1,
        method='linspace'
    )
    
    assert len(parameters['phi'])==4
    
    exp = ap.Experiment(WealthModel, sample, iterations=reps,
                    record = True)
    
    if run:
        results = exp.run()
        
    psample =  results.parameters.sample
    
    summary = results.variables.WealthModel.Cooperation_Level.groupby(['t', 'sample_id']).agg([np.mean, np.std, lambda x: x.quantile(0.025), lambda x:x.quantile(0.975)])

    summary.rename(columns = {'mean': 'avg', 'std': 'dev','<lambda_0>': 'q_low', '<lambda_1>': 'q_high'}, inplace = True)

    pickle_save = {'psample': psample, 'summary': summary}
    
    
    return pickle_save

def plot_compare_two(results, control_board):
    run = control_board['run'] 
    v2 = control_board['v2'] 
    save = control_board['save'] 
    title = control_board['title'] 
    filename = control_board['filename'] 
    reps = control_board['reps'] 
    MeansOnly = control_board['MeansOnly']
    CI = control_board['CI']
    legend = control_board['legend']
    colours = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown',\
           'tab:pink','tab:olive', 'tab:cyan', 'tab:gray' ]
    
    
    markers =['o','*', 'x', 'p', 's', 'd', 'p', 'h']
        
    phis = results.parameters.sample.phi
    colours = colours[:len(phis)]
    
    coops = results.variables.WealthModel.Cooperation_Level.groupby(['t', 'sample_id']).mean()
    
    
    ts = coops.index
    ts = ts.get_level_values(0).unique()
    
    df = results.parameters.sample
    coops2 = coops.to_frame().join(df)
    
    phi_graph = coops2.groupby(['t', 'phi', v2]).mean()
    if not MeansOnly:
        q_up = results.variables.WealthModel.Cooperation_Level.groupby(['t', 'sample_id']).quantile(0.975)
        q_down = results.variables.WealthModel.Cooperation_Level.groupby(['t', 'sample_id']).quantile(0.025)
        if CI:
            q_up = coops + 1.96/math.sqrt(reps)*results.variables.WealthModel.Cooperation_Level.groupby(['t', 'sample_id']).std()
            q_down = coops - 1.96/math.sqrt(reps)*results.variables.WealthModel.Cooperation_Level.groupby(['t', 'sample_id']).std()
            
        q_up = q_up.to_frame().join(df)
        q_down = q_down.to_frame().join(df)
        q_up = q_up.groupby(['t', 'phi', v2]).mean()
        q_down = q_down.groupby(['t', 'phi', v2]).mean()
        q_up = q_up.reset_index()
        q_down = q_down.reset_index()
        
    phi_graph = phi_graph.reset_index()
    graphs = results.parameters.sample[v2]
    
    fig,axs = plt.subplots(2,2, sharex = True, sharey = True)
    fig.suptitle(f'{title}')
        
    axesx = [0,0,1,1]
    axesy = [0,1,0,1]
    for i in range(len(phis.unique())):
        
        testing =phi_graph[phi_graph.phi ==phis.unique()[i]]
        
        if not MeansOnly:
            quant_up = q_up[q_up.phi==phis.unique()[i]]
            
            quant_down =  q_down[q_down.phi==phis.unique()[i]]
            if CI:
                pass
                #quant_up = tt+1.96/math.sqrt(reps)*testing.groupby(['t',v2]).std()
                #quant_down = tt-1.96/math.sqrt(reps)*testing.groupby(['t',v2]).std()
                
        for j in range(len(graphs.unique())):
            tt = testing.groupby(['t',v2]).mean()
            
            
            ys = tt.Cooperation_Level.iloc[tt.index.get_level_values(v2)==graphs.unique()[j]]
            axs[axesx[i], axesy[i]].set_title(f' r: {phis.unique()[i]}')
            axs[axesx[i], axesy[i]].set_ylim(0,1)
            axs[axesx[i], axesy[i]].plot(ts,ys,marker =markers[j], markevery = 0.5,ms = 5,linewidth = 1.75, c= colours[j], label = graphs.unique()[j])
            if not MeansOnly:
                qq_up = quant_up.groupby(['t',v2]).mean()
                qq_down = quant_down.groupby(['t',v2]).mean()
                y2s = qq_up.Cooperation_Level.iloc[tt.index.get_level_values(v2)==graphs.unique()[j]]
                #print(y2s-ys)
                
                y3s = qq_down.Cooperation_Level.iloc[tt.index.get_level_values(v2)==graphs.unique()[j]]
                #print(y3s-ys)
                axs[axesx[i], axesy[i]].plot(ts,y2s,linestyle = 'dashed', c = colours[j], alpha = 0.6,linewidth = 1.75, label = 'quant_up')
                axs[axesx[i], axesy[i]].plot(ts,y3s,linestyle = 'dashed', c = colours[j], alpha = 0.6,linewidth = 1.75)
    return fig, axs
    

def compare_two(parameters, control_board):
    '''to make the 4 subplots graph. needs parameters as usual
    then a control board consisting of 
    run, v2, save,title, filename, reps = control_board
    '''

        
    run = control_board['run'] 
    v2 = control_board['v2'] 
    save = control_board['save'] 
    title = control_board['title'] 
    filename = control_board['filename'] 
    reps = control_board['reps'] 
    MeansOnly = control_board['MeansOnly']
    CI = control_board['CI']
    legend = control_board['legend']
    
    
    sample = ap.Sample(
        parameters,
        n=1,
        method='linspace'
    )
    
    assert len(parameters['phi'])==4
    
    exp = ap.Experiment(WealthModel, sample, iterations=reps,
                    record = True)
    
    if run:
        results = exp.run()
        pass
    colours = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown',\
           'tab:pink','tab:olive', 'tab:cyan', 'tab:gray' ]
    
    
    markers =['o','*', 'x', 'p', 's', 'd', 'p', 'h']
        
    phis = results.parameters.sample.phi
    colours = colours[:len(phis)]
    
    coops = results.variables.WealthModel.Cooperation_Level.groupby(['t', 'sample_id']).mean()
    
    
    ts = coops.index
    ts = ts.get_level_values(0).unique()
    
    df = results.parameters.sample
    coops2 = coops.to_frame().join(df)
    
    phi_graph = coops2.groupby(['t', 'phi', v2]).mean()
    if not MeansOnly:
        q_up = results.variables.WealthModel.Cooperation_Level.groupby(['t', 'sample_id']).quantile(0.975)
        q_down = results.variables.WealthModel.Cooperation_Level.groupby(['t', 'sample_id']).quantile(0.025)
        if CI:
            q_up = coops + 1.96/math.sqrt(reps)*results.variables.WealthModel.Cooperation_Level.groupby(['t', 'sample_id']).std()
            q_down = coops - 1.96/math.sqrt(reps)*results.variables.WealthModel.Cooperation_Level.groupby(['t', 'sample_id']).std()
            
        q_up = q_up.to_frame().join(df)
        q_down = q_down.to_frame().join(df)
        q_up = q_up.groupby(['t', 'phi', v2]).mean()
        q_down = q_down.groupby(['t', 'phi', v2]).mean()
        q_up = q_up.reset_index()
        q_down = q_down.reset_index()
        
    phi_graph = phi_graph.reset_index()
    graphs = results.parameters.sample[v2]
    
    fig,axs = plt.subplots(2,2, sharex = True, sharey = True)
    fig.suptitle(f'{title}')
        
    axesx = [0,0,1,1]
    axesy = [0,1,0,1]
    for i in range(len(phis.unique())):
        
        testing =phi_graph[phi_graph.phi ==phis.unique()[i]]
        
        if not MeansOnly:
            quant_up = q_up[q_up.phi==phis.unique()[i]]
            
            quant_down =  q_down[q_down.phi==phis.unique()[i]]
            if CI:
                pass
                #quant_up = tt+1.96/math.sqrt(reps)*testing.groupby(['t',v2]).std()
                #quant_down = tt-1.96/math.sqrt(reps)*testing.groupby(['t',v2]).std()
                
        for j in range(len(graphs.unique())):
            tt = testing.groupby(['t',v2]).mean()
            
            
            ys = tt.Cooperation_Level.iloc[tt.index.get_level_values(v2)==graphs.unique()[j]]
            axs[axesx[i], axesy[i]].set_title(f' r: {phis.unique()[i]}')
            axs[axesx[i], axesy[i]].set_ylim(0,1)
            axs[axesx[i], axesy[i]].plot(ts,ys,marker =markers[j], markevery = 0.1,ms = 5,linewidth = 1.75, c= colours[j], label = graphs.unique()[j])
            if not MeansOnly:
                qq_up = quant_up.groupby(['t',v2]).mean()
                qq_down = quant_down.groupby(['t',v2]).mean()
                y2s = qq_up.Cooperation_Level.iloc[tt.index.get_level_values(v2)==graphs.unique()[j]]
                #print(y2s-ys)
                
                y3s = qq_down.Cooperation_Level.iloc[tt.index.get_level_values(v2)==graphs.unique()[j]]
                #print(y3s-ys)
                axs[axesx[i], axesy[i]].plot(ts,y2s,linestyle = 'dashed', c = colours[j], alpha = 0.6,linewidth = 1.75, label = 'quant_up')
                axs[axesx[i], axesy[i]].plot(ts,y3s,linestyle = 'dashed', c = colours[j], alpha = 0.6,linewidth = 1.75)
                
            
                
            
            
    handles, labels = axs[-1][-1].get_legend_handles_labels()
    if legend:
        fig.legend(handles, labels, loc='lower left')
    
    
    for ax in axs.flat:
        ax.set(xlabel = 'Steps')
        ax.set(ylabel = 'Cooperation')
        ax.label_outer()
        ax.set_yticks(ticks = [0,0.2,0.4,0.6,0.8,1.0])
        
    #fig.set_size_inches(7,5)
    
    
    if save: 
        plt.savefig(f'Overleaf/images/{filename}.pdf')
        print(f'saved fig: {title} as {filename}')
        #plt.close(fig)

  
    return
    
    
def lottery(parameters, control_board):
    run = control_board['run'] 
    #v2 = control_board['v2'] 
    save = control_board['save'] 
    title = control_board['title'] 
    filename = control_board['filename'] 
    reps = control_board['reps']
    CI = control_board['CI']
    MeansOnly = control_board['MeansOnly']
    legend = control_board['legend']
    
    assert legend*save <0.5
    
    
    sample = ap.Sample(
        parameters,
        n=1,
        method='linspace'
    )
    
    
    exp = ap.Experiment(LotteryModel, sample, iterations=reps,
                        record = True)
    if run:
        results = exp.run()
    
    props = results.variables.LotteryModel.groupby(['t']).mean()
    
    pct_up = results.variables.LotteryModel.groupby(['t']).quantile(0.975)
    pct_down = results.variables.LotteryModel.groupby(['t']).quantile(0.025)
    
    if CI:
        pct_up = props + 1/math.sqrt(reps)*1.96*results.variables.LotteryModel.groupby(['t']).std()
        pct_down = props - 1/math.sqrt(reps)*1.96*results.variables.LotteryModel.groupby(['t']).std()
    #pct_up = pct_up.rename('q_up')
    #pct_down = pct_up.rename('q_down')
    colours = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown',\
               'tab:pink','tab:olive', 'tab:cyan', 'tab:gray' ]
    markers =['o', '*', 'x', 'p', 's', 'd', 'p', 'h']
    
    
    fig, ax = plt.subplots()
    
    for i in range(len(props.columns)):
        y = props[props.columns[i]]
        y1 = pct_up[props.columns[i]]
        y2 = pct_down[props.columns[i]]
        x = props.index
        ax.plot(x,y, c= colours[i], marker = markers[i], markevery = 0.05, ms = 5, linewidth = 2.0)
        if not MeansOnly:
            ax.plot(x,y1, c = colours[i], linestyle = 'dashed', marker = markers[i], markevery = 0.1,ms = 5, alpha = 0.6)
            ax.plot(x,y2,c = colours[i],linestyle = 'dashed', marker = markers[i], markevery = 0.1, ms = 5,alpha = 0.6)
    if legend:
        ax.legend(props.columns)
    ax.set_xlabel('Generation')
    ax.set_ylabel('Count of Agents')
    ax.set_ylim(0,parameters['agents'])
    fig.suptitle(f'{title}')
    
    if save: 
        plt.savefig(f'Overleaf/images/{filename}.pdf')
        print('saved',title, f'as {filename}' )
        #plt.close(fig)
    return 


def plot_compare_two_from_pickle(pickle_in, control_board):
    run = control_board['run'] 
    v2 = control_board['v2'] 
    save = control_board['save'] 
    title = control_board['title'] 
    filename = control_board['filename'] 
    reps = control_board['reps'] 
    MeansOnly = control_board['MeansOnly']
    CI = control_board['CI']
    legend = control_board['legend']
    colours = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown',\
           'tab:pink','tab:olive', 'tab:cyan', 'tab:gray' ]
    
    
    markers =['o','*', 'x', 'p', 's', 'd', 'p', 'h']
    psample = pickle_in['psample']
    summary = pickle_in['summary']
    phis = psample.phi
    colours = colours[:len(phis)]
    
    coops = summary.avg
    
    
    ts = coops.index
    ts = ts.get_level_values(0).unique()
    
    df = psample
    coops2 = coops.to_frame().join(df)
    
    phi_graph = coops2.groupby(['t', 'phi', v2]).mean()
    if not MeansOnly:
        q_up = summary.q_high
        q_down = summary.q_low
        if CI:
            q_up = coops + 1.96/math.sqrt(reps)*summary.std
            q_down = coops - 1.96/summary.std
            
        q_up = q_up.to_frame().join(df)
        q_down = q_down.to_frame().join(df)
        q_up = q_up.groupby(['t', 'phi', v2]).mean()
        q_down = q_down.groupby(['t', 'phi', v2]).mean()
        q_up = q_up.reset_index()
        q_down = q_down.reset_index()
        
    phi_graph = phi_graph.reset_index()
    graphs = psample[v2]
    
    fig,axs = plt.subplots(2,2, sharex = True, sharey = True)
    fig.suptitle(f'{title}')
        
    axesx = [0,0,1,1]
    axesy = [0,1,0,1]
    for i in range(len(phis.unique())):
        
        testing =phi_graph[phi_graph.phi ==phis.unique()[i]]
        
        if not MeansOnly:
            quant_up = q_up[q_up.phi==phis.unique()[i]]
            
            quant_down =  q_down[q_down.phi==phis.unique()[i]]
            if CI:
                pass
                #quant_up = tt+1.96/math.sqrt(reps)*testing.groupby(['t',v2]).std()
                #quant_down = tt-1.96/math.sqrt(reps)*testing.groupby(['t',v2]).std()
                
        for j in range(len(graphs.unique())):
            tt = testing.groupby(['t',v2]).mean()
            #print(tt.head())
            
            ys = tt.iloc[tt.index.get_level_values(v2)==graphs.unique()[j]]
            axs[axesx[i], axesy[i]].set_title(f' r: {phis.unique()[i]}')
            axs[axesx[i], axesy[i]].set_ylim(0,1)
            axs[axesx[i], axesy[i]].plot(ts,ys,marker =markers[j], markevery = 0.5,ms = 5,linewidth = 1.75, c= colours[j], label = graphs.unique()[j])
            if not MeansOnly:
                qq_up = quant_up.groupby(['t',v2]).mean()
                qq_down = quant_down.groupby(['t',v2]).mean()
                y2s = qq_up.iloc[tt.index.get_level_values(v2)==graphs.unique()[j]]
                #print(y2s-ys)
                
                y3s = qq_down.iloc[tt.index.get_level_values(v2)==graphs.unique()[j]]
                #print(y3s-ys)
                axs[axesx[i], axesy[i]].plot(ts,y2s,linestyle = 'dashed', c = colours[j], alpha = 0.6,linewidth = 1.75, label = 'quant_up')
                axs[axesx[i], axesy[i]].plot(ts,y3s,linestyle = 'dashed', c = colours[j], alpha = 0.6,linewidth = 1.75)
    if legend:
        fig.legend( loc='lower right')
    for ax in axs.flat:
        ax.set(xlabel = 'Steps')
        ax.set(ylabel = 'Mean Cooperation')
        ax.label_outer()
        ax.set_yticks(ticks = [0,0.2,0.4,0.6,0.8,1.0])
    return fig, axs




def q_low(data):
    return data.quantile(q=0.025)
def q_high(data):
    return data.quantile(q=0.975)


