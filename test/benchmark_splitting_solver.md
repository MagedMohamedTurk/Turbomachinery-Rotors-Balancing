## Splitting plane BZ-A
|solver|%%timeit -r 3 output|error|
|-|-|-|
|xpress|56.5 ms ± 4.21 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)|array([2.10034846])|
|mip_cvxpy| 154 ms ± 1.01 ms per loop (mean ± std. dev. of 3 runs, 1 loop each)|array([2.10034846])|
|ECOS_BB| 1.62 s ± 6.36 ms per loop (mean ± std. dev. of 3 runs, 1 loop each)|array([2.10034846])|
