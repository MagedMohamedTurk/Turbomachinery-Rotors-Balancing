import numpy as np
import sys
import yaml
import pytest
sys.path.insert(0, '../')
import model
import tools
import test_tools

# Import test data from test_cases.yaml

#ALPHA = np.array([[41.47+66.37j, -13.99+11.74j],
#                  [9.33+1.65j, -25.97+20.29j]
#                  ])
#A = np.array([[-63.68+157.62j],
#              [11.02+51.84j]
#              ])
#expected = np.array([[-1.04-1.66j],
#                    [-.55+.91j]])
#my_model = model.Model(name='simple_least_square', A=A, ALPHA=ALPHA)
#W = my_model.solve()


tests, tests_id, timeout = test_tools.get_tests_from_yaml('least_squares')
print(tests)


@pytest.mark.parametrize('param, expected',
                         tests,
                         ids=tests_id
                         )
@pytest.mark.timeout(timeout)
def test_simple_LSE(param, expected):
    ALPHA = tools.convert_matrix_to_cart(param[0]['ALPHA'])
    A = tools.convert_matrix_to_cart(param[0]['A'])
    expected = tools.convert_matrix_to_cart(expected)
    my_model = model.Model(name='simple_least_square', A=A, ALPHA=ALPHA)
    W = my_model.solve()
    np.testing.assert_allclose(W, expected, rtol=0.01) # allowance 1% error
