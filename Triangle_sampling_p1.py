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
        
        self.n_trials = 100
        self.T_check = 100
        self.t_check = 0
    
        self._aux = dict()
        
    def _group_edges(self):
        self.edgelist = list(self.g.edges)
        self.dtype2idx = dict()
        idx = 0

        for e in self.edgelist:
            d1, d2 = self.g.degree(e[0]), self.g.degree(e[1])
            if d1 not in self.dtype2idx:
                self.dtype2idx[d1] = []
            if d2 not in self.dtype2idx:
                self.dtype2idx[d2] = []

            self.dtype2idx[d1] += [idx]
            if d1 != d2:
                self.dtype2idx[d2] += [idx]
            idx += 1
        
    def _check_connectivity(self):
        if self.T_check == self.t_check:
            self.t_check = 0
            
            if nx.is_connected(self.g):
                self.T_check += 1
                self.G = copy.deepcopy(self.g)
                
            else:
                self.T_check //= 2
                self.g = copy.deepcopy(self.G)
                
                self.n_trans = nx.transitivity(self.g)
                self._group_edges()
        else:
            self.t_check += 1
            
    def _delta_triangle(self, r1, r2):
        e1 = self.edgelist[r1]
        e2 = self.edgelist[r2]
        tri = len(set(self.g[e1[0]]) & set(self.g[e1[1]]))
        tri += len(set(self.g[e2[0]]) & set(self.g[e2[1]]) )
        
        if 'n_triads' not in self._aux :
            self._aux['n_triads'] = sum([n[1] * (n[1] - 1 ) / 2 for n in self.G.degree])
        
        return 3 * tri / self._aux['n_triads']
    
    def sample(self, n_trails = 100):
        n_e = len(self.edgelist)
        assert n_e > 1
        
        for _ in range(n_trails):                  
            r1 = random.randrange(0, n_e)
            e1 = self.edgelist[r1]
            d1 = [self.g.degree(e1[0]), self.g.degree(e1[1])]
            
            d = d1[random.randrange(0, 2)]
            candidates = self.dtype2idx[d]
            r2 = candidates[int(random.random() * len(candidates))]
            
            e2 = self.edgelist[r2]
            d2 = [self.g.degree(e2[0]), self.g.degree(e2[1])]
            
            if d1[1] != d2[1]:
                if d1[0] == d2[1]:
                    self.edgelist[r1] = (e1[1], e1[0])
                    e1 = self.edgelist[r1]
                    
                elif d1[1] == d2[0]:
                    self.edgelist[r2] = (e2[1], e2[0])
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

    def tune(self, target, std = 10, T_max = 10000):
        self.g = copy.deepcopy(self.G)
        self.n_trans = nx.transitivity(self.g)
        self._group_edges()
        
        n_trials = 100
        
        t = 0
        while t < T_max * len(self.g):
            assert n_trials < 1e5
            
            ### edgeswap
            r1, r2, sucess = self.sample(n_trials)
            if sucess:
                delta = -self._delta_triangle(r1, r2)
                self.swap(r1, r2)
                delta += self._delta_triangle(r1, r2)
                
                dist = (self.n_trans + delta - target) ** 2 - (self.n_trans - target) ** 2
                log_ratio = (-dist / 2 * std ** 2)
                if random.random() > np.exp(min(0, log_ratio)):
                    self.swap(r1, r2)
                else:
                    self.n_trans += delta
                t += 1
                
                n_trials = (n_trials + 1) // 2
            else:
                n_trials *= 2
                
                
            ### check connectivity
            self._check_connectivity()
            if t % len(self.g) == 0:
                std = min(1e7, 1.002 * std)
                print(t, std, nx.degree_assortativity_coefficient(self.g), self.n_trans)
                
            if np.isclose(self.n_trans, target) and np.isclose(1e7, std):
                break
            
        self.t_check = self.T_check
        self._check_connectivity()
        print(std, nx.degree_assortativity_coefficient(self.g), self.n_trans, target)
        #print(self.n_trans, nx.transitivity(self.G), nx.transitivity(self.g))

if __name__ == "__main__":
    sampler = Sampler(nx.read_edgelist('temp_graph.txt') )
    sampler.tune(float(sys.argv[1]))
    nx.write_edgelist(sampler.G, sys.argv[2], data = False)
    print(*sys.argv)

