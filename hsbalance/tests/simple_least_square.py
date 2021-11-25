import numpy as np
import sys
import yaml
import pytest
sys.path.insert(0, '../')
import model

# Import test data from test_cases.yaml
try:
    with open('config.yaml') as f:
        test_cases = yaml.load(f, Loader=yaml.FullLoader)
        # Loading global parameters
        timeout = test_cases['timeout']  # TODO check time to be a number
except (yaml.YAMLError, IOError):
    print('Error loading <config.yaml> file')

# Testing functions against test_cases
def get_tests_from_yaml(function):
    """Collects test_cases data from config.yaml file

    :function: function name -> str
    :returns: tests -> list of tuples (input, expected)
                , tests_id -> list

    """

    tests = []
    tests_id = []
    for test_id, test in test_cases[function]['test_cases'].items():
        tests.append(tuple(test))
        tests_id.append(test_id)
    return tests, tests_id


# Testing convert_to_polar
tests,tests_id = get_tests_from_yaml('convert_to_polar')
@pytest.mark.parametrize('param, expected',
                         tests,
                         ids=tests_id
                         )
@pytest.mark.timeout(timeout)
def test_convert_to_polar(param, expected):
    output = model.convert_to_polar(complex(param))
    error = max((x-y)/y for x, y in zip(output, expected))
    print('output=', output, '\n expected', expected,
          '\nerror', error)
    assert error < 0.01


# Testing convert_to_cartesian
tests,tests_id = get_tests_from_yaml('convert_to_cartesian')
@pytest.mark.parametrize('param, expected',
                         tests,
                         ids=tests_id
                         )
@pytest.mark.timeout(timeout)
def test_convert_to_cartesian(param, expected):
    output = model.convert_to_cartesian(param)
    expected = complex(expected)
    error = abs(output - expected)
    print('output=', output, '\n expected', expected
         , '\nerror', error)
    assert  error < 0.01








ALPHA = np.array([[41.47+66.37j, -13.99+11.74j],
                  [9.33+1.65j, -25.97+20.29j]
                  ])
A = np.array([[-63.68+157.62j],
              [11.02+51.84j]
              ])
expected = np.array([[-1.04-1.66j],
                    [-.55+.91j]])
my_model = model.Model(name='simple_least_square', A=A, ALPHA=ALPHA)
W = my_model.solve()
def test_simple_LSE():
    assert max((W- expected)/W) < 0.01

