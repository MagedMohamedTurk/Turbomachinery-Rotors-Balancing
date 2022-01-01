# Turbomachinery-Flexible-Rotors-Balancing  
Python Tools to Model and Solve the problem of High speed Rotor Balancing.  
## Introduction  
The purpose of this project is to solve the problem of turbomachinery [rotor balancing](https://en.wikipedia.org/wiki/Rotating_unbalance) when more than critical speed is required and where there are a large number of bearings.  
## The Rotor Balancing Module
The software in this repository is to give help to field balancing for large machinery. The original attempt by me was to create a single python module that takes user variables and give results in an easy way that the balancing personnel does not need heavy knowledge in programming or python language.  
This module is still available in .\Rotor_Balance_Module\, in order to use it:
1. Clone the repo to your local machine.  
`$ git clone https://github.com/MagedMohamedTurk/Turbomachinery-Rotors-Balancing`
2. `$ cd Rotor_Balance_Module`
3. Optional create an isolated environment for python 3.8. (for Anaconda users `e.g. $ conda create -n myenv python=3.8`)
4. Installed required packages (cvxpy - panadas - click)   
`$ pip install -r requirement.txt`
5. Run the program: 
`$ python3 -m Rotor_Balanceing `

## `hsbalance` Package:
Alternatively, I am developing a python package that essentially do the same job and more that the original module does. The package takes advantage of object oriented programming which makes it easier to build, extend and maintain.  
The package also make it possible to easily use the code in a notebook which is a great advantage to work freely, try different method of optimization and splitting for your case, get to compare results and RMS erros and even plot charts and diagrams.  
To quickly use the package:
1. Optional create an isolated environment for python 3.8. (for Anaconda users `e.g. $ conda create -n myenv python=3.8`)
2. `$ pip install hsbalance`
3. Take a look at the notebooks attached in the repo to see `hsbalance` in action.  
### Quick Example 
Script can be found in `example_script.py`  

Import package  
`>>> import hsbalance as hs`  

The example is taken from B&K document (https://www.bksv.com/media/doc/17-227.pdf) Table 1 for example 4.  

| Trial Mass|Sensor 1|Sensor 2|  
|-|-|-|
|None|170 mm/s @ 112 deg|53 mm/s @ 78 deg|
|1.15 g on Plane 1|235 mm/s @ 94 deg|58 mm/s @ 68 deg|
|1.15 g on Plane 2|185 mm/s @ 115 deg| 77 mm/s @ 104 deg|  


1. Stating Problem Data  
Vibration can be expressed in `hsbalance` as string 'amplitude @ phase' where amplitude is in any desired unit
(micro - mils - mm/sec) and phase in degrees as measured by tachometer.  
**A**: Initial Condition Matrix should be input as nested column vector (a list of a list) --> shape 1 x*M*  
**B**: Trial masses Runs Matrix should be input as nested column vector (list of lists) --> shape *M x N*  
**U**: Trial masses vector should be input as nested column vector (a list) --> Shape *N x 1*
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
>>> A = hs.convert_math_cart(A)
>>> B = hs.convert_math_cart(B)
>>> U = hs.convert_math_cart(U)
```

3. Create Influence Coefficient Matrix Alpha  
```
>>> alpha = hs.Alpha()  # Instantiate Alpha class
>>> alpha.add(A=A, B=B, U=U)
```
4. Now we have alpha instance and initial condition A; we can create a model  
```
model_LeastSquares = hs.LeastSquares(A=A, alpha=alpha)
w = model_LeastSquares.solve() #  Solve the model and get the correction weights vector
# Calculate Residual vibration vector
residual_vibration = hs.residual_vibration(alpha.value, w, A)
# Caculate Root mean square error for model
RMSE = hs.rmse(residual_vibration)
# Convert w back into mathmatical expression 
w = hs.convert_cart_math(w)
# print results
print('Correction Weights are: \n{}\n Root Mean Squares = {}\n '
      '\n Residule Vibration vector\n{}'.format(w, RMSE, residual_vibration))
```
5. As expected for when *M* = *N*, we can have an exact solution of the model and residual vibration and rmse comes to zero.  
The Real problem arises when *M* > *N* which is quite normal in large machines where two proximity installed in each bearing and number of bearings is high. Moreover, the number of balancing speeds can be up to 3 or 4 speeds (large machinery usually exceeds their first critical speeds). Recall that *M = Number of sensors x number of speeds*.  
6. In this case there is no exact solution and we are seeking for optimized solution that minimized the error.  
7. `hsbalace` package provides (till now) Three types of optimization models:  
a. **Least Squares model**: Minimize the square errors, this is the traditional method where we can get the best least accumulated error. The main disadvantage of this model is that it is very sensitive to outliers. This means that any faulty sensor in the system will lead to enormous error. Secondly, the model tried too hard to minimized the sum of errors. This can lead to very low residual vibration at one sensor and high vibration at another (can reach the alarm limit even!)  
b. **MinMax**: This model tries to minimize the maximum residual_vibration. This is beneficial to level of the residual vibrations to be almost equal preventing too-low too-high phenomena in the previous model.  
c. **LMI**: Linear Matrix Inequality model which allows lazy constraints.  
Lazy constraints mean that the model tries to relax the solution at certain sensors in order to get the best results at critical planes. This can be practically useful where not all planes should be treated equally. Sometimes, journal bearings with small clearance should be treated as critical planes (usually with low alarm and trip vibration limit), other planes can be considered non critical like casing sensors using accelerometers which we need to only to get the vibration below the alarm limit.  
For more details take a tour over the notebooks.
## Describing the problem  
### Back to Basics
> Balancing simply is to bring the center of mass of a rotating component to its center of rotation.  

Every rotating component such as impellers, discs of a motor, turbine, or compressor has a center of gravity in which the mass is distributed, and it has a center of rotation which is the line between their bearings.
At the manufacturing phase, they never coincide. But why?  
Simple answer: it's too expensive to machine each component to have the same centerline of mass and rotation. Second, bearings and impellers are usually made by different manufacturers at different places. However, even though the equipment is produced by the same company, their installation setup impacts the balance and thus the center of rotation of the equipment.  
Ubalance problem 
Why should we be concerned about unbalanced rotors?  
It generates large centrifugal forces on the rotor and bearings, resulting in high stresses on the bearings and other rotating parts of the machine. They lead to premature failure! Unplanned shutdowns happen, high-risk damages endanger lives and assets.
### Flexible Rotors
To increase efficiency, larger machines are often designed with longer shafts and multiple stages, along with higher rotational speeds. As a result, machines are running above their first or second critical levels.  
Failure may occur if the machine is run at a critical speed. We can all relate to the Tacoma Narrows Bridge incident.  
Two measures are necessary to overcome such a problem. First, to pass the critical speed as fast as possible, and then to balance the critical mode. Otherwise, the machine will never start due to vibration protection controls.  
For balancing the turbine at different critical speeds, you must be knowledgeable about the various modes and try to optimize. For example, balancing the first critical will not affect the second critical. This has been the traditional approach which is called “Modal Balancing”.  
The second method is to empirically find the balancing weights which give you the best vibration at all critical and running speeds. Commonly known as the “Influence Coefficient Method”.  
### The Mathmatical Model
Balance of flexible rotors is important in order to get optimal vibration levels at all rotor bearings since balancing weights must be calculated for each balancing plane. Turbines and compressors usually have measuring planes that are more than balancing planes. This creates an [over-determined mathematical model](https://en.wikipedia.org/wiki/Overdetermined_system#:~:text=In%20mathematics%2C%20a%20system%20of,when%20constructed%20with%20random%20coefficients.) that needs optimization methods to get the best results. The optimization problem is set to be [convex optimization](https://en.wikipedia.org/wiki/Convex_optimization#:~:text=Convex%20optimization%20is%20a%20subfield,is%20in%20general%20NP%2Dhard.) with constraints regarding balancing weights and maximum vibration allowed for certain locations. The challenge was also to beat the problem of ill-conditioned planes [multicollinearity](https://en.wikipedia.org/wiki/Multicollinearity#:~:text=Multicollinearity%20refers%20to%20a%20situation,equal%20to%201%20or%20%E2%88%921.)
The whole work was a trial to convert [Darlow "Balancing of High-Speed Machinery"](https://www.springer.com/gp/book/9781461281948) work published 1989 to a working python script that can be used in the filed.  
## How to Contribute:
You can help the project in various ways:  
1. Star, fork and clone the repository to keep the project active.
2. If you are a vibration analyst or plant maintenance engineer you can submit test cases from your equipment to added to our test cases. [contact me](newmaged@yahoo.com)
3. If you have enough vibration knowledge in the subject, you can assist in rewriting this article.
4. If you have enough mathematical knowledge, you can help in reformulating the optimization equations and expressions.
5. If you are a python developer you can contribute in the actual code. (fork and pull request).
6. Donate to the project via [paypal](Maged Mohamed Eltorkoman
@maged78)
7. [Buy me coffee](https://www.buymeacoffee.com/MagedM)

## About the Author:
Maged M.Eltorkoman   
1. B.SC in Mechanical engineering 2000, Alexandria University, Egypt.
2. [Certified ISO-CAT II vibration analyst.](https://certificates.mobiusinstitute.com/d8973420-d21e-42f8-a7ba-a13f889e035f#gs.kz6fsv)  
3. [Udacity Nanodegree in Advanced Data analysing]('https://www.linkedin.com/in/maged-eltorkoman/overlay/1611041255110/single-media-viewer/')
## Contact:
LinkedIn: https://www.linkedin.com/in/maged-eltorkoman/  
Email: newmaged@gmail.com
