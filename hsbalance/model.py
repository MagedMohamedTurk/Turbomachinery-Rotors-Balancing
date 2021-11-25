import cvxpy as cp
import numpy as np
import cmath as cm
import tools
class Model:

    """Docstring for Model. """

    def __init__(self, name='', A=np.empty([1,1]), ALPHA=np.empty([2,2])):
        """TODO: to be defined.
        A: Intial vibration vector -> np.ndarray
        ALPHA: Influence coefficient matrix -> NxM np.ndarray"""
        self.name = name
        self.A = A
        self.ALPHA = ALPHA
        self.N = ALPHA.shape[0]

    def solve(self, solver=None):
        W = cp.Variable((self.N, 1), complex=True)
        objective = cp.Minimize(cp.sum_squares(self.ALPHA@W+self.A))
        prob = cp.Problem(objective)
        prob.solve()
        return W.value
