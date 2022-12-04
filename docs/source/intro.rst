
Turbomachinery-Flexible-Rotors-Balancing
========================================

Python Tools to Model and Solve the problem of High speed Rotor Balancing.

Introduction
============
| The purpose of this project is to solve the problem of turbomachinery
  `rotor balancing <https://en.wikipedia.org/wiki/Rotating_unbalance>`__
  when more than one `critical speed <https://en.wikipedia.org/wiki/Critical_speed>`__ are required and where there are a large
  number of measuring points.


``hsbalance`` Package  :
========================

| |Downloads| |License: MIT| |pic1| |pic2| |Generic badge1| |Generic badge2|
| |Binder|

| `hsbalance <https://github.com/MagedMohamedTurk/Turbomachinery-Rotors-Balancing>`__ package is a python tool-kit that enables field engineer to
  do rotor balancing job on large number of measuring and balancing
  planes. It facilitates testing various scenarios through applying
  different optimization methods and applying different constraints. The
  package takes advantage of object oriented programming which makes it
  easier to build, extend and maintain.
| The package also make it possible to easily use the code in a `notebook <https://jupyter.org/>`__
  which is a great advantage to work freely, try different method of
  optimization and splitting for your case, get to compare results and
  RMS errors and even plot charts and diagrams.

Binder:
=======

| Use `mybinder
  link <https://mybinder.org/v2/gh/MagedMohamedTurk/Turbomachinery-Rotors-Balancing/HEAD?labpath=examples%2F>`__ to quickly navigate through examples with no installation required.

Installation:
=============

Prerequisites:
--------------

    `Python <https://www.python.org/downloads/release/python-380/>`__ >= 3.8

Quick Use:
----------

1. Create an isolated environment for python 3.8. :

.. note:: This step is optional

    * for `Anaconda <https://www.anaconda.com/>`__ users:
        ``$ conda create -n hsbalance python=3.8``

2. Installing Using PIP:
        ``$ pip install hsbalance``

hsbalance In Action:
====================

take a tour in `examples <https://github.com/MagedMohamedTurk/Turbomachinery-Rotors-Balancing/tree/master/examples>`__ to see ``hsbalance`` in action.

.. |Downloads| image:: https://pepy.tech/badge/hsbalance
.. |License: MIT| image:: https://img.shields.io/badge/License-MIT-yellow.svg
.. |pic1| image:: https://img.shields.io/badge/Python-14354C?&logo=python&logoColor=white
.. |pic2| image:: https://img.shields.io/badge/-Jupyter-white?logo=Jupyter
.. |Generic badge1| image:: https://img.shields.io/badge/Build-Dev-red.svg
.. |Generic badge2| image:: https://img.shields.io/badge/Test-Passing-Green.svg
.. |Binder| image:: https://mybinder.org/badge_logo.svg
