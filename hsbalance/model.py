import cmath
import cvxpy as cp
import numpy as np
from hsbalance import tools
from hsbalance.CI_matrix import Alpha
from mip_cvxpy import PYTHON_MIP
import pandas as pd
import warnings

class Model:

    # TODO
    """Abstract class for models"""

    #TODO ALPHA to be instance of ALPHA class not np to be checked
    def __init__(self, A:'intial_vibration', alpha: 'instance of Alpha class', name=''):
        """TODO: to be defined.
        A: Intial vibration vector -> np.ndarray
        ALPHA: Influence coefficient matrix -> MxN np.ndarray"""
        self.name = name
        self.A = A
        self.split_instance = []
        if isinstance(alpha, Alpha):
            ALPHA = alpha.value
        else:
            raise tools.CustomError('Please create Alpha instance first --> ex. alpha = Alpha()')

        try:
            _ = ALPHA.shape
            self.ALPHA = ALPHA
            self.N = ALPHA.shape[1]
            self.M = ALPHA.shape[0]
        except AttributeError:
            raise tools.CustomError('Missing valid ALPHA value')

    def solve(self):
        return self.W

    def expected_residual_vibration(self):
        return tools.residual_vibration(self.ALPHA, self.W, self.A)

    def rmse(self):
        return tools.rmse(self.expected_residual_vibration())






    def create_split(self):
        """ Factory method to create a split instance """
        return Model.Split(self)

    class Split:
        def __init__(self, model_instance):
            """ Enable accessing outer class variables """
            self.model = model_instance






        def split_setup(self, balancing_plane_index, holes_available, weights_available, max_number_weights_per_hole=None,
                  max_weight_per_plane=None):
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
            # define mixed integer matrix in cvxpy
            S = cp.Variable(self.weight_available_matrix.shape, integer=True)
            # define objective function
            Real = cp.sum(cp.multiply(np.real(self.weight_available_matrix), S)) - np.real(self.weight)
            Imag = cp.sum(cp.multiply(np.imag(self.weight_available_matrix), S)) - np.imag(self.weight)
            Residuals = cp.norm(cp.hstack([Real, Imag]))
            obj_split = cp.Minimize(Residuals)
            # constraints
            const_splitting = [S >= 0]
            if self.max_number_weights_per_hole:
                if isinstance(self.max_number_weights_per_hole, int):
                    const_splitting += [cp.sum(S, axis=0)
                                        <= self.max_number_weights_per_hole]
                else:
                    raise tools.CustomError('`max_number_weights_per_hole` should be integer number')
            if self.max_weight_per_plane:
                if isinstance(self.max_weight_per_plane, (float, int)):
                        const_splitting += [cp.sum(S.T @ self.weights_available, axis=0)
                                        <= self.max_weight_per_plane]
                else:
                    raise tools.CustomError('`max_weight_per_plane` should be float number')

            # solve
            Prob_S = cp.Problem(obj_split, const_splitting)
            Prob_S.solve(solver=cp.XPRESS)  # TODO make solver options PYTHON_MIP(), ECOS_BB
            S = np.array(np.round(S.value))
            self.S = S
            self.Prob_S = Prob_S.value
            return S



        def results(self):
            df_splitting = pd.DataFrame(self.S, index=self.weights_available, columns=self.holes_available)
            df_splitting = df_splitting.loc[:, (df_splitting != 0).any(axis=0)]
            return df_splitting
        def error(self, options='error'):
            # Error equivilant weight after splitting
            W_equ_split = np.sum(self.weight_available_matrix * self.S)
            self.W_equ_split = W_equ_split
            error = abs(self.W_equ_split - self.weight)
            # Estimate the error generated by using minmax instead of norm2 in the objective function
            problem_error = (self.Prob_S - error) / abs(self.weight)
            if options == 'error':
                return error
            elif options== 'problem_error':
                return problem_error
            elif options == 'equ':
                return tools.convert_cart_math(W_equ_split)
            else:
                raise tools.CustomError('Invalid options. Choose options="error" for solution error'
                                        'caused by splitting, options="problem_error" for solution'
                                        ' accuracy and options="equ" for equivilant weight.')
        def update(self, confirm=False):
            if confirm:
                self.model.W[self.balancing_plane_index] = self.W_equ_split
                self.model.split_instance.append(self)
            elif not confirm:
                warnings.warn('This will change your model optimium solution.'
                        'Choose confirm=True')
                self.model.W[self.balancing_plane_index] = self.weight
            return self.model.W


class LeastSquares(Model):

    # TODO
    """Docstring for OLE
    subclass of model"""

    def __init__(self, A:np.array, alpha:'instance of Alpha class', name=''):
        """TODO: to be defined.
        A: Intial vibration vector -> np.ndarray
        ALPHA: Influence coefficient matrix -> NxM np.ndarray"""
        super().__init__(A, alpha, name=name)

    def solve(self, solver=None):
        W = cp.Variable((self.N, 1), complex=True)
        objective = cp.Minimize(cp.sum_squares(self.ALPHA @ W + self.A))
        prob = cp.Problem(objective)
        prob.solve()
        self.W = W.value
        return W.value


class Min_max(Model):

    # TODO
    """Docstring for OLE
    subclass of model"""

    def __init__(self, A:np.array, alpha:'instance of Alpha class', weight_const={}, name=''):
        """TODO: to be defined.
        A: Intial vibration vector -> np.ndarray
        ALPHA: Influence coefficient matrix -> NxM np.ndarray"""
        self.weight_const = weight_const
        super().__init__(A, alpha, name=name)

    def solve(self, solver=None):
        W=cp.Variable((self.N,1),complex=True)
        objective=cp.Minimize(cp.norm((self.ALPHA @ W + self.A),"inf"))
        constrains = []
        if self.weight_const != {}:
            try:
                for key, value in self.weight_const.items():
                    constrains += [cp.norm(W[key]) <= value]
            except NameError:
                raise tools.CustomError('Invalid weight constraint format')
        else:
            pass
        prob=cp.Problem(objective, constrains)
        prob.solve()
        self.W = W.value
        return W.value


class LMI(Model):

    # TODO
    """Docstring for OLE
    subclass of model"""

    def __init__(self, A:np.array, alpha:'instance of Alpha class',
                 weight_const={},
                 critical_planes={}, V_max=None, name=''):
        """TODO: to be defined.
        A: Intial vibration vector -> np.ndarray
        ALPHA: Influence coefficient matrix -> NxM np.ndarray
        critical_planes:  set of critical planes
       """
        self.weight_const = weight_const
        self.critical_planes = list(critical_planes)
        self.V_max = V_max
        super().__init__(A, alpha, name=name)

    def solve(self, solver=None):

        # Weight constraints
        N = self.N
        M = self.M
        wc = np.zeros(N)
        if self.weight_const != {}:
            try:
                for key, value in self.weight_const.items():
                    wc[key] = value
            except NameError:
                raise tools.CustomError('Invalid weight constraint format')
        else:
            pass

        # Identify critical planes
        if self.V_max:
            Vm = self.V_max
        else:
            raise tools.CustomError('V_max is not specified')

        if self.critical_planes and len(self.critical_planes)>0:
            list_cr = self.critical_planes
        else:
            raise tools.CustomError('Critical Planes are not set.')

        ALPHA = self.ALPHA.copy()
        A = self.A.copy()
        ALPHAcr = self.ALPHA[list_cr]
        Acr = A[list_cr]
        ALPHAncr = np.delete(ALPHA, list_cr, axis=0)
        Ancr = np.delete(A, list_cr, axis=0)
        # assign cvxpy variables
        WR= cp.Variable((N, 1))
        WI= cp.Variable((N, 1))
        Vc=cp.Variable()

        RRfcr=cp.diag(np.real(Acr)+np.real(ALPHAcr)@WR-np.imag(ALPHAcr)@WI)
        IRfcr=cp.diag(np.imag(Acr)+np.imag(ALPHAcr)@WR+np.real(ALPHAcr)@WI)

        RRfNcr=cp.diag(np.real(Ancr)+np.real(ALPHAncr)@WR-np.imag(ALPHAncr)@WI)
        IRfNcr=cp.diag(np.imag(Ancr)+np.imag(ALPHAncr)@WR+np.real(ALPHAncr)@WI)
        zcr=np.zeros((RRfcr.shape[0],RRfcr.shape[1]))
        Icr=np.eye(RRfcr.shape[0])
        zncr=np.zeros((RRfNcr.shape[0],RRfNcr.shape[1]))
        Incr=np.eye(RRfNcr.shape[0])

        objective=cp.Minimize(Vc)
        LMI_real =cp.bmat( [
                                [Vc*Icr,        RRfcr,    zcr,        -IRfcr],
                                [RRfcr,          Icr,      IRfcr,          zcr],
                                [zcr,            IRfcr,    Vc*Icr,        RRfcr],
                                [-IRfcr,         zcr,       RRfcr,          Icr]
                                                                                    ])
        LMI_imag =cp.bmat( [
                            [Vm**2*Incr,        RRfNcr,    zncr,        -IRfNcr],
                            [RRfNcr,          Incr,      IRfNcr,          zncr],
                            [zncr,            IRfNcr,    Vm**2*Incr,        RRfNcr],
                            [-IRfNcr,         zncr,       RRfNcr,          Incr]
                                                                                ])
        # Model weight constraints
        const_LMI_w=[]
        for i in range(N):
            LMI_weight =cp.bmat( [
                                [wc[i]**2,        WR[i],    0,        -WI[i]],
                                [WR[i],          1,      WI[i],          0],
                                [0,       WI[i],    wc[i]**2,        WR[i]],
                                [-WI[i],         0,       WR[i],          1]
                                                                                          ])
            const_LMI_w.append(LMI_weight>>0)
        const_LMI_w.append( LMI_real  >>0)
        const_LMI_w.append( LMI_imag >>0)
        # Stating the problem
        prob=cp.Problem(objective,const_LMI_w)
        prob.solve(cp.CVXOPT, kktsolver=cp.ROBUST_KKTSOLVER)
        W = WR + WI * 1j
        self.W = W.value
        return self.W



