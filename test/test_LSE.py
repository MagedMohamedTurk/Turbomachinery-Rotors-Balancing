import numpy as np
import sys
import yaml
import pytest
sys.path.insert(0, '../')
from hsbalance import model
from hsbalance import tools
import test_tools
from hsbalance.CI_matrix import Alpha


'''This module is for testing Least square model solver'''
# Reading the test cases from config.yaml file, to add more tests follow the rules on the file
tests, tests_id, timeout = test_tools.get_tests_from_yaml('least_squares')


@pytest.mark.parametrize('param, expected',
                         tests,
                         ids=tests_id
                         )
@pytest.mark.timeout(timeout)
def test_simple_LSE(param, expected):
    '''
    Testing instantiate LMI model and test it against test cases
    '''
    my_ALPHA = Alpha()
    A = tools.convert_matrix_to_cart(param[0]['A'])
    A0 = [0]
    # It is acceptable to enter either direct_matrix or A,B,U matrices
    try:
        direct_matrix = tools.convert_matrix_to_cart(param[0]['ALPHA'])
        my_ALPHA.add(direct_matrix=direct_matrix)
    except KeyError:
        B = tools.convert_matrix_to_cart(param[0]['B'])
        U = tools.convert_matrix_to_cart(param[0]['U'])
        my_ALPHA.add(A=A, B=B, U=U)
    try:
         A0 = tools.convert_matrix_to_cart(param[0]['A0'])
    except KeyError:
        pass
    expected_W = tools.convert_matrix_to_cart(expected)
    my_model = model.LeastSquares(A-A0, my_ALPHA, name='simple_least_square')
    W = my_model.solve()
    print('Residual Vibration rmse calculated = ', my_model.rmse())
    print('Residual Vibration rmse from test_case = ',
          tools.rmse(tools.residual_vibration(my_ALPHA.value, expected_W, A)))
    print('expected_residual_vibration',
          tools.convert_matrix_to_math(my_model.expected_residual_vibration()))
    np.testing.assert_allclose(W, expected_W, rtol=0.05) # allowance 5% error

tests, tests_id, timeout = test_tools.get_tests_from_yaml('ill_condition_test')

@pytest.mark.parametrize('param, expected',
                         tests,
                         ids=tests_id
                         )
@pytest.mark.timeout(timeout)
def test_ill_condition(param, expected):
    '''
    Testing instantiate LMI model and test it against test cases
    '''
    my_ALPHA = Alpha()
    A = tools.convert_matrix_to_cart(param[0]['A'])
    A0 = [0]
    # It is acceptable to enter either direct_matrix or A,B,U matrices
    try:
        direct_matrix = tools.convert_matrix_to_cart(param[0]['ALPHA'])
        my_ALPHA.add(direct_matrix=direct_matrix)
        my_ALPHA.check(ill_condition_remove=True)
    except KeyError:
        B = tools.convert_matrix_to_cart(param[0]['B'])
        U = tools.convert_matrix_to_cart(param[0]['U'])
        my_ALPHA.add(A=A, B=B, U=U)
    try:
         A0 = tools.convert_matrix_to_cart(param[0]['A0'])
    except KeyError:
        pass
    expected_W = tools.convert_matrix_to_cart(expected)
    my_model = model.LeastSquares(A-A0, my_ALPHA, name='simple_least_square')
    W = my_model.solve()
    print('Residual Vibration rmse calculated = ', my_model.rmse())
    print('Residual Vibration rmse from test_case = ',
          tools.rmse(tools.residual_vibration(my_ALPHA.value, expected_W, A)))
    print('expected_residual_vibration',
          tools.convert_matrix_to_math(my_model.expected_residual_vibration()))
    np.testing.assert_allclose(W, expected_W, rtol=0.05) # allowance 5% error
