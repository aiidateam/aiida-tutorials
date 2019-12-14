.. _Chiba 2019 Homepage:

2019, ISSP University of Tokyo, Chiba, Japan
=============================================

+-----------------+--------------------------------------------------------------------------------+
| Related resources                                                                                |
+=================+================================================================================+
| Virtual Machine | `Quantum Mobile (ISSP special)`_                                               |
+-----------------+--------------------------------------------------------------------------------+
| python packages | `aiida-core 1.0.1`_, `aiida-quantumespresso 3.0.0a5`_, `aiidalab 19.11.0a2`_   |
+-----------------+--------------------------------------------------------------------------------+
| codes           | `Quantum Espresso 6.4.1`_                                                      |
+-----------------+--------------------------------------------------------------------------------+

.. _Quantum Mobile (ISSP special): http://phonondb.mtl.kyoto-u.ac.jp/aiida_tutorial/Quantum_Mobile_ISSP.ova
.. _aiida-core 1.0.1: https://pypi.org/project/aiida-core/1.0.1
.. _aiida-quantumespresso 3.0.0a5: https://pypi.org/project/aiida-quantumespresso/3.0.0a5
.. _aiidalab 19.11.0a2: https://pypi.org/project/aiidalab/19.11.0a2
.. _Quantum Espresso 6.4.1: https://github.com/QEF/q-e/releases/tag/qe-6.4.1

These are the hands-on materials from the 2-day AiiDA tutorial
|tutorial_name| from December 19-20, 2019.

Participants of the tutorial use the Quantum Mobile VirtualBox virtual
machine (VM) image linked above on their own computer. The image
already contains all the required software. This VM image can be
imported from the GUI interface of VirtualBox by "File => Import
Appliance" or from the Virtualbox window "[Tools] =>
[Import]".

Getting started
---------------

.. toctree::
   :maxdepth: 1
   :numbered:

   ./sections/setup
   ./sections/first_taste

Sections
--------

.. toctree::
   :maxdepth: 1
   :numbered:

   ./sections/verdi_cmdline
   ./sections/verdi_shell
   ./sections/calculations
   ./sections/querybuilder
   ./sections/workflows

Appendices
----------

.. toctree::
   :maxdepth: 1
   :numbered:

   ./sections/appendix_computer_code_setup
   ./sections/appendix_structure_data
   ./sections/appendix_upf_data
   ./sections/appendix_input_validation
   ./sections/appendix_restarting_calculations
   ./sections/appendix_queries
   ./sections/appendix_workflow_logic

Acknowledgements
----------------

The |tutorial_name| was made possible by support from ISSP
Univ. Tokyo, MARVEL, and kindly hosted by ISSP Univ. Tokyo.

.. image:: sponsors/issplogo_en.jpg
   :target: http://www.issp.u-tokyo.ac.jp/index_en.html
   :width: 120px

.. image:: sponsors/marvel.png
   :target: http://nccr-marvel.ch
   :width: 105px

.. image:: sponsors/epfl.png
   :target: https://epfl.ch
   :width: 105px

.. |tutorial_name| raw:: html

   <a href="https://atztogo.github.io/AiiDA-tutorial-ISSP/" target="_blank">Workshop on Writing reproducible workflows for computational materials science using AiiDA</a>
