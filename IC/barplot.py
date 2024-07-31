import numpy as np
import matplotlib.pyplot as plt



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
from randomHeuristic import randomHeuristic
from Algorithms import degreeHeuristic
import matplotlib.path as mpath
import numpy as np
from singleDiscount import singleDiscount 
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
    S1_maxk=algo(G1,maxk,p)
    #print(len(S1_maxk))
    S2_maxk=algo(G2,maxk,p)
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
    #print(S1)
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
    tim=[0,0,0,0,0,0]
    if(algo=="randomHeuristic"):
            star = time.time()
            S3=getdata1(G1,G2,randomHeuristic,maxk,p)
            #print(S3)
            finis = time.time()
            tim[3]=finis - star
            #print("Random", len(S3))
    
    else:
        if(algo=="find_k_cliques"):
            start = time.time()
            F1=find_k_cliques(G1,maxk,p)
            F2=find_k_cliques(G2,maxk,p)
            S1=list(G1.nodes)
            S2=list(G2.nodes)
            #print(len(F1),len(F2))
            S3=getdata2(F1,F2,S1,S2,maxk)
            finish = time.time()
            tim[0]=finish - start
        #print("cliques", len(S3))
        if(algo=="degreeDiscountIC" and axis=="time"):
            start = time.time()
            S3=getdata1(G1,G2,degreeDiscountIC,maxk,p)
            #print(S3)
            finish = time.time()
            tim[2]=finish - start
        if(algo=="degreeHeuristic" and axis=="time"):
            start = time.time()
            S3=getdata1(G1,G2,degreeHeuristic,maxk,p)
            #print(S3)
            finish = time.time()
            tim[1]=finish - start
        if(algo=="singleDiscount" and axis=="time"):
            start = time.time()
            S3=getdata1(G1,G2,singleDiscount,maxk,p)
            #print(S3)
            finish = time.time()
            tim[4]=finish - start
        if(algo=="generalGreedy" and axis=="time"):
            start = time.time()
            S3=getdata1(G1,G2,singleDiscount,maxk,p)
            #print(S3)
            finish = time.time()
            tim[5]=finish - start
    return tim
        
if __name__ == "__main__":
    time2implement = time.time()
    time2build = time.time()
    G1 = nx.Graph()
    with open(r'C:\Users\VIT-AP\Desktop\New fold\TARE\Priya\influence-maximization-master\graphdata\homogenetic1.txt') as f:
        data = f.readlines()
    #print(data)
        for line in data:
            #coloumn2.append(line.split(" ")[1])
            u=line.split(" ")[1]
            v=line.split(" ")[2]
    
    #with open(r'celegans_layer_gaps.txt') as f:
     #   n, m = f.readline().split()
      #  for line in f:
       #     u, v = map(int, line.split())
            try:
                G1[u][v]['weight'] += 1
            except:
                #G1.add_edge(u,v, weight=1)
                G1.add_edge(u,v, weight=random.random())
            # G.add_edge(u, v, weight=1)
    #print ('Built graph G')
    #print (time.time() - time2build)
        
    G2 = nx.Graph()
    
    #coloumn2 = []
    with open(r'C:\Users\VIT-AP\Desktop\New fold\TARE\Priya\influence-maximization-master\graphdata\homogenetic2.txt') as f:
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
    algor=['degreeHeuristic', 'singleDiscount', 'generalGreedy' ,'randomHeuristic','degreeDiscountIC','find_k_cliques']
    for i in range(len(algor)):
        data1=getData(G1,G2,50,algor[i],.01,"time")
data2=[0.15560483932495117, 0.15560483932495117, 0.15560483932495117, 0.15560483932495117, 0.15560483932495117]

height = [3, 12, 5, 18, 45]
bars = ('A', 'B', 'C', 'D', 'E')
y_pos = np.arange(len(bars))

print(data1)     
bars = ('A', 'B', 'C', 'D', 'E', 'F')
y_pos = np.arange(len(bars))
plt.bar(y_pos, data1, color=['blue', 'red', 'green', 'blue', 'cyan','black'])
plt.xticks(y_pos, bars)
plt.show()
