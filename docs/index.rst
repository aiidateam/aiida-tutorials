AiiDA virtual tutorial 2022
===========================

Welcome to the official home of the latest tutorial materials and videos of the AiiDA virtual tutorial, which is being organised from 4-7 October 2022!
Below you can find the schedule of the tutorial, as well as the AiiDA cheat sheet, which will come in handy as you are working through the material:

.. panels::
   :body: bg-light text-center large-text

   ------
   :column: col-lg-6 pl-0 pr-0
   :download:`The Tutorial Schedule <include/images/schedule.pdf>`

   -------
   :column: col-lg-6 pl-0 pr-0
   :download:`AiiDA Cheat Sheet <cheatsheet/cheatsheet.pdf>`

Presentations
-------------

For this virtual tutorial, most presentations have been recorded beforehand, so you can watch them at the time that is most convenient for you.
However, you are required to watch certain presentations before the hands-on sessions of certain days.
These are tabulated below:

.. list-table::
   :widths: 30 25 45
   :class: skinny-table
   :header-rows: 1

   * - **Date**
     - **Presenter**
     - **Title**
   * - **Tuesday October 4th**
     - Marnik Bercx
     - (LIVE) Welcome and AiiDA Tutorial Overview
   * - **Wednesday October 5th**
     - Kristjan Eimre
     - The Materials Cloud
   * -
     - Jusong Yu
     - AiiDA and OPTIMADE
   * - **Thursday October 6th**
     - Marnik Bercx
     - Provenance and workflows in AiiDA
   * -
     - Jusong Yu
     - Creating your development environment
   * - **Friday October 7th**
     - Jusong Yu
     - The AiiDA Plugin Ecosystem
   * -
     - Aliaksandr Yakotovich
     - AiiDA lab

Hands-on sessions
-----------------

The material for the hands-on sessions is divided in 5 units:

.. toctree::

   sections/getting_started/index
   sections/running_processes/index
   sections/managing_data/index
   sections/writing_workflows/index
   sections/creating_plugins/index

These are also accessible via the sidebar on the left.
The tutorial will be run in your browser by accessing an AiiDAlab JupyterHub deployed on the `Azure Kubernetes Service`_.
See the "Set up" section, also accessible by clicking below, along with the module for the first hands-on topic.

.. panels::
   :body: bg-light text-center

   ------
   :column: col-lg-6 pl-0 pr-0

   .. link-button:: fundamentals-setup
      :type: ref
      :text: Set up
      :classes: btn-link btn-block stretched-link

   ------
   :column: col-lg-6 pl-0 pr-0

   .. link-button:: fundamentals-basics
      :type: ref
      :text: First hands-on: AiiDA basics
      :classes: btn-link btn-block stretched-link

Contributed talks
-----------------

Supplementing the presentations above, there are also contributed talks from plugin developers and experienced AiiDA users.
These can be watched at any time, but please try to watch them **before Friday October 7th**, as we have planned a Q&A with the plugin developers at the start of the first hands-on session of that day.
Here is a list of all the contributed talks:

.. list-table::
   :widths: 30 70
   :class: skinny-table
   :header-rows: 1

   * - **Presenter**
     - **Title**
   * - Emanuele Bosoni
     - `Introducing aiida-siesta`_
   * - Dou Du
     - `OSSCAR`_
   * - Daniele Ongari
     - `Using AiiDA to study gas adsorption in microporous crystals`_
   * - Dominik Gresch
     - `Introduction to aiida-optimize`_
   * - Atsushi Togo
     - `Harmonic phonon calculation using AiiDA AiiDA-VASP and AiiDA-phonopy`_
   * - Bonan Zhu
     - `Introducing aiida-castep`_
   * - Philipp Rüßmann
     - `The aiida-kkr plugin`_
   * - Miki Bonacci
     - `The Yambo-AiiDA plugin`_
   * - Leonid Kahle
     - `Using AiiDA to screen for solid-state Li-ion conductors`_
   * - Jens Bröder
     - `Introduction to AiiDA-Fleur`_
   * - Espen Flage-Larsen
     - `Introduction to AiiDA-VASP`_

.. _Welcome and AiiDA Tutorial Overview (LIVE): https://youtu.be/0lWYphVDSJc
.. _Introduction to AiiDA: https://www.youtube.com/watch?v=jigMCyWGNAE
.. _Setting up an environment with Quantum Mobile Cloud: https://www.youtube.com/watch?v=vlmjVwGJgEU
.. _Provenance and workflows in AiiDA: https://www.youtube.com/watch?v=KpiLIA8ge1w
.. _The AiiDA Plugin Ecosystem: https://www.youtube.com/watch?v=bjTUnHXZ6oY
.. _The Materials Cloud: https://www.youtube.com/watch?v=_T8HBuOYUyc
.. _AiiDA lab: https://www.youtube.com/watch?v=BwtxyTAVugY
.. _AiiDA and OPTIMADE: https://www.youtube.com/watch?v=F0e3cQHNbNM
.. _OSSCAR: https://www.youtube.com/watch?v=3rkhzYBUuA4
.. _Using AiiDA to study gas adsorption in microporous crystals: https://www.youtube.com/watch?v=9p_krkdEz_A
.. _Introduction to aiida-optimize: https://www.youtube.com/watch?v=YzHuIrYhyFI
.. _Harmonic phonon calculation using AiiDA AiiDA-VASP and AiiDA-phonopy: https://www.youtube.com/watch?v=Uqz-i29JD5U
.. _Introducing aiida-castep: https://www.youtube.com/watch?v=X18SiQwVPQo
.. _Introducing aiida-siesta: https://www.youtube.com/watch?v=0S7rvut8gpE
.. _The aiida-kkr plugin: https://www.youtube.com/watch?v=ccmEWKgVfVc
.. _The Yambo-AiiDA plugin: https://www.youtube.com/watch?v=NzhN5ce0Sc8
.. _Using AiiDA to screen for solid-state Li-ion conductors: https://youtu.be/UFC2UWwIHwE
.. _Introduction to AiiDA-Fleur: https://www.youtube.com/watch?v=qPVWA2motO4
.. _AiiDA Installation Tutorial: https://youtu.be/skx9VZierbk
.. _Introduction to AiiDA-VASP: https://youtu.be/iH7KJgdkPTE

Acknowledgements
----------------

We are very grateful to our sponsors for helping to make this event possible:

The `MaX European Centre of Excellence`_, the `MARVEL National Centre of Competence in Research`_, the `swissuniversities P-5 project “Materials Cloud”`_, the `H2020 MARKETPLACE project`_, and the `BIG-MAP project`_.
Computational resources on Azure were provided by `Microsoft Azure Quantum`_.

.. _Azure Kubernetes Service: https://azure.microsoft.com/en-us/products/kubernetes-service/
.. _MaX European Centre of Excellence: http://www.max-centre.eu/
.. _MARVEL National Centre of Competence in Research: http://nccr-marvel.ch/
.. _swissuniversities P-5 project “Materials Cloud”: https://www.materialscloud.org/swissuniversities
.. _H2020 MARKETPLACE project: https://www.the-marketplace-project.eu/
.. _BIG-MAP project: https://www.big-map.eu/
.. _Microsoft Azure Quantum: https://azure.microsoft.com/en-us/products/quantum/

.. list-table::
   :widths: 60 40
   :class: skinny-table
   :header-rows: 0

   * - .. figure:: _static/MaX-logo.jpeg
     - .. figure:: _static/MARVEL-logo.png

.. list-table::
   :widths: 60 20 20
   :class: skinny-table
   :header-rows: 0

   * - .. figure:: _static/microsoft-logo.png
     -
     - .. figure:: _static/bigmap-logo.png

.. list-table::
   :widths: 50 50
   :class: skinny-table
   :header-rows: 0

   * - .. figure:: _static/swissuniversities-logo.png
     - .. figure:: _static/marketplace-logo.png
