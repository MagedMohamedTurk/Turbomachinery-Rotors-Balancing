import time
from scipy.interpolate import make_interp_spline
import matplotlib.pyplot as plt
import scipy.optimize as opt
import numpy as np
import sys
import yaml
import pytest
import test_tools
import hsbalance as hs


def test_faults():
    with pytest.raises(hs.CustomError) as error:
        hs.LeastSquares([1, 2], [1, 2])

@pytest.fixture()
def test_alpha():
    '''
    Creating alpha instance to test throwing faults
    '''
    alpha = hs.Alpha()
    value = np.random.uniform(0, 10, [2, 2])
    alpha.add(value + value * 1j)
    return alpha

def test_A_dim():
    '''
    Test the dimension of A to be 2x1
    '''
    real = np.random.uniform(0, 10, [1, 2])
    imag = np.random.uniform(0, 10, [1, 2])
    A = real + imag * 1j
    with pytest.raises(hs.CustomError) as e_info:
        hs.LeastSquares(test_A_dim, test_alpha)
    real = np.random.uniform(0, 10, [2, 2])
    imag = np.random.uniform(0, 10, [2, 2])
    A = real + imag * 1j
    with pytest.raises(hs.CustomError) as e_info:
        hs.LeastSquares(test_A_dim, test_alpha)


@pytest.fixture()
def n():
    '''
    tests for various matrix sizes
    for n = 1000 it took around 5 minutes on my machine
    '''
    return 250

@pytest.fixture()
def test_big_alpha(n):
    '''
    Creating alpha instance to test throwing faults
    '''
    alpha = hs.Alpha()
    real = np.random.uniform(0, 10, [n, n])
    imag = np.random.uniform(0, 10, [n, n])
    alpha.add(real + imag * 1j)
    return alpha

@pytest.fixture()
def test_big_A(n):
    '''
    Creating alpha instance to test throwing faults
    '''
    real = np.random.uniform(0, 10, [n, 1])
    imag = np.random.uniform(0, 10, [n, 1])
    return real + imag * 1j

@pytest.fixture
def test_model_LSQ(test_big_A, test_big_alpha):
    '''
    Creating a test model
    '''
    w =  hs.LeastSquares(test_big_A, test_big_alpha).solve()
    return w


@pytest.mark.timeout(100)
def test_big_matrix_LSQ(test_big_alpha, test_big_A, test_model_LSQ):
    '''
    Testing the perfromance of model
    '''
    start = time.time()
    error = hs.residual_vibration(test_big_alpha.value, test_model_LSQ, test_big_A)
    end = time.time()
    print(error.shape)
    print ('Time elapsed = ', end-start)
    np.testing.assert_allclose(error, 0, atol=1e-5)

if __name__ == '__main__':
    def test_performance(n):
        alpha = hs.Alpha()
        real = np.random.uniform(0, 10, [n, n])
        imag = np.random.uniform(0, 10, [n, n])
        alpha.add(real + imag * 1j)
        real = np.random.uniform(0, 10, [n, 1])
        imag = np.random.uniform(0, 10, [n, 1])
        A= real + imag * 1j
        start = time.time()
        w =  hs.LeastSquares(A, alpha).solve()
        error = hs.residual_vibration(alpha.value, w, A)
        t = time.time() - start
        return round(t, 2)
    performance_time = []
    N = [2, 10, 50, 100, 200, 400, 600, 800]
    for n in N:
        performance_time.append(test_performance(n))
    print(N, performance_time)
    spline = make_interp_spline(N, performance_time)
    x = np.linspace(min(N), max(N), 500)
    y  = spline(x)
    plt.plot(x, y, label="Performace Test")
    plt.xlabel('N (dimension of a Squared Influence Coeffecient Matrix)')
    plt.ylabel('Time (seconds)')
    plt.title('Performance Test of LeastSquares model')
    plt.savefig('../data/performace_test.png')
    plt.show()
