# Turbomachinery-Flexible-Rotors-Balancing  
Python Tools to Model and Solve the problem of High speed Rotor Balancing.  
## Introduction  
The purpose of this project is to solve the problem of turbomachinery [rotor balancing](https://en.wikipedia.org/wiki/Rotating_unbalance) when more than critical speed are required and where there are a large number of bearings.  

## `hsbalance` Package:

[![Downloads](https://pepy.tech/badge/hsbalance)](https://pepy.tech/project/hsbalance)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![pic](https://img.shields.io/badge/Python-14354C?&logo=python&logoColor=white)
![pic](https://img.shields.io/badge/-Jupyter-white?logo=Jupyter)
[![Generic badge](https://img.shields.io/badge/Build-Dev-red.svg)]()
[![Generic badge](https://img.shields.io/badge/Test-Passing-Green.svg)]()
 
HSBALANCE package is a python tool-kit that enables field engineer to do rotor balancing job on large number of measuring and balancing planes. It facilitates testing various scenarios through applying different optimization methods and applying different constraints. The package takes advantage of object oriented programming which makes it easier to build, extend and maintain.  
The package also make it possible to easily use the code in a notebook which is a great advantage to work freely, try different method of optimization and splitting for your case, get to compare results and RMS errors and even plot charts and diagrams.  
To quickly use the package:
1. Optional create an isolated environment for python 3.8. (for Anaconda users `e.g. $ conda create -n myenv python=3.8`)
2. `$ pip install hsbalance`
3. Take a look at the notebooks in 'examples\' attached in the repo to see `hsbalance` in action.  
### Quick Example 
Script can be found in `examples\example_script.py`  

Import package  
`import hsbalance as hs`  

The example is taken from B&K document (https://www.bksv.com/media/doc/17-227.pdf) Table 2 for example 6.  

| Trial Mass|Sensor 1|Sensor 2|  
|-|-|-|
|None|170 mm/s @ 112 deg|53 mm/s @ 78 deg|
|1.15 g on Plane 1|235 mm/s @ 94 deg|58 mm/s @ 68 deg|
|1.15 g on Plane 2|185 mm/s @ 115 deg| 77 mm/s @ 104 deg|  


1. Stating Problem Data  
Vibration can be expressed in `hsbalance` as string 'amplitude @ phase' where amplitude is in any desired unit
(micro - mils - mm/sec) and phase in degrees as measured by tachometer.  
The following nomenclature are taken from Goodman's paper.
**A**: Initial Condition Matrix should be input as nested column vector (a list of a list) --> shape *M x 1*
**B**: Trial masses Runs Matrix should be input as nested column vector (list of lists) --> shape *M x N*  
**U**: Trial masses vector should be input as nested column vector (a list) --> Shape *N X 1*
Where  
*M* : Number of measuring points (number of sensors x number of balancing speeds)  
*N* : Number of balancing planes  
```
A = [['170@112'], ['53@78']]  # --> Initial vibration conditions First Row in Table  above.  
B = [['235@94', '185@115'],  # --> Vibration at sensor 1 when trial masses were added at plane 1&2 (First column for both trial runs)  
     ['58@68', '77@104']]  # Vibration at sensor 2 when trial masses were added at plane 1&2 (Second column for both trial runs)  
U = ['1.15@0', '1.15@0']  # Trial masses 2.5 g at plane 1 and 2 consequently
```
2. Convert from mathematical expression into complex numbers:  
using `convert_math_cart` function
```
A = hs.convert_math_cart(A)
B = hs.convert_math_cart(B)
U = hs.convert_math_cart(U)
```

3. Create Influence Coefficient Matrix Alpha  
```
alpha = hs.Alpha()  # Instantiate Alpha class
alpha.add(A=A, B=B, U=U)
```
4. Now we have alpha instance and initial condition A; we can create a model  
```
model_LeastSquares = hs.LeastSquares(A=A, alpha=alpha)
w = model_LeastSquares.solve() #  Solve the model and get the correction weights vector
# Calculate Residual vibration vector
residual_vibration = hs.residual_vibration(alpha.value, w, A)
# Calculate Root mean square error for model
RMSE = hs.rmse(residual_vibration)
# Convert w back into mathematical expression 
w = hs.convert_cart_math(w)
# print results
print(model_LeastSquares.info())
```
Output:
--------
```

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
MODEL
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
MODEL TYPE
==================================================
LeastSquares
==================================================
End of MODEL TYPE
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

                   
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
INFLUENCE COEFFICIENT MATRIX
==================================================

++++++++++++++++++++++++++++++++++++++++
Influence Coefficient Matrix
++++++++++++++++++++++++++++++++++++++++

++++++++++++++++++++++++++++++++++++++++
Coefficient Values
==============================
                Plane 1        Plane 2
Sensor 1  78.433 @ 58.4  15.34 @ 145.3
Sensor 2   9.462 @ 10.2  32.56 @ 142.4
==============================
End of Coefficient Values
++++++++++++++++++++++++++++++++++++++++

                   
++++++++++++++++++++++++++++++++++++++++
Initial Vibration
==============================
              Vibration
Sensor 1  170.0 @ 112.0
Sensor 2    53.0 @ 78.0
==============================
End of Initial Vibration
++++++++++++++++++++++++++++++++++++++++

                   
++++++++++++++++++++++++++++++++++++++++
Trial Runs Vibration
==============================
               Plane 1        Plane 2
Sensor 1  235.0 @ 94.0  185.0 @ 115.0
Sensor 2   58.0 @ 68.0   77.0 @ 104.0
==============================
End of Trial Runs Vibration
++++++++++++++++++++++++++++++++++++++++

                   
++++++++++++++++++++++++++++++++++++++++
Trial Masses
==============================
               Mass
Plane 1  1.15 @ 0.0
Plane 2  1.15 @ 0.0
==============================
End of Trial Masses
++++++++++++++++++++++++++++++++++++++++

                   
==================================================
End of INFLUENCE COEFFICIENT MATRIX
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

                   
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
INITIAL VIBRATION
==================================================
              Vibration
Sensor 1  170.0 @ 112.0
Sensor 2    53.0 @ 78.0
==================================================
End of INITIAL VIBRATION
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

                   
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
SOLUTION
==================================================
        Correction Masses
Plane 1     1.979 @ 236.2
Plane 2     1.071 @ 121.8
==================================================
End of SOLUTION
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

                   
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
RMSE
==================================================
0.0
==================================================
End of RMSE
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

                   
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
```
5. As expected for when *M* = *N*, we can have an exact solution of the model and residual vibration and rmse comes to zero.  
The Real problem arises when *M* > *N* which is quite normal in large machines where two proximity installed in each bearing and number of bearings is high. Moreover, the number of balancing speeds can be up to 3 or 4 speeds (large machinery usually exceeds their first critical speeds). Recall that *M = Number of sensors x number of speeds*.  
6. In this case there is no exact solution and we are seeking for optimized solution that minimized the error.  
7. `hsbalace` package provides (till now) Three types of optimization models:  
a. **Least Squares model**: Minimize the square errors, this is the traditional method where we can get the best least accumulated error. The main disadvantage of this model is that it is very sensitive to outliers. This means that any faulty sensor in the system will lead to enormous error. Secondly, the model tried too hard to minimized the sum of errors. This can lead to very low residual vibration at one sensor and high vibration at another (can reach the alarm limit even!)  
b. **MinMax**: This model tries to minimize the maximum residual_vibration. This is beneficial to level of the residual vibrations to be almost equal preventing too-low too-high phenomena in the previous model.  
c. **LMI**: Linear Matrix Inequality model which allows lazy constraints.  
Lazy constraints mean that the model tries to relax the solution at certain sensors in order to get the best results at critical planes. This can be practically useful where not all planes should be treated equally. Sometimes, journal bearings with small clearance should be treated as critical planes (usually with low alarm and trip vibration limit), other planes can be considered non critical like casing sensors using accelerometers which we need to only to get the vibration below the alarm limit.  
For more details take a tour over the notebooks in `examples\`.
## Performance Test:
I tested the package against injected random Influence coefficient matrices (Alpha) with N x N size. 
The output can be summarized in the following plot. 
![plot](./data/performace_test.png)  

The graph was a test for the Least Squares model. It shows a good time performance of 800 x 800 matrix under 3 minutes.  
The hardware and software for the machine running the test can be found [data/test_conditions.txt](./data/test_conditions.txt)  
The code below is to generate the previous plot.  
```

import time
from scipy.interpolate import make_interp_spline
import numpy as np
import matplotlib.pyplot as plt
from hsbalance import Alpha, model, tools



def test_performance(n):
    '''
    Test the performance of model time_wise.
    Args:
      n : dimension of influence coefficient matrix nxn.
    Output:
      t : time elapsed in the test rounded to 2 decimal.
    '''
    # Generate alpha matrix nxn dimension
    alpha = Alpha()
    real = np.random.uniform(0, 10, [n, n])
    imag = np.random.uniform(0, 10, [n, n])
    alpha.add(real + imag * 1j)
    # Generate initial condition A matrix nx1
    real = np.random.uniform(0, 10, [n, 1])
    imag = np.random.uniform(0, 10, [n, 1])
    A= real + imag * 1j
    # start timing
    start = time.time()
    # building model LeastSquare.
    w =  model.LeastSquares(A, alpha).solve()
    # implement the model to get run time.
    error = tools.residual_vibration(alpha.value, w, A)
    t = time.time() - start
    return round(t, 2)
performance_time = []
N = [2, 10, 50, 100, 200, 400, 600, 800]
for n in N:
    performance_time.append(test_performance(n))
print(N, performance_time)
spline = make_interp_spline(N, performance_time)
x = np.linspace(min(N), max(N), 500)
y  = spline(x)
plt.plot(x, y, label="Performace Test")
plt.xlabel('N (dimension of a Squared Influence Coeffecient Matrix)')
plt.ylabel('Time (seconds)')
plt.title('Performance Test of LeastSquares model')
plt.show()
```
## The Rotor Balancing Module
The original attempt by me was to create a single python module that takes user variables and give results in an easy way that the balancing personnel does not need heavy knowledge in programming or python language.  
This module is still available in .\Rotor_Balance_Module\, in order to use it:
1. Clone the repo to your local machine.  
`$ git clone https://github.com/MagedMohamedTurk/Turbomachinery-Rotors-Balancing`
2. `$ cd Rotor_Balance_Module`
3. Optional create an isolated environment for python 3.8. (for Anaconda users `e.g. $ conda create -n myenv python=3.8`)
4. Installed required packages (cvxpy - panadas - click)   
`$ pip install -r requirement.txt`
5. Run the program: 
`$ python -m Rotor_Balanceing `

## Describing the problem  
### Back to Basics
> Balancing simply is to bring the center of mass of a rotating component to its center of rotation.  

Every rotating component such as impellers, discs of a motor, turbine, or compressor has a center of gravity in which the mass is distributed, and it has a center of rotation which is the line between their bearings.
At the manufacturing phase, they never coincide. But why?  
Simple answer: it's too expensive to machine each component to have the same centreline of mass and rotation. Second, bearings and impellers are usually made by different manufacturers at different places. However, even though the equipment is produced by the same company, their installation setup impacts the balance and thus the center of rotation of the equipment.  
### Unbalance problem 
Why should we be concerned about unbalanced rotors?  
It generates large centrifugal forces on the rotor and bearings, resulting in high stresses on the bearings and other rotating parts of the machine. They lead to premature failure! Unplanned shutdowns happen, high-risk damages endanger lives and assets.
### Flexible Rotors
To increase efficiency, larger machines are often designed with longer shafts and multiple stages, along with higher rotational speeds. As a result, machines are running above their first or second critical levels.  
Failure may occur if the machine is run at a critical speed. We can all relate to the Tacoma Narrows Bridge incident.  
Two measures are necessary to overcome such a problem. First, to pass the critical speed as fast as possible, and then to balance the critical mode. Otherwise, the machine will never start due to vibration protection controls.  
For balancing the turbine at different critical speeds, you must be knowledgeable about the various modes and try to optimize. For example, balancing the first critical will not affect the second critical. This has been the traditional approach which is called “Modal Balancing”.  
The second method is to empirically find the balancing weights which give you the best vibration at all critical and running speeds. Commonly known as the “Influence Coefficient Method”.  
### The Mathematical Model
Balance of flexible rotors is important in order to get optimal vibration levels at all rotor bearings since balancing weights must be calculated for each balancing plane. Turbines and compressors usually have measuring planes that are more than balancing planes. This creates an [over-determined mathematical model](https://en.wikipedia.org/wiki/Overdetermined_system#:~:text=In%20mathematics%2C%20a%20system%20of,when%20constructed%20with%20random%20coefficients.) that needs optimization methods to get the best results. The optimization problem is set to be [convex optimization](https://en.wikipedia.org/wiki/Convex_optimization#:~:text=Convex%20optimization%20is%20a%20subfield,is%20in%20general%20NP%2Dhard.) with constraints regarding balancing weights and maximum vibration allowed for certain locations. The challenge was also to beat the problem of ill-conditioned planes [multicollinearity](https://en.wikipedia.org/wiki/Multicollinearity#:~:text=Multicollinearity%20refers%20to%20a%20situation,equal%20to%201%20or%20%E2%88%921.)
The whole work was a trial to convert [Darlow "Balancing of High-Speed Machinery"](https://www.springer.com/gp/book/9781461281948) work published 1989 to a working python script that can be used in the filed.  

## References:

1. Goodman, Thomas P. "A least-squares method for computing balance corrections." (1964): 273-277.
Foiles W.C., Allaire P.E., and Gunter E.J., 2000, “Min-max optimum flexible rotor balancing compared to weighted least squares”, Proceedings of the Seventh International Conference on Vibrations in Rotating Machinery, Nottingham, UK, C576/097/2000 , pp.141-148
2. Feese, Troy D., and Phillip E. Grazier. "Balance This! Case Histories From Difficult Balance Jobs." Proceedings of the 33rd Turbomachinery Symposium. Texas A&M University. Turbomachinery Laboratories, 2004.
3. Kelm, Ray, Walter Kelm, and Dustin Pavelek. "Rotor Balancing Tutorial." Proceedings of the 45th Turbomachinery Symposium. Turbomachinery Laboratories, Texas A&M Engineering Experiment Station, 2016.
4. Darlow, M. S. "The identification and elimination of non-independent balance planes in influence coefficient balancing." Turbo Expo: Power for Land, Sea, and Air. Vol. 79603. American Society of Mechanical Engineers, 1982.
5. Darlow, Mark S. Balancing of high-speed machinery. Springer Science & Business Media, 2012.

## How to Contribute:
You can help the project in various ways:  
1. Star, fork and clone the repository to keep the project active.
2. If you are a vibration analyst or plant maintenance engineer you can submit test cases from your equipment to added to our test cases. [contact me](newmaged@yahoo.com)
3. If you have enough vibration knowledge in the subject, you can assist in rewriting this article.
4. If you have enough mathematical knowledge, you can help in reformulating the optimization equations and expressions.
5. If you are a python developer you can contribute in the actual code. (fork and pull request).
6. [!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/MagedM)


## About the Author:
Maged M.Eltorkoman   
1. B.SC in Mechanical engineering 2000, Alexandria University, Egypt.
2. [Certified ISO-CAT II Vibration Analyst.](https://certificates.mobiusinstitute.com/d8973420-d21e-42f8-a7ba-a13f889e035f#gs.kz6fsv)  
3. [Udacity Nanodegree in Advanced Data Analysing](https://www.linkedin.com/in/maged-eltorkoman/overlay/1611041255110/single-media-viewer/)
4. [Freelance Data Analyst](https://www.upwork.com/freelancers/~010cf5d4f25c9fa689)
## Contact:
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=plastic&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/maged-eltorkoman/)  [![Email](https://img.shields.io/badge/Gmail-D14836?style=plastic&logo=gmail&logoColor=white)](mailto:newmaged@gmail.com)  
Email: newmage@gmail.com
