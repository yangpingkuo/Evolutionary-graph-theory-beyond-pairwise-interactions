import sys
import numpy as np
import networkx as nx
#from population import strucutred_population

A = 0#10
n = 2

def rastigin(G, T, s):
    N = len(G)
    mutation_w = 0.012 #0.12
    pop = np.random.randn(N, n) / 4 + 5 * np.ones((N, n))
    prob = np.zeros(N) 
    
    traj = np.zeros((T, n))
    var = np.zeros((T, n))
    
    best_array = np.zeros(T)
    mean_array = np.zeros(T)
    
    for t in range(T):
        rugged = np.cos(2 * np.pi * pop)
        fit = (pop**2 + A * (1 - rugged)).sum(1)
        if t % 10 == 0:
            print(t, fit.mean(), fit.min())

        prob[fit.argsort()] = (1 + np.linspace(-s, s, N))[::-1]
        prob = np.maximum(prob, 1/N)

        traj[t, :] = pop.mean(0)
        var[t,:] = pop.std(0)
        
        best_array[t] = fit.min()
        mean_array[t] = fit.mean()
        
        for _ in range(N):
            prob /= prob.sum()

            birth = np.random.choice(range(N), p = prob)
            death = np.random.choice(list(G.neighbors(birth)) )
            pop[death,:] = pop[birth,:]
            prob[death] = prob[birth]
            
            if np.random.rand() > 0.5:
                pop[death,:] += mutation_w * np.random.randn(n) / np.sqrt(n)
            else:
                pop[birth,:] += mutation_w * np.random.randn(n) / np.sqrt(n)

    return np.hstack([mean_array[:,None], best_array[:,None]])

if __name__ == "__main__":
    T_train = int(sys.argv[1])
    runs = int(sys.argv[2])
    el = np.loadtxt(sys.argv[3]).astype(int)
    out_path = sys.argv[4]
    
    N = np.max(el) + 1
    results = np.zeros((runs, T_train, 2))
    
    G = nx.Graph()
    G.add_nodes_from(range(N))
    G.add_edges_from(el)
    
    for i in range(runs):
        results[i] = rastigin(G, T_train, 1)
    
    #G = nx.complete_graph(N)
    #results[runs] = rastigin(G, T_train, 1)
    np.savetxt(out_path, results.mean(0), header='\"mean functional value\" \t \"best functional value\"')
    
    
    
