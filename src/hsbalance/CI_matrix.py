import logging
import warnings
import numpy as np
import hsbalance.tools as tools
import pandas as pd

logger = logging.getLogger(__name__)
logger.propagate = False
logger.setLevel(logging.DEBUG)
console_handle = logging.StreamHandler()
console_handle.setLevel(logging.INFO)
logger.addHandler(console_handle)

pd.set_option('display.max_columns', 1000)  # Set maximum number of columns to 1000
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
        if self.value is not None:
            self.M = self.value.shape[0]
            self.N = self.value.shape[1]


    def check(self, ill_condition_remove=False):
        '''
        Method to check the alpha value
            * check the symmetrical of the matrix (check for square matrix only,
            for square matrix it should be symmetric obeying the reciprocity law)
            * check for ill conditioned planes:
                if for any reason two or more planes has independent readings
                for example [[1, 2 , 3], [2, 4, 6]] this is named as ill-conditioned planes
                as they does not carry new information from the system and considering them
                cause solution infiltration.
            ill_condition_remove = True : remove the ill_condition planes after the check
        '''
        if self.M == self.N:
            _check_sym = np.allclose(self.value, self.value.T, 0.1, 1e-06)
            if not _check_sym:
                warnings.warn('\nWarning: Influence Matrix is asymmetrical!')
                logger.info('\nInfluence Matrix is asymmetrical, check your data.')
            else:
                logger.info('\nInfluence Matrix is symmetric --> OK')
        else:
            logger.info('\nNot a square matrix --> no exact solution.')

        # Checking ILL-CONDITIONED planes
        ill_plane = tools.ill_condition(self.value)
        if ill_plane:
            logger.info(f'\nIll-conditioned found in plane # {ill_plane}')
            if ill_condition_remove:
                logger.warn(f'\nRemoving Ill-conditioned plane # {ill_plane}')
                logger.info(f'\nIC matrix before removing\n{tools.convert_cart_math(self.value)}\n')
                self.value = np.delete(self.value,[ill_plane], axis=1)
                logger.info(f'\nIC matrix after removing\n{tools.convert_cart_math(self.value)}\n')
        else:
            logger.info('\nNo ill conditioned planes --> ok')

    def _info(self):
        '''
        Method to summarize the results for alpha.
        return generator of tuples(title:str, item)
        '''
        if self.name:
            yield ('Name', self.name)
        if self.value is not None:
            _index = (f'Sensor {m+1}' for m in range(self.value.shape[0]))
            _columns = (f'Plane {n+1}' for n in range(self.value.shape[1]))
            yield ('Coefficient Values', pd.DataFrame(tools.convert_cart_math(self.value),
                        index=_index, columns=_columns))
        if self.A is not None:
            _index = (f'Sensor {m+1}' for m in range(self.A.shape[0]))
            yield ('Initial Vibration', pd.DataFrame(tools.convert_cart_math(self.A),
                        index=_index, columns=['Vibration']))
        if self.B is not None:
            _index = (f'Sensor {m+1}' for m in range(self.B.shape[0]))
            _columns = (f'Plane {n+1}' for n in range(self.B.shape[1]))
            yield ('Trial Runs Vibration', pd.DataFrame(tools.convert_cart_math(self.B),
                        index=_index, columns=_columns))
        if self.U is not None:
            _index = (f'Plane {n+1}' for n in range(self.U.shape[0]))
            yield ('Trial Masses', pd.DataFrame(tools.convert_cart_math(self.U),
                        index=_index, columns=['Mass']))

    def __repr__(self):
        '''
        Method to print out alpha value
        '''
        formatter = tools.InfoFormatter(name = 'Influence Coefficient Matrix', info_parameters=
                                        self._info())
        return ''.join(formatter.info())

    def save(self, file:str):
        '''
        Method to save influence coefficient values
        '''
        if isinstance(file, str):
            self.file = file
        np.save(file, self.value)


    def load(self, file:str):
        '''
        Method to load influence coefficient value
        '''
        if isinstance(file, str):
            self.file = file + '.npy'
        _matrix = np.load(self.file)
        self.add(direct_matrix=_matrix)

    @property
    def shape(self):
        '''
        returns shape of Influence coefficient matrix
        (no. Measuring Points, no. Balancing Planes)
        '''
        if (self.M is not None) and (self.N is not None):
            return (self.M, self.N)





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

    def add(self, alpha:'Alpha instance', A:'initial_vibration numpy.array'):
        '''
        Method to add a new condition
        Args:
            alpha: Alpha class instance
            A: Initial vibration column array -> numpy array
        '''
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


    def _info(self):
        '''
        Method to summarize the results for condition.
        '''
        if self.name:
            yield ('Name', self.name)
        if self.alpha is not None:
            yield ('Condition IC Matrix', str(self.alpha))
        if self.A is not None:
            _index = (f'Sensor {m+1}' for m in range(self.A.shape[0]))
            yield ('Initial Vibration', pd.DataFrame(tools.convert_cart_math(self.A),
                        index=_index, columns=['Vibration']))


    def __repr__(self):
        '''
        Method to print out condition value
        '''

        formatter = tools.InfoFormatter(name = 'Operation Condition', info_parameters=
                                        self._info(), level=2)

        return ''.join(formatter.info())

def test_save():
    alpha = Alpha(name='Model_IC')
    alpha.add(np.random.rand(3, 3))
    alpha.save('my_alpha')


if __name__ == '__main__':
    test_save()
    my_alpha = Alpha()
    my_alpha.load('my_alpha')
    print(my_alpha)



