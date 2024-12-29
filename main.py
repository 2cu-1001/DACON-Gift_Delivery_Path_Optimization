import argparse
from dataset import DataSet
from path import Path, Node
from utils import make_group_nodes_order_optimal
from simulatedAnnealing import SimulatedAnnealing
from pathVisualizer import visualize_path
import utils


def main(T, T_final, delta1, delta2, const, max_iter, target_cost, rollback_iter):
    data_path = "./data/data.csv"
    dataSet = DataSet(data_path)  
    nodes = dataSet.make_datas2nodes()

    path = Path()
    path.make_initial_path(nodes)
    print(f"initial path feasiblity : {utils.check_path_feasibility(path.path)}")
    
    simulator = SimulatedAnnealing(T_init=T, T_final=T_final, delta1=delta1, delta2=delta2, const=const,
                                   max_iter=max_iter, init_sate=path, target_cost=target_cost, rollback_iter=rollback_iter)
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
    parser = argparse.ArgumentParser()
    parser.add_argument("--T", type=float, default=150000)
    parser.add_argument("--T_final", type=float, default=0.01)
    parser.add_argument("--delta1", type=float, default=0.9995)
    parser.add_argument("--delta2", type=float, default=0.99)
    parser.add_argument("--const", type=int, default=5000)
    parser.add_argument("--max_iter", type=int, default=1000000)
    parser.add_argument("--target_cost", type=float, default=2000)
    parser.add_argument("--rollback_iter", type=float, default=20000)

    args = parser.parse_args()

    main(
        T=args.T,
        T_final=args.T_final,
        delta1=args.delta1,
        delta2=args.delta2,
        const=args.const,
        max_iter=args.max_iter,
        target_cost=args.target_cost,
        rollback_iter=args.rollback_iter
    )
