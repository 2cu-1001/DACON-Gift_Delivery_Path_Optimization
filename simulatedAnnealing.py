import numpy as np
import random
import math
import copy
from tqdm import tqdm
from path import Path, Node
import matplotlib.pyplot as plt


class SimulatedAnnealing():
    def __init__(self, T_init, T_final, delta1, delta2, const, max_iter, init_sate, target_cost):
        self.T = T_init
        self.T_init = T_init
        self.T_final = T_final
        self.delta1 = delta1
        self.delta2 = delta2
        self.max_iter = max_iter
        self.iter_cnt = 0
        self.target_cost = target_cost
        self.cur_state = Path(init_sate.path)
        self.best_sate = Path(init_sate.path)
        self.const = const
        self.cost_hist = []
        self.best_cost_hist = []
        
    
    def training(self):
        to_worse_cnt = 0
        with tqdm(total=self.max_iter, desc="Training", unit="iter") as pbar:
            for iter in range(1, self.max_iter + 1):
                if self.T < self.T_final: break
                
                neighbor_type = random.randint(0, 8)
                nxt_path = self.cur_state.make_neighbor_path(neighbor_type)
                nxt_state = Path(nxt_path)
                
                if nxt_state.tot_cost <= self.cur_state.tot_cost:
                    self.cur_state = nxt_state
                    
                elif nxt_state.tot_cost > self.cur_state.tot_cost:
                    P = math.exp((-(nxt_state.tot_cost - self.cur_state.tot_cost)) / (self.T))
                    if P > random.random():
                        # print("state changed into worse case")
                        self.cur_state = nxt_state
                        to_worse_cnt += 1
                        
                if self.cur_state.tot_cost < self.best_sate.tot_cost:
                    self.best_sate = copy.deepcopy(self.cur_state)
                
                # improved_rate = (self.cur_state.tot_cost - self.target_cost) / (self.target_cost)
                # if improved_rate > 0.01: self.T *= self.delta1
                # else: self.T *= self.delta2
                self.T = self.T_init / (1 + self.const * math.log(1 + iter))
                    
                self.cost_hist.append(self.cur_state.tot_cost)
                self.best_cost_hist.append(self.best_sate.tot_cost)
                pbar.set_postfix(cur_T = self.T, BestCost=self.best_sate.tot_cost, CurCost=self.cur_state.tot_cost, GorupCnt=len(self.cur_state.path), toWorse=to_worse_cnt)
                pbar.update(1)
            
        plt.plot(self.cost_hist)
        plt.plot(self.best_cost_hist)
        plt.show()
        return self.best_sate
