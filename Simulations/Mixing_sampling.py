import networkx as nx
import numpy as np
import random
import copy
import sys

class Sampler(object):
    def __init__(self, g):
        #self.G = nx.random_regular_graph(d, n)
        self.G = copy.deepcopy(g)
        self.g = copy.deepcopy(self.G)
        self.edgelist = list(self.g.edges)
        
        self.n_trials = 100
        self.T_check = 100
        self.t_check = 0
        
        self._aux = dict()

    def _check_connectivity(self):
        if self.T_check == self.t_check:
            self.t_check = 0
            
            if nx.is_connected(self.g):
                self.T_check += 1
                self.G = copy.deepcopy(self.g)
                
            else:
                self.T_check //= 2
                self.g = copy.deepcopy(self.G)
                self.edgelist = list(self.g.edges)
        else:
            self.t_check += 1

    def sample(self, n_trails = 100):
        n_e = len(self.edgelist)
        assert n_e > 1
        
        for _ in range(n_trails):                  
            r1 = random.randrange(0, n_e)
            r2 = (int(random.random() * (n_e - 1)) + r1 + 1) % n_e
            
            e1 = self.edgelist[r1]
            e2 = self.edgelist[r2]
            
            if (len(set(e1 + e2)) == 4 
                and not self.g.has_edge(e1[0], e2[1]) 
                and not self.g.has_edge(e2[0], e1[1]) ):
                return r1, r2, True
            
        return r1, r2, False
        
    def swap(self, r1, r2):
        e1 = copy.deepcopy(self.edgelist[r1])
        e2 = copy.deepcopy(self.edgelist[r2])
        
        self.g.remove_edge(e1[0], e1[1])
        self.g.remove_edge(e2[0], e2[1])
        
        self.g.add_edge(e1[0], e2[1])
        self.g.add_edge(e2[0], e1[1])

        self.edgelist[r1] = (e1[0], e2[1])
        self.edgelist[r2] = (e2[0], e1[1])
        
        
    def tune(self, target, std = 10, T_max = 500):
        self.g = copy.deepcopy(self.G)
        self.edgelist = list(self.g.edges)
        self.n_trans = nx.transitivity(self.g)
        
        n_trials = 100
        
        t = 0
        while t < T_max * len(self.g):
            assert n_trials < 1e5
            
            ### edgeswap
            r1, r2, sucess = self.sample(n_trials)
            if sucess:
                dist = -(nx.degree_assortativity_coefficient(self.g)-target)**2
                self.swap(r1, r2)
                dist += (nx.degree_assortativity_coefficient(self.g)-target)**2
                log_ratio = (-dist / 2 * std ** 2)
                
                if random.random() > np.exp(min(0, log_ratio)):
                    self.swap(r1, r2)
                t += 1
                
                n_trials = (n_trials + 1) // 2
            else:
                n_trials *= 2
                
                
            ### check connectivity
            self._check_connectivity()
            if t % len(self.g) == 0:
                std = min(1e7, 1.01 * std)
                print(t // len(self.g), np.array(g.degree)[:,1].std(), nx.degree_assortativity_coefficient(self.g))
                
            #if np.isclose(self.n_trans, target) and np.isclose(1e7, std):
            #    break
            
        self.t_check = self.T_check
        self._check_connectivity()

    def mix(self, T_max = 100):
        self.g = copy.deepcopy(self.G)
        self.edgelist = list(self.g.edges)
        
        n_trials = 100
        t = 0
        while t < T_max * len(self.g):
            assert n_trials < 1e5
            
            ### edgeswap
            r1, r2, sucess = self.sample(n_trials)
            if sucess:
                delta_tri = self.swap(r1, r2)
                t += 1

if __name__ == "__main__":
    d1, d2 = int(sys.argv[1]), int(sys.argv[2])

    g = nx.random_regular_graph(d1, 50)
    g.add_edges_from([(e[0] + 50, e[1] + 50) for e in nx.random_regular_graph(d2,50).edges])
    
    print("Iteration\t Degree standard deviations\t Assortativity_coefficient")
    sampler = Sampler(g)
    while True:
        sampler.mix()
        g = sampler.g
        if nx.is_connected(g):
            break
    
    sampler.tune(float(sys.argv[3]))
    nx.write_edgelist(sampler.G, sys.argv[4], data = False)

    print(*sys.argv)
