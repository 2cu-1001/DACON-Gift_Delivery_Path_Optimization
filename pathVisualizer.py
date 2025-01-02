import matplotlib.pyplot as plt
from path import Path, Node


def visualize_path(path):
    depot = (0, 0) 
    plt.figure(figsize=(8, 8))

    for group in path.path:
        x_coords = [depot[0]] + [node.xpos for node in group] + [depot[0]]
        y_coords = [depot[1]] + [node.ypos for node in group] + [depot[1]]
        plt.plot(x_coords, y_coords, marker='o', label=f"Group {group[0].id} to {group[-1].id}")

    plt.scatter(depot[0], depot[1], c='red', label='Depot', s=100, zorder=5)
    plt.text(depot[0], depot[1], "Depot", fontsize=12, ha='right')

    plt.title("Optimized Path Visualization")
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.grid()
    plt.legend()
    plt.savefig("./output/path_visualization.png")
    plt.show()