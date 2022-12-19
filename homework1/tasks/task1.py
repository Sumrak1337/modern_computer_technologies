import networkx as nx
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from logger import get_logger
from homework1.task_defaults import DATA_ROOT, RESULT_ROOT

log = get_logger(__name__)


class Task1:
    prefix = 'task1'

    def __init__(self):
        self.g = nx.read_gml(DATA_ROOT / 'netscience.gml')

    def run(self):
        n_nodes = len(nx.nodes(self.g))
        n_edges = len(nx.edges(self.g))
        avg_degree = 2 * n_edges / n_nodes
        greater_avg_degree = np.sum(np.array([True if value > avg_degree
                                              else False
                                              for value in dict(self.g.degree()).values()]))
        lcc = max(nx.connected_components(self.g), key=len)
        subgraph = nx.subgraph(self.g, lcc)
        n_sub_nodes = len(nx.nodes(subgraph))
        n_sub_edges = len(nx.edges(subgraph))

        # Main features description for original graph
        log.info(f'# of nodes: {n_nodes}')
        log.info(f'# of edges: {n_edges}')
        log.info(f'Average degree: {avg_degree:.3f}')
        log.info(f"# of nodes' degree greater than average: {greater_avg_degree}")
        log.info(f'# of connectivity components: {nx.number_connected_components(self.g)}')
        log.info(f'# of nodes in the largest connectivity component: {n_sub_nodes}')
        log.info(f'# of edges in the largest connectivity component: {n_sub_edges}')
        log.info(f"Subgraph's nodes proportion: {n_sub_nodes / n_nodes:.3f}")
        log.info(f"Subgraph's edges proportion: {n_sub_edges / n_edges:.3f}")

        # Histogram of degree distribution
        self.get_hist()

        # Main features description for subgraph
        nodes = list(nx.nodes(subgraph))
        all_paths = []
        for i in range(n_sub_nodes - 1):
            for j in range(i + 1, n_sub_nodes):
                s_path = nx.shortest_path_length(subgraph,
                                                 source=nodes[i],
                                                 target=nodes[j])
                all_paths.append(s_path)
        all_paths = pd.Series(all_paths)

        log.info('For the largest connectivity component:')
        log.info(f'Radius: {nx.radius(subgraph)}')
        log.info(f'Diameter: {nx.diameter(subgraph)}')
        log.info(f'P90: {all_paths.quantile(q=0.9)}')

    def get_hist(self):
        degree_seq = [degree[1] for degree in nx.degree(self.g)]
        unique, heights = np.unique(degree_seq, return_counts=True)

        plt.figure()
        plt.title("Degree distribution")
        plt.xlabel("Degree")
        plt.ylabel("# of nodes")
        plt.bar(unique, heights)
        plt.tight_layout()
        plt.savefig(RESULT_ROOT / 'degree_distr.png')
        plt.close('all')
