AiiDA Quantum ESPRESSO tutorial
===============================

.. _Homepage:

+-----------------+-----------------------------------------------------------------------------------------------------------+
| Related resources                                                                                                           |
+=================+===========================================================================================================+
| Quantum Mobile  | Custom `Quantum Mobile`_ version                                                                          |
+-----------------+-----------------------------------------------------------------------------------------------------------+
| AiiDAlab        | `AiiDAlab docker stack 21.02.1`_, `AiiDAlab k8s deployment`_                                              |
+-----------------+-----------------------------------------------------------------------------------------------------------+
| python packages | `aiida-core 1.5.2`_, `aiida-quantumespresso 3.3.0`_                                                       |
+-----------------+-----------------------------------------------------------------------------------------------------------+
| codes           | `Quantum ESPRESSO 6.0.0`_                                                                                 |
+-----------------+-----------------------------------------------------------------------------------------------------------+

.. _`Quantum Mobile`: https://quantum-mobile.readthedocs.io/en/latest/index.html
.. _AiiDAlab docker stack 21.02.1: https://github.com/aiidalab/aiidalab-docker-stack/releases/tag/v21.02.1
.. _AiiDAlab k8s deployment: https://github.com/aiidalab/aiidalab-k8s
.. _aiida-core 1.5.2: https://pypi.org/project/aiida-core/1.5.2/
.. _aiida-quantumespresso 3.3.0: https://pypi.org/project/aiida-quantumespresso/3.3.0/
.. _Quantum ESPRESSO 6.0.0: https://github.com/QEF/q-e/releases/tag/qe-6.0.0

This tutorial is a short introduction to some of the features of AiiDA where you will run some Quantum ESPRESSO calculations and workflows, as well as learn how to organize and query your data.

Setup
-----

The tutorial can either be run in the Quantum Mobile virtual machine, or on the AiiDAlab demo cluster.
Note that since the AiiDAlab demo cluster can only handle a limited number of consecutive users, using Quantum Mobile can offer a more reliable experience.

.. tabs::

   .. tab:: Quantum Mobile

      Quantum Mobile is a virtual machine that provides a ready-to-run environment for computational materials science.
      We have prepared a custom VirtualBox image for this tutorial, you can find it via |Quantum Mobile image link|.

      Download the image and install |VirtualBox| 6.1.6 or later.
      Once you have VirtualBox installed, you should be able to import the ``.ova`` file by simply double clicking it.
      Alternatively, you can open VirtualBox and import the file via ``File -> Import Appliance``.
      Set the "Machine Base Folder" to your preferred location, and click "Import" and then "Agree" to start the import process.
      This can take a bit of time, so this the perfect opportunity to make sure you have some coffee before you get started. |:coffee:|

      Once the process is complete, just click the big green arrow that says "Start" to launch the virtual machine!
      Next open a terminal by clicking the icon in the dock on the left and type:

      .. code-block:: console

         $ workon aiida

      .. figure:: source/images/QM-terminal.png
         :width: 100%

      This will activate the Python environment that has AiiDA and the Quantum ESPRESSO plugin installed.
      You can then also double check that everything is running smoothly with the command:

      .. code-block:: console

         $ verdi status

      If you see all green check marks, you're ready to start with the tutorial!

   .. tab:: AiiDAlab cluster

      The |AiiDAlab demo cluster| is a Jupyter-based web platform installed on a cluster that can run some basic calculations for demonstration and tutorial purposes.
      Simply click the link and log in with the EGI check-in.

      The first part of the tutorial will be run in the terminal.
      Just click on the "Terminal" icon in the header to open one in a new tab.

      .. figure:: source/images/AiiDAlab_header-terminal.png
         :width: 100%

      Once the terminal is opened, you're all set to get started with the tutorial!

.. |AiiDAlab demo cluster| raw:: html

   <a href="https://aiidalab-demo.materialscloud.org" target="_blank">AiiDAlab demo cluster</a>

.. |Quantum Mobile image link| raw:: html

   <a href="https://u.pcloud.link/publink/show?code=XZMvUBXZ2zughxF5dkQItIzW5pikxLx3JEwV" target="_blank">this link</a>

.. |VirtualBox| raw:: html

   <a href="https://www.virtualbox.org/" target="_blank">VirtualBox</a>

Hands-on materials
------------------

The hands-on sessions consist of one short session on running calculations and a simple workflow with Quantum ESPRESSO, as well as a session on organising and querying your data.
If you have time left after going through the first two sections, you can have a look at the "Provenance tutorial", which explains more about the basic concepts of AiiDA.

.. toctree::
   :maxdepth: 2
   :caption: Hands-on sessions
   :numbered:

   ./source/sections/qe
   ./source/sections/data
   ./source/sections/install

.. toctree::
   :maxdepth: 1
   :caption: Appendices
   :numbered:

   ./source/sections/basics

In-depth tutorial
-----------------

This tutorial is only a short introduction to AiiDA and its features.
If you want to learn more, you can check the `2020 AiiDA virtual tutorial <https://aiida-tutorials.readthedocs.io/en/tutorial-2020-intro-week/index.html>`_.
Note that some of the material there can be outdated, and may require you to install the corresponding Quantum Mobile version to run smoothly.

Acknowledgements
----------------

This tutorial was made possible by support from the MaX European Centre of Excellence, the MARVEL National Centre of Competence in Research and the H2020 INTERSECT project.

.. image:: source/sponsors/max.png
   :target: http://www.max-centre.eu/
   :width: 35%

.. image:: source/sponsors/marvel.png
   :target: http://nccr-marvel.ch/
   :width: 25%

.. image:: source/sponsors/INTERSECT_logo.png
   :target: https://intersect-project.eu/
   :width: 30%
