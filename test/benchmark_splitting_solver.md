# Introduction
This work was based on Huang et al. work[[1]](#1)  
The benchmark is referenced to notebook `hsbalance_Playground.ipynb`
After I calculate the optimum solution for a model, I need to put the weight in its location per plane as precisely as possible.  
In practice, there are a lot of difficulties to overcome. Mostly there are limited number of holes in every plane to put weights. In turbo machinery the shape and size of the weight is special, that the manufacturer tend to produce weight types with certain discrete weights.   
So in our problem, we have discrete weight types (masses) in discrete number of holes. There are other constraints such as how many weights can be put per hole and how much weight is allowable per plane.  
The package tries to practical assist the engineer to get the best possible split in this matter.
The mathematical modeling of the problem is `mixed integer programming` where the expected output is how many weights are to put in each hole and with which weight type to minimize the objective function of the second norm of the error (difference between the equivalent from from splitting and actual weight)
Solving this type of problems proves to be expensive time-wise and even more difficult to solve with SOCP (second order cone programming) quadratic conditions (norm2 objective function).
[CVXPY documentation](https://www.cvxpy.org/tutorial/advanced/index.html) in Choosing solver section, we can find CPLEX, GUROBI, MOSEK, SCIP and XPRESS solvers that have both ticks on the SOCP and MIP problems. The issue that all of them are commercial solvers that require commercial licence which does not go with the spirit of our package.  
I finally chose XPRESS, it is free licence include using matrix that does not exceed 5000 elements which is convenient for our balancing issues. I don't except to find number of holes x number of weights to be more than 5000 in everyday turbine. Xpress is also fast which I tried to prove in this benchmark file.
# The benchmark
## ECOS_BB: 
[ECO_BB](https://web.stanford.edu/~boyd/papers/ecos.html) is a built in free solver for `MIP` problem in `CVXPY`, but it have three main problems:
1. Slow: as per the table below.
2. Not accurate: as per CVXPY documentation (see previous).  
3. Not designed to mixed integer programming which is exactly what we aim for.   

## MIP_cvxpy:
Alternative solver was to use [CBC](https://github.com/coin-or/Cbc) solver (Coin-or Branch and Cut Solver).
In order to use it with cvxpy in python I tried [mip_cvxpy](https://github.com/jurasofish/mip_cvxpy) to directly use the solver. The solver is not for mixed integer programming but it does not support SOCP. 

## XPRESS
[XPRESS](https://www.fico.com/en/products/fico-xpress-solver) can solve this kind of mixed integer cone programming with high performance. The issue is that it is a commercial solver but it for a free use it allows 5000 matrix elements.   
It worth mentioning that matrix of only 50 elements takes long time to solve, so even if we have solver handles matrix that exceeds 5000 elements, we will face another problem of time optimization, cloud parallel processing or GPU.   
This size is convenient for practical rotor balancing (i.e. number of angles available x number of weight types does not exceed 5000).  
> In future, we may find a free solver that does the job with no limit(or warning messages in notebooks)


## Splitting plane BZ-A 
|solver|%%timeit -r 3 output|error|
|-|-|-|
|xpress|56.5 ms ± 4.21 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)|array([2.10034846])|
|mip_cvxpy[2](#2)| 154 ms ± 1.01 ms per loop (mean ± std. dev. of 3 runs, 1 loop each)|array([2.10034846])|
|ECOS_BB[3](#3)| 1.62 s ± 6.36 ms per loop (mean ± std. dev. of 3 runs, 1 loop each)|array([2.10034846])|  
|SCIP[4](#4)| 242 ms ± 19.8 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)|array([2.10034846])|
<a id="1">[1]</a>  Huang, Bin, et al. "Constrained balancing of two industrial rotor systems: Least squares and min-max approaches." Shock and Vibration 16.1 (2009): 1-12.  
<a id="2">[2]</a> solving with objective function minimize L1 norm  
<a id="3">[3]</a> solving with objective function minimize L1 norm  
<a id="4">[4]</a> solving with SCIP interface with Python [PySCIPOpt](https://github.com/scipopt/PySCIPOpt). The solver is free, capable of solving MISOCP(Mixed Integer Second Order Cone Programming) and accurate but it is way too slow and not easy to install.

