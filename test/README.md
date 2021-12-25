# Installation 
> pip install pytest  

# Contribute
Follow the instructions for test cases found in `config.yaml`
# Test
> $ pytest -v

# References
|Test Case Label|Citation|Remarks|
|---|---|---|
|goodman64|Goodman, Thomas P. "A least-squares method for computing balance corrections." (1964): 273-277.|passed|
|Foiles_Min-Max|Foiles W.C., Allaire P.E., and Gunter E.J., 2000, “Min-max optimum flexible rotor balancing compared to weighted least squares”, Proceedings of the Seventh International Conference on Vibrations in Rotating Machinery, Nottingham, UK, C576/097/2000 , pp.141-148|failed within 5% error (passed when tol. increased to 9%)|
|Balanceit_Example_Two_Plane|Feese, Troy D., and Phillip E. Grazier. "Balance This! Case Histories From Difficult Balance Jobs." Proceedings of the 33rd Turbomachinery Symposium. Texas A&M University. Turbomachinery Laboratories, 2004.|passed|
|Pavelek_1|Kelm, Ray, Walter Kelm, and Dustin Pavelek. "Rotor Balancing Tutorial." Proceedings of the 45th Turbomachinery Symposium. Turbomachinery Laboratories, Texas A&M Engineering Experiment Station, 2016.|passed|
|Darlow|Darlow, M. S. "The identification and elimination of non-independent balance planes in influence coefficient balancing." Turbo Expo: Power for Land, Sea, and Air. Vol. 79603. American Society of Mechanical Engineers, 1982.||
