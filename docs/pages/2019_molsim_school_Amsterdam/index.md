# Metal-organic frameworks for methane storage applications

In this tutorial, we will screen metal-organic frameworks (MOFs) for their possible application
as methane adsorbents, allowing to store natural gas at increased density and lower storage pressure.
We will use the [AiiDA framework](www.aiida.net) in order to automate the screening workflow
and to record the full provenance of the calculations for reproducibility.

The tutorial is meant to be run inside the [Quantum Mobile](https://www.materialscloud.org/work/quantum-mobile) virtual machine,
using a compute resource with [zeo++](http://www.zeoplusplus.org/) and [RASPA2](https://github.com/numat/RASPA2) installed.

**Note:** This tutorial requires a basic knowledge of
[python](https://docs.python.org/2.7/tutorial/index.html). If you are not
familiar with python, we suggest you partner with someone who is.

## Analyzing the database

 1. [Getting set up](./tutorial/setup.md)
 1. [Browsing the provenance graph](./tutorial/provenance-graph)
 1. [The verdi command line](./tutorial/verdi-commands)
 1. [The AiiDA python interface](./tutorial/python-interface)
 1. [Querying the AiiDA database](./tutorial/queries)
 1. [Selecting candidate materials](./tutorial/candidate-selection)

## Computing properties of candidate materials

 1. [Submit, monitor and debug calculations](./screening/calculations)
 1. [Perform geometric analysis](./screening/geometry)
 1. [Compute methane loading](./screening/methane-loading)
 1. [Screening](./screening/screening)
 1. [Upload your results](./screening/export)

## Theoretical background

  1. [Origin of the MOF database](./theoretical/502-mofs)
  1. [Geometric properties](./theoretical/geometric-properties)
  1. [Multiply the unit cell](./theoretical/multiply-uc)
  1. [Settings for Raspa](./theoretical/settings-raspa)
  1. [Extra challenge: MOFs for CO2 capture](./theoretical/charged-adsorbates)


This tutorial is part of the
[Understanding molecular simulation](http://www.acmm.nl/molsim/molsim2019/)
school held at the University of Amsterdam from January 7-18 2019.

