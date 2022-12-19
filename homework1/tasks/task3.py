import networkx as nx
import numpy as np

from homework1.task_defaults import DATA_ROOT
from homework1.tasks.abstract_task import AbstractTask
from logger import get_logger

log = get_logger(__name__)


class Task3(AbstractTask):
    prefix = 'task3'

    def __init__(self):
        self.g = self.to_undirected(nx.read_gexf(DATA_ROOT / 'vk_friends_graph.gexf'))

    def run(self):
        res_dict = {}
        for node in nx.nodes(self.g):
            # Calculate a considered node degree
            degree = nx.degree(self.g, node)

            # Calculate a number of edges in ego-graph
            ego_graph = nx.ego_graph(self.g, node)
            edges = len(nx.edges(ego_graph))

            # Calculate a number of edges, which connect its ego-graph with other graph
            edges2 = -degree
            for ego_node in nx.nodes(ego_graph):
                if ego_node != node:
                    edges2 += nx.degree(self.g, ego_node)

            res_dict[node] = np.array([degree, edges, edges2])

        n = len(nx.nodes(self.g))
        cs = np.zeros((n, n))
        for i, n1 in enumerate(nx.nodes(self.g)):
            for j, n2 in enumerate(nx.nodes(self.g)):
                if i == j:
                    continue

                vec1 = res_dict[n1]
                vec2 = res_dict[n2]
                cs[i][j] = vec1 @ vec2 / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

        cs_triu = np.triu(cs)
        res_cs = self.get_cs(cs_triu)
        log.info('Cosine Similarity:')
        self.print_cosine_similarity(self.g, cs, res_cs)
