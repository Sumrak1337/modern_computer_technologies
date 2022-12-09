import networkx as nx
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from homework2.task_defaults import DATA_ROOT, get_logger
from homework2.tasks.task_assigment import TaskAssigment

log = get_logger(__file__)


class Task1:
    prefix = 'task1'

    def run(self):
        for i in range(1, 3):
            main_matrix = pd.read_csv(DATA_ROOT / f'var{i}.csv', sep=',', header=None).to_numpy()
            ta = TaskAssigment(main_matrix)

            cost_ap, solution_ap, indices_ap = ta.all_permutation()
            cost_h, solution_h, indices_h = ta.hungary()

            bsm_ap = np.zeros(main_matrix.shape).astype(int)
            for k, (idx, val) in enumerate(zip(indices_ap, solution_ap)):
                bsm_ap[k][idx] = val

            bsm_h = np.zeros(main_matrix.shape).astype(int)
            for k, (idx, val) in enumerate(zip(indices_h, solution_h)):
                bsm_h[k][idx] = val

            self.plot_from_matrix(main_matrix, bsm_h, i)

            # TODO: add time
            log.info(f"\nCost matrix: "
                     f"\n{main_matrix}")

            log.info(f'\nAll permutation:'
                     f'\nmin_cost: {cost_ap}'
                     f'\nbest_solution: {solution_ap}')

            log.info(f'\nHungary:'
                     f'\nmin_cost: {cost_h}'
                     f'\nbest_solution: {solution_h}'
                     f'\n')

    @staticmethod
    def nx_graph_from_biadjacency_matrix(matrix):
        u = [f'u{i+1}' for i in range(matrix.shape[0])]
        v = [f'v{i+1}' for i in range(matrix.shape[1])]

        graph = nx.Graph()
        graph.add_nodes_from(u, bipartite=0)
        graph.add_nodes_from(v, bipartite=1)
        graph.add_weighted_edges_from([(u[i], v[j], matrix[i][j]) for i, j in zip(*matrix.nonzero())])

        return graph

    def plot_from_matrix(self, main_matrix, solution, index):
        main_graph = self.nx_graph_from_biadjacency_matrix(main_matrix)
        solution_graph = self.nx_graph_from_biadjacency_matrix(solution)

        special_edgelist = nx.edges(main_graph) - nx.edges(solution_graph)
        labels = nx.get_edge_attributes(main_graph, 'weight')
        top_nodes = list(nx.nodes(main_graph))[:int(len(nx.nodes(main_graph)) / 2)]
        pos = nx.bipartite_layout(main_graph, top_nodes)

        plt.figure()
        plt.title(f"Var{index} full graph + solution")
        nx.draw_networkx_nodes(main_graph, pos=pos)
        nx.draw_networkx_edges(main_graph, pos=pos, edge_color='red', edgelist=nx.edges(solution_graph))
        nx.draw_networkx_edges(main_graph, pos=pos, edge_color='black', edgelist=special_edgelist)
        nx.draw_networkx_labels(main_graph, pos=pos)
        nx.draw_networkx_edge_labels(main_graph, pos=pos, edge_labels=labels, label_pos=0.83, font_size=6)
        plt.tight_layout()
        plt.show()
