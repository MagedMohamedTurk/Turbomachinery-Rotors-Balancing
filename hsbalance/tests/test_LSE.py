import numpy as np
import sys
import yaml
import pytest
sys.path.insert(0, '../')
import model
import tools
import test_tools


tests, tests_id, timeout = test_tools.get_tests_from_yaml('least_squares')


@pytest.mark.parametrize('param, expected',
                         tests,
                         ids=tests_id
                         )
@pytest.mark.timeout(timeout)
def test_simple_LSE(param, expected):
    ALPHA = tools.convert_matrix_to_cart(param[0]['ALPHA'])
    A = tools.convert_matrix_to_cart(param[0]['A'])
    expected_W = tools.convert_matrix_to_cart(expected)
    my_model = model.Model(name='simple_least_square', A=A, ALPHA=ALPHA)
    W = my_model.solve()
    print('Residual Vibration rmse calculated = ', my_model.rmse())
    print('Residual Vibration rmse from test_case = ',
          tools.rmse(tools.residual_vibration(ALPHA, expected_W, A)))
    np.testing.assert_allclose(W, expected_W, rtol=0.05) # allowance 5% error
