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

def getData (G, maxk, algo, p, axis):
    data = dict()
    for k in range(1,maxk+1):
        if axis == "size":
            S = algo(G, k, p)
            size = avgSize(G, S, p, 200)
            data[k] = size
        elif axis == "time":
            start = time.time()
            S = algo(G, k, p)
            #print(S)
            finish = time.time()
            data[k] = finish - start
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
    
    G = nx.Graph()
    with open(r'C:\Users\hp\Downloads\latex pictures\influence-maximization-master\graphdata\celegans_layer_syn.txt') as f:
        n, m = f.readline().split()
        for line in f:
            u, v = map(int, line.split())
            try:
                G[u][v]['weight'] += 1
            except:
                G.add_edge(u,v, weight=1)
            # G.add_edge(u, v, weight=1)
    print ('Built graph G')
    print (time.time() - time2build)

    print ("Started calculating data for plot time vs k")
    data1 = getData(G, 20, degreeDiscountIC, .01, "size")
    data2 = getData(G, 20, randomHeuristic, .01, "size")
    data3 = getData(G, 20, singleDiscount, .01, "size")
    data4 = getData(G, 20, degreeHeuristic, .01, "size")
    
    fig = plt.figure()
    d1plt, = plt.semilogy(data1.keys(), data1.values(), 'r--')
    d2plt, = plt.semilogy(data2.keys(), data2.values(), 'b--')
    d3plt, = plt.semilogy(data3.keys(), data3.values(), 'g--')
    d4plt, = plt.semilogy(data4.keys(), data4.values(), 'y--')
    plt.xlabel("Seed set size k")
    plt.ylabel("# of Influenced nodes")
    #plt.title("Running time for different k")
    plt.legend([d1plt,d2plt,d3plt,d4plt], ["Degree Discount", "Randomhueristic", "singleDiscount","degreeHeuristic"], loc=9)
    # plt.show()
    plt.yscale('linear')
    plt.show()
    fig.savefig('time_vs_k.png', dpi=fig.dpi)

    

    console = []
