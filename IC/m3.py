#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 24 12:36:53 2019

@author: 18071001
"""

import time
import matplotlib.pyplot as plt
from degreeDiscount import degreeDiscountIC
import random
#from CCHeuristic import CC_heuristic
import networkx as nx
#from singleDiscount import singleDiscount
#from itertools import izip
# from randomHeuristic import randomHeuristic
from cpm import CPM
from Algorithms import degreeHeuristic
import matplotlib.path as mpath
import numpy as np
#######################################################
from IC import *
from clique1 import *
from generalGreedy import generalGreedy

#from avgshortestpath import *
def getdata1(G1,G2,algo,maxk,p):
    S1=list(G1.nodes)
    S2=list(G2.nodes)
    #print(algo,len(S1))
    #print(algo,len(S2))
    if algo=="CPM": 
        S1_maxk = algo(G1,4)
        print(len(S1_maxk))
        S2_maxk = algo(G2,4)
    else:
        S1_maxk = algo(G1,maxk,p)
        S2_maxk = algo(G2,maxk,p)
    #print(len(S2_maxk))
    S3=[]
    l=0
    for i in range(maxk):
        for j in range(len(S2)):
            if(S1_maxk[i]==S2[j]):
                if(S1_maxk[i] not in S3):
                    if(l==maxk):
                        return S3
                    else:
                        S3.append(S1_maxk[i])
                        l=l+1
                break
        for j in range(len(S1)):
            if(S2_maxk[i]==S1[j]):
                if(S2_maxk[i] not in S3):
                    if(l==maxk):
                        return S3
                    else:
                        S3.append(S2_maxk[i])
                        l=l+1
                break
    #print(len(S3))
    return S3





def getdata3(G1,G2,algo,maxk,p):
    S1=list(G1.nodes)
    S2=list(G2.nodes)
    print(algo,len(S1))
    print(algo,len(S2))
    S1_maxk=algo(G1,maxk,p)
    #print(len(S1_maxk))
    S2_maxk=algo(G2,maxk,p)
    #print(len(S2_maxk))
    print(S1)
    return S1,S2



def getdata2(F1,F2,S1,S2,maxk):
    F3=[]
    l=0
    for i in range(maxk):
        for j in range(len(S2)):
            if(F1[i]==S2[j]):
                if(F1[i] not in F3):
                    if(l==maxk):
                        return F3
                    else:
                        F3.append(F1[i])
                        l=l+1
        for j in range(len(S1)):
            if(F2[i]==S1[j]):
                if(F2[i] not in F3):
                    if(l==maxk):
                        return F3
                    else:
                        F3.append(F2[i])
                        l=l+1
    return F3
def getData (G1,G2, maxk, algo, p, axis):
    S3=""
    if(algo=="find_k_cliques"):
        F1=find_k_cliques(G1,maxk,p)
        F2=find_k_cliques(G2,maxk,p)
        S1=list(G1.nodes)
        S2=list(G2.nodes)
        print(len(F1),len(F2))
        S3=getdata2(F1,F2,S1,S2,maxk)
        #print("cliques", len(S3))
    else:
        if(algo=="CPM"):
            S3=getdata1(G1,G2,CPM,maxk,p)
            #print("Random", len(S3))
        if(algo=="degreeDiscountIC"):
            S3=getdata1(G1,G2,degreeDiscountIC,maxk,p)
        if(algo=="generalGreedy"):
            S3=getdata1(G1,G2,generalGreedy,maxk,p)
        if(algo=="degreeHeuristic"):
            S3=getdata1(G1,G2,degreeHeuristic,maxk,p)
        if(algo=="withDijkstra"):
            S3=getdata1(G1,G2,withDijkstra,maxk,p)
    data = dict()
    for k in range(maxk):
        if axis == "size" and algo=="CPM" and algo=="degreeDiscountIC" or algo=="generalGreedy" or algo=="degreeHeuristic" or algo=="find_k_cliques":
            #print("list of seed nodes are")
            #print(S)
            size1 = runIC(G1, S3[0:k+1], p)
            size2 = runIC(G2, S3[0:k+1], p)
            size=len(list(set(size1+size2)))
            #print(size)
            data[k] = size
#         elif axis == "size" and algo=="CPM":
#             size1 = runIC(G1, S3[0:k+1], p)
#             size2 = runIC(G2, S3[0:k+1], p)
#             size=len(list(set(size1+size2)))
#             #print(size)
#             data[k] = size
    return data
if __name__ == "__main__":
    time2implement = time.time()
    time2build = time.time()
    G1 = nx.Graph()
    with open(r'C:\Users\VIT-AP\Desktop\New fold\TARE\Priya\influence-maximization-master to send\influence-maximization-master\graphdata\celegans_layer_gaps.txt') as f:
        data = f.readlines()
    #print(data)
        for line in data:
            #coloumn2.append(line.split(" ")[1])
            u=line.split(" ")[1]
            v=line.split(" ")[2]
            try:
                G1[u][v]['weight'] += 1
            except:
                #G1.add_edge(u,v, weight=1)
                G1.add_edge(u,v, weight=random.random())
        
    G2 = nx.Graph()
    
    #coloumn2 = []
    with open(r'C:\Users\VIT-AP\Desktop\New fold\TARE\Priya\influence-maximization-master to send\influence-maximization-master\graphdata\celegans_layer_syn.txt') as f:
        data = f.readlines()
    #print(data)
        for line in data:
            #coloumn2.append(line.split(" ")[1])
            u=line.split(" ")[1]
            v=line.split(" ")[2]
            #print(u,v)
    
    #with open(r'celegans_layer_syn.txt') as f:
     #   n, m = f.readline().split()
     #   for line in f:
     #       u, v = map(int, line.split())
            try:
                G2[u][v]['weight'] += 1
            except:
                #G2.add_edge(u,v, weight=1)
                G2.add_edge(u,v, weight=random.random())
    
    fig = plt.figure()
    plot=list()
    algor=['degreeHeuristic','CPM','degreeDiscountIC','find_k_cliques']
    shape=['^','c','v','o']
    col=['orange','red','green', 'cyan','magenta']
    for i in range(len(algor)):
        data1=getData(G1,G2,50,algor[i],.01,"size")
        star = mpath.Path.unit_regular_star(6)
        circle = mpath.Path.unit_circle()
        verts = np.concatenate([circle.vertices, star.vertices[::-1, ...]])
        codes = np.concatenate([circle.codes, star.codes])
        cut_star = mpath.Path(verts, codes)
        d,= plt.semilogy(list(data1.keys()),list( data1.values()),'--', color=col[i])
        plot.append(d)
    #d2plt, = plt.semilogy(data2.keys(), data2.values(), 'b--')
    plt.xlabel("Seed set size k")
    plt.ylabel("# of Influenced nodes")
    plt.xlabel("Seed set size k")
    plt.ylabel("# of Influenced nodes")
    #plt.title("Running time for different k")
    plt.legend([plot[0],plot[1],plot[2],plot[3]],['degreeHeuristic','CPM','degreeDiscountIC','find_k_cliques'], loc=9)
    #plt.legend([plot[0]],["Degree hueristic"], loc=9)
    # plt.show()
    plt.yscale('linear')
    plt.show()
    fig.savefig('413.png', dpi=fig.dpi)
    console = []
