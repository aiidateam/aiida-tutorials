.. _2020_Intro_Week_Homepage:

2020 AiiDA tutorial week "Virtual Edition"
==========================================

+-----------------+----------------------------------------------------------------------------------------------------------------------+
| Related resources                                                                                                                      |
+=================+======================================================================================================================+
| Virtual Machine | AWS access sent individually or desktop VM available using                                                           |
|                 | `this release <https://github.com/marvel-nccr/quantum-mobile/releases/tag/20.06.1>`__                                |
+-----------------+----------------------------------------------------------------------------------------------------------------------+
| python packages | `aiida-core 1.3.0`_, `aiida-quantumespresso 3.0.0`_                                                                  |
+-----------------+----------------------------------------------------------------------------------------------------------------------+
| codes           | `Quantum ESPRESSO 6.5`_                                                                                              |
+-----------------+----------------------------------------------------------------------------------------------------------------------+

.. _Quantum Mobile 20.03.1: https://github.com/marvel-nccr/quantum-mobile/releases/tag/20.03.1
.. _aiida-core 1.3.0: https://pypi.org/project/aiida-core/1.3.0
.. _aiida-quantumespresso 3.0.0: https://github.com/aiidateam/aiida-quantumespresso/releases/tag/v3.0.0
.. _Quantum ESPRESSO 6.5: https://github.com/QEF/q-e/releases/tag/qe-6.5

This is the content of the `AiiDA virtual tutorial <http://www.aiida.net/aiida-virtual-tutorial-july-2020/>`_, organised from July 7-10 2020.

Presentations
-------------

For this virtual tutorial, all presentations have been recorded beforehand, so you can watch them at the time that is most convenient for you.
However, you are required to watch certain presentations before the hands-on sessions of certain days.
These are tabulated below:

+------------------------+-------------------------+--------------------------------------------------------------------+
| **Date**               | **Presenter**           | **Title**                                                          |
+========================+=========================+====================================================================+
| **Tuesday July 7th**   | Marnik Bercx            | `AiiDA Tutorial Overview`_                                         |
+                        +-------------------------+--------------------------------------------------------------------+
|                        | Francisco Ramirez       | `Introduction to AiiDA`_                                           |
+                        +-------------------------+--------------------------------------------------------------------+
|                        | Chris Sewell            | `Setting up an environment with Quantum Mobile Cloud`_             |
+------------------------+-------------------------+--------------------------------------------------------------------+
| **Wednesday July 8th** | Sebastiaan Huber        | `Provenance and workflows in AiiDA`_                               |
+------------------------+-------------------------+--------------------------------------------------------------------+
| **Thursday July 9th**  | Leopold Talirz          | `The AiiDA Plugin Ecosystem`_                                      |
+------------------------+-------------------------+--------------------------------------------------------------------+
| **Friday July 10th**   | Giovanni Pizzi          | `The Materials Cloud`_                                             |
+                        +-------------------------+--------------------------------------------------------------------+
|                        | Aliaksandr Yakotovich   | `AiiDA lab`_                                                       |
+                        +-------------------------+--------------------------------------------------------------------+
|                        | Casper Andersen         | `AiiDA and OPTIMADE`_                                              |
+                        +-------------------------+--------------------------------------------------------------------+
|                        | Dou Du                  | `OSSCAR`_                                                          |
+------------------------+-------------------------+--------------------------------------------------------------------+

.. _AiiDA Tutorial Overview: https://www.youtube.com/watch?v=RtdXXWFLvF8&list=PL19kfLn4sO_-e_A9lVYb_NBNcwoVvUP6V
.. _Introduction to AiiDA: https://www.youtube.com/watch?v=jigMCyWGNAE&list=PL19kfLn4sO_-e_A9lVYb_NBNcwoVvUP6V
.. _Setting up an environment with Quantum Mobile Cloud: https://www.youtube.com/watch?v=vlmjVwGJgEU&list=PL19kfLn4sO_-e_A9lVYb_NBNcwoVvUP6V
.. _Provenance and workflows in AiiDA: https://www.youtube.com/watch?v=KpiLIA8ge1w&list=PL19kfLn4sO_-e_A9lVYb_NBNcwoVvUP6V
.. _The AiiDA Plugin Ecosystem: https://www.youtube.com/watch?v=bjTUnHXZ6oY&list=PL19kfLn4sO_-e_A9lVYb_NBNcwoVvUP6V
.. _The Materials Cloud: https://www.youtube.com/watch?v=_T8HBuOYUyc&list=PL19kfLn4sO_-e_A9lVYb_NBNcwoVvUP6V
.. _AiiDA lab: https://www.youtube.com/watch?v=BwtxyTAVugY&list=PL19kfLn4sO_-e_A9lVYb_NBNcwoVvUP6V
.. _AiiDA and OPTIMADE: https://www.youtube.com/watch?v=F0e3cQHNbNM&list=PL19kfLn4sO_-e_A9lVYb_NBNcwoVvUP6V
.. _OSSCAR: https://www.youtube.com/watch?v=3rkhzYBUuA4&list=PL19kfLn4sO_-e_A9lVYb_NBNcwoVvUP6V

Supplementing these presentations from the ``aiida-core`` developers, there are also contributed talks from the plugin developers.
These can be watched at any time, but please try to watch them **before Friday July 10th**, as we have planned a Q&A with the plugin developers at the start of the first hands-on session of that day.
Here is a list of all the contributed talks:

+--------------------------+----------------------------------------------------------------------------------------------------------------------+
| **Presenter**            | **Title**                                                                                                            |
+==========================+======================================================================================================================+
| Daniele Ongari           | `Using AiiDA to study gas adsorption in microporous crystals`_                                                       |
+--------------------------+----------------------------------------------------------------------------------------------------------------------+
| Dominik Gresch           | `Introduction to aiida-optimize`_                                                                                    |
+--------------------------+----------------------------------------------------------------------------------------------------------------------+
| Atsushi Togo             | `Harmonic phonon calculation using AiiDA AiiDA-VASP AiiDA-phonopy`_                                                  |
+--------------------------+----------------------------------------------------------------------------------------------------------------------+
| Bonan Zhu                | `Introducing aiida-castep`_                                                                                          |
+--------------------------+----------------------------------------------------------------------------------------------------------------------+
| Emanuele Bosoni          | `Introducing aiida-siesta`_                                                                                          |
+--------------------------+----------------------------------------------------------------------------------------------------------------------+
| Philipp Rüßmann          | `The aiida-kkr plugin`_                                                                                              |
+--------------------------+----------------------------------------------------------------------------------------------------------------------+
| Miki Bonacci             | `The Yambo-AiiDA plugin`_                                                                                            |
+--------------------------+----------------------------------------------------------------------------------------------------------------------+

.. _Using AiiDA to study gas adsorption in microporous crystals: https://www.youtube.com/watch?v=9p_krkdEz_A&list=PL19kfLn4sO_-e_A9lVYb_NBNcwoVvUP6V
.. _Introduction to aiida-optimize: https://www.youtube.com/watch?v=YzHuIrYhyFI&list=PL19kfLn4sO_-e_A9lVYb_NBNcwoVvUP6V
.. _Harmonic phonon calculation using AiiDA AiiDA-VASP AiiDA-phonopy: https://www.youtube.com/watch?v=Uqz-i29JD5U&list=PL19kfLn4sO_-e_A9lVYb_NBNcwoVvUP6V
.. _Introducing aiida-castep: https://www.youtube.com/watch?v=X18SiQwVPQo&list=PL19kfLn4sO_-e_A9lVYb_NBNcwoVvUP6V
.. _Introducing aiida-siesta: https://www.youtube.com/watch?v=0S7rvut8gpE&list=PL19kfLn4sO_-e_A9lVYb_NBNcwoVvUP6V
.. _The aiida-kkr plugin: https://www.youtube.com/watch?v=ccmEWKgVfVc&list=PL19kfLn4sO_-e_A9lVYb_NBNcwoVvUP6V
.. _The Yambo-AiiDA plugin: https://www.youtube.com/watch?v=NzhN5ce0Sc8&list=PL19kfLn4sO_-e_A9lVYb_NBNcwoVvUP6V

Hands-on sessions
-----------------

Here are the links to the material for the hands-on sessions:

.. toctree::
    :maxdepth: 1
    :numbered:

    ./sections/setup
    ./sections/basics
    ./sections/running
    ./sections/data
    ./sections/workflows_basic
    ./sections/workflows_adv
    ./sections/plugins
    ./sections/bands

Appendices
----------

.. toctree::
   :maxdepth: 1
   :numbered:

   ./appendices/exploring_provenance
   ./appendices/input_validation
   ./appendices/workflow_logic

Acknowledgements
----------------

We are very grateful to the plugin developers for their contributed talks.

The `AiiDA virtual tutorial <http://www.aiida.net/aiida-virtual-tutorial-july-2020/>`__  was made possible by support from the MaX European Centre of Excellence, the swissuniversities P-5 project “Materials Cloud”, the MARVEL National Centre of Competence in Research, the H2020 MARKETPLACE project, the H2020 INTERSECT project and the PASC project.

.. image:: sponsors/max.png
   :target: http://www.max-centre.eu/
   :width: 155px

.. image:: sponsors/swissuniversities.png
   :target: https://swissuniversities.ch
   :width: 135px

.. image:: sponsors/marvel.png
   :target: http://nccr-marvel.ch
   :width: 105px

.. image:: sponsors/marketplace.png
   :target: https://www.the-marketplace-project.eu/
   :width: 145px

.. image:: sponsors/intersect.png
   :target: http://intersect-project.eu/
   :width: 125px

.. image:: sponsors/pasc.png
   :target: https://www.pasc-ch.org/
   :width: 155px
