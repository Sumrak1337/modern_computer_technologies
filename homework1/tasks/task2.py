import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from homework1.tasks.abstract_task import AbstractTask
from homework1.defaults import RESULT_ROOT


class Task2(AbstractTask):
    prefix = 'task2'

    def __init__(self, graph: nx.Graph):
        super().__init__(graph=graph)

        self._degree_centrality = None
        self._closeness_centrality = None
        self._betweenness_centrality = None
        self._eigenvector_centrality = None
        self._cosine_similarity = None

    def run(self):
        self._degree_centrality = nx.centrality.degree_centrality(self.G)
        self._closeness_centrality = nx.centrality.closeness_centrality(self.G)
        self._betweenness_centrality = nx.centrality.betweenness_centrality(self.G)
        self._eigenvector_centrality = nx.centrality.eigenvector_centrality(self.G)

        self._get_top_10(self._degree_centrality, 'Degree Centrality')
        self._get_top_10(self._closeness_centrality, 'Closeness Centrality')
        self._get_top_10(self._betweenness_centrality, 'Betweenness Centrality')
        self._get_top_10(self._eigenvector_centrality, 'Eigenvector Centrality')

        adj_matrix = nx.to_scipy_sparse_array(self.G)
        self._cosine_similarity = cosine_similarity(adj_matrix)
        cs = self._cosine_similarity.copy()
        n = len(cs)
        for i in range(n):
            for j in range(n):
                if i <= j:
                    cs[i, j] = 0.
        print('Cosine Similarity:')
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

            print(f'{x_name:15} + {y_name:20}: {self._cosine_similarity[x, y]:.3f}')

        plt.matshow(self._cosine_similarity)
        title = 'Cosine Similarity'
        plt.title(title)
        plt.savefig(RESULT_ROOT / f'{title}.png')
        plt.close('all')

    @staticmethod
    def _get_top_10(metric: dict, tag: str):
        lst = sorted(metric.items(), key=lambda x: x[1], reverse=True)
        print(f'{tag}:')
        for name, value in lst[:10]:
            print(f'{name:20}: {value:.4f}')
        print()

        # visualization
        plt.figure()
        plt.title(f"Distribution histogram of {tag}")
        plt.xlabel(f"{tag}")
        plt.ylabel("# of nodes")
        values = metric.values()
        plt.hist(values, bins=10, range=(min(values), max(values)), rwidth=0.95)
        plt.savefig(RESULT_ROOT / f'{tag} distr.png')
        plt.close('all')
