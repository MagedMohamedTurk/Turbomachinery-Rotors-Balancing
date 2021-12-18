import numpy as np
import sys
import yaml
import pytest
sys.path.insert(0, '../')
from hsbalance import model
from hsbalance import tools
import test_tools
from hsbalance.CI_matrix import Alpha


tests, tests_id, timeout = test_tools.get_tests_from_yaml('splitting')


@pytest.mark.parametrize('param, expected',
                         tests,
                         ids=tests_id
                         )
@pytest.mark.timeout(timeout)
def test_split_LSE(param, expected):
    my_ALPHA = Alpha()
    A = tools.convert_matrix_to_cart(param[0]['A'])
    A0 = [0]
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
    expected_W = tools.convert_matrix_to_cart(expected)[0]
    my_model = model.LeastSquares(A-A0, my_ALPHA, name='simple_least_square')
    W = my_model.solve()
    # Splitting model for weight at plane 0
    angles = np.arange(100,300,5)  # angles
    split = my_model.create_split()
    split.split_setup(0, max_number_weights_per_hole=1, holes_available=[angles]
                                                   ,weights_available=[10])
    split.split_solve()
    W_split = tools.convert_math_cart(split.error(options='equ'))

    np.testing.assert_allclose(W_split, expected_W, rtol=0.05) # allowance 5% error
    # Splitting model for weight at plane 1
    expected_W = tools.convert_matrix_to_cart(expected)[1]
    angles = np.arange(-50,50,5)  # angles
    split = my_model.create_split()
    split.split_setup(1, max_number_weights_per_hole=1, holes_available=[angles]
                                                   ,weights_available=[20])
    split.split_solve()
    W_split = tools.convert_math_cart(split.error(options='equ'))

    np.testing.assert_allclose(W_split, expected_W, rtol=0.05) # allowance 5% error
