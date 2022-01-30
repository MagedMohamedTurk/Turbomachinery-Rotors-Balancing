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

def test_model_with_no_argument():
    with pytest.raises(TypeError) as e_info:
        model = hs.LeastSquares()
        assert 'Either (A and Alpha) or `conditions` should be assigned.' in str(e_info)
        A = np.random.rand(2,1)
        condition = hs.Conditions()
        model = hs.LeastSquares(A=A, conditions=[condition])
        assert 'Either (A and Alpha) or `conditions` should be assigned.' in str(e_info)
def test_faults():
    with pytest.raises(hs.CustomError) as error:
        hs.LeastSquares([1, 2], [1, 2])

@pytest.fixture()
def test_A():
    '''
    Creating alpha instance to test throwing faults
    '''
    A = np.random.uniform(0, 10, [2, 1])
    return A

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

# Testing Condition
def test_Condition(test_A, test_alpha):
    condition = hs.Condition()
    condition.add(test_alpha, test_A)
    assert condition.alpha == test_alpha
    np.testing.assert_allclose(condition.A, test_A)

    with pytest.raises(IndexError) as e_info:
        row_A = np.random.rand(5)
        condition.add(test_alpha, row_A)
    assert 'A should be column vector of Mx1 dimension' in str(e_info)

    with pytest.raises(IndexError) as e_info:
        square_A = np.random.rand(5, 5)
        condition.add(test_alpha, square_A)
    assert 'A should be column vector of Mx1 dimension' in str(e_info)

    with pytest.raises(IndexError) as e_info:
        mismatch_A = np.random.rand(3,1)
        condition.add(test_alpha, mismatch_A)
    assert 'A and alpha should have the same 0 dimension(M).' in str(e_info)

    with pytest.raises(TypeError) as e_info:
        A = [[3], [3], [3]]
        condition.add(test_alpha, A)
    assert 'numpy array' in str(e_info)

    with pytest.raises(IndexError) as e_info:
        alpha = hs.Alpha()
        alpha.add(np.random.rand(5,5))
        wrong_first_dim_A = np.random.rand(3, 1)
        condition.add(alpha, wrong_first_dim_A)
    print(condition.alpha.value, condition.A)
    assert 'same 0 dimension(M)' in str(e_info)

def test_model_conditions():
    test_alpha_1 = hs.Alpha()
    test_alpha_1.add(np.ones((2,2)))
    test_alpha_2 = hs.Alpha()
    test_alpha_2.add(np.ones((2,2)) * 2)
    test_A_1 = np.ones((2,1))
    test_A_2 = np.ones((2,1)) * 2
    condition_1 = hs.Condition()
    condition_1.add(test_alpha_1, test_A_1)
    condition_2 = hs.Condition()
    condition_2.add(test_alpha_2, test_A_2)
    model = hs.LeastSquares(conditions =[condition_1, condition_2])
    np.testing.assert_allclose(model.ALPHA , np.array([[1, 1],
                                                              [1, 1],
                                                              [2, 2],
                                                              [2, 2]]))
    np.testing.assert_allclose(model.A , np.array([[1],
                                                   [1],
                                                   [2],
                                                   [2]]))

def test_info_model():
    # Set random data
    np.random.seed(42)
    m = 3
    n = 3
    real = np.random.rand(m, n)
    imag = np.random.rand(m, n)
    comp= real + imag*1j
    alpha1 = hs.Alpha()
    alpha1.add(comp)
    real = np.random.rand(m, n)
    imag = np.random.rand(m, n)
    comp= real + imag*1j
    alpha2 = hs.Alpha()
    alpha2.add(comp)
    # Condition logging and printing
    condition1 = hs.Condition(name='Speed 1300')
    condition1.add(alpha2, A=np.random.rand(m,1))
    condition2 = hs.Condition(name='Speed 2500')
    condition2.add(alpha2, A=np.random.rand(m,1))
    model = hs.LeastSquares(conditions=[condition1, condition2])
    model.solve()
    angles = np.arange(100,300,10)  # angles
    split1 = model.create_split()
    split1.split_setup(0, max_number_weights_per_hole=1, holes_available=[angles]
                                                   ,weights_available=[0.1])
    split2 = model.create_split()
    split2.split_setup(1, max_number_weights_per_hole=1, holes_available=[angles]
                                                   ,weights_available=[0.2])
    split1.split_solve()
    split2.split_solve()
    split1.update(confirm=True)
    split2.update(confirm=True)
    print(model.info())


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
