.. _Chiba 2019 Homepage:

2019, ISSP University of Tokyo, Chiba, Japan
=============================================

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
.. _aiida-quantumespresso 3.0.0a5: https://pypi.org/project/aiida-quantumespresso/3.0.0a5
.. _aiidalab 19.08.0a1: https://pypi.org/project/aiidalab/19.8.0a1
.. _Quantum Espresso 6.4.1: https://github.com/QEF/q-e/releases/tag/qe-6.4.1

These are the hands-on materials from the 2-day AiiDA tutorial
|tutorial_name| from December 19-20, 2019.

Participants of the tutorial use the Quantum Mobile VirtualBox image
linked above or from `this mirror
<http://phonondb.mtl.kyoto-u.ac.jp/quantum_mobile_19.09.0.ova>`_ on
their own computer. The image already contains all the required
software.

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
