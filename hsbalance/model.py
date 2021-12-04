import cvxpy as cp
import numpy as np
from hsbalance import ALPHA, tools
from hsbalance.ALPHA import CustomError


class Model:

    # TODO
    """Abstract class for models"""

    #TODO ALPHA to be instance of ALPHA class not np to be checked
    def __init__(self, A:np.array, ALPHA:np.array, name=''):
        """TODO: to be defined.
        A: Intial vibration vector -> np.ndarray
        ALPHA: Influence coefficient matrix -> MxN np.ndarray"""
        self.name = name
        self.A = A
        try:
            _ = ALPHA.shape
            self.ALPHA = ALPHA
            self.N = ALPHA.shape[1]
            self.M = ALPHA.shape[0]
        except AttributeError:
            raise CustomError('Missing valid ALPHA value')


    def solve(self):
        pass

    def expected_residual_vibration(self):
        return tools.residual_vibration(self.ALPHA, self.W, self.A)

    def rmse(self):
        return tools.rmse(self.expected_residual_vibration())


class LeastSquares(Model):

    # TODO
    """Docstring for OLE
    subclass of model"""

    def __init__(self, A:np.array, ALPHA:np.array, name=''):
        """TODO: to be defined.
        A: Intial vibration vector -> np.ndarray
        ALPHA: Influence coefficient matrix -> NxM np.ndarray"""
        super().__init__(A, ALPHA, name=name)

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

    def __init__(self, A:np.array, ALPHA:np.array, weight_const={}, name=''):
        """TODO: to be defined.
        A: Intial vibration vector -> np.ndarray
        ALPHA: Influence coefficient matrix -> NxM np.ndarray"""
        self.weight_const = weight_const
        super().__init__(A, ALPHA, name=name)

    def solve(self, solver=None):
        W=cp.Variable((self.N,1),complex=True)
        objective=cp.Minimize(cp.norm((self.ALPHA @ W + self.A),"inf"))
        constrains = []
        if self.weight_const != {}:
            try:
                for key, value in self.weight_const.items():
                    constrains += [cp.norm(W[key]) <= value]
            except NameError:
                raise CustomError('Invalid weight constraint format')
        else:
            pass
        prob=cp.Problem(objective, constrains)
        prob.solve(cp.CVXOPT, kktsolver=cp.ROBUST_KKTSOLVER)
        self.W = W.value
        return W.value


class LMI(Model):

    # TODO
    """Docstring for OLE
    subclass of model"""

    def __init__(self, A:np.array, ALPHA:np.array,
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
        super().__init__(A, ALPHA, name=name)

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
                raise CustomError('Invalid weight constraint format')
        else:
            pass

        # Identify critical planes
        if self.V_max:
            Vm = self.V_max
        else:
            raise CustomError('V_max is not specified')

        if self.critical_planes and len(self.critical_planes)>0:
            list_cr = self.critical_planes
        else:
            raise CustomError('Critical Planes are not set.')

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
