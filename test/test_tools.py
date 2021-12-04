import numpy as np
import sys
import yaml
import pytest
sys.path.insert(0, '../')
from hsbalance import tools

# Import test data from test_cases.yaml


# Testing functions against test_cases
def get_tests_from_yaml(function):
    """Collects test_cases data from config.yaml file

    :function: function name -> str
    :returns: tests -> list of tuples (input, expected)
                , tests_id -> list

    """
    try:
        with open('config.yaml') as f:
            test_cases = yaml.load(f, Loader=yaml.FullLoader)
            # Loading global parameters
            timeout = test_cases['timeout']  # TODO check time to be a number
    except (yaml.YAMLError, IOError):
        print('Error loading <config.yaml> file')
    tests = []
    tests_id = []
    for test_id, test in test_cases[function]['test_cases'].items():
        tests.append(test)
        tests_id.append(test_id)
    return tests, tests_id, timeout


# Testing convert_to_polar
tests, tests_id, timeout = get_tests_from_yaml('convert_to_polar')


@pytest.mark.parametrize('param, expected',
                         tests,
                         ids=tests_id
                         )
@pytest.mark.timeout(timeout)
def test_convert_to_polar(param, expected):
    output = tools.convert_to_polar(complex(param))
    error = max((x-y)/y for x, y in zip(output, expected))
    print('output=', output, '\n expected', expected,
          '\nerror', error)
    assert error < 0.01


# Testing convert_to_cartesian
tests, tests_id, timeout= get_tests_from_yaml('convert_to_cartesian')


@pytest.mark.parametrize('param, expected',
                         tests,
                         ids=tests_id
                         )
@pytest.mark.timeout(timeout)
def test_convert_to_cartesian(param, expected):
    output = tools.convert_to_cartesian(param)
    expected = complex(expected)
    error = abs(output - expected)
    print('output=', output, '\n expected', expected, '\nerror', error)
    assert error < 0.01


# Testing convert_math_cart
tests, tests_id, timeout  = get_tests_from_yaml('convert_math_cart')


@pytest.mark.parametrize('param, expected',
                         tests,
                         ids=tests_id
                         )
@pytest.mark.timeout(timeout)
def test_convert_math_cart(param, expected):
    output = tools.convert_math_cart(param)
    expected = complex(expected)
    error = abs(output - expected)
    print('output=', output, '\n expected', expected, '\nerror', error)
    assert error < 0.01


# Testing convert_matrix_to_cart
tests, tests_id, timeout = get_tests_from_yaml('convert_matrix_to_cart')


@pytest.mark.parametrize('param, expected',
                         tests,
                         ids=tests_id
                         )
@pytest.mark.timeout(timeout)
def test_convert_matrix_to_cart(param, expected):
    output = tools.convert_matrix_to_cart(param)
    try:
        expected = list(list(complex(x) for x in item) for item in expected)
    except ValueError:
        expected = list(complex(x) for x in expected)
    print(output, expected)
    expected = np.array(expected)
    print('output=', output, '\n expected', expected, '\nerror',
          (output - expected) / expected)
    # estimation rtol 5% error to compensate manual entry error
    np.testing.assert_allclose(output, expected, rtol=0.05)

# Testing rmse
tests, tests_id, timeout = get_tests_from_yaml('rmse')


@pytest.mark.parametrize('param, expected',
                         tests,
                         ids=tests_id
                         )
@pytest.mark.timeout(timeout)
def test_rmse(param, expected):
    output = tools.rmse(tools.convert_matrix_to_cart(param))
    error = output - expected
    print('output=', output, '\n expected', expected,
          '\nerror', error)
    assert error < 0.01

# Testing convert_cart_math
tests, tests_id, timeout = get_tests_from_yaml('convert_cart_math')


@pytest.mark.parametrize('param, expected',
                         tests,
                         ids=tests_id
                         )
@pytest.mark.timeout(timeout)
def test_convert_cart_math(param, expected):

    output = tools.convert_cart_math(complex(param))
    assert expected == str(output)
