import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

from homework_1.abstract_task import AbstractTask
from homework_1.defaults import TASK_ROOT, RESULT_ROOT


class Task1(AbstractTask):
    def __init__(self, graph: nx.Graph):
        super().__init__(graph=graph)

        self.n_nodes = None
        self.n_edges = None
        self.avg_degree = None
        self.n_nodes_gr_avg = None
        self.n_connectivity = None
        self.n_nodes_largest_cc = None
        self.n_edges_largest_cc = None
        self.nodes_proportion = None
        self.edges_proportion = None
        self.radius_in_largest_connectivity = None
        self.diameter_in_largest_connectivity = None
        self.dist_90 = None

    def run(self):
        self.n_nodes = len(nx.nodes(self.G))
        self.n_edges = len(nx.edges(self.G))
        self.avg_degree = 2 * self.n_edges / self.n_nodes
        self.n_nodes_gr_avg = np.sum(np.array([True if value > self.avg_degree
                                               else False
                                               for value in dict(self.G.degree()).values()]))
        self.n_connectivity = nx.number_connected_components(self.G)
        largest_cc = max(nx.connected_components(self.G), key=len)
        graph_largest_cc = self.G.subgraph(largest_cc).copy()
        self.n_nodes_largest_cc = len(nx.nodes(graph_largest_cc))
        self.n_edges_largest_cc = len(nx.edges(graph_largest_cc))
        self.nodes_proportion = self.n_nodes_largest_cc / self.n_nodes
        self.edges_proportion = self.n_edges_largest_cc / self.n_edges
        self.get_hist()
        self.radius_in_largest_connectivity = nx.radius(graph_largest_cc)
        self.diameter_in_largest_connectivity = nx.diameter(graph_largest_cc)
        self.dist_90 = 0  # TODO: ask about it

    def get_hist(self):
        plt.figure()
        degree_seq = [degree[1] for degree in nx.degree(self.G)]
        unique, heights = np.unique(degree_seq, return_counts=True)
        plt.bar(unique, heights)
        plt.title("Degree Distribution")
        plt.xlabel("Degree")
        plt.ylabel("Number of nodes")
        plt.tight_layout()
        plt.savefig(RESULT_ROOT / 'degree_distr.png')


G = nx.read_gml(TASK_ROOT / 'graphs' / 'netscience.gml')
task = Task1(G)
task.run()
task.report()
