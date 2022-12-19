import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib import cm
from sklearn.metrics.pairwise import cosine_similarity

from logger import get_logger
from homework1.task_defaults import DATA_ROOT, RESULT_ROOT
from homework1.tasks.abstract_task import AbstractTask

log = get_logger(__name__)


class Task2(AbstractTask):
    prefix = 'task2'

    def __init__(self):
        self.g = self.to_undirected(nx.read_gexf(DATA_ROOT / 'vk_friends_graph.gexf'))

    def run(self):
        lcc = max(nx.connected_components(self.g), key=len)
        subgraph = nx.subgraph(self.g, lcc)
        pos = nx.spring_layout(subgraph,
                               seed=42)
        cmap = plt.get_cmap('jet')

        def get_graph_visualization(cntr, tag):
            norm = mcolors.Normalize(vmin=min(cntr.values()), vmax=max(cntr.values()))
            scmp = cm.ScalarMappable(norm=norm, cmap=cmap)
            color = [scmp.to_rgba(v, alpha=0.5) for v in cntr.values()]
            norm_centrality = [v * 1 / max(cntr.values()) for v in cntr.values()]
            node_size = [v * 1.5e3 for v in norm_centrality]

            plt.figure(figsize=(16, 10))
            plt.title(f'Visualization of {tag}')
            nx.draw_networkx_nodes(subgraph,
                                   pos=pos,
                                   node_color=color,
                                   node_size=node_size)
            nx.draw_networkx_edges(subgraph,
                                   pos=pos,
                                   alpha=0.2)
            nx.draw_networkx_labels(subgraph,
                                    pos=pos,
                                    font_size=9)
            plt.colorbar(scmp)
            plt.tight_layout()
            plt.savefig(RESULT_ROOT / f'{tag}_vis.png')
            plt.close('all')

        centrality_names = ['degree_centrality',
                            'closeness_centrality',
                            'betweenness_centrality',
                            'eigenvector_centrality']
        for name in centrality_names:
            centrality = getattr(nx.centrality, name)(subgraph)
            self.get_top_10(centrality, name)
            self.get_values_distribution(centrality, name)

            get_graph_visualization(centrality, name)

        # Cosine similarity visualisation
        adj_matrix = nx.to_scipy_sparse_array(self.g)
        cs = cosine_similarity(adj_matrix)
        plt.figure()
        plt.matshow(cs)
        plt.savefig(RESULT_ROOT / 'cosine_similarity.png')

        # Consider only upper triangular part of matrix
        cs_triu = np.triu(cs, 1)

        res_cs = self.get_cs(cs_triu)

        # The first 10 pairs with the highest cosine similarity
        log.info('Cosine Similarity:')
        self.print_cosine_similarity(self.g, cs, res_cs)

    @staticmethod
    def get_top_10(metric, tag):
        lst = sorted(metric.items(), key=lambda x: x[1], reverse=True)

        log.info(f'{tag}:')
        for name, value in lst[:10]:
            print(f'{name:20}: {value:.4f}')

    @staticmethod
    def get_values_distribution(metric, tag):
        plt.figure()
        plt.title(f'Value distribution histogram of {tag}')
        plt.xlabel(f'{tag}')
        plt.ylabel(f'# of nodes')
        values = metric.values()
        plt.hist(values, bins=10, range=(min(values), max(values)), rwidth=0.95)
        plt.savefig(RESULT_ROOT / f'{tag}_distr.png')
        plt.close('all')
