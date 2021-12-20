import numpy as np
import cmath as cm

class CustomError(Exception):
    '''
    The class is used to raise custom expections
    '''
    pass

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
    return complex(polar[0]*cm.cos(theta), polar[0] * cm.sin(theta))


def convert_math_cart(str):
    '''
    docs: Convert from polar mathematical expression to cartesian.
    :inputs:
    str: mathematical expression for polar number in form of
        modulus@angle(degrees) ex. 12@20 -> 12 at 20 degree angle.
    output: Complex number in cartesian number ex. 12+23j
         -> <class 'complex'>
    '''
    # TODO BUG: accept real numbers without @
    polar = tuple(map(float, str.split(sep='@')))
    return convert_to_cartesian(polar)

convert_math_cart = np.vectorize(convert_math_cart)

def convert_cart_math(complex_num):
    """TODO: inverse of convert_math_cart

    :complex: TODO
    :returns: TODO

    """
    polar = convert_to_polar(complex_num)
    return (str(round(polar[0], 3)))+'@'+(str(round(polar[1], 1)))

convert_cart_math = np.vectorize(convert_cart_math)
def convert_matrix_to_cart(ALPHA_math):
    """
    docs: Convert influence coeffecient matrix ALPHA from mathematical expression
    form to cartesian form.

    :ALPHA_math: list of lists with polar mathmematical expression
            ex . [[90@58, 21@140]
                  [10.9@10, 37.9@142]]
    :returns: np.dnarray with cartesian form

    """
    return convert_math_cart(ALPHA_math)


def convert_matrix_to_math(matrix):
    """
    inverse of convert_matrix_to_cart

    """
    return convert_cart_math(matrix)

def rmse(residual_vibration):
    '''
    Calculate the root mean square error for residual_vibration column matrix
    subtract each residual vibration from zero and taking the square root
    of the summation, rounding the result to the fourth decimal point
    Args:
        residual_vibration: numpy array
    Return: RMSE deviated from 0
    '''
    return round(np.sqrt(np.abs(residual_vibration) ** 2).mean(), 4)

def residual_vibration(ALPHA, W, A):
    '''
    Calculate the residual vibration between ALPHA matrix
    and solution W with intial vibration A
    Args:
        ALPHA : Influence coefficient matrix -> np.array
        A : Initial vibration column array -> np.array
        W : Solution balancing weight row vector -> np.array
    Return:
        residual_vibration column array -> np.array
    '''
    return ALPHA @ W + A

