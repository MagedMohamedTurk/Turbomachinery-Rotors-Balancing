import numpy as np
import sys
import yaml
import pytest
sys.path.insert(0, '../')
from ALPHA import ALPHA
import tools
import test_tools

'''This module if for testing ALPHA class'''

tests, tests_id, timeout = test_tools.get_tests_from_yaml('ALPHA_direct')
print(tests)
@pytest.mark.parametrize('param, expected',
                         tests,
                         ids=tests_id
                         )
@pytest.mark.timeout(timeout)
def test_ALPHA_direct(param, expected):
    my_ALPHA = ALPHA()
    my_ALPHA.add(direct_matrix=tools.convert_matrix_to_cart(param))
    expected = list(list(complex(x) for x in item) for item in expected)
    np.testing.assert_allclose(my_ALPHA.value, expected, rtol=0.05)  # allowance 5% error

tests, tests_id, timeout = test_tools.get_tests_from_yaml('ALPHA_from_matrices')

@pytest.mark.parametrize('param, expected',
                         tests,
                         ids=tests_id
                         )
@pytest.mark.timeout(timeout)
def test_ALPHA_from_matrices(param, expected):
    print(param, expected)
    for key, value in param[0].items():
        globals()[key] = value
    my_ALPHA = ALPHA()
    my_A = tools.convert_matrix_to_cart(A)
    my_B = tools.convert_matrix_to_cart(B)
    my_U = tools.convert_matrix_to_cart(U)
    print(A, B, U, keep_trial)
    my_ALPHA.add(A=my_A, B=my_B, U=my_U, keep_trial=keep_trial)
    expected = tools.convert_matrix_to_cart(expected)
    np.testing.assert_allclose(my_ALPHA.value, expected, rtol=0.05)  # allowance 5% error
