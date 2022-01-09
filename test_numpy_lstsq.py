import numpy as np
import cvxpy as cp
import statsmodels.api as sm
n = 4
m = 6
np.random.seed(42)
a_real = np.random.rand(m, 1)
a_imag = np.random.rand(m, 1)
A = a_real + a_imag * -1j

alpha_real = np.random.rand(m, n)
alpha_imag = np.random.rand(m, n)
alpha = alpha_real + alpha_imag * -1j


# using equations
w_equ = - np.linalg.inv(alpha.conj().T@alpha)@alpha.conj().T @ A
r_equ = alpha @ w_equ + A
rms_equ = round(np.sqrt(np.abs(r_equ) ** 2).mean(), 4)

# using lstsq
w_lstsq = - np.linalg.lstsq(alpha, A, rcond=None)[0]
r_lstsq = alpha @ w_lstsq + A
rms_lstsq = round(np.sqrt(np.abs(r_lstsq) ** 2).mean(), 4)

# using cvxpy
def cvxpy_method():
    w = cp.Variable((n, 1), complex=True)
    obj = cp.Minimize(cp.sum_squares(alpha @ w + A))
    cp.Problem(obj).solve()
    return w.value

w_cvx = cvxpy_method()
r_cvx = alpha @ w_cvx + A
rms_cvx = round(np.sqrt(np.abs(r_cvx) ** 2).mean(), 4)

print(f'''Using direct equation:\n{30*'='}\n{np.abs(w_equ)}\n\nr =\n{
          np.abs(r_equ)}\nrmse={rms_equ}\n\nUsing numpy lstsq function\n{30*'='}\n{
    np.abs(w_lstsq)}\nr =\n {np.abs(r_lstsq)}\nrmse={rms_lstsq}''')
print(f'''Using cvxpy:\n{30*'='}\n{np.abs(w_cvx)}\n\nr =\n{
          np.abs(r_cvx)}\nrmse={rms_cvx}''')



w1 = - np.linalg.pinv(alpha)@ A
w2 = - (np.linalg.inv(np.matrix(alpha).H@alpha)@np.matrix(alpha).H) @ A
np.testing.assert_allclose(w1, w2)

