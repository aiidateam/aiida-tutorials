Metal-organic frameworks for methane storage applications
=========================================================

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

Analyzing the database
----------------------

.. toctree::
   :maxdepth: 1
   :numbered:

   Getting set up <./tutorial/setup>
   Browsing the provenance graph <./tutorial/provenance-graph>
   The verdi command line <./tutorial/verdi-commands>
   The AiiDA python interface <./tutorial/python-interface>
   Querying the AiiDA database <./tutorial/queries>
   Selecting candidate materials <./tutorial/candidate-selection>

Computing properties of candidate materials
-------------------------------------------

.. toctree::
   :maxdepth: 1
   :numbered:

   Setting up remote computers and codes <./screening/calculations>
   Compute methane loading <./screening/methane-loading>
   Screening <./screening/screening>
   Upload your results <./screening/export>

Theoretical background
----------------------

.. toctree::
   :maxdepth: 1
   :numbered:

   Origin of the MOF database <./theoretical/502-mofs>
   Geometric properties <./theoretical/geometric-properties>
   Multiply the unit cell <./theoretical/multiply-uc>
   Settings for Raspa <./theoretical/settings-raspa>
   Extra challenge: MOFs for CO2 capture <./theoretical/charged-adsorbates>

This tutorial is part of the `Understanding molecular
simulation <http://www.acmm.nl/molsim/molsim2019/>`__ school held at the
University of Amsterdam from January 7-18 2019.
