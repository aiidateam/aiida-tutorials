.. _SINTEF 2019 Homepage:

2019, SINTEF, Oslo, Norway
======================================

+-----------------+--------------------------------------------------------------------------------+
| Related resources                                                                                |
+=================+================================================================================+
| Virtual Machine | `Quantum Mobile 19.09.0`_                                                      |
+-----------------+--------------------------------------------------------------------------------+
| python packages | `aiida-core 1.0.0b6`_, `aiida-quantumespresso 3.0.0a5`_, `aiidalab 19.08.0a1`_ |
+-----------------+--------------------------------------------------------------------------------+
| codes           | `Quantum Espresso 6.4.1`_                                                      |
+-----------------+--------------------------------------------------------------------------------+

.. _Quantum Mobile 19.09.0: https://github.com/marvel-nccr/quantum-mobile/releases/tag/19.09.0
.. _aiida-core 1.0.0b6: https://pypi.org/project/aiida-core/1.0.0b6
.. _aiida-quantumespresso 3.0.0a5: https://github.com/aiidateam/aiida-quantumespresso/releases/tag/v3.0.0a5
.. _aiidalab 19.08.0a1: https://pypi.org/project/aiidalab/19.8.0a1
.. _Quantum Espresso 6.4.1: https://github.com/QEF/q-e/releases/tag/qe-6.4.1

These are the hands-on materials for the week long AiiDA tutorial, part of the `VASP and AiiDA workshop at SINTEF in Oslo, Norway <https://www.sigma2.no/content/vasp-and-aiida-workshop>`__  from September 23-27, 2019.

While participants of the tutorial used virtual machines on a cloud service, one can follow the tutorial just as well using the Quantum Mobile VirtualBox image linked above. The image already contains all the required software.

AiiDA hands-on materials
^^^^^^^^^^^^^^^^^^^^^^^^

Demo
----

.. toctree::
   :maxdepth: 1
   :numbered:

   ./sections/setup
   ./sections/first_taste

In-depth tutorial
-----------------

.. toctree::
   :maxdepth: 1
   :numbered:

   ./sections/verdi_cmdline
   ./sections/verdi_shell
   ./sections/calculations
   ./sections/querybuilder
   ./sections/workflows
   ./sections/bands

Appendices
----------

.. toctree::
   :maxdepth: 1
   :numbered:

   ./sections/appendix_computer_code_setup
   ./sections/appendix_input_validation
   ./sections/appendix_restarting_calculations
   ./sections/appendix_queries
   ./sections/appendix_workflow_logic
