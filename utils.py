import copy 
import random
import math
from itertools import permutations


def calc_dist(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def check_demand_cap(node, dst_group, val=0):
    demand_cap = 25
    tot_demand = 0
    
    for in_group_node in dst_group:
        tot_demand += in_group_node.demand
    tot_demand += node.demand
    
    return tot_demand - val <= demand_cap


def make_group_nodes_order_optimal(group):
    node_perm = [list(p) for p in permutations(group)]
    min_dist = 999999999999999
    opt_group = []
    
    for cur_group in node_perm:
        cur_dist = 0
        for i in range(len(cur_group) - 1):
            cur_node = cur_group[i]
            nxt_node = cur_group[i + 1]
            cur_dist += calc_dist(cur_node.xpos, cur_node.ypos, nxt_node.xpos, nxt_node.ypos)
        cur_dist += calc_dist(0, 0, cur_group[0].xpos, cur_group[0].ypos)
        cur_dist += calc_dist(cur_group[-1].xpos, cur_group[-1].ypos, 0, 0)
        
        if cur_dist < min_dist:
            opt_group = cur_group
            min_dist = cur_dist
            
    return opt_group
    

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
        for node in nodes:
            if node.id == 0: continue
            self.path.append([node])
        random.shuffle(self.path)
        self.calc_cur_cost()


    def make_neighbor_path(self, neighbor_type):
        neighbor_path = copy.deepcopy(self.path)
        
        if neighbor_type == 0:
            src_idx, dst_idx = random.sample(range(len(neighbor_path)), 2)
            if neighbor_path[src_idx]:
                node_idx = random.randint(0, len(neighbor_path[src_idx]) - 1)
                node = neighbor_path[src_idx][node_idx]
                if check_demand_cap(node, neighbor_path[dst_idx]):
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
                
                
        elif neighbor_type == 1:
            src_idx, dst_idx = random.sample(range(len(neighbor_path)), 2)
            if neighbor_path[src_idx]:
                src_node_idx = random.randint(0, len(neighbor_path[src_idx]) - 1)
                src_node = neighbor_path[src_idx][src_node_idx]
                dst_node_idx = random.randint(0, len(neighbor_path[dst_idx]) - 1)
                dst_node = neighbor_path[dst_idx][dst_node_idx]
                
                if (check_demand_cap(src_node, neighbor_path[dst_idx], dst_node.demand) and
                    check_demand_cap(dst_node, neighbor_path[src_idx], src_node.demand)):
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
            
            
        elif neighbor_type == 2:
            idx = random.randint(0, len(neighbor_path) - 1)
            group = neighbor_path[idx]
            if len(group) <= 6 and len(group) > 1:
                opt_group = make_group_nodes_order_optimal(group)
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
                in_group_cost += calc_dist(cur_node.xpos, cur_node.ypos, nxt_node.xpos, nxt_node.ypos)
            
            in_group_cost += calc_dist(0, 0, group[0].xpos, group[0].ypos)
            in_group_cost += calc_dist(group[-1].xpos, group[-1].ypos, 0, 0)
            cur_cost += in_group_cost
        
        self.tot_cost = cur_cost
        return cur_cost