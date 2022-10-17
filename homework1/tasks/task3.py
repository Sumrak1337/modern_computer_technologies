import networkx as nx
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from homework1.tasks.abstract_task import AbstractTask


class Task3(AbstractTask):
    prefix = 'task3'

    def __init__(self, graph: nx.Graph):
        super().__init__(graph=graph)

        self._degree_list = []
        self._inside_ego_edges_list = []
        self._outside_ego_edges_list = []
        self._some_dict = {}

    def run(self):
        for node in self.G.nodes:
            # add a considered node degree
            tmp_result = [nx.degree(self.G, node)]

            # add a number of edges in ego-graph
            ego_graph = nx.ego_graph(self.G, node)
            tmp_result.append(nx.edges(ego_graph))

            # add a number of edges, which connect its ego-graph with other graph
            # (it is enough to compare number of edges in 1ego-graph and 2ego-graph)
            ego_graph2 = nx.ego_graph(self.G, node, 2)
            tmp_result.append(len(nx.nodes(ego_graph2)) - len(nx.nodes(ego_graph)))

            self._some_dict[node] = tmp_result

        adj_matrix = nx.to_scipy_sparse_matrix(self.G)
        cos_sim = cosine_similarity(adj_matrix)
        cs = cos_sim.copy()
        n = len(cs)
        for i in range(n):
            for j in range(n):
                if i <= j:
                    cs[i, j] = 0.
        # TODO: add calculation of cosine similarity to function into abstract_task

        res_cs = []
        for i in range(10):
            xmax, ymax = np.where(cs == cs.max())
            for x, y in zip(xmax, ymax):
                res_cs.append((x, y))
                if len(res_cs) >= 10:
                    break
            if len(res_cs) >= 10:
                break
            cs[xmax, ymax] = 0.

        for node in res_cs:
            x, y = node
            x_name = list(nx.nodes(self.G))[x]
            y_name = list(nx.nodes(self.G))[y]

            print(f'{x_name:15} + {y_name:20}: {cos_sim[x, y]:.3f}')
