+-----------------+------------------------------------------------------------------+
| Related resources                                                                  |
+=================+==================================================================+
| Virtual Machine | `Quantum Mobile 18.04.0`_                                        |
+-----------------+------------------------------------------------------------------+
| python packages | `aiida-core 0.11.4`_, `aiida-zeopp 0.1.0`_, `aiida-raspa 0.2.1`_ |
+-----------------+------------------------------------------------------------------+
| codes           | `zeo++ 0.3`_, `raspa 2.0.30`_                                    |
+-----------------+------------------------------------------------------------------+

.. _Quantum Mobile 18.04.0: https://github.com/marvel-nccr/quantum-mobile/releases/tag/18.04.0
.. _aiida-core 0.11.4: https://pypi.org/project/aiida-core/0.11.4/
.. _aiida-zeopp 0.1.0: https://pypi.org/project/aiida-zeopp/0.1.0/
.. _aiida-raspa 0.2.1: https://pypi.org/project/aiida-raspa/0.2.1/
.. _zeo++ 0.3: http://www.zeoplusplus.org/download.html
.. _raspa 2.0.30: https://github.com/iRASPA/RASPA2/releases/tag/v2.0.30

The following tutorial is part of the course `Understanding advanced molecular
simulation <http://edu.epfl.ch/coursebook/en/understanding-advanced-molecular-simulation-CH-420>`__
held at EPF Lausanne during the spring semester 2018.


Understanding advanced molecular simulation
===========================================

This tutorial makes use of the AiiDA plugins for the `zeo++
<http://www.zeoplusplus.org/>`__ and `RASPA2
<https://github.com/numat/RASPA2>`__ codes.
It is meant to be run inside the `Quantum
Mobile <https://www.materialscloud.org/work/quantum-mobile>`__ virtual
machine.


AiiDA tutorial
--------------


.. toctree::
   :maxdepth: 1
   :numbered:

   Preparation <./tutorial/preparation>
   Using the verdi command line <./tutorial/verdi-commands>
   Submit, monitor and debug calculations <./tutorial/calculations>
   The AiiDA python interface <./tutorial/python-interface>
   Queries in AiiDA: The QueryBuilder <./tutorial/queries>

Screening nanoporous materials
------------------------------

**Task:** Screen a set of metal-organic frameworks (MOFs) for their
performance in storing methane at room temperature by computing their
*deliverable capacities*, i.e. the difference between the amount of
methane stored in a fully loaded tank (at 65 bar) and an empty tank (at
5.8 bar) per volume.

**Report:** Write a short report (1 page) outlining your approach and
identifying the five MOFs with the highest deliverable capacities.
Include an export of your AiiDA database [1]_.

**Note:** This exercise requires a basic knowledge of python. If you are
not familiar with python, partner with someone who is.

.. toctree::
   :maxdepth: 1
   :numbered:

   Import the structures <screening/import>
   Perform geometric analysis <./screening/geometry>
   Compute methane loading <./screening/methane-loading>
   Screening <./screening/screening>
   Ranking <./screening/ranking>
   Exporting your database <./screening/export>

.. [1]
   Upload to a file hosting service like
   `SWITCHdrive <https://drive.switch.ch/>`__ or
   `Dropbox <https://www.dropbox.com/>`__ and include a download link in
   the report.
