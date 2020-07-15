+-----------------+-------------------------------------------+
| Related resources                                           |
+=================+===========================================+
| Virtual Machine | `Quantum Mobile 18.10.0RC1`_              |
+-----------------+-------------------------------------------+
| python packages | `aiida-core 0.12.2`_, `aiidalab 19.01.2`_ |
+-----------------+-------------------------------------------+
| codes           | `zeo++ 0.3`_, `raspa 2.0.36`_             |
+-----------------+-------------------------------------------+

.. _Quantum Mobile 18.10.0RC1: https://github.com/marvel-nccr/quantum-mobile/releases/tag/18.10.0RC1
.. _aiida-core 0.12.2: https://pypi.org/project/aiida-core/0.12.2
.. _aiidalab 19.01.2: https://pypi.org/project/aiidalab/19.1.2
.. _zeo++ 0.3: http://www.zeoplusplus.org/download.html
.. _raspa 2.0.36: https://github.com/iRASPA/RASPA2/releases/tag/v2.0.36

Metal-organic frameworks for methane storage applications
=========================================================

This tutorial is part of the `Understanding molecular
simulation <http://www.acmm.nl/molsim/molsim2019/>`__ school held at the
University of Amsterdam from January 7-18 2019.

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

.. note::

   This tutorial requires a basic knowledge of
   `python <https://docs.python.org/2.7/tutorial/index.html>`__. If you are
   not familiar with python, we suggest you partner with someone who is.

Analyzing the database
----------------------

.. toctree::
   :maxdepth: 1
   :numbered:

   Getting set up <./pages/2019_molsim_school_Amsterdam/tutorial/setup>
   Browsing the provenance graph <./pages/2019_molsim_school_Amsterdam/tutorial/provenance-graph>
   The verdi command line <./pages/2019_molsim_school_Amsterdam/tutorial/verdi-commands>
   The AiiDA python interface <./pages/2019_molsim_school_Amsterdam/tutorial/python-interface>
   Querying the AiiDA database <./pages/2019_molsim_school_Amsterdam/tutorial/queries>
   Selecting candidate materials <./pages/2019_molsim_school_Amsterdam/tutorial/candidate-selection>

Computing properties of candidate materials
-------------------------------------------

.. toctree::
   :maxdepth: 1
   :numbered:

   Setting up remote computers and codes <./pages/2019_molsim_school_Amsterdam/screening/calculations>
   Compute methane loading <./pages/2019_molsim_school_Amsterdam/screening/methane-loading>
   Screening <./pages/2019_molsim_school_Amsterdam/screening/screening>
   Upload your results <./pages/2019_molsim_school_Amsterdam/screening/export>

Theoretical background
----------------------

.. toctree::
   :maxdepth: 1
   :numbered:

   Origin of the MOF database <./pages/2019_molsim_school_Amsterdam/theoretical/502-mofs>
   Geometric properties <./pages/2019_molsim_school_Amsterdam/theoretical/geometric-properties>
   Multiply the unit cell <./pages/2019_molsim_school_Amsterdam/theoretical/multiply-uc>
   Settings for Raspa <./pages/2019_molsim_school_Amsterdam/theoretical/settings-raspa>
   Extra challenge: MOFs for CO2 capture <./pages/2019_molsim_school_Amsterdam/theoretical/charged-adsorbates>
