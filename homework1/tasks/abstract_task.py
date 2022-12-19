import networkx as nx
import numpy as np


class AbstractTask:
    def run(self):
        raise NotImplementedError

    @staticmethod
    def to_undirected(graph):
        g = nx.Graph()
        for edge in nx.edges(graph):
            g.add_edge(*edge)
        return g

    @staticmethod
    def get_cs(cs_triu):
        res = []
        for i in range(len(cs_triu)):
            x_max, y_max = np.where(cs_triu == cs_triu.max())
            for x, y in zip(x_max, y_max):
                res.append((x, y))
            cs_triu[x_max, y_max] = 0.
        return res

    @staticmethod
    def print_cosine_similarity(graph, cs, res_cs):
        for node in res_cs[:10]:
            x, y = node
            x_name = list(nx.nodes(graph))[x]
            y_name = list(nx.nodes(graph))[y]

            print(f'{x_name:25} + {y_name:25}: {cs[x, y]:.5f}')
