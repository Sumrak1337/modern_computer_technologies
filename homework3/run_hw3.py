from tasks.task1 import Task1


def main():
    for Task in [
        Task1,
    ]:
        Task().run()


if __name__ == '__main__':
    main()
