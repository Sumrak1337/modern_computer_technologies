import networkx as nx
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity

from homework_1.abstract_task import AbstractTask
from homework_1.defaults import TASK_ROOT, RESULT_ROOT


class Task2(AbstractTask):
    def __init__(self, graph: nx.Graph):
        super().__init__(graph=graph)

        self.degree_centrality = None
        self.closeness_centrality = None
        self.betweenness_centrality = None
        self.eigenvector_centrality = None
        self.cosine_similarity = None

    def run(self):
        self.degree_centrality = nx.centrality.degree_centrality(self.G)
        self.closeness_centrality = nx.centrality.closeness_centrality(self.G)
        self.betweenness_centrality = nx.centrality.betweenness_centrality(self.G)
        self.eigenvector_centrality = nx.centrality.eigenvector_centrality(self.G)

        self.get_top_10(self.degree_centrality, 'Degree Centrality')
        self.get_top_10(self.closeness_centrality, 'Closeness Centrality')
        self.get_top_10(self.betweenness_centrality, 'Betweenness Centrality')
        self.get_top_10(self.eigenvector_centrality, 'Eigenvector Centrality')

        # adj_matrix = nx.adjacency_matrix(self.G)
        adj_matrix = nx.to_scipy_sparse_array(self.G)
        self.cosine_similarity = cosine_similarity(adj_matrix)
        plt.matshow(self.cosine_similarity)
        title = 'Cosine Similarity'
        plt.title(title)
        plt.savefig(RESULT_ROOT / f'{title}.png')
        plt.close('all')

    @staticmethod
    def get_top_10(metric: dict, tag: str):
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

    def report(self):
        ...


G = nx.read_gml(TASK_ROOT / 'graphs' / 'netscience.gml')
task2 = Task2(G)
task2.run()
task2.report()
