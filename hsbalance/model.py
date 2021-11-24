import cvxpy as cp
import numpy as np
import cmath as cm

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



def convert_to_polar(cart):
    '''
    docs: Convert complex number in the cartesian form
          into polar form.
    :inputs:
    cart: Complex number in cartesian number ex. 12+23j
         -> <class 'complex'>
    output: Complex number in polar form (modulus, phase in degrees)
            ex.(12, 90) -> <class 'tuple'>
    '''
    phase = cm.phase(cart) * 180 / cm.pi
    if phase<0:
            phase= phase+360
    return (abs(cart), phase)

def convert_to_cartesian(polar):
    theta = polar[1] * cm.pi / 180
    return polar[0]*cm.cos(theta)+ polar[0]* cm.sin(theta)*1j
model = Model()
W = model.solve()
