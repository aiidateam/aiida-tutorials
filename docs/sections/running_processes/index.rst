.. _processes:

Running processes
=================

.. rst-class:: header-text

    In this section you can find modules that explain the concepts and steps related to running processes (calculations and workflows) in AiiDA.

.. panels::
    :header: panel-header-text
    :body: bg-light
    :footer: bg-light border-0

    ------
    :column: col-lg-12

    .. link-button:: basics
        :type: ref
        :text: Running calculations
        :classes: btn-light text-left stretched-link font-weight-bold
    ^^^^^^^^^^^^

    This base module will take you through the procedures for running your first calculation job with Quantum ESPRESSO.
    You will learn how to prepare the inputs for the calculation, submit it to the engine, follow its status, and analyze its results.

    +++++++++++++
    .. list-table::
        :widths: 50 50
        :class: footer-table
        :header-rows: 0

        * -
          - :badge:`Quantum ESPRESSO,badge-qe text-white`
        * - |time| 60 min
          - |aiida| :aiida-green:`Basic`

    ---
    :column: col-lg-12

    Alternatives:
    :link-badge:`https://aiida-vasp.readthedocs.io/en/latest/tutorials/fcc_si_step1.html, "VASP",cls=badge-vasp text-white, tooltip=Go to a similar tutorial for the VASP plugin.`

.. panels::
    :header: panel-header-text
    :body: bg-light
    :footer: bg-light border-0

    ------
    :column: col-lg-6

    .. link-button:: errors
        :type: ref
        :text: Troubleshooting
        :classes: btn-light text-left stretched-link font-weight-bold
    ^^^^^^^^^^^^

    This module will highlight some of the common issues that can happen when submitting calculations and how to deal with them.

    +++++++++++++
    .. list-table::
        :widths: 50 50
        :class: footer-table
        :header-rows: 0

        * -
          - :badge:`Quantum ESPRESSO,badge-qe text-white`
        * - |time| 15 min
          - |aiida| :aiida-blue:`Intermediate`

    ------
    :column: col-lg-6

    .. link-button:: workflows
        :type: ref
        :text: Running workflows
        :classes: btn-light text-left stretched-link font-weight-bold
    ^^^^^^^^^^^^

    Once you know how to submit calculations, you can learn how to launch workflows in this module.

    +++++++++++++
    .. list-table::
        :widths: 50 50
        :class: footer-table
        :header-rows: 0

        * -
          - :badge:`Quantum ESPRESSO,badge-qe text-white`
        * - |time| 15 min
          - |aiida| :aiida-blue:`Intermediate`

.. toctree::
    :hidden:

    basics
    errors
    workflows
