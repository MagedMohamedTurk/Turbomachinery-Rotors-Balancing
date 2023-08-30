.. _primer:

Describing the problem
======================

Back to Basics
--------------

   Balancing simply is to bring the center of mass of a rotating
   component to its center of rotation.

   .. figure:: ../source/media/FBD.svg
        :scale: 50 %
        :align: center
        :alt: Free Body Diagram 

        When the center of gravity does not coincide with center of rotation, centerifugal forces generated tangential to the direction of rotation causing unbalance force.
        table:

        +-----------------------+-----------------------+
        | Symbol                | Meaning               |
        +=======================+=======================+
        |  CR                   | Center of Rotation    |
        +-----------------------+-----------------------+
        |  CG                   | Center of Gravity     |
        +-----------------------+-----------------------+


Where :math:`F_{unbalance}` is the centerifugal force generated due to the eccentricty of CG off the CR by the amount of distance r and can be calculated from the equation:

.. math:: F_{unbalance} = m\cdot\omega^2\cdot r 
   :label: centerifugal

Where:
   | m: Mass
   | :math:`\omega`: Rotational speed
   | r: Eccentricty

| In equation :eq:`centerifugal`, notice that :math:`F\alpha\left(speed\right)^2`
| Every rotating component such as impellers, discs of a motor, turbine,
  or compressor has a center of gravity in which the mass is
  distributed, and it has a center of rotation which is the line between
  their bearings. At the manufacturing phase, they never coincide. But
  why?
| Simple answer: it’s too expensive to machine each component to have
  the same centreline of mass and rotation. Second, bearings and
  impellers are usually made by different manufacturers at different
  places. However, even though the equipment is produced by the same
  company, their installation setup impacts the balance and thus the
  center of rotation of the equipment.
| ### Unbalance problem Why should we be concerned about unbalanced
  rotors?
| It generates large centrifugal forces on the rotor and bearings,
  resulting in high stresses on the bearings and other rotating parts of
  the machine. They lead to premature failure! Unplanned shutdowns
  happen, high-risk damages endanger lives and assets. ### Flexible
  Rotors To increase efficiency, larger machines are often designed with
  longer shafts and multiple stages, along with higher rotational
  speeds. As a result, machines are running above their first or second
  critical levels.
| Failure may occur if the machine is run at a critical speed. We can
  all relate to the Tacoma Narrows Bridge incident.
| Two measures are necessary to overcome such a problem. First, to pass
  the critical speed as fast as possible, and then to balance the
  critical mode. Otherwise, the machine will never start due to
  vibration protection controls.



| For balancing the turbine at different critical speeds, you must be
  knowledgeable about the various modes and try to optimize. For
  example, balancing the first critical will not affect the second
  critical. This has been the traditional approach which is called
  “Modal Balancing”.
| The second method is to empirically find the balancing weights which
  give you the best vibration at all critical and running speeds.
  Commonly known as the “Influence Coefficient Method”.

Least Square Model:
-------------------
given:  
        | n: balance planes(locations for corrections masses)
        | m: vibration readings at k different conditions of speed and load 
        | l: different locations. 
        | where :math:`m=k\cdot{l}`
| the problem is to find the optimum corrections masses in the `n` balance planes.
| the idea here is to add a `trial weight` which is a mass of typically any value to be put at every `n` plane and measure the vibration at each `m` plane.
| each trial mass addition round is called `trial run`
| **initial vibration matrix is:**
.. math:: a= \left. {\begin{pmatrix} a_1 \\ a_2 \\ \vdots \\a_i\\\vdots\\ a_m \end{pmatrix}}\right\}\begin{array}{}\\\ _{\text{m measuring points}}\\{}\end{array}, a \in \mathbb{C^m}
    :label: a 
where :math:`\pmb{a_i}`: initial vibration measured at plane :math:`{\pmb{i}}` with no trial mass added

| **trial vibration matrix is:**
.. math:: b = \left. {\underset{\text{n balancing planes}}{\underbrace{\begin{pmatrix} b_{11} & b_{12} & \dots b_{1j} & b_{1n}\\
                              b_{21} & b_{22} & \dots b_{2j} & b_{2n}\\
                              \vdots & \vdots & \vdots\ddots & \vdots\\ 
                              b_{i1} & b_{i2} & \dots b_{ij} & b_{in}\\
                              \vdots & \vdots & \vdots\ddots & \vdots\\ 
                              b_{m1} & b_{m2} & \dots b_{mj} & b_{mn} 
              \end{pmatrix}_{}}}}\right\}\begin{array}{}\\\ _{\text{m measuring points}}\\{}\end{array}, b\in{\mathbb{C^{m\times{n}}}}
   :label: b
| where: :math:`\pmb{b_{ij}}`: vibration at measuring point :math:`\pmb{i}` when mass were added in balancing plane :math:`\pmb{j}`.
| **trial weights matrix is:**
.. math:: u= \underset{\text{n balancing planes}}{\underbrace{\begin{pmatrix} u_1 & u_2 & \dots &u_j & \dots & u_n \end{pmatrix}_{}}}, u \in \mathbb{C}
   :label: u 
| where: :math:`\pmb{u_{j}}`: mass added in balancing plane :math:`\pmb{j}`.


| **influence coefficient matrix is:**
.. math:: \alpha= \left. {\underset{\text{n balancing planes}}{\underbrace{\begin{pmatrix} \alpha_{11} & \alpha_{12} & \dots \alpha_{1j} & \alpha_{1n}\\
                              \alpha_{21} & \alpha_{22} & \dots \alpha_{2j} & \alpha_{2n}\\
                              \vdots & \vdots & \vdots\ddots & \vdots\\ 
                              \alpha_{i1} & \alpha_{i2} & \dots \alpha_{ij} & \alpha_{in}\\
                              \vdots & \vdots & \vdots\ddots & \vdots\\ 
                              \alpha_{m1} & \alpha_{m2} & \dots \alpha_{mj} & \alpha_{mn} 
              \end{pmatrix}_{}}}}\right\}\begin{array}{}\\\ _{\text{m measuring points}}\\{}\end{array}, \alpha\in{\mathbb{C^{m\times{n}}}}
   :label: alpha
| where: :math:`\pmb{\alpha_{ij}}`: influence coefficient of a mass added in balancing plane :math:`\pmb{j}` has on the vibration at measuring point :math:`\pmb{i}` and can be calculated as follows:
.. math:: \alpha_{ij} = \frac{b_{ij} - a_{i}}{u_j}
   :label: calculate_alpha
| For general :math:`M \le N` **Least Square Equation is:**
.. math:: W = - (\alpha^T \cdot \alpha)^{-1} \cdot \alpha^T \cdot A
| but as :math:`\alpha \in \mathbb{C}`, we should replace :math:`\alpha^T` with :math:`\alpha^H` where:
| :math:`\alpha^H` is the Hermitian transpose or the conjugate transpose of a complex matrix, can be expressed as:
| :math:`\alpha^H=(\bar{\alpha})^T`, where :math:`\bar{\alpha}` : the conjugate of matrix :math:`\alpha`.
| rewriting the equation:
.. math:: W = - (\alpha^H \cdot \alpha)^{-1} \cdot \alpha^H \cdot A
   :label: least_squares



| ### The Mathematical Model Balance of flexible rotors is important in
  order to get optimal vibration levels at all rotor bearings since
  balancing weights must be calculated for each balancing plane.
  Turbines and compressors usually have measuring planes that are more
  than balancing planes. This creates an `over-determined mathematical
  model <https://en.wikipedia.org/wiki/Overdetermined_system#:~:text=In%20mathematics%2C%20a%20system%20of,when%20constructed%20with%20random%20coefficients.>`__
  that needs optimization methods to get the best results. The
  optimization problem is set to be `convex
  optimization <https://en.wikipedia.org/wiki/Convex_optimization#:~:text=Convex%20optimization%20is%20a%20subfield,is%20in%20general%20NP%2Dhard.>`__
  with constraints regarding balancing weights and maximum vibration
  allowed for certain locations. The challenge was also to beat the
  problem of ill-conditioned planes
  `multicollinearity <https://en.wikipedia.org/wiki/Multicollinearity#:~:text=Multicollinearity%20refers%20to%20a%20situation,equal%20to%201%20or%20%E2%88%921.>`__
  The whole work was a trial to convert `Darlow “Balancing of High-Speed
  Machinery” <https://www.springer.com/gp/book/9781461281948>`__ work
  published 1989 to a working python script that can be used in the
  filed.

