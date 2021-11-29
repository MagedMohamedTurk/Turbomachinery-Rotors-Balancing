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
    print(param[0])
    for key, value in param[0].items():
        globals()[key] = tools.convert_matrix_to_cart(value)
    my_ALPHA = ALPHA()
    print(A, B, U)
    my_ALPHA.add(A=A, B=B, U=U)
    expected = (B- A)/U 
    np.testing.assert_allclose(my_ALPHA.value, expected, rtol=0.05)  # allowance 5% error
