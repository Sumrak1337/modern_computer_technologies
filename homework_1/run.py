import networkx as nx

from defaults import GRAPH_ROOT
from task_1.task_1 import Task1
from task_2.task_2 import Task2
from task_3.task_3 import Task3

# TODO: add logging


def main():
    g = nx.read_gml(GRAPH_ROOT / 'netscience.gml')

    tasks = [Task1, Task2, Task3]
    for Task in tasks:
        print(f'Run {Task.prefix}')
        task = Task(g)
        task.run()


if __name__ == '__main__':
    main()
