import networkx as nx
import matplotlib.pyplot as plt

from homework2.task_defaults import DATA_ROOT, RESULTS_ROOT


class Task3:
    prefix = 'task3'

    def run(self):
        for i in range(1, 4):
            graph = self.read_txt(DATA_ROOT / f'sample3.{i}.txt')
            fig, ax = plt.subplots(1, 1, figsize=(16, 10))
            pos = nx.circular_layout(graph)
            node_colors = ["skyblue" if n in {"s", "t"} else "lightgray" for n in graph.nodes]

            res_graph = nx.flow.dinitz(graph, s="s", t="t", capacity="capacity", cutoff=16)
            edge_colors = ["lightgray" if res_graph[u][v]["flow"] == 0 else "black" for u, v in graph.edges]
            edge_labels = {(u, v): f"{res_graph[u][v]['flow']}/{graph[u][v]['capacity']}"
                           for u, v in graph.edges
                           if res_graph[u][v]["flow"] != 0}

            nx.draw_networkx_nodes(graph,
                                   pos=pos,
                                   ax=ax,
                                   node_size=500,
                                   node_color=node_colors)
            nx.draw_networkx_labels(graph,
                                    pos=pos,
                                    ax=ax,
                                    font_size=14)
            nx.draw_networkx_edges(graph,
                                   pos=pos,
                                   ax=ax,
                                   edge_color=edge_colors)
            nx.draw_networkx_edge_labels(graph,
                                         pos=pos,
                                         ax=ax,
                                         edge_labels=edge_labels,
                                         font_size=14)
            ax.set_title(f"Cutoff value = {16}; Max Flow = {res_graph.graph['flow_value']}", size=22)

            fig.tight_layout()
            plt.savefig(RESULTS_ROOT / f'sample3.{i}.png')

    @staticmethod
    def read_txt(file):
        graph = nx.DiGraph()
        with open(file) as f:
            for line in f.readlines():
                if line[0] != f'#':
                    n1, n2, capacity, weight = line.split()
                    graph.add_edge(n1, n2, weight=int(weight), capacity=int(capacity))
        return graph
