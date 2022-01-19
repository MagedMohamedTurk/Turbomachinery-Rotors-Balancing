import numpy as np
import hsbalance.tools as tools
import warnings
import pandas as pd


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
        self.value = None

    def add(self, direct_matrix:'np.array'=None, A:'initial_vibration numpy.array'=None,
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
        self.A = A
        self.B = B
        self.U = U
        self.keep_trial = keep_trial
        try:  # test if direct input
            _ = direct_matrix.shape
            if direct_matrix.ndim < 2:
                raise IndexError('Influence coefficient matrix should be of more than 1 dimensions.')
            if direct_matrix.shape[0] >= direct_matrix.shape[1]:
                self.value = direct_matrix
            else:
                raise tools.CustomError('Number of rows(measuring points) should be '
                                  'equal or  more than the number of columns '
                                  '(balancing planes)!')
            if self.A is not None or self.B is not None or self.U is not None:
                raise ValueError('Either (direct Matrix) or (A, B, U) should be input, but not both.')


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
                    self.A = A
                    self.B = B
                    self.U = U
                    if not keep_trial:
                        self.value = (self.B - self.A) / self.U
                    else:
                        _A_keep_trial = np.delete((np.insert(self.B, [0], self.A, axis=1)),
                                                 -1, axis=1)
                        self.value = (self.B - _A_keep_trial) / self.U
            except AttributeError:
                raise tools.CustomError('Either direct_matrix or (A,B,U) '
                                        'should be passed "numpy arrays"')

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
            _check_sym = np.allclose(self.value, self.value.T, 0.1, 1e-06)
            if not _check_sym:
                warnings.warn('Warning: Influence Matrix is asymmetrical!')
                _check_status_sym = 'Influence Matrix is asymmetrical, check your data'
            else:
                _check_status_sym = 'Influence Matrix is symmetric --> OK'
        else:
            _check_status_sym = 'Not a square matrix --> no exact solution'

        # Checking ILL-CONDITIONED planes
        ill_plane = tools.ill_condition(self.value)
        if ill_plane:
            _check_ill_condition = 'Ill condition found in plane{}'.format(ill_plane)
            if ill_condition_remove:
                self.value = np.delete(self.value,[ill_plane], axis=1)
        else:
            _check_ill_condition ='No ill conditioned planes --> ok'
        return print('{}\n\n{}'.format(_check_status_sym, _check_ill_condition))

    def __repr__(self):
        '''
        Method to summarize the results for alpha.
        '''
        _header = f'\t\tInfluence Coefficient Matrix\t\t\n' + 60*'*'
        if self.name:
            _name = f'\nName:\t{self.name}'
        else:
            _name =''
        if self.value is not None:
            _value = f'\nValue:\n{tools.convert_cart_math(self.value)}'
        else:
            value = ''
        if self.A is not None:
            _A = f'\nInitial Vibration:\n{tools.convert_cart_math(self.A)}'
        else:
            _A = ''
        if self.B is not None:
            _B = f'\nTrial Runs Vibration:\n{tools.convert_cart_math(self.B)}'
        else:
            _B = ''
        if self.U is not None:
            _U = f'\nTrial Masses:\n{tools.convert_cart_math(self.U)}'
        else:
            _U = ''

        assembled = _header + _name + _value + _A + _B + _U
        return assembled





class Condition():

    """
    Docstring for conditions.
    Condition is defined as speed or load or operating condition that is concerned in
    the balancing process.
    Conditions class is meant to be used for creating multispeed-multi_condition
    It is designed to arrange the conditions speeds and loads in explicit way.
    """

    def __init__(self:'condition', name:'string'=''):
        """
        Instantiate a conditions instance that will encapsulate all model speeds and loads
        name: optional name of Alpha
        """
        self.name = name

    def add(self, alpha:'Alpha instance', A:'initial_vibration numpy.array', name:'string'=''):
        '''
        Method to add a new condition
        Args:
            alpha: Alpha class instance
            A: Initial vibration column array -> numpy array
        '''
        self.name = name
        if isinstance(alpha, Alpha):
            self.alpha = alpha
        else:
            raise TypeError('alpha should be class Alpha.')
        try:
            _A_shape = A.shape
            # Test dimensions
            if A.ndim != 2:
                raise IndexError('A should be column vector of Mx1 dimension.')
            elif _A_shape[1] != 1:
                raise IndexError('A should be column vector of Mx1 dimension.')
            elif _A_shape[0] != self.alpha.value.shape[0]:
                raise IndexError('A and alpha should have the same 0 dimension(M).')
            else:
                self.A = A
        except AttributeError:
            raise TypeError('`A` should be passed as "numpy array"')

    def __repr__():
        pass



if __name__ == '__main__':
    alpha1 = Alpha()
    alpha1.name = 'Turbine'
    real = np.random.rand(2,2)
    imag = np.random.rand(2,2)
    comp= real + imag*1j
    alpha1.add(A = np.random.rand(3,1)+np.random.rand(3,1)*1j,
              B=np.random.rand(3,5)+np.random.rand(3,5)*1j,
              U=np.random.rand(5)+np.random.rand(5)*1j)
    alpha2 = Alpha()
    alpha2.add(comp)
    print(alpha2)
