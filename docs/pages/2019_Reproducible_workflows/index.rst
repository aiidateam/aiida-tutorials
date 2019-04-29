+-----------------+--------------------------------------------+
| Prerequisite    | Version                                    |
+=================+============================================+
| Virtual Machine | `Quantum Mobile 19.05.0`_                  |
+-----------------+--------------------------------------------+
| python packages | `aiida-core 1.0.0b3`_, `aiidalab 19.04.2`_ |
+-----------------+--------------------------------------------+
| codes           | `Quantum Espresso 6.3`_                    |
+-----------------+--------------------------------------------+

.. _Quantum Mobile 19.05.0: https://github.com/marvel-nccr/quantum-mobile/releases/tag/19.05.0
.. _aiida-core 1.0.0b3: https://pypi.org/project/aiida-core/1.0.0b3
.. _aiidalab 19.04.2: https://pypi.org/project/aiidalab/19.4.2
.. _Quantum Espresso 6.3: https://github.com/QEF/q-e/releases/tag/qe-6.3

These are the notes of the `AiiDA tutorial on writing reproducible workflows
for computational materials science
<http://www.aiida.net/tutorial-reproducible-workflows/>`__ taking place from
May 21-24, 2019 at EPF Lausanne, Switzerand.

Writing reproducible workflows for computational materials science
==================================================================

In this tutorial, we will screen metal-organic frameworks (MOFs) for
their possible application as methane adsorbents, allowing to store
natural gas at increased density and lower storage pressure. We will use
the `AiiDA framework <www.aiida.net>`__ in order to automate the
screening workflow and to record the full provenance of the calculations
for reproducibility.

The tutorial is meant to be run inside the `Quantum
Mobile <https://www.materialscloud.org/work/quantum-mobile>`__ virtual
machine, using a compute resource with
`zeo++ <http://www.zeoplusplus.org/>`__ and
`RASPA2 <https://github.com/numat/RASPA2>`__ installed.

**Note:** This tutorial requires a basic knowledge of
`python <https://docs.python.org/2.7/tutorial/index.html>`__. If you are
not familiar with python, we suggest you partner with someone who is.

