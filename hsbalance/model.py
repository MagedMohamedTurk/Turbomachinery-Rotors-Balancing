import cvxpy as cp
import numpy as np
import cmath as cm
import tools
import ALPHA
from ALPHA import CustomError
class Model:

    # TODO
    """Docstring for Model. """

    def __init__(self, A:np.array, ALPHA:np.array, name=''):
        """TODO: to be defined.
        A: Intial vibration vector -> np.ndarray
        ALPHA: Influence coefficient matrix -> NxM np.ndarray"""
        self.name = name
        self.A = A
        try:
            _ = ALPHA.shape
            self.ALPHA = ALPHA
            self.N = ALPHA.shape[1]
        except AttributeError:
            raise CustomError('Missing valid ALPHA value')


    def solve(self, solver=None):
        W = cp.Variable((self.N, 1), complex=True)
        objective = cp.Minimize(cp.sum_squares(self.ALPHA @ W + self.A))
        prob = cp.Problem(objective)
        prob.solve()
        self.W = W.value
        return W.value

    def expected_residual_vibration(self):
        return tools.residual_vibration(self.ALPHA, self.W, self.A)

    def rmse(self):
        return tools.rmse(self.expected_residual_vibration())

