import numpy as np
import sys
sys.path.insert(0, '../')
import model

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

def test_convert_to_polar():
    output = model.convert_to_polar(6+8j)
    expected = (10,53.13)
    error = max((x-y)/y for x,y  in zip(output, expected))
    print('output=', output, '\n expected', expected
         , '\nerror', error)
    assert  error < 0.01

def test_convert_to_cartesian():
    output = model.convert_to_cartesian((4, 30))
    expected = 3.4641+2j
    error = abs(output - expected)
    print('output=', output, '\n expected', expected
         , '\nerror', error)
    assert  error < 0.01
