import numpy as np
import itertools
from scipy.optimize import linear_sum_assignment


class TaskAssigment:
    def __init__(self, matrix: np.array):
        self.matrix = matrix

    def all_permutation(self):
        n_choice = len(self.matrix)
        solutions = []
        values = []
        indices = []

        for each_solution in itertools.permutations(range(n_choice)):
            each_solution = list(each_solution)
            solution = []
            ind = []
            value = 0
            for i in range(len(self.matrix)):
                current_value = self.matrix[i][each_solution[i]]
                value += current_value
                solution.append(current_value)
                ind.append(each_solution[i])
            values.append(value)
            solutions.append(solution)
            indices.append(ind)

        min_cost = np.min(values)
        best_index = values.index(min_cost)
        best_solution = solutions[best_index]
        return min_cost, best_solution, indices[best_index]

    def hungary(self):
        tmp_matrix = self.matrix.copy()
        n, dim = tmp_matrix.shape

        for i in range(n):
            row_min = np.min(tmp_matrix[i])
            for j in range(dim):
                tmp_matrix[i][j] -= row_min

        for i in range(dim):
            col_min = np.min(tmp_matrix[:, i])
            for j in range(n):
                tmp_matrix[j][i] -= col_min

        line_count = 0
        while line_count < n:
            line_count = 0
            row_zero_count = []
            col_zero_count = []

            for i in range(n):
                row_zero_count.append(np.sum(tmp_matrix[i] == 0))
            for j in range(dim):
                col_zero_count.append(np.sum(tmp_matrix[:, j] == 0))

            line_order = []
            row_or_col = []
            for i in range(dim, 0, -1):
                while i in row_zero_count:
                    line_order.append(row_zero_count.index(i))
                    row_or_col.append(0)
                    row_zero_count[row_zero_count.index(i)] = 0
                while i in col_zero_count:
                    line_order.append(col_zero_count.index(i))
                    row_or_col.append(1)
                    col_zero_count[col_zero_count.index(i)] = 0

            delete_count_of_row = []
            delete_count_of_col = []
            row_and_col = []
            for i in range(len(line_order)):
                if row_or_col[i] == 0:
                    delete_count_of_row.append(line_order[i])
                else:
                    delete_count_of_col.append(line_order[i])

                new_matrix = np.delete(tmp_matrix, delete_count_of_row, axis=0)
                new_matrix = np.delete(new_matrix, delete_count_of_col, axis=1)
                line_count = len(delete_count_of_row) + len(delete_count_of_col)
                if line_count == n:
                    break

                if 0 not in new_matrix:
                    row_sub = list(set(row_and_col) - set(delete_count_of_row))
                    min_value = np.min(new_matrix)
                    for j in row_sub:
                        tmp_matrix[j] - min_value
                    for j in delete_count_of_col:
                        tmp_matrix[:, j] = tmp_matrix[:, j] + min_value
                    break
        row_ind, col_ind = linear_sum_assignment(tmp_matrix)
        final_value = self.matrix[row_ind, col_ind]
        min_cost = final_value.sum()
        best_solution = list(final_value)

        return min_cost, best_solution, col_ind
