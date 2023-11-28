import networkx as nx
import numpy as np
import random
import copy
import sys

class Sampler(object):
    def __init__(self, g):
        self.G = copy.deepcopy(g)
        self.g = copy.deepcopy(self.G)
        self.edgelist = list(self.g.edges)
        
        self.n_trials = 100
        self.T_check = 100
        self.t_check = 0
        
    def _check_connectivity(self):
        if self.T_check == self.t_check:
            self.t_check = 0
            
            if nx.is_connected(self.g):
                self.T_check += 1
                self.G = copy.deepcopy(self.g)
                
            else:
                self.T_check //= 2
                self.g = copy.deepcopy(self.G)
                self.n_tri = sum(nx.triangles(self.g).values()) // 3
                self.edgelist = list(self.g.edges)
        else:
            self.t_check += 1
            
    def _delta_triangle(self, r1, r2):
        e1 = self.edgelist[r1]
        e2 = self.edgelist[r2]
        tri = len(set(self.g[e1[0]]) & set(self.g[e1[1]]))
        tri += len(set(self.g[e2[0]]) & set(self.g[e2[1]]) )
        return tri
    
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
        
        t1 = len(set(self.g[e1[0]]) & set(self.g[e1[1]]) )
        t1 += len(set(self.g[e2[0]]) & set(self.g[e2[1]]) )

        self.g.remove_edge(e1[0], e1[1])
        self.g.remove_edge(e2[0], e2[1])
        
        self.g.add_edge(e1[0], e2[1])
        self.g.add_edge(e2[0], e1[1])

        self.edgelist[r1] = (e1[0], e2[1])
        self.edgelist[r2] = (e2[0], e1[1])
        
        t2 = len(set(self.g[e1[0]]) & set(self.g[e2[1]]) )
        t2 += len(set(self.g[e2[0]]) & set(self.g[e1[1]]) )
        return (t2 - t1)    
        
    def tune(self, std = 10, T_max = 2000):
        self.g = copy.deepcopy(self.G)
        self.edgelist = list(self.g.edges)
        self.n_tri = sum(nx.triangles(self.g).values()) // 3
        target = self.n_tri
        
        n_triads = sum([n[1] * (n[1] - 1 ) / 2 for n in self.G.degree])
        n_trials = 100
        
        t = 0
        while t < T_max * len(self.g):
            assert n_trials < 1e5
            
            ### edgeswap
            r1, r2, sucess = self.sample(n_trials)
            if sucess:
                delta = -self._delta_triangle(r1, r2)
                delta_tri = self.swap(r1, r2)
                delta += self._delta_triangle(r1, r2)
                
                dist = (self.n_tri + delta - target) ** 2 - (self.n_tri - target) ** 2
                dist = 9 * dist / n_triads ** 2
                log_ratio = (-dist / 2 * std ** 2)
                if random.random() > np.exp(min(0, log_ratio)):
                    self.swap(r1, r2)
                else:
                    self.n_tri += delta
                t += 1
                
                n_trials = (n_trials + 1) // 2
            else:
                n_trials *= 2
                
                
            ### check connectivity
            self._check_connectivity()
            if t % len(self.g) == 0:
                std = min(1e7, 1.01 * std)
                print(t, std, 3 * self.n_tri / n_triads)
        
        self.t_check = self.T_check
        self._check_connectivity()
        
        print(3 * self.n_tri / n_triads)
        print(nx.transitivity(self.G), nx.transitivity(self.g), 3 * target / n_triads)

if __name__ == "__main__":
    sampler = Sampler(nx.read_edgelist(sys.argv[1]))
    sampler.tune()
    nx.write_edgelist(sampler.G, sys.argv[2], data = False)




