import hsbalance as hs
print('\n'*80)
# The example is taken from B&K document (https://www.bksv.com/media/doc/17-227.pdf)
#Table 1 for example 4
# Stating Problem Data
# Vibration can be expressed as string 'amplitude @ phase' where amplitude is in any desired unit
# (micro - mils - mm/sec) and phase in degrees as measured by tachometer.
A = [['170@112'], ['53@78']]  # Initial vibration conditions
B = [['235@94', '185@115'],  # Vibration at sensor 1 when trial masses were added at plane 1&2
     ['58@68', '77@104']]  # Vibration at sensor 2 when trial masses were added at plane 1&2
U = ['1.15@0', '1.15@0']  # Trial masses 2.5 g at plane 1 and 2 consequently
# Convert from mathematical expression into complex numbers
A = hs.convert_math_cart(A)
B = hs.convert_math_cart(B)
U = hs.convert_math_cart(U)
# Create Influence Coeffecient Matrix Alpha
alpha = hs.Alpha()  # Instantiate Alpha class
alpha.add(A=A, B=B, U=U)
# Now we have alpha instance and initial condition A; we can create a model
model_LeastSquares = hs.LeastSquares(A=A, alpha=alpha)
w = model_LeastSquares.solve() #  Solve the model and get the correction weights vector
residual_vibration = hs.residual_vibration(alpha.value, w, A)
RMSE = hs.rmse(residual_vibration)
w = hs.convert_cart_math(w)
print('Correction Weights are: \n{}\n Root Mean Squares = {}\n '
      '\n Residule Vibration vector\n{}'.format(w, RMSE, residual_vibration))
