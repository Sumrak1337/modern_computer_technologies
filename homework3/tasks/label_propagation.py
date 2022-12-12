import sys

import numpy as np


class LabelPropagation:
    def __init__(self,
                 t,
                 y,
                 diff: float,
                 max_iter: int,
                 labelled: list):
        self.t = t
        self.y = y
        self.diff = diff
        self.max_iter = max_iter
        self.labelled = labelled

    def label_propagation(self):
        # Initialize
        y_init = self.y.copy()
        y1 = self.y.copy()

        # Initialize convergence parameters
        n = 0
        current_diff = sys.maxsize

        # Iterate till difference reduces below diff or till the maximum number of iterations is reached
        while current_diff > self.diff:
            # Set Y(t)
            y0 = y1.copy()

            # Calculate Y(t+1)
            y1 = self.t @ y0

            # Clamp labelled data
            for i in range(len(y_init)):
                if i in self.labelled:
                    for j in range(len(y_init[i])):
                        if i != j:
                            y1[i][j] = y_init[i][j]

            current_diff = np.sum(np.abs(y1 - y0))
            n += 1
            if n > self.max_iter:
                break
        return y1
