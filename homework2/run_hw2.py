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


if __name__ == '__main__':
    main()
