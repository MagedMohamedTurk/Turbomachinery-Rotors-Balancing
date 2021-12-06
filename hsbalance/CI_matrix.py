import numpy as np
from hsbalance import tools
import warnings


class Alpha():

    """Docstring for ALPHA. """

    def __init__(self, name=''):
        """TODO: to be defined.
        """
        self.value = ''
        pass

    def add(self, direct_matrix=None, A=None,
            B=None, U=None, keep_trial=False, name=''):
        '''docs'''
        try:  # test if direct input
            _ = direct_matrix.shape
            if direct_matrix.shape[0] >= direct_matrix.shape[1]:
                self.value = direct_matrix
            else:
                raise tools.CustomError('Number of rows(measuring points) should be\
                                  equal or  more than the number of columns\
                                  (balancing planes)!')
        except AttributeError:
            # if direct matrix is not input calculate it from A, B, U
            # test the exstiance of A, A0, B, U to calculate ALPHA
            try:
                all([A.shape, B.shape, U.shape])
                # Test dimensions
                if A.shape[1] > 1:
                    raise tools.CustomError('`A` should be column vector')
                elif U.ndim > 1:
                    raise tools.CustomError('`U` should be row vector')
                elif B.shape[0] != A.shape[0] or B.shape[1] != U.shape[0]:
                    raise tools.CustomError('`B` dimensions should match `A`and `U`')
                else:
                    if not keep_trial:
                        self.value = (B - A) / U
                    else:
                        A_keep_trial = np.delete((np.insert(B, [0], A, axis=1)),
                                                 -1, axis=1)
                        self.value = (B - A_keep_trial) / U
            except AttributeError:
                raise tools.CustomError('Either direct_matrix or (A,B,U)\
                                        should be passed "numpy arrays"')

    def check(self, ill_condition_remove=False):
        self.M = self.value.shape[0]
        self.N = self.value.shape[1]
        if self.M == self.N:
            check_sym = np.allclose(self.value, self.value.T, 0.1, 1e-06)
            if not check_sym:
                warnings.warn('Warning: Influence Matrix is asymmetrical!')
                check_status_sym = 'Influence Matrix is asymmetrical, check your data'
            else:
                check_status_sym = 'Influence Matrix is symmetric --> OK'
        else:
            check_status_sym = 'Not a square matrix --> no exact solution'
        # Checking ILL-CONDITIONED planes
        Q, R = np.linalg.qr(self.value)
        dep = []
        Rdia = abs(np.diag(R))
        for i in range(R.shape[0]):
            if abs(Rdia[i]/max(Rdia)) < 0.2:
                dep.append(i)
                warnings.warn('Warning ! one or more planes are ill-Conditioned!!')
                print('Plane# ' + str(i) + ' is ill-Conditioned!!')
                check_status_ill = "ill-conditioned plane #{} found".format(i)
        if dep != []:
            if ill_condition_remove:
                self.value = np.delete(self.value, dep, axis=1)
                check_status_ill = 'Removed ill-conditioned planes'
            else:
                check_status_ill = 'Ill-conditioned planes found in the model, choose\
                                                 ill_condition_remove = True to remove them'
        else:
            check_status_ill = 'No ill-conditioned planes --> OK'
        return print('{}\n\n{}'.format(check_status_sym, check_status_ill))

