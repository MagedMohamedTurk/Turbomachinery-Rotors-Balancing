
.. _readme:
Turbomachinery-Flexible-Rotors-Balancing
========================================

Python Tools to Model and Solve the problem of High speed Rotor Balancing.
`hsbalance` was built on the shoulders of great packages 🛠️💡😍 :  

1. `CVXPY <https://www.cvxpy.org/>`__: The core package that is used to process the optimization problems needed.   

2. `pandas <https://pandas.pydata.org/>`__: For printing tabulated results.    

3. `Numpy <https://pandas.pydata.org/>`__: For Linear Algebra.    

4. `Xpress <https://www.fico.com/en/products/fico-xpress-solver>`__ : Solver that is used to solve the splitting mass problems.



Jump to :ref:`The Walk-Through Example <walkthrough example>` for
a quick starter.



Introduction
------------
| The purpose of this project is to solve the problem of turbomachinery
  `rotor balancing <https://en.wikipedia.org/wiki/Rotating_unbalance>`__
  when more than one `critical speed <https://en.wikipedia.org/wiki/Critical_speed>`__ are required and where there are a large
  number of measuring points.

.. admonition:: Rotor Balancing

     When a rotating object does not have a *perfect* mass distribution, the `center of gravity <https://en.wikipedia.org/wiki/Center_of_mass#Center_of_gravity>`__ does not lay on its `rotation axis <https://simple.wikipedia.org/wiki/Axis_of_rotation>`__.
     This causes rotating `centrifugal force <https://en.wikipedia.org/wiki/Centrifugal_force>`__ to occur and generates `vibrating <http://www.vibrationschool.com/mans/SpecInter/SpecInter02.htm>`__ force transmitted to the support `bearings <https://en.wikipedia.org/wiki/Bearing_(mechanical)>`__.
     | The vibration forces is usually of destructive type and reduces the life of the machine.
     | Perfect mass distribution is generally impossible to achieve in real world, so the need to reduce the effect of unbalance force is needed.

     The solution is usually to install a counter weight to produce the same magnitude of force as mush as the unbalance but in the opposite direction. This is called rotor balancing.

If you wish to be more familiar to dynamic rotor balancing and
this documentation terminology
refer to :ref:`primer to rotor balancing <primer>`


What is ``hsBalance``?
----------------------

hsBalance is Python package used as an API interface
to provide programmers with tools to analyze balancing
flexible rotors.

.. note:: This is **not** a user interacting program which asks for inputs and gives outputs back. A premitive trial by me was
   :ref:`this program <module>` *(which still needs software refactoring and heavy documentation to be used properly)*.




``hsBalance`` Package
---------------------

| |Downloads| |License: MIT| |pic1| |pic2| |Generic badge1| |Generic badge2|
| |Binder|

| `hsBalance <https://github.com/MagedMohamedTurk/Turbomachinery-Rotors-Balancing>`__ package is a python tool-kit that enables field engineer to
  do rotor balancing job on large number of measuring and balancing
  planes. It facilitates testing various scenarios through applying
  different optimization methods and applying different constraints. The
  package takes advantage of object oriented programming which makes it
  easier to build, extend and maintain.
| The package also make it possible to easily use the code in a `notebook <https://jupyter.org/>`__
  which is a great advantage to work freely, try different method of
  optimization and splitting for your case, get to compare results and
  RMS errors and even plot charts and diagrams.

Binder
------

| Use `mybinder
  link <https://mybinder.org/v2/gh/MagedMohamedTurk/Turbomachinery-Rotors-Balancing/HEAD?labpath=examples%2F>`__ to quickly navigate through examples with no installation required.

Installation
------------
.. warning:: The installation steps were tested in Linux OS, other systems may differ accordingly.

Prerequisites
+++++++++++++

    `Python <https://www.python.org/downloads/release/python-380/>`__ >= 3.8

Quick Use
+++++++++

1. Create an isolated virtual environment for python 3.8. :

    .. note:: This step is optional

    * for `Anaconda <https://www.anaconda.com/>`__ users:
        ::

        $ conda create -n hsbalance python=3.8
        $ conda activate hsbalance

    * `Virtualenv <https://virtualenv.pypa.io/en/latest/>`__ users:
        ::

            $ virtualenv hsbalance
            $ source hsbalance/bin/activate

        OR: To specify python 3.8 version

        ::

            $ virtualenv -p /usr/bin/python3.8 hsbalance
            $ source hsbalance/bin/activate



2. Installing Using PIP:
   ::

        $ pip install hsbalance

hsBalance In Action
-------------------

Take a tour in `examples <https://github.com/MagedMohamedTurk/Turbomachinery-Rotors-Balancing/tree/master/examples>`__ to see ``hsBalance`` in action.

Walkthrough Example
-------------------

A walkthrough through an example with detailed
discussion can be found
:ref:`here <walkthrough example>`.


.. |Downloads| image:: https://pepy.tech/badge/hsbalance
.. |License: MIT| image:: https://img.shields.io/badge/License-MIT-yellow.svg
.. |pic1| image:: https://img.shields.io/badge/Python-14354C?&logo=python&logoColor=white
.. |pic2| image:: https://img.shields.io/badge/-Jupyter-white?logo=Jupyter
.. |Generic badge1| image:: https://img.shields.io/badge/Build-Dev-red.svg
.. |Generic badge2| image:: https://img.shields.io/badge/Test-Passing-Green.svg
.. |Binder| image:: https://mybinder.org/badge_logo.svg
