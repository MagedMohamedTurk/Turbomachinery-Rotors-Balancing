1. Model:
- [ ] make scaled least squares method
  - Objective cp.Minimize(cp.diag(scale) @ cp.sum_square(ALPHA@W+A))
  - Scale vector[0, 0.5, 1.5] cancel sensor 1 and gives sensor 3 high importance
- [x] Add weight constrains
- [x] Make ALPHA class



