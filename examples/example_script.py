import hsbalance as hs
A = [['170@112'], ['53@78']]  # --> Initial vibration conditions First Row in Table  above.
B = [['235@94', '185@115'],  # --> Vibration at sensor 1 when trial masses were added at plane 1&2 (First column for both trial runs)
     ['58@68', '77@104']]  # Vibration at sensor 2 when trial masses were added at plane 1&2 (Second column for both trial runs)
U = ['1.15@0', '1.15@0']  # Trial masses 2.5 g at plane 1 and 2 consequently
A = hs.convert_math_cart(A)
B = hs.convert_math_cart(B)
U = hs.convert_math_cart(U)
alpha = hs.Alpha()  # Instantiate Alpha class
alpha.add(A=A, B=B, U=U)
model_LeastSquares = hs.LeastSquares(A=A, alpha=alpha)
w = model_LeastSquares.solve() #  Solve the model and get the correction weights vector
# Calculate Residual vibration vector
residual_vibration = hs.residual_vibration(alpha.value, w, A)
# Caculate Root mean square error for model
RMSE = hs.rmse(residual_vibration)
# Convert w back into mathmatical expression
w = hs.convert_cart_math(w)
# print results
print(model_LeastSquares.info())
