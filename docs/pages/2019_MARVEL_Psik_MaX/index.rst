+-----------------+----------------------------------------------------------------------------+
| Prerequisite    | Version                                                                    |
+=================+============================================================================+
| Virtual Machine | `Quantum Mobile 19.05.0-tutorial`_                                         |
+-----------------+----------------------------------------------------------------------------+
| python packages | `aiida-core 1.0.0b3`_, `aiida-quantumespresso 3.0.0a3`_, `aiidalab 19.05`_ |
+-----------------+----------------------------------------------------------------------------+
| codes           | `Quantum Espresso 6.3`_                                                    |
+-----------------+----------------------------------------------------------------------------+

.. _Quantum Mobile 19.05.0-tutorial: https://github.com/marvel-nccr/quantum-mobile/releases/tag/tutorial-2019-05
.. _aiida-core 1.0.0b3: https://pypi.org/project/aiida-core/1.0.0b3
.. _aiida-quantumespresso 3.0.0a3: https://github.com/aiidateam/aiida-quantumespresso/releases/tag/v3.0.0a3
.. _aiidalab 19.05: https://github.com/aiidalab/aiidalab-metapkg/releases/tag/tutorial-2019-05
.. _Quantum Espresso 6.3: https://github.com/QEF/q-e/releases/tag/qe-6.3

These are the notes of the `AiiDA tutorial on writing reproducible workflows for computational materials science <http://www.aiida.net/tutorial-reproducible-workflows/>`__  (supported by MARVEL, Psi-k, MaX, swissuniversitites and INTERSECT) taking place from May 21-24, 2019 at EPF Lausanne, Switzerland.

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

   ./sections/appendix_computer_code_setup
   ./sections/appendix_input_validation
   ./sections/appendix_restarting_calculations
   ./sections/appendix_queries
   ./sections/appendix_workflow_logic
