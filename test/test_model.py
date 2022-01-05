import numpy as np
import sys
import yaml
import pytest
import test_tools
sys.path.insert(0, '../src/hsbalance')
import model
import tools
from CI_matrix import Alpha



def test_faults():
    with pytest.raises(tools.CustomError) as error:
        model.Model([1, 2], [1, 2])

@pytest.fixture()
def test_alpha():
    '''
    Creating alpha instance to test throwing faults
    '''
    alpha = Alpha()
    value = np.random.uniform(0, 10, [2, 2])
    alpha.add(value + value * 1j)
    return Alpha()

@pytest.fixture()
def test_A():
    '''
    Creating Intial vibration test vector
    '''
    value = np.random.uniform(0, 10, [1, 2])
    return value + value * 1j

def test_model_LSQ(test_A, test_alpha):
    '''
    Creating a test model
    '''
    assert isinstance(test_alpha, Alpha)
