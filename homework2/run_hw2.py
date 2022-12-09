from tasks.task1 import Task1
from tasks.task2 import Task2
from tasks.task3 import Task3


def main():
    for Task in [
        Task1,
        # Task2,
        # Task3
    ]:
        Task().run()

    # g = nx.Graph()
    # g.add_edge('a', 'b')
    # g.add_edge('d', 'c')
    # nx.draw(g, pos=nx.bipartite_layout(g, ['a', 'c']))
    # plt.show()
    # task = Task()
    # task.run()


if __name__ == '__main__':
    main()
