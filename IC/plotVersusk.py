
from IC import avgSize
import time
import matplotlib.pyplot as plt
from degreeDiscount import degreeDiscountIC
#from CCHeuristic import CC_heuristic
#from newGreedyIC import newGreedyIC
import networkx as nx
from singleDiscount import singleDiscount
#from plotVersusR import getDataTvsR
from generalGreedy import generalGreedy
#from itertools import izip
from randomHeuristic import randomHeuristic
from degreeHeuristic import degreeHeuristic
from degreeHeuristic import Avg

"""def getData (G, maxk, algo, p, axis):
    data = dict()
    for k in range(1,maxk+1):
        if axis == "size":
            
            S = algo(G, k, p)
            #size = avgSize(G, S, p, 200)
            #data[k] = size
            data[k] = S
            
        elif axis == "time":
            start = time.time()
            S = algo(G, k, p)
            #print(S)
            finish = time.time()
            data[k] = finish - start
    return data"""

def getData (G1, G2, maxk, algo, p, axis):
    data = dict()
    #k=0
    for k in range(1,maxk+1):
        if axis == "size":
            #k=G.no_of_nodes()    
            S = algo(G1,G2,k)
            size = avgSize(G2,S,p,200)
            data[k] = size
            #data[k] = S
            #print(data[k])
            
        elif axis == "time":
            start = time.time()
            S = algo(G, k, p)
            #print(S)
            finish = time.time()
            data[k] = finish - start
    return data


def getdat (G1, G2, maxk, algo, p, axis):
    data=dict()
    for k in range(1,maxk+1):
        S1 = algo(G1,k)
        S2= algo(G2,k)
        S3 = list(set(S1 + S2))
        #print(S3)
        size=avgSize(G2,S3,p,200)
        #print(size)
        data[k]=size
    return data

if __name__ == "__main__":
    time2implement = time.time()

    time2build = time.time()
    # read in graph


   # with open("textfile1") as textfile1, open("textfile2") as textfile2: 
    #    for x, y in izip(textfile1, textfile2):
     #       x = x.strip()
      #      y = y.strip()
            #print("{0}\t{1}".format(x, y))
    
    G1 = nx.Graph()
    with open(r'C:\Users\VIT-AP\Desktop\New fold\TARE\Priya\influence-maximization-master to send\influence-maximization-master\graphdata\BIOGRID_genetic.txt') as f:
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
    with open(r'C:\Users\VIT-AP\Desktop\New fold\TARE\Priya\influence-maximization-master to send\influence-maximization-master\graphdata\BIOGRID_physical.txt') as f:
        n, m = f.readline().split()
        for line in f:
            u, v = map(int, line.split())
            try:
                G2[u][v]['weight'] += 1
            except:
                G2.add_edge(u,v, weight=1)
            # G.add_edge(u, v, weight=1)
    print ('Built graph G')
    print (time.time() - time2build)

    print ("Started calculating data for plot time vs k")
    data1 = getdat(G1,G2, 20, degreeDiscountIC, .01, "size")
    data2 = getdat(G1,G2, 20, randomHeuristic, .01, "size")
    data3 = getdat(G1,G2, 20, singleDiscount, .01, "size")
    data4 = getdat(G1,G2, 20, degreeHeuristic, .01, "size")
    data5 = getdat(G1,G2, 20, generalGreedy, .01, "size")
    #k=G2.number_of_nodes()
    #for i in range(1,k):
    #    ab=G2.degree(i)
    #    print(ab)
    #print("nanik")
    #data5 = getData(G2, 20, degreeHeuristic2, .01, "size")
    #print(data5)
    #S=Avg(data4, data5,G1,G2, 40, .01)
    #data6 = getdat(G1, S,40, .01)
    
    fig = plt.figure()
    d1plt, = plt.semilogy(data1.keys(), data1.values(), 'g--')
    d2plt, = plt.semilogy(data2.keys(), data2.values(), 'b--')
    d3plt, = plt.semilogy(data3.keys(), data3.values(), 'r--')
    d4plt, = plt.semilogy(data4.keys(), data4.values(), 'y--')
    d5plt, = plt.semilogy(data5.keys(), data5.values(), 'p--')
    plt.xlabel("Seed set size k")
    plt.ylabel("# of Influenced nodes")
    #plt.title("Running time for different k")
    plt.legend([d4plt,d1plt,d2plt,d3plt,d5plt], ["Degree", "DegreeDiscount", "randomHeuristic","Singlediscount","GeneralGreedy"], loc=9)
    # plt.show()
    plt.yscale('linear')
    plt.show()
    fig.savefig('time_vs_kri.png')

    

    console = []
