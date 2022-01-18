import numpy as np
import sys
import yaml
import pytest
import test_tools
import hsbalance as hs


'''This module is for testing Least square model solver'''
np.random.seed(42)
@pytest.fixture()
def n():
    '''
    tests for various matrix sizes
    for n = 1000 it took around 5 minutes on my machine
    '''
    return 10

@pytest.fixture()
def m():
    '''
    tests for various matrix sizes
    for n = 1000 it took around 5 minutes on my machine
    '''
    return 30

@pytest.fixture()
def test_alpha(m, n):
    '''
    Creating alpha instance
    '''
    alpha = hs.Alpha()
    real = np.random.uniform(0, 1, [m, n])
    imag = np.random.uniform(0, 1, [m, n])
    alpha.add(real + imag * 1j)
    return alpha

@pytest.fixture()
def test_A(m):
    '''
    Creating alpha instance
    '''
    real = np.random.uniform(0, 10, [m, 1])
    imag = np.random.uniform(0, 10, [m, 1])
    return real + imag * 1j
# @pytest.fixture()
# def C(m):
#     C = np.ones((m,1))
#     return C

# @pytest.fixture
# def test_model_WLS(test_A, test_alpha, n, C):
#     '''
#     Creating a test model
#     '''
#     w = model.LeastSquares(test_A, test_alpha, C).solve(solver='WLS')
#     return w


def test_matrix_WLS(test_alpha, test_A, m):
    '''
    Testing the performance of model
    '''
    alpha = test_alpha.value
    print(alpha)
    C = np.ones((m,1)) # weight matrix coefficient C
    # Carry out the test for c = 0 in all vector C indcies
    for c0 in range(len(C)):
        C[c0] = 0
        w = hs.model.LeastSquares(test_A, test_alpha, C=C).solve('WLS')
        # Cross check with the equation w = - pseudo_iverse(diag(C).alpha).A
        expected = - np.linalg.pinv(np.diag(C.T[0]) @ alpha) @ test_A
        np.testing.assert_allclose(expected, w)
        C[c0] = 1
