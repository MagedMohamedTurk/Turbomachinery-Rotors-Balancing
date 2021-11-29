import numpy as np
import cmath as cm
import tools


class CustomError(Exception):
    pass


class ALPHA():

    """Docstring for ALPHA. """

    def __init__(self, name=''):
        """TODO: to be defined.
        """
        self.value = ''
        pass

    def add(self, direct_matrix=None, A=None,
            A0=np.array([0]), B=None, U=None, name=''):
        '''docs'''
        try:  # test if diect_matrix input
            _ = direct_matrix.shape
            self.value = direct_matrix
        except AttributeError:
            # if direct matrix is not input calculate it from A, B, U
            # test the exstiance of A, A0, B, U to calculate ALPHA
            try:
                all([A.shape, B.shape, U.shape])
                self.value = (B - (A-A0)) / U
            except AttributeError:
                raise CustomError('Either direct_matrix or (A,B,U) should be passed')
