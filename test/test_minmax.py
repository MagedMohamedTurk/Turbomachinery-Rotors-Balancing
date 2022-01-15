import numpy as np
import sys
import yaml
import pytest
import test_tools
import hsbalance as hs

'''This module is for testing Min_Max model solver'''
# Reading the test cases from config.yaml file, to add more tests follow the rules on the file
tests, tests_id, timeout = test_tools.get_tests_from_yaml('Min_max')


@pytest.mark.parametrize('param, expected',
                         tests,
                         ids=tests_id
                         )
@pytest.mark.timeout(timeout)
def test_Min_max(param, expected):
    '''
    Testing instantiate Min_Max model and test it against test cases
    '''
    my_ALPHA = hs.Alpha()
    A = hs.convert_matrix_to_cart(param[0]['A'])
    weight_const = param[0]['weight_const']
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

    my_model = hs.Min_max(A, my_ALPHA,
                             weight_const=weight_const,name='Min_max')  # Setting the model almost with no constraints
    W = my_model.solve()
    print((expected))
    print('Residual Vibration rmse calculated = ', my_model.rmse())
    print('Residual Vibration rmse from test_case = ',
          hs.rmse(hs.residual_vibration(my_ALPHA.value, expected_W, A)))
    print('expected_residual_vibration',
          hs.convert_matrix_to_math(my_model.expected_residual_vibration()))
    print('Correction weights', hs.convert_cart_math(W))
    # Constraint Minmax algorithm was slightly inefficient in CVXPY
    # The rmse was marginally more than the author solution
    np.testing.assert_allclose(W, expected_W, rtol=0.09) # allowance 9% error


