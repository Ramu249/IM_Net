from IC import avgSize
import time
import matplotlib.pyplot as plt
#from degreeDiscount import degreeDiscountIC
#from CCHeuristic import CC_heuristic
#from newGreedyIC import newGreedyIC
import networkx as nx
#from singleDiscount import singleDiscount
#from plotVersusR import getDataTvsR
#from generalGreedy import generalGreedy
#from itertools import izip
#from randomHeuristic import randomHeuristic
from Algorithms import degreeHeuristic
from Algorithms import degreeHeuristic2
#######################################################
from IC import *
def degr(G1,G2):
    g1=dict(G1.degree)
    g2=dict(G2.degree)
    max1=max(g1,key=int)
    max2=max(g2,key=int)
    g1=list(G1.degree)
    g2=list(G2.degree)
    data1=[]
    if(max2>max1):
        for l in range(max2+1):
            a=[]
            x=0
            for j in range(len(g1)):
                if(l==g1[j][0]):
                    x=x+g1[j][1]
                    break
            for j in range(len(g2)):
                if(l==g2[j][0]):
                    x=x+g2[j][1]
                    break
            a.append(l)
            a.append(x)
            data1.append(a)
    else:
        for l in range(max1+1):
            a=[]
            x=0
            for j in range(len(g1)):
                if(l==g1[j][0]):
                    x=x+g1[j][1]
                    break
            for j in range(len(g2)):
                if(l==g2[j][0]):
                    x=x+g2[j][1]
                    break
            a.append(l)
            a.append(x)
            data1.append(a)
    return data1
if __name__ == "__main__":
    time2implement = time.time()
    time2build = time.time()
    G1 = nx.Graph()
    with open(r'C:\Users\VIT-AP\Desktop\New fold\TARE\Priya\influence-maximization-master to send\influence-maximization-master\graphdata\celegans_layer_gaps.txt') as f:
        n, m = f.readline().split()
        for line in f:
            u, v = map(int, line.split())
            try:
                G1[u][v]['weight'] += 1
            except:
                G1.add_edge(u,v, weight=1)
            # G.add_edge(u, v, weight=1)
    #print ('Built graph G')
    #print (time.time() - time2build)
        
    G2 = nx.Graph()
    with open(r'C:\Users\VIT-AP\Desktop\New fold\TARE\Priya\influence-maximization-master to send\influence-maximization-master\graphdata\celegans_layer_syn.txt') as f:
        n, m = f.readline().split()
        for line in f:
            u, v = map(int, line.split())
            try:
                G2[u][v]['weight'] += 1
            except:
                G2.add_edge(u,v, weight=1)
    print ("Started calculating data for plot time vs k")
    #data1 = getData(G, 10, degreeDiscountIC, .01, "size")
    #data2 = getData(G, 10, randomHeuristic, .01, "size")
    #data3 = getData(G, 10, singleDiscount, .01, "size")
    #data4 = getData(G, 10, degreeHeuristic, .01, "size")
    data1 = degreeHeuristic2(G1,.01)
    data2 = degreeHeuristic2(G2,.01)
    max1=data1[0][0]
    for i in range(G1.number_of_nodes()-1):
        if(data1[i+1][0]>max1):
              max1=data1[i][0]
    max2=data2[0][0]
    for i in range(G2.number_of_nodes()-1):
        if(data2[i+1][0]>max2):
              max2=data2[i][0]
    data3=[]
    if(max2>max1):
        for i in range(max2+1):
            a=[]
            x=0
            for j in range(G1.number_of_nodes()-1):
               if(i==data1[j][0]):
                   x=x+data1[j][1]
                   break
            for j in range(G2.number_of_nodes()-1):
               if(i==data2[j][0]):
                   x=x+data2[j][1]
                   break
            a.append(i)
            a.append(x)
            data3.append(a)
            
    else:
        for i in range(max1+1):
            a=[]
            x=0
            for j in range(G1.number_of_nodes()-1):
               if(i==data1[j][0]):
                   x=x+data1[j][1]
                   break
            for j in range(G2.number_of_nodes()-1):
               if(i==data2[j][0]):
                   x=x+data2[j][1]
                   break
            a.append(i)
            a.append(x)
            data3.append(a)
    temp=dict(data3)
    final=[]
    for i in range(len(data3)):
        u=max(temp,key=temp.get)
        degree=max(temp.values())
        temp.pop(u)
        final.append(u)
    print("Top 10 nodes are:")
    print(final[0:30])
    print("-----------------------------------")
    print("top 1o nodes are")
    temp1=degr(G1,G2)
    temp1=dict(temp1)
    final1=[]
    for i in range(len(temp1)):
        u=max(temp1,key=temp1.get)
        degree=max(temp1.values())
        temp1.pop(u)
        final1.append(u)
    print(final1[0:30])
