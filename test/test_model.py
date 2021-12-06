import numpy as np
import sys
import yaml
import pytest
sys.path.insert(0, '../')
from hsbalance import model
from hsbalance import tools
import test_tools
from hsbalance.CI_matrix import Alpha



def test_faults():
    with pytest.raises(tools.CustomError) as error:
        model.Model([1, 2], [1, 2])
