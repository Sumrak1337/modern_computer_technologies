import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

from homework1.tasks.abstract_task import AbstractTask
from homework1.defaults import RESULT_ROOT


class Task1(AbstractTask):
    prefix = 'task1'

    def __init__(self, graph: nx.Graph):
        super().__init__(graph=graph)

        self._n_nodes = None
        self._n_edges = None
        self._avg_degree = None
        self._n_nodes_gr_avg = None
        self._n_connectivity = None
        self._n_nodes_largest_cc = None
        self._n_edges_largest_cc = None
        self._nodes_proportion = None
        self._edges_proportion = None
        self._radius_in_largest_connectivity = None
        self._diameter_in_largest_connectivity = None
        self._dist_90 = None

    def run(self):
        self._n_nodes = len(nx.nodes(self.G))
        self._n_edges = len(nx.edges(self.G))
        self._avg_degree = 2 * self._n_edges / self._n_nodes
        self._n_nodes_gr_avg = np.sum(np.array([True if value > self._avg_degree
                                               else False
                                                for value in dict(self.G.degree()).values()]))
        self._n_connectivity = nx.number_connected_components(self.G)
        largest_cc = max(nx.connected_components(self.G), key=len)
        graph_largest_cc = self.G.subgraph(largest_cc).copy()
        self._n_nodes_largest_cc = len(nx.nodes(graph_largest_cc))
        self._n_edges_largest_cc = len(nx.edges(graph_largest_cc))
        self._nodes_proportion = self._n_nodes_largest_cc / self._n_nodes
        self._edges_proportion = self._n_edges_largest_cc / self._n_edges
        self._get_hist()
        self._radius_in_largest_connectivity = nx.radius(graph_largest_cc)
        self._diameter_in_largest_connectivity = nx.diameter(graph_largest_cc)
        # self._dist_90 = 0  # TODO: ask about it

        self._print_params()

    def _get_hist(self):
        plt.figure()
        degree_seq = [degree[1] for degree in nx.degree(self.G)]
        unique, heights = np.unique(degree_seq, return_counts=True)
        plt.bar(unique, heights)
        plt.title("Degree Distribution")
        plt.xlabel("Degree")
        plt.ylabel("# of nodes")
        plt.tight_layout()
        plt.savefig(RESULT_ROOT / 'degree_distr.png')

    def _print_params(self):
        for feature in self.get_features():
            v = getattr(self, feature)
            s = f'{feature}'
            if isinstance(v, float):
                print(f'{s:40}: {v:.3f}')
            else:
                print(f'{s:40}: {v}')
