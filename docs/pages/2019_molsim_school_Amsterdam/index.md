# Metal-organic frameworks for methane storage applications

In this tutorial, we will screen metal-organic frameworks (MOFs) for their possible application
as methane adsorbents, allowing to store natural gas at increased density and lower storage pressure.
We will use the [AiiDA framework](www.aiida.net) in order to automate the screening workflow
and to record the full provenance of the calculations for reproducibility.

This tutorial is part of the
[Understanding molecular simulation](http://www.acmm.nl/molsim/molsim2019/)
school held at the University of Amsterdam from January 7-18 2019.

It is meant to be run inside the [Quantum Mobile](https://www.materialscloud.org/work/quantum-mobile) virtual machine,
using a compute resource with [zeo++](http://www.zeoplusplus.org/) and [RASPA2](https://github.com/numat/RASPA2) installed.

**Note:** This tutorial requires a basic knowledge of
[python](https://docs.python.org/2.7/tutorial/index.html). If you are not
familiar with python, we suggest you partner with someone who is.

### Using AiiDA:

 1. [Getting set up](./tutorial/setup.md)
 1. [Using the verdi command line](./tutorial/verdi-commands)
 1. [Submit, monitor and debug calculations](./tutorial/calculations)
 1. [The AiiDA python interface](./tutorial/python-interface)
 1. [Queries in AiiDA: The QueryBuilder](./tutorial/queries)
 1. [Import the structures](./screening/import)
 1. [Perform geometric analysis](./screening/geometry)
 1. [Compute methane loading](./screening/methane-loading)
 1. [Screening](./screening/screening)
 1. [Ranking](./screening/ranking)
 1. [Exporting your database](./screening/export)

### Theoretical background:

  1. [Reference for the 502 CoRE-MOFs](./theoretical/502-mofs)
  1. [Geometric properties](./theoretical/geometric-properties)
  1. [Geometric/performances relationship](./theoretical/geometric-performance)
  1. [Multiply the unit cell](./theoretical/multiply-uc)
  1. [Settings for Raspa](./theoretical/settings-raspa)
  1. [Extra: working with adsorbates with partial charges](./theoretical/charged-adsorbates)
