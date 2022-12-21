from itertools import permutations
import copy
import os
import shutil

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import imageio.v2 as imageio

from homework2.task_defaults import DATA_ROOT, RESULTS_ROOT
from logger import get_logger

log = get_logger(__name__)


class Task2:
    prefix = 'task2'

    def run(self):
        for i in range(1, 4):
            log.info(f'Sample{i}')
            graph = self.read_txt(DATA_ROOT / f'sample2.{i}.txt')

            odd_nodes = []
            for node in nx.nodes(graph):
                if nx.degree(graph, node) % 2 == 1:
                    odd_nodes.append(node)

            odd_nodes = sorted(odd_nodes)
            d = np.array([[nx.shortest_path_length(graph,
                                                   source=node1,
                                                   target=node2,
                                                   weight='weight')
                           for node2 in odd_nodes]
                          for node1 in odd_nodes])

            d = pd.DataFrame(d, columns=odd_nodes, index=odd_nodes)

            # Find matching with minimal weights
            min_path = np.inf
            min_permutation = None
            min_weights = None
            for permutation in permutations(odd_nodes, len(odd_nodes)):
                current_array = np.array(permutation).reshape(-1, 2)
                path = 0
                weights = []
                for indices in current_array:
                    i1, i2 = indices[0], indices[1]
                    d_value = d[i1][i2]
                    path += d_value
                    weights.append(d_value)

                if path < min_path:
                    min_path = path
                    min_permutation = current_array
                    min_weights = weights

            # Create MultiGraph
            mgraph = nx.MultiGraph()
            for c, v in nx.get_edge_attributes(graph, 'weight').items():
                mgraph.add_edge(*c, weight=v)

            # Add fictitious edges' chains
            for edge, weight in zip(min_permutation, min_weights):
                new_path = nx.shortest_path(mgraph, *edge)
                for j in range(len(new_path) - 1):
                    mgraph.add_edge(new_path[j], new_path[j + 1], weight=weight)
            euler_circuit = list(nx.eulerian_circuit(mgraph))

            main_path = 0
            euler_path = [edge[0] for edge in euler_circuit]
            euler_path.append(euler_circuit[-1][-1])
            euler_path = " -> ".join(euler_path)
            visit_colors = {1: 'green', 2: 'red'}
            visit_edges = {}
            el = nx.get_edge_attributes(graph, 'weight')
            pos = nx.spring_layout(mgraph, seed=42)
            for k, e in enumerate(euler_circuit, start=1):
                main_path += nx.shortest_path_length(mgraph, e[0], e[1], weight='weight')

                # Full graph (faded in background)
                plt.figure(figsize=(32, 20))
                nx.draw_networkx(mgraph, pos=pos, node_size=100, node_color='gray', alpha=0.07)
                nx.draw_networkx_labels(mgraph, pos=pos, alpha=0.8, font_size=20, font_color='black')
                nx.draw_networkx_edge_labels(graph, pos=pos, edge_labels=el, font_size=15)

                # Edges walked as of iteration i
                euler_circuit_i = copy.deepcopy(euler_circuit[0:k])
                graph_i = nx.MultiGraph(euler_circuit_i)

                if e in visit_edges.keys():
                    visit_edges[e] += 1
                    visit_edges[(e[1], e[0])] += 1
                else:
                    visit_edges[e] = 1
                    visit_edges[(e[1], e[0])] = 1

                graph_i_edge_colors = [visit_colors[visit_edges[edge]] for edge in nx.edges(graph_i)]

                nx.draw_networkx_nodes(graph_i, pos=pos, node_size=6, alpha=0.6, node_color='lightgray', linewidths=0.1)
                nx.draw_networkx_edges(graph_i, pos=pos, edge_color=graph_i_edge_colors, alpha=0.8)

                plt.axis('off')
                plt.text(-0.8, 0.9, f'Total weight={main_path}', size=12)
                plt.text(-0.8, 0.8, f'Path: {euler_path}', size=12)
                os.makedirs(RESULTS_ROOT / f'imgforgif', exist_ok=True)
                plt.savefig(RESULTS_ROOT / f'imgforgif' / f'img{k}.png', dpi=120, bbox_inches='tight')
                plt.close()

            log.info(f'Path with minimal weight: \n{euler_path}')
            log.info(f"Minimal weight for sample{i}: {main_path}")

            self.make_circuit_video(i)

    @staticmethod
    def read_txt(file):
        graph = nx.Graph()
        with open(file) as f:
            for line in f.readlines():
                if line[0] != f'#':
                    n1, n2, w = line.split()
                    graph.add_edge(n1, n2, weight=int(w))
        return graph

    @staticmethod
    def make_circuit_video(s_number, fps=3):
        # Sorting filenames in order
        filenames = os.listdir(RESULTS_ROOT / f'imgforgif')
        filenames_sort_indices = np.argsort([int(os.path.basename(filename).split('.')[0][3:]) for filename in filenames])
        filenames = [filenames[i] for i in filenames_sort_indices]

        # Make gif
        with imageio.get_writer(RESULTS_ROOT / f'sample{s_number}.gif', mode='I', fps=fps) as writer:
            for filename in filenames:
                image = imageio.imread(RESULTS_ROOT / f'imgforgif' / filename)
                writer.append_data(image)

        shutil.rmtree(RESULTS_ROOT / 'imgforgif')
