import networkx as nx

from homework1.abstract_task import AbstractTask


class Task3(AbstractTask):
    prefix = 'task3'

    def __init__(self, graph: nx.Graph):
        super().__init__(graph=graph)

    def run(self):
        ...
