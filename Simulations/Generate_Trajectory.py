import sys
import random
import numpy as np
import networkx as nx

if __name__ == "__main__":
    g = nx.Graph()
    g.add_edges_from(np.loadtxt(sys.argv[1]).astype(int))
    nodes = np.arange(100)
    edgelist = np.array(g.edges)
    ########################################################################
    ########################################################################
    t_max = 10000
    s = 0.01

    n_trail = 500
    data_nef = np.zeros((n_trail, t_max, 3))
    print(data_nef.shape)
    cnt = 0
    i = 0
    while cnt < n_trail:
        mutant = np.zeros_like(nodes)
        mutant[:1] = 1
        node_mean = 0.01
        t = 0

        temp_nef = np.array([1,0,2]) * np.ones((t_max, 3))
        i += 1
        while(0 < node_mean < 1): #for t in range(t_max):
            #print(node_mean)
            if t < t_max:
                edge_mean = np.mean((mutant[edgelist[:,0]] + mutant[edgelist[:,1]]) == 1)
                temp_nef[t] = [node_mean, edge_mean, edge_mean / (node_mean * (1 - node_mean))]

            fitness = 1 + s * mutant 
            birth_node = np.random.choice(nodes, p = fitness/ fitness.sum()) 
            death_node = random.sample(list(g.neighbors(birth_node)), 1) 
            mutant[death_node] = mutant[birth_node]

            node_mean = mutant.mean()
            t += 1 

        if node_mean == 1:
            print(cnt, i)
            print(temp_nef)
            
            data_nef[cnt] = temp_nef  
            cnt += 1

    data_save = np.zeros((t_max, 9))
    data_save[:, :3] = data_nef.mean(0)
    data_save[:, 3:6] = data_nef.std(0)
    data_save[:, 6:] = data_nef[-1]

    np.savetxt(sys.argv[2], data_save, fmt = "%g")
    
