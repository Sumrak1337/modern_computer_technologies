import pandas as pd
import numpy as np

from homework2.task_defaults import DATA_ROOT, get_logger
from homework2.tasks.task_assigment import TaskAssigment

log = get_logger(__file__)


class Task1:
    prefix = 'task1'

    @staticmethod
    def run():
        for i in range(1, 3):
            main_matrix = pd.read_csv(DATA_ROOT / f'var{i}.csv', sep=',', header=None).to_numpy()
            ta = TaskAssigment(main_matrix)

            cost_ap, solution_ap, indices_ap = ta.all_permutation()
            cost_h, solution_h, indices_h = ta.hungary()

            bsm_ap = np.zeros(main_matrix.shape).astype(int)
            for k, (idx, val) in enumerate(zip(indices_ap, solution_ap)):
                bsm_ap[k][idx] = val

            bsm_h = np.zeros(main_matrix.shape).astype(int)
            for k, (idx, val) in enumerate(zip(indices_h, solution_h)):
                bsm_h[k][idx] = val

            # TODO: add time
            log.info(f"\nCost matrix: "
                     f"\n{main_matrix}")

            log.info(f'\nAll permutation:'
                     f'\nmin_cost: {cost_ap}'
                     f'\nbest_solution: {solution_ap}'
                     f'\nbest_solution_matrix:'
                     f'\n{bsm_ap}')

            log.info(f'\nHungary:'
                     f'\nmin_cost: {cost_h}'
                     f'\nbest_solution: {solution_h}'
                     f'\nbest_solution_matrix:'
                     f'\n{bsm_h}'
                     f'\n')

