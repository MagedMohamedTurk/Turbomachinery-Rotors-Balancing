import cmath
import cvxpy as cp
import numpy as np
from hsbalance import tools
from hsbalance.CI_matrix import Alpha
import pandas as pd
import warnings

class Model:
    """Abstract class for models"""

    def __init__(self, A:'initial_vibration', alpha: 'instance of Alpha class', name:'string'=''):
        """ Instantiate the model
        Args:
        A: Initial vibration vector -> np.ndarray
        ALPHA: Influence coefficient matrix -> class Alpha
        name: optional name of the model -> string
        """
        self.name = name
        self.A = A
        self.split_instance = []  # List of all related splits that has modified the solution
        # Test if Alpha is an instance of Alpha class
        if isinstance(alpha, Alpha):
            ALPHA = alpha.value
        else:
            raise tools.CustomError('Please create Alpha instance first --> ex. alpha = Alpha()')

        try:
            _ = ALPHA.shape  # Test that alpha.value returns np.array
            self.ALPHA = ALPHA
            self.N = ALPHA.shape[1]  # Get N number of balancing_planes
            self.M = ALPHA.shape[0] # Get M number of measuring points
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
        return Model.Split(self)

    class Split:
        '''
        Inner class for splitting weights
        '''
        def __init__(self, model_instance):
            """
            Enable accessing outer class variables
            args:
                model_instance: Model class
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
            __S = cp.Variable(self.weight_available_matrix.shape, integer=True)
            # define objective function
            __Real = cp.sum(cp.multiply(np.real(self.weight_available_matrix), __S)) - np.real(self.weight)
            __Imag = cp.sum(cp.multiply(np.imag(self.weight_available_matrix), __S)) - np.imag(self.weight)
            __Residuals = cp.norm(cp.hstack([__Real, __Imag]))
            __obj_split = cp.Minimize(__Residuals)
            # constraints
            __const_splitting = [__S >= 0]
            if self.max_number_weights_per_hole:
                if isinstance(self.max_number_weights_per_hole, int):
                    __const_splitting += [cp.sum(__S, axis=0)
                                        <= self.max_number_weights_per_hole]
                else:
                    raise tools.CustomError('`max_number_weights_per_hole` should be integer number')
            if self.max_weight_per_plane:
                if isinstance(self.max_weight_per_plane, (float, int)):
                        __const_splitting += [cp.sum(__S.T @ self.weights_available, axis=0)
                                        <= self.max_weight_per_plane]
                else:
                    raise tools.CustomError('`max_weight_per_plane` should be float number')

            # solve
            __prob_S = cp.Problem(__obj_split, __const_splitting)
            __prob_S.solve(solver=cp.XPRESS)  # TODO make solver options PYTHON_MIP(), ECOS_BB
            __S = np.array(np.round(__S.value))
            self.__S = __S
            self.__prob_S = __prob_S.value
            return __S



        def results(self):
            '''
            Method to print comprehensive results of the solution
            transfer the numpy array to non-zeros dataframe
            Args:
                Instance of split model
            Return:
                df_splitting: panads dataframe
            '''
            df_splitting = pd.DataFrame(self.__S, index=self.weights_available, columns=self.holes_available)
            df_splitting = df_splitting.loc[:, (df_splitting != 0).any(axis=0)]
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
            __W_equ_split = np.sum(self.weight_available_matrix * self.__S)
            self.__W_equ_split = __W_equ_split
            __error = abs(self.__W_equ_split - self.weight)
            # Estimate the error generated by using minmax instead of norm2 in the objective function
            __problem_error = (self.__prob_S - __error) / abs(self.weight)
            if options == 'error':
                return __error
            elif options== 'problem_error':
                return __problem_error
            elif options == 'equ':
                return tools.convert_cart_math(__W_equ_split)
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
            if confirm:
                self.model.W[self.balancing_plane_index] = self.__W_equ_split
                self.model.split_instance.append(self)
            elif not confirm:
                warnings.warn('This will change your model optimum solution.'
                        'Choose confirm=True')
                self.model.W[self.balancing_plane_index] = self.weight
            return self.model.W


class LeastSquares(Model):
    """subclass of Model
    solving the model using Least squares method, The objective function
    is to minimize the least squares of residual vibration.
    """


    def __init__(self, A:np.array, alpha:'instance of Alpha class', name=''):
        """ Instantiate the model
        Args:
        A: Initial vibration vector -> np.ndarray
        ALPHA: Influence coefficient matrix -> class Alpha
        name: optional name of the model -> string
        """
        super().__init__(A, alpha, name=name)

    def solve(self, solver='OLE'):
        '''
        Method to solve the model
        Args:
            solver:'OLE' Ordinary Least Squares method
            'Huber': Uses Huber smoother to down estimate the outliers.
        '''
        W = cp.Variable((self.N, 1), complex=True)
        if solver == 'OLE': # Ordinary least squares
            __objective = cp.Minimize(cp.sum_squares(self.ALPHA @ W + self.A))
        elif solver == 'Huber':  # TODO test Huber solver for robust optimization
            __real = cp.real(self.ALPHA @ W + self.A)
            __imag = cp.imag(self.ALPHA @ W + self.A)
            __objective = cp.Minimize(cp.sum_squares(cp.huber(cp.hstack([__real, __imag]))))
        prob = cp.Problem(__objective)
        prob.solve()
        self.W = W.value
        return W.value


class Min_max(Model):
    """
    subclass of model: Solving the model using Minmax optimization method
    to minimize the maximum of residual_vibration.
    """

    def __init__(self, A:np.array, alpha:'instance of Alpha class', weight_const={}, name=''):
        """ Instantiate the model
        Args:
            A: Initial vibration vector -> np.ndarray
            alpha: instance of Alpha class
            weight_const: dict class of planes index and maximum permissible weight
        Returns: solution matrix W
        """
        self.weight_const = weight_const
        super().__init__(A, alpha, name=name)

    def solve(self, solver=None):
        '''
        Method to solve the Minmax model
        '''
        W = cp.Variable((self.N,1),complex=True)
        __objective = cp.Minimize(cp.norm((self.ALPHA @ W + self.A),"inf"))
        # Define weight constraints
        __constrains = []
        if self.weight_const != {}:
            try:
                for key, value in self.weight_const.items():
                    __constrains += [cp.norm(W[key]) <= value]
            except NameError:
                raise tools.CustomError('Invalid weight constraint format')
        else:
            pass
        prob=cp.Problem(__objective, __constrains)
        prob.solve()
        self.W = W.value
        return W.value


class LMI(Model):
    """
    subclass of model
    solving using linear matrix inequality this is mainly to insert 'lazy constraints'
    Lazy constraints will relax the solution at certain planes (not to exceed certain vibration limit)
    """

    def __init__(self, A:np.array, alpha:'instance of Alpha class',
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
        super().__init__(A, alpha, name=name)

    def solve(self, solver=None):
        '''
        solving the LMI model
        returns solution matrix W
        '''

        # Weight constraints
        N = self.N
        M = self.M
        __wc = np.zeros(N)
        if self.weight_const != {}:
            try:
                for key, value in self.weight_const.items():
                    __wc[key] = value
            except NameError:
                raise tools.CustomError('Invalid weight constraint format')
        else:
            pass

        # Identify critical planes
        if self.V_max:
            __Vm = self.V_max
        else:
            raise tools.CustomError('V_max is not specified')

        if self.critical_planes and len(self.critical_planes)>0:
            __list_cr = self.critical_planes
        else:
            raise tools.CustomError('Critical Planes are not set.')

        __ALPHA = self.ALPHA.copy()
        A = self.A.copy()
        __ALPHAcr = __ALPHA[__list_cr]
        Acr = A[__list_cr]
        __ALPHAncr = np.delete(__ALPHA, __list_cr, axis=0)
        __Ancr = np.delete(A, __list_cr, axis=0)
        # assign cvxpy variables
        __WR = cp.Variable((N, 1))
        __WI = cp.Variable((N, 1))
        __Vc = cp.Variable()

        __RRfcr = cp.diag(np.real(Acr) + np.real(__ALPHAcr) @ __WR-np.imag(__ALPHAcr) @ __WI)
        __IRfcr = cp.diag(np.imag(Acr) + np.imag(__ALPHAcr) @ __WR+np.real(__ALPHAcr) @ __WI)

        __RRfNcr = cp.diag(np.real(__Ancr) + np.real(__ALPHAncr) @ __WR - np.imag(__ALPHAncr) @ __WI)
        __IRfNcr = cp.diag(np.imag(__Ancr)+ np.imag(__ALPHAncr) @ __WR + np.real(__ALPHAncr) @ __WI)
        __zcr = np.zeros((__RRfcr.shape[0], __RRfcr.shape[1]))
        __Icr = np.eye(__RRfcr.shape[0])
        __zncr = np.zeros((__RRfNcr.shape[0], __RRfNcr.shape[1]))
        __Incr = np.eye(__RRfNcr.shape[0])

        __objective = cp.Minimize(__Vc)
        __LMI_real = cp.bmat( [
                                [__Vc*__Icr,        __RRfcr,    __zcr,        -__IRfcr],
                                [__RRfcr,          __Icr,      __IRfcr,          __zcr],
                                [__zcr,            __IRfcr,    __Vc*__Icr,        __RRfcr],
                                [-__IRfcr,         __zcr,       __RRfcr,          __Icr]
                                                                                    ])
        __LMI_imag =cp.bmat( [
                            [__Vm**2*__Incr,        __RRfNcr,    __zncr,        -__IRfNcr],
                            [__RRfNcr,          __Incr,      __IRfNcr,          __zncr],
                            [__zncr,            __IRfNcr,    __Vm**2*__Incr,        __RRfNcr],
                            [-__IRfNcr,         __zncr,       __RRfNcr,          __Incr]
                                                                                ])
        # Model weight constraints
        __const_LMI_w = []
        for i in range(N):
            __LMI_weight = cp.bmat( [
                                [__wc[i]**2,        __WR[i],    0,        -__WI[i]],
                                [__WR[i],          1,      __WI[i],          0],
                                [0,       __WI[i],    __wc[i]**2,        __WR[i]],
                                [-__WI[i],         0,       __WR[i],          1]
                                                                                          ])
            __const_LMI_w.append(__LMI_weight >> 0)
        __const_LMI_w.append( __LMI_real  >> 0)
        __const_LMI_w.append( __LMI_imag >> 0)
        # Stating the problem
        prob = cp.Problem(__objective, __const_LMI_w)
        prob.solve(cp.CVXOPT, kktsolver=cp.ROBUST_KKTSOLVER)
        W = __WR + __WI * 1j
        self.W = W.value
        return self.W
