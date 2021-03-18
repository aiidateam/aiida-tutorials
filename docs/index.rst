AiiDA Quantum ESPRESSO tutorial
===============================

.. todo::

   Update Quantum Mobile version + links

.. _Homepage:

+-----------------+-----------------------------------------------------------------------------------------------------------+
| Related resources                                                                                                           |
+=================+===========================================================================================================+
| Quantum Mobile  | ADD QUANTUM MOBILE VERSION WHEN RELEASED                                                                  |
+-----------------+-----------------------------------------------------------------------------------------------------------+
| AiiDAlab        | `AiiDAlab docker stack 21.02.1`_, `AiiDAlab k8s deployment`_                                              |
+-----------------+-----------------------------------------------------------------------------------------------------------+
| python packages | `aiida-core 1.5.2`_, `aiida-quantumespresso 3.3.0`_                                                       |
+-----------------+-----------------------------------------------------------------------------------------------------------+
| codes           | `Quantum ESPRESSO 6.0.0`_                                                                                 |
+-----------------+-----------------------------------------------------------------------------------------------------------+

.. _AiiDAlab docker stack 21.02.1: https://github.com/aiidalab/aiidalab-docker-stack/releases/tag/v21.02.1
.. _AiiDAlab k8s deployment: https://github.com/aiidalab/aiidalab-k8s
.. _aiida-core 1.5.2: https://pypi.org/project/aiida-core/1.5.2/
.. _aiida-quantumespresso 3.3.0: https://pypi.org/project/aiida-quantumespresso/3.3.0/
.. _Quantum ESPRESSO 6.0.0: https://github.com/QEF/q-e/releases/tag/qe-6.0.0

This tutorial is a short introduction to some of the features of AiiDA based on Quantum ESPRESSO.

Setup
-----

The tutorial can either be run in the Quantum Mobile virtual machine, or on the AiiDAlab demo cluster.

.. tabs::

   .. tab:: Quantum Mobile

      Quantum Mobile is a virtual machine that provides a ready-to-run environment for computational materials science.

      .. todo::

         Add more instructions once image is released.

   .. tab:: AiiDAlab cluster

      The |AiiDAlab demo cluster| is a Jupyter-based web platform installed on a cluster that can run some basic calculations for demonstration and tutorial purposes.
      Simply click the link and log in with the EGI check-in.

.. |AiiDAlab demo cluster| raw:: html

   <a href="https://aiidalab-demo.materialscloud.org" target="_blank">AiiDAlab demo cluster</a>

Hands-on materials
------------------

The hands-on sessions consist of one short session on running calculations and a simple workflow with Quantum ESPRESSO, as well as a session on organising and querying your data.
If you have time left after going through the first two sections, you can have a look at the "Provenance tutorial", which explains more about the basic concepts of AiiDA.

.. toctree::
   :maxdepth: 2
   :caption: Hands-on sessions
   :numbered:

   ./source/sections/qe
   ./source/sections/data
   ./source/sections/install

.. toctree::
   :maxdepth: 1
   :caption: Appendices
   :numbered:

   ./source/sections/basics

In-depth tutorial
-----------------

This tutorial is only a short introduction to AiiDA and its features.
If you want to learn more, you can check the `2020 AiiDA virtual tutorial <https://aiida-tutorials.readthedocs.io/en/tutorial-2020-intro-week/index.html>`_.

Acknowledgements
----------------

.. todo::

   Update Acknowledgements

This tutorial was made possible by support from the MaX European Centre of Excellence, the MARVEL National Centre of Competence in Research and the H2020 INTERSECT project.

.. image:: source/sponsors/max.png
   :target: http://www.max-centre.eu/
   :width: 35%

.. image:: source/sponsors/marvel.png
   :target: http://nccr-marvel.ch/
   :width: 25%

.. image:: source/sponsors/INTERSECT_logo.png
   :target: https://intersect-project.eu/
   :width: 30%
