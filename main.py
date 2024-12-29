from dataset import DataSet
from path import Path, Node
from utils import make_group_nodes_order_optimal
from simulatedAnnealing import SimulatedAnnealing
from pathVisualizer import visualize_path
import utils


def main():
    #Simulated Annealing Setting
    T = 100000
    T_final = 0.01
    delta1 = 0.9995
    delta2 = 0.99
    const = 2000
    max_iter = 1000000
    target_cost = 2000
    #Simulated Annealing Setting
    
    data_path = "./data/data.csv"
    dataSet = DataSet(data_path)  
    nodes = dataSet.make_datas2nodes()

    path = Path()
    path.make_initial_path(nodes)
    print(f"initial path feasiblity : {utils.check_path_feasibility(path.path)}")
    
    simulator = SimulatedAnnealing(T_init=T, T_final=T_final, delta1=delta1, delta2=delta2, const=const,
                                   max_iter=max_iter, init_sate=path, target_cost=target_cost)
    fin_path = simulator.training()
    
    for i, group in enumerate(fin_path.path):
        fin_path.path[i] = make_group_nodes_order_optimal(group)
    print(f"final path feasiblity : {utils.check_path_feasibility(fin_path.path)}")

    save_path = "./data/submission.csv"
    dataSet.save2submission(fin_path, save_path)
    visualize_path(fin_path)
    print(f"final cost : {fin_path.tot_cost}")
    print("done")


if __name__ == "__main__":
    main()