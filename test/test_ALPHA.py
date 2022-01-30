import numpy as np
import sys
import yaml
import pytest
import test_tools
import warnings
import hsbalance as hs

'''This module is for testing ALPHA class'''
# Reading the test cases from config.yaml file
tests, tests_id, timeout = test_tools.get_tests_from_yaml('ALPHA_direct')
# Parametrized the test for all testcases
@pytest.mark.parametrize('param, expected',
                         tests,
                         ids=tests_id
                         )
@pytest.mark.timeout(timeout)
def test_ALPHA_direct(param, expected):
    '''
    Pytest function to test instantiate Alpha from direct_matrix
    Inputs:
        param, expected : from config.yaml file
    '''
    # Instantiate Alpha class
    my_ALPHA = hs.Alpha()
    # Add direct matrix to the instance
    my_ALPHA.add(direct_matrix = hs.convert_matrix_to_cart(param))
    expected = list(list(complex(x) for x in item) for item in expected)
    np.testing.assert_allclose(my_ALPHA.value, expected, rtol=0.05)  # allowance 5% error

tests, tests_id, timeout = test_tools.get_tests_from_yaml('ALPHA_from_matrices')

@pytest.mark.parametrize('param, expected',
                         tests,
                         ids=tests_id
                         )
@pytest.mark.timeout(timeout)
def test_ALPHA_from_matrices(param, expected):
    '''
    Function to test instantiating Alpha class from matrices
    param, expected : from config.yaml file
    '''
    for key, value in param[0].items():
        globals()[key] = value
    my_ALPHA = hs.Alpha()
    my_A = hs.convert_matrix_to_cart(A)
    my_B = hs.convert_matrix_to_cart(B)
    my_U = hs.convert_matrix_to_cart(U)
    print(A, B, U, keep_trial)
    my_ALPHA.add(A=my_A, B=my_B, U=my_U, keep_trial=keep_trial)
    expected = hs.convert_matrix_to_cart(expected)
    np.testing.assert_allclose(my_ALPHA.value, expected, rtol=0.05)  # allowance 5% error


# Test symmetric
@pytest.fixture()
def test_alpha():
    '''
    creating alpha instance to test throwing faults
    '''
    return hs.Alpha()

def test_alpha_check(test_alpha):
    '''
    Test raising symmetric matrix warning
    '''
    with pytest.warns(UserWarning):
        test_alpha.add(direct_matrix=np.array([[1, 2], [2.8, 0.9]]))
        test_alpha.check()
# Test ill_condition
def test_alpha_ill(test_alpha):
    '''
    Test ill conditioned planes
    '''
    test_alpha.add(direct_matrix=np.array([[1, 3], [2.5, 6.5]]))
    with pytest.warns(UserWarning):
        test_alpha.check(ill_condition_remove=True)
        # ill_condition_remove should remove the second column as it is depending of the first
        # (multiplied by 2 approx.)
        np.testing.assert_allclose(test_alpha.value, np.array([[3], [6.5]]))

def test_direct_matrix_dim(test_alpha):
    '''
    Check raising error due to improper dimension of matrix
    '''
    with pytest.raises(hs.CustomError) as e_info:
        test_alpha.add(direct_matrix=np.array([[1, 2, 3], [4, 5, 6]]))
    assert 'Number of rows(measuring points)' in str(e_info)

def test_alpha_dim(test_alpha):
    '''
    Check raising error due to improper dimension of matrix
    '''
    with pytest.raises(IndexError) as e_info:
        # one dim matrix
        test_alpha.add(direct_matrix=np.array([1, 2, 3, 4, 5, 6]))
    assert 'Influence coefficient matrix should be of more than 1 dimensions.' in str(e_info)
    with pytest.raises(hs.CustomError) as e_info:
        # wrong dim matrix
        test_alpha.add(direct_matrix=np.array([[1, 2, 3], [4, 5, 6]]))
    assert 'Number of rows(measuring points)' in str(e_info)
    with pytest.raises(hs.CustomError) as e_info:
        # not numpy array
        test_alpha.add(direct_matrix=[[2,3], [3,4]])
    assert 'numpy arrays' in str(e_info)
    with pytest.raises(hs.CustomError) as e_info:
        # missing U and B
        test_alpha.add(A=np.array([[1],[2]]))
    assert 'Either' in str(e_info)
    with pytest.raises(hs.CustomError) as e_info:
        # A mismatch dim
        test_alpha.add(A=np.array([[1,2],[1,2]]), B=np.array([[1,2], [2,3]]), U=np.array([1, 3]))
    assert '`A` should be column ' in str(e_info)
    with pytest.raises(hs.CustomError) as e_info:
        # B mismatch dim
        test_alpha.add(A=np.array([[1],[1]]), B=np.array([[1,2,3], [2,3,3]]), U=np.array([1, 3]))
    assert '`B` dimensions' in str(e_info)
    with pytest.raises(hs.CustomError) as e_info:
        # U mismatch dim
        test_alpha.add(A=np.array([[1],[1]]), B=np.array([[1,2], [2,3]]), U=np.array([[1, 3, 3, 4]]))
    assert '`U` should be row' in str(e_info)
    with pytest.raises(hs.CustomError) as e_info:
        # U mismatch dim
        test_alpha.add(A=np.array([[1],[1]]), B=np.array([[1,2], [2,3]]), U='this is non sense')
    assert 'numpy arrays' in str(e_info)

def test_alpha_shape(test_alpha):
    test_alpha.add(np.random.rand(6,4))
    assert test_alpha.shape == (6,4)


def test_info():
    # Set random data
    np.random.seed(42)
    alpha1 = hs.Alpha()
    alpha1.name = 'Turbine'
    m = 3
    n = 3
    real = np.random.rand(m, n)
    imag = np.random.rand(m, n)
    comp= real + imag*1j
    # alpha1 from A, B, U
    alpha1.add(A = np.random.rand(3,1)+np.random.rand(3,1)*1j,
              B=np.random.rand(3,5)+np.random.rand(3,5)*1j,
              U=np.random.rand(5)+np.random.rand(5)*1j)
    # alpha2 from direct_matrix
    alpha2 = hs.Alpha()
    alpha2.add(comp)
    # Condition logging and printing
    condition1 = hs.Condition(name='Speed 2500')
    condition1.add(alpha2, A=np.random.rand(m,1))
    print(alpha1, alpha2, condition1)
