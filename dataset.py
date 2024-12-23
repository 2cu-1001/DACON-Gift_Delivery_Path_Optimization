import pandas as pd
import numpy as np
import csv
from utils import Node, Path


class DataSet:
    def __init__(self, data_path):
        self.data = pd.read_csv(data_path)
        

    def make_datas2nodes(self):
        node_list = []

        for _, cur_row in self.data.iterrows():
            id = 0
            #DEPOT -> id=0
            if cur_row["point_id"] != "DEPOT": 
                id = (int)(cur_row["point_id"][-2:])
            cur_node = Node(id, cur_row["x"], cur_row["y"], cur_row["demand"])
            node_list.append(cur_node)

        return node_list
    

    def save2submission(self, path, save_path):
        data = ["point_id"]
        data.append("DEPOT")
        
        for group in path.path:
            for node in group:
                cur_data = "TOWN_" + "{:02}".format(node.id)
                data.append(cur_data)
            data.append("DEPOT")
        
        with open(save_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            for d in data:
                writer.writerow([d])
            
        print("save submission file : done")