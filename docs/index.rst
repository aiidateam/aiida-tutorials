AiiDA Quantum ESPRESSO tutorial
===============================

.. _Homepage:

This tutorial is a short introduction to some of the features of AiiDA where you will run some Quantum ESPRESSO calculations and workflows, as well as learn how to organize and query your data.

Setup
-----

The hands-on for the `"MaX School on Advanced Materials and Molecular Modelling with Quantum ESPRESSO" <http://indico.ictp.it/event/9616/>`_ will be run on a dedicated JupyterHub cluster that can be accessed via the following link:

https://qe-school.aiida-tutorials.net/

Simply log in with a username and password of your choosing, your account will be created automatically.
The first log in might take a few minutes, but subsequent logins will be much faster.

.. important::

   Note down your password so that you can login again in case you get inadvertently logged out. In case you forgot your password, the admin can make a new account, **but you will lose your progress!**

This cluster will be taken down on **Saturday 29 May at 12:00 CEST**.
Be sure to download any data you want to keep before this time.

Afterwards, the material can still be run on the `Quantum Mobile <https://quantum-mobile.readthedocs.io/en/latest/>`_ virtual machine.
You could also use the AiiDAlab demo cluster, but since it can only handle a limited number of simultaneous users, the Quantum Mobile can offer a more reliable experience.


.. note::

   Some of the procedures might be slightly different depending on whether you are using the "Quantum Mobile" virtual machine or the "AiiDAlab cluster".
   We have included the instructions for both, so at certain points in the hands-on you will find boxes like the one below, with different tabs for each case.

   When running the hands-on via the link above, you need to follow the instructions in the "**AiiDAlab cluster**" tab.


.. tabs::

   .. tab:: AiiDAlab cluster

      +-----------------+-----------------------------------------------------------------------------------------------------------+
      | Related resources                                                                                                           |
      +=================+===========================================================================================================+
      | AiiDAlab        | `AiiDAlab docker stack 21.02.1`_, `AiiDAlab k8s deployment`_                                              |
      +-----------------+-----------------------------------------------------------------------------------------------------------+
      | python packages | `aiida-core 1.5.2`_, `aiida-quantumespresso 3.3.0`_                                                       |
      +-----------------+-----------------------------------------------------------------------------------------------------------+
      | codes           | `Quantum ESPRESSO 6.0.0`_                                                                                 |
      +-----------------+-----------------------------------------------------------------------------------------------------------+

      The |AiiDAlab demo cluster| is a Jupyter-based web platform installed on a cluster that can run some basic calculations for demonstration and tutorial purposes.
      Simply click the link and log in with the EGI check-in.

      The first part of the tutorial will be run in the terminal.
      Just click on the "Terminal" icon in the header to open one in a new tab.

      .. figure:: source/images/AiiDAlab_header-terminal.png
         :width: 100%

      Once the terminal is opened, you're all set to get started with the tutorial!

   .. tab:: Quantum Mobile

      +-----------------+-----------------------------------------------------------------------------------------------------------+
      | Related resources                                                                                                           |
      +=================+===========================================================================================================+
      | Quantum Mobile  | `Quantum Mobile v21.03.18-qe`_                                                                            |
      +-----------------+-----------------------------------------------------------------------------------------------------------+
      | python packages | `aiida-core 1.5.2`_, `aiida-quantumespresso 3.4.0`_                                                       |
      +-----------------+-----------------------------------------------------------------------------------------------------------+
      | codes           | `Quantum ESPRESSO 6.5`_                                                                                   |
      +-----------------+-----------------------------------------------------------------------------------------------------------+

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

.. |AiiDAlab demo cluster| raw:: html

   <a href="https://aiidalab-demo.materialscloud.org" target="_blank">AiiDAlab demo cluster</a>

.. |Quantum Mobile image link| raw:: html

   <a href="http://bit.ly/2OLjz2o" target="_blank">this link</a>

.. |VirtualBox| raw:: html

   <a href="https://www.virtualbox.org/" target="_blank">VirtualBox</a>

.. _`Quantum Mobile v21.03.18-qe`: https://quantum-mobile.readthedocs.io/en/latest/releases/both/21.03.18-qe.html
.. _AiiDAlab docker stack 21.02.1: https://github.com/aiidalab/aiidalab-docker-stack/releases/tag/v21.02.1
.. _AiiDAlab k8s deployment: https://github.com/aiidalab/aiidalab-k8s
.. _aiida-core 1.5.2: https://pypi.org/project/aiida-core/1.5.2/
.. _aiida-quantumespresso 3.3.0: https://pypi.org/project/aiida-quantumespresso/3.3.0/
.. _aiida-quantumespresso 3.4.0: https://pypi.org/project/aiida-quantumespresso/3.4.0/
.. _Quantum ESPRESSO 6.0.0: https://github.com/QEF/q-e/releases/tag/qe-6.0.0
.. _Quantum ESPRESSO 6.5: https://github.com/QEF/q-e/releases/tag/qe-6.5
