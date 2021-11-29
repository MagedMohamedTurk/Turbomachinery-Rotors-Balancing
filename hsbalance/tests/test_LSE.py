import numpy as np
import sys
import yaml
import pytest
sys.path.insert(0, '../')
import model
import tools
import test_tools
from ALPHA import ALPHA


tests, tests_id, timeout = test_tools.get_tests_from_yaml('least_squares')


@pytest.mark.parametrize('param, expected',
                         tests,
                         ids=tests_id
                         )
@pytest.mark.timeout(timeout)
def test_simple_LSE(param, expected):
    my_ALPHA = ALPHA()
    A = tools.convert_matrix_to_cart(param[0]['A'])
    try:
         direct_matrix = tools.convert_matrix_to_cart(param[0]['ALPHA'])
         my_ALPHA.add(direct_matrix=direct_matrix)
    except KeyError:
         B = tools.convert_matrix_to_cart(param[0]['B'])
         U = tools.convert_matrix_to_cart(param[0]['U'])
         try:
             A0 = tools.convert_matrix_to_cart(param[0]['ALPHA'])
             my_ALPHA.add(A=A, B=B, A0=A0, U=U)
         except KeyError:
             my_ALPHA.add(A=A, B=B, U=U)

    expected_W = tools.convert_matrix_to_cart(expected)
    my_model = model.Model(name='simple_least_square', A=A, ALPHA=my_ALPHA.value)
    W = my_model.solve()
    print('Residual Vibration rmse calculated = ', my_model.rmse())
    print('Residual Vibration rmse from test_case = ',
          tools.rmse(tools.residual_vibration(my_ALPHA.value, expected_W, A)))
    np.testing.assert_allclose(W, expected_W, rtol=0.05) # allowance 1% error
