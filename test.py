import cvxpy as cp
import numpy as np

# Generate a random problem
print(cp.__version__)
print(np.__version__)
np.random.seed(0)
m, n= 10, 8

A = np.random.rand(m, n) + np.random.rand(m, n)*1j
b = np.random.randn(1,m) + np.random.randn(1,m)*1j
print(A, b)
# Construct a CVXPY problem
x = cp.Variable(A.shape, integer=True)
real = np.real(A) @ x.T - np.real(b)
imag = np.imag(A) @ x.T - np.imag(b)
objective = cp.Minimize(cp.sum_squares(cp.hstack([real, imag])))
const = [x>=0]
prob = cp.Problem(objective, const)
prob.solve(solver='ECOS_BB')
print("Status: ", prob.status)
print("The optimal value is", prob.value)
print("A solution x is")
print(np.round(x.value))
