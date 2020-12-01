.. _BIGMAP_2020_Homepage:

BIG-MAP meeting AiiDA tutorial
==============================

+-----------------+-----------------------------------------------------------------------------------------------------------+
| Related resources                                                                                                           |
+=================+===========================================================================================================+
| Virtual Machine | `Quantum Mobile v20.06.1 <https://github.com/marvel-nccr/quantum-mobile/releases/tag/20.06.1>`_           |
+-----------------+-----------------------------------------------------------------------------------------------------------+
| python packages | `aiida-core 1.3.0`_, `aiida-quantumespresso 3.0.0`_                                                       |
+-----------------+-----------------------------------------------------------------------------------------------------------+
| codes           | `Quantum ESPRESSO 6.5`_                                                                                   |
+-----------------+-----------------------------------------------------------------------------------------------------------+

.. _Quantum Mobile 20.03.1: https://github.com/marvel-nccr/quantum-mobile/releases/tag/20.03.1
.. _aiida-core 1.3.0: https://pypi.org/project/aiida-core/1.3.0
.. _aiida-quantumespresso 3.0.0: https://github.com/aiidateam/aiida-quantumespresso/releases/tag/v3.0.0
.. _Quantum ESPRESSO 6.5: https://github.com/QEF/q-e/releases/tag/qe-6.5

This is the content of the AiiDA tutorial organised for the BIG-MAP meeting on 2 December 2020.


Setup
-----

The tutorial will be run on the |AiiDAlab tutorials cluster|, just click the link and log in with your email address as username and a password of your choosing.

.. important::

    Note down your password so that you can login again in case you get inadvertently logged out.
    In case your forgot your password, either just create a new account (and lose previous progress) or contact one of the administrators to reset your password.

It will take a few minutes for your server to start up on first login, after that you are all set and ready to start with the tutorial!

We will begin with a short demonstration on AiiDAlab, where you will set up a code for Quantum ESPRESSO, install a family of pseudopotentials and calculate the band structure of silicon.
Then we will go under the hood and explain the basic concepts of AiiDA, as well as run some Quantum ESPRESSO calculations and workflows via the Python API.

.. |AiiDAlab tutorials cluster| raw:: html

   <a href="http://aiidalab-tutorials.materialscloud.org/" target="_blank">AiiDAlab tutorials cluster</a>

Hands-on materials
------------------

.. toctree::
   :maxdepth: 1
   :numbered:

   ./sections/basics
   ./sections/qe

In-depth tutorial
-----------------

This tutorial is only a short introduction to AiiDA and its features.
If you want to learn more, you can check the :ref:`2020 AiiDA virtual tutorial <2020_Intro_Week_Homepage>`.

Acknowledgements
----------------

.. todo::

   Add Acknowledgements.

.. .. image:: sponsors/image.png
..    :target: add link here
..    :width: 200px
