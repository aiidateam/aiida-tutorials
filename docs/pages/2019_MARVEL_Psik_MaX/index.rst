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
<http://www.aiida.net/tutorial-reproducible-workflows/>`__  (supported by MARVEL, Psi-k, MaX, swissuniversitites and INTERSECT) taking place from
May 21-24, 2019 at EPF Lausanne, Switzerand.

Writing reproducible workflows for computational materials science
==================================================================

Sections
--------

.. toctree::
   :maxdepth: 1
   :numbered:

   ./sections/setup
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

   ./sections/appendix_input_validation
   ./sections/appendix_restarting_calculations
   ./sections/appendix_queries
   ./sections/appendix_workflow_logic
