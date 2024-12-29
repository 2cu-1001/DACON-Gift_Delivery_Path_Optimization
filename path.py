import utils
import numpy as np
from sklearn.neighbors import NearestNeighbors
import copy 
import random


class Node:
    def __init__(self, id, xpos, ypos, demand):
        self.id = id
        self.xpos = xpos
        self.ypos = ypos
        self.demand = demand
        
        
class Path:
    def __init__(self, init_path=None):
        self.path = []
        self.tot_cost = 0
        if init_path is not None:
            self.path = init_path
            self.tot_cost = self.calc_cur_cost()
            
            
    def make_initial_path(self, nodes):
        towns = [node for node in nodes if node.id != 0]
        coords = np.array([[node.xpos, node.ypos] for node in towns])
        demands = [node.demand for node in towns]
        
        neighbors = NearestNeighbors(n_neighbors=len(towns), algorithm='auto').fit(coords)
        depot = np.array([[0, 0]])  
        dist, indices = neighbors.kneighbors(depot)
        
        visited = set()
        max_capacity = 25  

        for idx in indices[0]:  
            if idx in visited:
                continue
            
            group = []
            group_demand = 0
            
            for neighbor_idx in indices[0]: 
                if neighbor_idx in visited:
                    continue
                
                if group_demand + demands[neighbor_idx] <= max_capacity:
                    group.append(towns[neighbor_idx])
                    group_demand += demands[neighbor_idx]
                    visited.add(neighbor_idx)
                else:
                    break
            
            if group:
                self.path.append(group)
        
        self.calc_cur_cost()


    def make_neighbor_path(self, neighbor_type):
        neighbor_path = copy.deepcopy(self.path)
        
        
        if neighbor_type >= 1 and neighbor_type <= 2: 
            src_idx = random.randint(0, len(neighbor_path) - 1)
            group = neighbor_path[src_idx]
            if len(group) > 2:
                i, j = sorted(random.sample(range(len(group)), 2))
                new_group = group[:i] + list(reversed(group[i:j+1])) + group[j+1:]

                if sum(node.demand for node in new_group) <= 25:
                    neighbor_path[src_idx] = new_group
                else:
                    pass
                    # print("2opt failed : demand cap")
            else:
                pass
                # print("2opt failed : too few nodes")
        
        
        elif neighbor_type >= 3 and neighbor_type <= 4:
            src_idx, dst_idx = random.sample(range(len(neighbor_path)), 2)
            src_group, dst_group = neighbor_path[src_idx], neighbor_path[dst_idx]
            
            if len(src_group) > 1 and len(dst_group) > 1:
                src_seg = src_group[:len(src_group)//2]
                dst_seg = dst_group[:len(dst_group)//2]

                new_src_group = dst_seg + src_group[len(src_seg):]
                new_dst_group = src_seg + dst_group[len(dst_seg):]
                
                if (sum(node.demand for node in new_src_group) <= 25 and
                    sum(node.demand for node in new_dst_group) <= 25):
                    neighbor_path[src_idx] = new_src_group
                    neighbor_path[dst_idx] = new_dst_group
                else:
                    pass
                    # print("segment swap failed : demand cap")
            else:
                pass
                # print("segment swap failed : too few nodes")
                
        
        elif neighbor_type >= 4 and neighbor_type <= 5:
            src_idx, dst_idx = random.sample(range(len(neighbor_path)), 2)
            if neighbor_path[src_idx]:
                node_idx = random.randint(0, len(neighbor_path[src_idx]) - 1)
                node = neighbor_path[src_idx][node_idx]
                if utils.check_demand_cap(node, neighbor_path[dst_idx]):
                    neighbor_path[src_idx].pop(node_idx)
                    neighbor_path[dst_idx].append(node)
                    if len(neighbor_path[src_idx]) == 0:
                        neighbor_path.pop(src_idx)
                else:
                    pass
                    # print("merge failed : demand cap")
            else:
                pass
                # print("merge failed : empty src list")
                
                
        elif neighbor_type >= 6 and neighbor_type <= 7:
            src_idx, dst_idx = random.sample(range(len(neighbor_path)), 2)
            if neighbor_path[src_idx]:
                src_node_idx = random.randint(0, len(neighbor_path[src_idx]) - 1)
                src_node = neighbor_path[src_idx][src_node_idx]
                dst_node_idx = random.randint(0, len(neighbor_path[dst_idx]) - 1)
                dst_node = neighbor_path[dst_idx][dst_node_idx]
                
                if (utils.check_demand_cap(src_node, neighbor_path[dst_idx], dst_node.demand) and
                    utils.check_demand_cap(dst_node, neighbor_path[src_idx], src_node.demand)):
                    neighbor_path[src_idx].pop(src_node_idx)
                    neighbor_path[dst_idx].append(src_node)
                    neighbor_path[dst_idx].pop(dst_node_idx)
                    neighbor_path[src_idx].append(dst_node)

                else:
                    pass
                    # print("merge failed : demand cap")
            else:
                pass
                # print("merge failed : empty src list")
                
            
            
        elif neighbor_type == 8:
            idx = random.randint(0, len(neighbor_path) - 1)
            group = neighbor_path[idx]
            if len(group) <= 6 and len(group) > 1:
                opt_group = utils.make_group_nodes_order_optimal(group)
                neighbor_path[idx] = opt_group
                
            else:
                pass
                # print("make optimal failed : too many nodes")
        
        return neighbor_path
    

    def calc_cur_cost(self):
        cur_cost = 0
        
        for group in self.path:
            in_group_cost = 0
            
            for i, _ in enumerate(group):
                if i == len(group) - 1: break
                cur_node, nxt_node = group[i], group[i + 1]
                in_group_cost += utils.calc_dist(cur_node.xpos, cur_node.ypos, nxt_node.xpos, nxt_node.ypos)
            
            in_group_cost += utils.calc_dist(0, 0, group[0].xpos, group[0].ypos)
            in_group_cost += utils.calc_dist(group[-1].xpos, group[-1].ypos, 0, 0)
            cur_cost += in_group_cost
        
        self.tot_cost = cur_cost
        return cur_cost