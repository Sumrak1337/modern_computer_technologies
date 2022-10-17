import networkx as nx
import logging

from defaults import GRAPH_ROOT
from tasks.task1 import Task1
from tasks.task2 import Task2
from tasks.task3 import Task3

# TODO: add logging
# TODO: translate .gml to .yaml and work with DictConfig in future


def main():
    g = nx.read_gml(GRAPH_ROOT / 'netscience.gml')

    for Task in [Task1,
                 Task2,
                 Task3]:
        print(f'Run {Task.prefix}')
        task = Task(g)
        task.run()


if __name__ == '__main__':
    main()
