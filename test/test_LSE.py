import numpy as np
import sys
import yaml
import pytest
import test_tools
import hsbalance as hs


'''This module is for testing Least square model solver'''
# Reading the test cases from config.yaml file, to add more tests follow the rules on the file
tests, tests_id, timeout = test_tools.get_tests_from_yaml('least_squares')


@pytest.mark.parametrize('param, expected',
                         tests,
                         ids=tests_id
                         )
@pytest.mark.timeout(timeout)
def test_WLS(param, expected):
    '''
    Testing instantiate LMI model and test it against test cases
    '''
    my_ALPHA = hs.Alpha()
    A = hs.convert_matrix_to_cart(param[0]['A'])
    A0 = [0]
    # It is acceptable to enter either direct_matrix or A,B,U matrices
    try:
        direct_matrix = hs.convert_matrix_to_cart(param[0]['ALPHA'])
        my_ALPHA.add(direct_matrix=direct_matrix)
    except KeyError:
        B = hs.convert_matrix_to_cart(param[0]['B'])
        U = hs.convert_matrix_to_cart(param[0]['U'])
        my_ALPHA.add(A=A, B=B, U=U)
    try:
         A0 = hs.convert_matrix_to_cart(param[0]['A0'])
    except KeyError:
        pass
    expected_W = hs.convert_matrix_to_cart(expected)
    my_model = hs.LeastSquares(A-A0, my_ALPHA, name='simple_least_square')
    W = my_model.solve(solver='WLS')
    print('Residual Vibration rmse calculated = ', my_model.rmse())
    print('Residual Vibration rmse from test_case = ',
          hs.rmse(hs.residual_vibration(my_ALPHA.value, expected_W, A)))
    print('expected_residual_vibration',
          hs.convert_matrix_to_math(my_model.expected_residual_vibration()))
    np.testing.assert_allclose(W, expected_W, rtol=0.05) # allowance 5% error

