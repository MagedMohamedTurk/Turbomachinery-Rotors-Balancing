import cmath
import cvxpy as cp
import numpy as np
import hsbalance.tools as tools
from hsbalance.CI_matrix import Alpha, Condition
import pandas as pd
import warnings

class _Model:
    """Abstract class for models"""

    def __init__(self, A:'initial_vibration'=None, alpha: 'instance of Alpha class'=None,
                 conditions: 'list of condition instances'=None, name:'string'=''):
        """ Instantiate the model
        Args:
        A: Initial vibration vector -> np.ndarray
        ALPHA: Influence coefficient matrix -> class Alpha
        conditions: List of conditions instance that express the model various
                    setpoints for balancing -> list of `class Condition`
        name: optional name of the model -> string
        """
        self.name = name
        self.alpha = alpha
        self.W = None
        self.split_instance = []  # List of all related splits that has modified the solution
        self.conditions = conditions
        if self.conditions is None:
            if A is None or alpha is None:
                raise TypeError('Either (A and Alpha) or `conditions` should be assigned.')
            try:
                if A.shape[1] == 1:
                    self.A = A
            except AttributeError:
                raise tools.CustomError('Either direct_matrix or (A,B,U) '
                                        'should be passed "numpy arrays"')
            except IndexError:
                raise tools.CustomError('`A` should be a column vector (Mx1) dimension')

            # Test if Alpha is an instance of Alpha class
            if not isinstance(alpha, Alpha):
                raise tools.CustomError('Please create an `Alpha instance` first --> ex. alpha = Alpha()')
            else:
                self.alpha = alpha
                self.ALPHA = alpha.value
        elif isinstance(self.conditions, list) == False:
            raise TypeError('Conditions should be a list')
        else:
            if all(isinstance(condition, Condition) for condition in self.conditions):
                self.ALPHA = np.vstack([condition.alpha.value for condition in self.conditions])
                self.A = np.vstack([condition.A for condition in self.conditions])
            else:
                raise TypeError('''`conditions` should be a list of `Condition class` try condition
                                = Condition()''')

        try:
            _ = self.ALPHA.shape  # Test that alpha.value returns np.array
            self.N = self.ALPHA.shape[1]  # Get N number of balancing_planes
            self.M = self.ALPHA.shape[0] # Get M number of measuring points
        except AttributeError:
            raise tools.CustomError('Missing valid ALPHA value')

    def solve(self):
        """
        Solve the problem and return W which is
        row vector of balancing weights
        """
        return self.W

    def expected_residual_vibration(self):
        """
        Returns the residual_vibration from tools module
        """
        return tools.residual_vibration(self.ALPHA, self.W, self.A)
    def rmse(self):
        """
        Returns the root mean squares from tools module
        """
        return tools.rmse(self.expected_residual_vibration())
    def create_split(self):
        """
        Factory method to create a split instance
        """
        return _Model.Split(self)

    class Split:
        '''
        Inner class for splitting weights
        '''
        def __init__(self, model_instance):
            """
            Enable accessing outer class variables
            args:
                model_instance: _Model class
            """
            self.model = model_instance

        def split_setup(self, balancing_plane_index, holes_available, weights_available, max_number_weights_per_hole=None,
                  max_weight_per_plane=None):
            """
            Split method to determine the optimized splitted weight
            over available holes and with some availabe weight types
            the optimization is mixed integer quadratic type that
            minimize the residule of the caluclated model weight from
            a combination of availabe weights on the availble holes
            Args:
                balancing_plane_index: the index of weight to be split
                    from the model. (model.W[index]) -> complex class
                holes_available: list of holes available, this can be
                    entered as numpy array (ex. np.arange(0, 100, 10) represents
                    the holes from 0 deg to 100 deg spaced 10 degress each)-> list
                weights_available: list of type of weights available
                    ex. [185, 90] represents that factory weights available
                    are 185 and 90 grams for instance. -> list
                max_number_weights_per_hole: maximum number of weights premissible
                    to be added in each hole. (ex. 1 -> only one weight is allowable
                    per hole) -> int
                max_weight_per_plane: max weight allowable per plane.
                    (ex 2000 -> maximum weight allowable per plane is 2 kg) -> float
            Returns: weight_available_matrix which represents all possible weights at
                    all possible holes.

            """
            self.balancing_plane_index = balancing_plane_index
            self.holes_available = holes_available
            self.weights_available = weights_available
            self.max_number_weights_per_hole = max_number_weights_per_hole
            self.max_weight_per_plane =  max_weight_per_plane
            self.weight = self.model.W[balancing_plane_index]


            # Vectorizing cmath `rect` function to be applied on holes
            vrect = np.vectorize(cmath.rect)
            # list to np.array
            if isinstance(holes_available, list):
                if holes_available:
                    holes_available = np.array(holes_available)
                else:
                    raise tools.CustomError('holes_available should contian at least one element')
            else:
                raise tools.CustomError('holes_available should be a list')
            if isinstance(weights_available, list):
                if weights_available:
                    weights_available = np.array(weights_available)
                else:
                    raise tools.CustomError('weights_available should contain at least one element')
            else:
                raise tools.CustomError('weights_available should be a list')
            # Transfer weights from row to column
            weights_available = weights_available[:, np.newaxis]
            # Make weight matrix in complex form
            weight_available_matrix = weights_available * vrect(1, holes_available * cmath.pi/180)  # from deg to rad
            self.weight_available_matrix = weight_available_matrix
            pass

        def split_solve(self):
            '''
            Mehtod to solve the splitting problem
            function takes the weight_available_matrix of the split instance
            and find the optimum number of weights types in the candidated holes_available
            that minimize the error.
            Args:
                split model instance
            Returns:
                S: numpy array of the same shape as weight_available_matrix of a model
            '''

            # define mixed integer matrix in cvxpy
            _S = cp.Variable(self.weight_available_matrix.shape, integer=True)
            # define objective function
            _Real = cp.sum(cp.multiply(np.real(self.weight_available_matrix), _S)) - np.real(self.weight)
            _Imag = cp.sum(cp.multiply(np.imag(self.weight_available_matrix), _S)) - np.imag(self.weight)
            _Residuals = cp.norm(cp.hstack([_Real, _Imag]))
            _obj_split = cp.Minimize(_Residuals)
            # constraints
            _const_splitting = [_S >= 0]
            if self.max_number_weights_per_hole:
                if isinstance(self.max_number_weights_per_hole, int):
                    _const_splitting += [cp.sum(_S, axis=0)
                                        <= self.max_number_weights_per_hole]
                else:
                    raise tools.CustomError('`max_number_weights_per_hole` should be integer number')
            if self.max_weight_per_plane:
                if isinstance(self.max_weight_per_plane, (float, int)):
                        _const_splitting += [cp.sum(_S.T @ self.weights_available, axis=0)
                                        <= self.max_weight_per_plane]
                else:
                    raise tools.CustomError('`max_weight_per_plane` should be float number')

            # solve
            _prob_S = cp.Problem(_obj_split, _const_splitting)
            _prob_S.solve(solver=cp.XPRESS)  # TODO make solver options PYTHON_MIP(), ECOS_BB
            _S = np.array(np.round(_S.value))
            self._S = _S
            self._prob_S = _prob_S.value
            _W_equ_split = np.sum(self.weight_available_matrix * self._S)
            self._W_equ_split = _W_equ_split
            return _S



        def results(self):
            '''
            Method to print comprehensive results of the solution
            transfer the numpy array to non-zeros DataFrame
            Args:
                Instance of split model
            Return:
                df_splitting: panads dataframe
            '''
            df_splitting = pd.DataFrame(self._S, index=self.weights_available, columns=self.holes_available)
            df_splitting = df_splitting.loc[:, (df_splitting != 0).any(axis=0)]
            df_splitting.index.name = 'weights_available'
            return df_splitting
        def error(self, options='error'):
            '''
            Method to determine different ways of error in the splitting.
            Args:
                Instance of split model
                options: kwarg to define the type of error.
                'error': default value returns the relative value of error.
                'problem_error': returns the accuracy of the solution.
                'equ': returns the equivilant weight of splitting solution
                    in math form.
            '''

            # Error equivilant weight after splitting
            _error = abs(self._W_equ_split - self.weight)
            # Estimate the error generated by using minmax instead of norm2 in the objective function
            _problem_error = (self._prob_S - _error) / abs(self.weight)
            if options == 'error':
                return _error
            elif options== 'problem_error':
                return _problem_error
            elif options == 'equ':
                return tools.convert_cart_math(self._W_equ_split)
            else:
                raise tools.CustomError('Invalid options. Choose options="error" for solution error'
                                        'caused by splitting, options="problem_error" for solution'
                                        ' accuracy and options="equ" for equivilant weight.')
        def update(self, confirm=False):
            '''
            Method to override the model solution with the split solution for
            the balancing plane.
            confirm: Boolean= False: the default value the method does nothing.
                    It is important to inform the user that implementing this method
                    will cause a change of the optimum solution of the model.
            confirm = True: override the model solution, it is essential for user to
                            estimate the RMSE and residual_vibration change caused by splitting

            '''
            if confirm and self._W_equ_split is not None:
                self.model.W[self.balancing_plane_index] = self._W_equ_split
                self.model.split_instance.append(self)
            elif not confirm:
                warnings.warn('This will change your model optimum solution.'
                        'Choose confirm=True')
                self.model.W[self.balancing_plane_index] = self.weight
            return self.model.W

    def _info(self):
        '''
        Method to summarize the results for Model.
        '''
        yield ('MODEL TYPE', type(self).__name__)
        if self.name:
            yield ('MODEL NAME' , self.name)
        if self.alpha is not None:
            yield ('INFLUENCE COEFFICIENT MATRIX', str(self.alpha))
        if self.A is not None and self.conditions is None:
            _index = (f'Sensor {m+1}' for m in range(self.A.shape[0]))
            yield ('INITIAL VIBRATION' , pd.DataFrame(tools.convert_cart_math(self.A),
                        index=_index, columns=['Vibration']))
        if self.conditions is not None:
            yield ('CONDITIONS',''.join(str(condition) for condition in self.conditions))
        if self.W is not None:
            _index = (f'Plane {n+1}' for n in range(self.W.shape[0]))
            yield ('SOLUTION', pd.DataFrame(tools.convert_cart_math(self.W), index=_index,
                        columns=['Correction Masses']))
            yield ('RMSE', self.rmse())
            _index = (f'Sensor {m+1}' for m in range(self.A.shape[0]))
            yield ('Resiudal Vibration Expected', pd.DataFrame(tools.convert_cart_math(self.expected_residual_vibration()), index=_index,
                        columns=['Expected Vibration']))
        else:
            yield ('SOLUTION','No solution calculated.')

        if self.split_instance is not None :
            if self.split_instance:
                yield ('SPLITS','\n\n'.join(str(split.results()) for split in self.split_instance))
    def info(self):
        formatter = tools.InfoFormatter(name='MODEL', info_parameters=self._info(), level=3)
        return ''.join(formatter.info())


class LeastSquares(_Model):
    """subclass of Model
    solving the model using Least squares method, The objective function
    is to minimize the least squares of residual vibration.
    """


    def __init__(self, A:np.array=None, alpha:'instance of Alpha class'=None, conditions=None, C=np.zeros(1), name=''):
        """ Instantiate the model
        Args:
        A: Initial vibration vector -> np.ndarray
        ALPHA: Influence coefficient matrix -> class Alpha
        C: Weighted Least squares coefficients
        name: optional name of the model -> string
        """
        super().__init__(A=A, alpha=alpha, conditions=conditions, name=name)
        if C.any():
            self.C = C
        else:
            self.C = np.ones(self.A.shape)
    def solve(self, solver='OLE'):
        '''
        Method to solve the model
        Args:
            solver:'OLE' Ordinary Least Squares method
            'Huber': Uses Huber smoother to down estimate the outliers.
        '''
        W = cp.Variable((self.N, 1), complex=True)
        if solver.upper() == 'OLE': # Ordinary least squares
            _objective = cp.Minimize(cp.sum_squares(self.ALPHA @ W + self.A))
        elif solver.upper() == 'HUBER':  # TODO test Huber solver for robust optimization
            _real = cp.real(self.ALPHA @ W + self.A)
            _imag = cp.imag(self.ALPHA @ W + self.A)
            _objective = cp.Minimize(cp.sum_squares(cp.huber(cp.hstack([_real, _imag]), M=0)))
        elif solver.upper() == 'WLS':  #  TODO test weighted least squares
            _objective = cp.Minimize(cp.sum_squares(cp.diag(self.C) @ (self.ALPHA @ W + self.A)))
        else:
            raise tools.CustomError('Unrecognized Solver name')
        prob = cp.Problem(_objective)
        prob.solve()
        self.W = W.value
        return W.value


class Min_max(_Model):
    """
    subclass of model: Solving the model using Minmax optimization method
    to minimize the maximum of residual_vibration.
    """

    def __init__(self, A:np.array, alpha:'instance of Alpha class', conditions=None, weight_const={}, name=''):
        """ Instantiate the model
        Args:
            A: Initial vibration vector -> np.ndarray
            alpha: instance of Alpha class
            weight_const: dict class of planes index and maximum permissible weight
        Returns: solution matrix W
        """
        self.weight_const = weight_const
        super().__init__(A=A, alpha=alpha, conditions=conditions, name=name)

    def solve(self, solver=None):
        '''
        Method to solve the Minmax model
        '''
        W = cp.Variable((self.N,1),complex=True)
        _objective = cp.Minimize(cp.norm((self.ALPHA @ W + self.A),"inf"))
        # Define weight constraints
        _constrains = []
        if self.weight_const != {}:
            try:
                for key, value in self.weight_const.items():
                    _constrains += [cp.norm(W[key]) <= value]
            except NameError:
                raise tools.CustomError('Invalid weight constraint format')
        else:
            pass
        prob=cp.Problem(_objective, _constrains)
        prob.solve()
        self.W = W.value
        return W.value


class LMI(_Model):
    """
    subclass of model
    solving using linear matrix inequality this is mainly to insert 'lazy constraints'
    Lazy constraints will relax the solution at certain planes (not to exceed certain vibration limit)
    """

    def __init__(self, A:np.array, alpha:'instance of Alpha class',
                 conditions=None,
                 weight_const={},
                 critical_planes={}, V_max=None, name=''):
        """
        Args:
            A: Initial vibration vector -> np.ndarray
            alpha: Instance of Alpha class
            critical_planes:  set of critical planes
            weight_const: dict class of planes index and maximum permissible weight
            V_max: max vibration for non-critical_planes
        Return: Solution Matrix W
       """
        self.weight_const = weight_const
        self.critical_planes = list(critical_planes)
        self.V_max = V_max
        super().__init__(A=A, alpha=alpha, conditions= conditions, name=name)

    def solve(self, solver=None):
        '''
        solving the LMI model
        returns solution matrix W
        '''

        # Weight constraints
        N = self.N
        M = self.M
        _wc = np.zeros(N)
        if self.weight_const != {}:
            try:
                for key, value in self.weight_const.items():
                    _wc[key] = value
            except NameError:
                raise tools.CustomError('Invalid weight constraint format')
        else:
            pass

        # Identify critical planes
        if self.V_max:
            _Vm = self.V_max
        else:
            raise tools.CustomError('V_max is not specified')

        if self.critical_planes and len(self.critical_planes)>0:
            _list_cr = self.critical_planes
        else:
            raise tools.CustomError('Critical Planes are not set.')

        _ALPHA = self.ALPHA.copy()
        A = self.A.copy()
        _ALPHAcr = _ALPHA[_list_cr]
        Acr = A[_list_cr]
        _ALPHAncr = np.delete(_ALPHA, _list_cr, axis=0)
        _Ancr = np.delete(A, _list_cr, axis=0)
        # assign cvxpy variables
        _WR = cp.Variable((N, 1))
        _WI = cp.Variable((N, 1))
        _Vc = cp.Variable()

        _RRfcr = cp.diag(np.real(Acr) + np.real(_ALPHAcr) @ _WR-np.imag(_ALPHAcr) @ _WI)
        _IRfcr = cp.diag(np.imag(Acr) + np.imag(_ALPHAcr) @ _WR+np.real(_ALPHAcr) @ _WI)

        _RRfNcr = cp.diag(np.real(_Ancr) + np.real(_ALPHAncr) @ _WR - np.imag(_ALPHAncr) @ _WI)
        _IRfNcr = cp.diag(np.imag(_Ancr)+ np.imag(_ALPHAncr) @ _WR + np.real(_ALPHAncr) @ _WI)
        _zcr = np.zeros((_RRfcr.shape[0], _RRfcr.shape[1]))
        _Icr = np.eye(_RRfcr.shape[0])
        _zncr = np.zeros((_RRfNcr.shape[0], _RRfNcr.shape[1]))
        _Incr = np.eye(_RRfNcr.shape[0])

        _objective = cp.Minimize(_Vc)
        _LMI_real = cp.bmat( [
                                [_Vc*_Icr,        _RRfcr,    _zcr,        -_IRfcr],
                                [_RRfcr,          _Icr,      _IRfcr,          _zcr],
                                [_zcr,            _IRfcr,    _Vc*_Icr,        _RRfcr],
                                [-_IRfcr,         _zcr,       _RRfcr,          _Icr]
                                                                                    ])
        _LMI_imag =cp.bmat( [
                            [_Vm**2*_Incr,        _RRfNcr,    _zncr,        -_IRfNcr],
                            [_RRfNcr,          _Incr,      _IRfNcr,          _zncr],
                            [_zncr,            _IRfNcr,    _Vm**2*_Incr,        _RRfNcr],
                            [-_IRfNcr,         _zncr,       _RRfNcr,          _Incr]
                                                                                ])
        # Model weight constraints
        _const_LMI_w = []
        for i in range(N):
            _LMI_weight = cp.bmat( [
                                [_wc[i]**2,        _WR[i],    0,        -_WI[i]],
                                [_WR[i],          1,      _WI[i],          0],
                                [0,       _WI[i],    _wc[i]**2,        _WR[i]],
                                [-_WI[i],         0,       _WR[i],          1]
                                                                                          ])
            _const_LMI_w.append(_LMI_weight >> 0)
        _const_LMI_w.append( _LMI_real  >> 0)
        _const_LMI_w.append( _LMI_imag >> 0)
        # Stating the problem
        prob = cp.Problem(_objective, _const_LMI_w)
        prob.solve(cp.CVXOPT, kktsolver=cp.ROBUST_KKTSOLVER)
        W = _WR + _WI * 1j
        self.W = W.value
        return self.W


