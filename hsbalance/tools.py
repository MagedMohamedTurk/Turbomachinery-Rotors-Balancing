import numpy as np
import cmath as cm


def convert_to_polar(cart):
    '''
    docs: Convert complex number in the cartesian form
          into polar form.
    :inputs:
    cart: Complex number in cartesian number ex. 12+23j
         -> <class 'complex'>
    output: Complex number in polar form (modulus, phase in degrees)
            ex.(12, 90) -> <class 'tuple'>
    '''
    phase = cm.phase(cart) * 180 / cm.pi
    if phase<0:
            phase= phase+360
    return (abs(cart), phase)

def convert_to_cartesian(polar):
    '''
    docs: Convert number from polar form to cartesian complex number.
    :inputs:
    polar: Complex number in polar form (modulus, phase in degrees)
            ex.(12, 90) -> <class 'tuple'>
    output: Complex number in cartesian number ex. 12+23j
         -> <class 'complex'>
    '''
    theta = polar[1] * cm.pi / 180
    return polar[0]*cm.cos(theta)+ polar[0]* cm.sin(theta)*1j

def convert_math_cart(str):
    '''
    docs: Convert from polar mathematical expression to cartesian.
    :inputs:
    str: mathematical expression for polar number in form of
        modulus@angle(degrees) ex. 12@20 -> 12 at 20 degree angle.
    output: Complex number in cartesian number ex. 12+23j
         -> <class 'complex'>
    '''
    polar = tuple(map(float, str.split(sep='@')))
    return convert_to_cartesian(polar)

def convert_matrix_to_cart(ALPHA_math):
    """
    docs: Convert influence coeffecient matrix ALPHA from mathematical expression
    form to cartesian form.

    :ALPHA_math: list of lists with polar mathmematical expression
            ex . [[90@58, 21@140]
                  [10.9@10, 37.9@142]]
    :returns: np.dnarray with cartesian form

    """
    try: # test if input is list of list or a simple list
        ALPHA = list(list(map(convert_math_cart, item))
                         for item in ALPHA_math)
    except TypeError:
        ALPHA = list(map(convert_math_cart, item)
                         for item in ALPHA_math)
    ALPHA = np.array(ALPHA)
    return ALPHA
