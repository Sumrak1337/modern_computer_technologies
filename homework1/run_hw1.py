from tasks.task1 import Task1
from tasks.task2 import Task2
from logger import get_logger

log = get_logger(__name__)


def main():

    for Task in [
        Task1,
        Task2,
    ]:
        log.info(f'Run {Task.prefix}')
        Task().run()


if __name__ == '__main__':
    main()
