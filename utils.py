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


def check_path_feasibility(path):
    ch = [0] * 76
    for group in path:
        tot_demand = 0
        for node in group:
            tot_demand += node.demand
            if ch[node.id] == 1:
                return False
            if tot_demand > 25:
                return False
            ch[node.id] = 1
    
    return True


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