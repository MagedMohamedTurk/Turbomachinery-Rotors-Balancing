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
4. Run the program  
`$ python3 -m Rotor_Balanceing `

## `hsbalance` package:
Alternatively, I am developing a python package that essentially do the same job and more that the original module does. The package takes advantage of object oriented programming which makes it easier to build, extend and maintain.  
The package also make it possible to easily use the code in a notebook which is a great advantage to work freely, try different method of optimization and splitting for your case, get to compare results and RMS erros and even plot charts and diagrams.  
To quickly use the package:
1. Clone the repo to your local machine.  
`$ git clone https://github.com/MagedMohamedTurk/Turbomachinery-Rotors-Balancing`
2. `$ pip install hsbalance`
3. Take a look at the notebooks attached in the repo to see `hsbalance` in action.
### Descripting the problem  
#### Back to Basics
> Balancing simply is to bring the center of mass of a rotating component to its center of rotation.  

Every rotating component such as impellers, discs of a motor, turbine, or compressor has a center of gravity in which the mass is distributed, and it has a center of rotation which is the line between their bearings.
At the manufacturing phase, they never coincide. But why?  
Simple answer: it's too expensive to machine each component to have the same centerline of mass and rotation. Second, bearings and impellers are usually made by different manufacturers at different places. However, even though the equipment is produced by the same company, their installation setup impacts the balance and thus the center of rotation of the equipment.  
Ubalance problem 
Why should we be concerned about unbalanced rotors?  
It generates large centrifugal forces on the rotor and bearings, resulting in high stresses on the bearings and other rotating parts of the machine. They lead to premature failure! Unplanned shutdowns happen, high-risk damages endanger lives and assets.
#### Flexible Rotors
To increase efficiency, larger machines are often designed with longer shafts and multiple stages, along with higher rotational speeds. As a result, machines are running above their first or second critical levels.  
Failure may occur if the machine is run at a critical speed. We can all relate to the Tacoma Narrows Bridge incident.  
Two measures are necessary to overcome such a problem. First, to pass the critical speed as fast as possible, and then to balance the critical mode. Otherwise, the machine will never start due to vibration protection controls.  
For balancing the turbine at different critical speeds, you must be knowledgeable about the various modes and try to optimize. For example, balancing the first critical will not affect the second critical. This has been the traditional approach which is called “Modal Balancing”.  
The second method is to empirically find the balancing weights which give you the best vibration at all critical and running speeds. Commonly known as the “Influence Coefficient Method”.  
## The Mathmatical Model
Balance of flexible rotors is important in order to get optimal vibration levels at all rotor bearings since balancing weights must be calculated for each balancing plane. Turbines and compressors usually have measuring planes that are more than balancing planes. This creates an [over-determined mathematical model](https://en.wikipedia.org/wiki/Overdetermined_system#:~:text=In%20mathematics%2C%20a%20system%20of,when%20constructed%20with%20random%20coefficients.) that needs optimization methods to get the best results. The optimization problem is set to be [convex optimization](https://en.wikipedia.org/wiki/Convex_optimization#:~:text=Convex%20optimization%20is%20a%20subfield,is%20in%20general%20NP%2Dhard.) with constraints regarding balancing weights and maximum vibration allowed for certain locations. The challenge was also to beat the problem of ill-conditioned planes [multicollinearity](https://en.wikipedia.org/wiki/Multicollinearity#:~:text=Multicollinearity%20refers%20to%20a%20situation,equal%20to%201%20or%20%E2%88%921.)
The whole work was a trial to convert [Darlow "Balancing of High-Speed Machinery"](https://www.springer.com/gp/book/9781461281948) work published 1989 to a working python script that can be used in the filed.
