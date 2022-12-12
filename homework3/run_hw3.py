from tasks.task1 import Task1
from tasks.task2 import Task2


def main():
    for Task in [
        Task1,
        Task2,
    ]:
        Task().run()


if __name__ == '__main__':
    main()
