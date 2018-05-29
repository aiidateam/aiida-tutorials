# Understanding advanced molecular simulation

The following tutorial are part of the course
[Understanding advanced molecular simulation](http://edu.epfl.ch/coursebook/en/understanding-advanced-molecular-simulation-CH-420) held at EPF Lausanne
during the spring semester 2018.

##1. AiiDA tutorial

This is a brief AiiDA tutorial, making use of the AiiDA plugins for the
[zeo++](http://www.zeoplusplus.org/) and [RASPA2](https://github.com/numat/RASPA2) codes.

The tutorial is meant to be run inside the [Quantum Mobile](https://www.materialscloud.org/work/quantum-mobile) virtual machine.

###1. [Preparation](./tutorial/preparation)

###1. [Using the verdi command line](./tutorial/verdi-commands)

###1. [Submit, monitor and debug calculations](./tutorial/calculations)

###1. [The AiiDA python interface](./tutorial/python-interface)

###1. [Queries in AiiDA: The QueryBuilder](./tutorial/queries)

##1. Screening nanoporous materials

**Task:** Screen a set of metal-organic frameworks (MOFs) for their
performance in storing methane at room temperature by computing their
*deliverable capacities*, i.e. the difference between the amount of
methane stored in a fully loaded tank (at 65 bar) and an empty tank (at
5.8 bar) per volume.

**Report:** Write a short report (1 page) outlining your approach and
identifying the five MOFs with the highest deliverable capacities.
Include an export of your AiiDA database[^1].

**Note:** This exercise requires a basic knowledge of python. If you are
not familiar with python, partner with someone who is.

###1. [Import the structures](./screening/import)

###1. [Perform geometric analysis](./screening/geometry)

###1. [Compute methane loading](./screening/methane-loading)

###1. [Screening](./screening/screening)

###1. [Ranking](./screening/ranking)

###1. [Exporting your database](./screening/export)



[^1]: Upload to a file hosting service like
    [SWITCHdrive](https://drive.switch.ch/) or
    [Dropbox](https://www.dropbox.com/) and include a download link in
    the report.
