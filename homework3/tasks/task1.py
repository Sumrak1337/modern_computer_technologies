import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

from homework3.tasks.label_propagation import LabelPropagation


colors = list(mcolors.TABLEAU_COLORS)


class Task1:
    def __init__(self):
        self.graph = nx.to_directed(nx.karate_club_graph())

    def run(self):
        for labelled in [
            [0, 33],
            [0, 5, 33]
        ]:
            graph = self.graph_processing(labelled)
            a = nx.to_numpy_array(graph, weight='')
            d = np.diag([degree[1] for degree in graph.out_degree()])
            t = np.linalg.inv(d) @ a
            y = np.zeros((len(nx.nodes(graph)), len(labelled)))
            for i, node in enumerate(labelled):
                y[node][i] = 1.

            lp = LabelPropagation(t=t,
                                  y=y,
                                  diff=1e-8,
                                  max_iter=100,
                                  labelled=labelled)
            labels = lp.label_propagation()
            lab_vector = labels.argmax(1)
            lbl = np.squeeze(np.array(lab_vector))
            # TODO: add nicer plot
            node_colors = [colors[lbl[node]] for node in nx.nodes(graph)]
            pos = nx.spring_layout(graph, iterations=500, seed=42)
            nx.draw(graph, pos=pos, node_color=node_colors, node_size=200, with_labels=True)
            plt.show()

    def graph_processing(self, labelled: list):
        graph = self.graph.copy()
        for label in labelled:
            # Remove incoming (or out-coming) edges
            graph.remove_edges_from([(label, nbr) for nbr, _ in graph.adj[0].items()])
            # Add loop
            graph.add_edge(label, label)

        return graph
