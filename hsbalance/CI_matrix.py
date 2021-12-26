import numpy as np
from hsbalance import tools
import warnings


class Alpha():

    """
    Docstring for ALPHA.
    Alpha is the an influence coefficient matrix
    Influence coefficient matrix is a representation of the change of vibration
    vector in a measuring point when putting a unit weight on a balancing plane.
    """

    def __init__(self:'Influence matrix', name:'string'=''):
        """
        Instantiate an instance of Alpha
        name: optional name of Alpha
        """
        self.name = name

    def add(self, direct_matrix:'np.array'=None, A:'intial_vibraion numpy.array'=None,
            B:'trial matrix numpy.array'=None, U:'trial weight row vector numpy.array'=None,
            keep_trial:'optional keep the previous trial weight in every succeeding trial'=False,
            name:'string'=''):
        '''
        Method to add new values for Alpha instance
        either the direct_matrix is needed or ALL of (A, B, U)
        Args:
            direct_matrix: numpy array M rows -> measuring points,
                        N columns -> balancing planes
            A: Initial vibration column array -> numpy array
            B: Trial matrix MxN array -> numpy array
            U: Trial weights row array -> numpy array
            alpha = (A - B) / U
        '''
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
                        __A_keep_trial = np.delete((np.insert(B, [0], A, axis=1)),
                                                 -1, axis=1)
                        self.value = (B - __A_keep_trial) / U
            except AttributeError:
                raise tools.CustomError('Either direct_matrix or (A,B,U)\
                                        should be passed "numpy arrays"')

    def check(self, ill_condition_remove=False):
        '''
        Method to check the alpha value
            * check the symmetrical of the matrix (check for square matrix only,
            for square matrix it should be symmetric obeyin the reciprocity law)
            * check for ill conditioned planes:
                if for any reason two or more planes has independent readings
                for example [[1, 2 , 3], [2, 4, 6]] this is named as ill-conditioned planes
                as they does not carry new information from the system and considering them
                cause solution infliteration.
            ill_condition_remove = True : remove the ill_condition planes after the check
        '''
        self.M = self.value.shape[0]
        self.N = self.value.shape[1]
        if self.M == self.N:
            __check_sym = np.allclose(self.value, self.value.T, 0.1, 1e-06)
            if not __check_sym:
                warnings.warn('Warning: Influence Matrix is asymmetrical!')
                __check_status_sym = 'Influence Matrix is asymmetrical, check your data'
            else:
                __check_status_sym = 'Influence Matrix is symmetric --> OK'
        else:
            __check_status_sym = 'Not a square matrix --> no exact solution'

        # Checking ILL-CONDITIONED planes
        ill_plane = tools.ill_condition(self.value)
        if ill_plane:
            __check_ill_condition = 'Ill condition found in plane{}'.format(ill_plane)
            if ill_condition_remove:
                self.value = np.delete(self.value,[ill_plane], axis=1)
        else:
            __check_ill_condition ='No ill conditioned planes --> ok' 
        return print('{}\n\n{}'.format(__check_status_sym, __check_ill_condition))
