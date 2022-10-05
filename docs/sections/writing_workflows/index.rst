Writing workflows
=================

.. rst-class:: header-text

    A workflow in AiiDA is a process that can call other workflows and calculations to encode the logic of a typical scientific workflow.
    Currently, there are two ways of implementing a workflow process: work *functions* and work *chains*.
    In this section you will learn how to write both, as well as deal with more advanced topics such as debugging, input validation and error handling.

.. panels::
    :header: panel-header-text
    :body: bg-light
    :footer: bg-light border-0

    ------
    :column: col-lg-12

    .. link-button:: workfunction
        :type: ref
        :text: Work functions
        :classes: btn-light text-left stretched-link font-weight-bold
    ^^^^^^^^^^^^

    A short module on how to write the basic type of workflows in AiiDA: work functions.
    The module also revises the usage of calculation functions to add simple Python functions to the provenance.

    +++++++++++++
    .. list-table::
        :widths: 50 50
        :class: footer-table
        :header-rows: 0

        * - |time| 30 min
          - |aiida| :aiida-green:`Basic`

.. panels::
    :header: panel-header-text
    :body: bg-light
    :footer: bg-light border-0

    ------
    :column: col-lg-12

    .. link-button:: workchain
        :type: ref
        :text: Work chains
        :classes: btn-light text-left stretched-link font-weight-bold
    ^^^^^^^^^^^^

    A step-by-step introduction to the basics of writing work chains in AiiDA.
    After completing this module, you will be ready to start writing your own scientific workflows!

    +++++++++++++
    .. list-table::
        :widths: 50 50
        :class: footer-table
        :header-rows: 0

        * - |time| 60 min
          - |aiida| :aiida-green:`Basic`

.. panels::
    :header: panel-header-text
    :body: bg-light
    :footer: bg-light border-0

    ------
    :column: col-lg-6

    .. link-button:: debugging
        :type: ref
        :text: Debugging work chains
        :classes: btn-light text-left stretched-link font-weight-bold
    ^^^^^^^^^^^^

    When writing your own work chain, things are bound to go wrong!
    Here we list some common issues with AiiDA work chains, what to expect, and how to debug them.

    +++++++++++++
    .. list-table::
        :widths: 50 50
        :class: footer-table
        :header-rows: 0

        * - |time| 30 min
          - |aiida| :aiida-green:`Basic`

    ------
    :column: col-lg-6

    .. link-button:: realworld
        :type: ref
        :text: A Real-world example - Equation of state
        :classes: btn-light text-left stretched-link font-weight-bold
    ^^^^^^^^^^^^

    A fully explained real-world work chain implemented in AiiDA, that can be used an example to start writing your own work chain.

    +++++++++++++
    .. list-table::
        :widths: 50 50
        :class: footer-table
        :header-rows: 0

        * -
          - :badge:`Quantum ESPRESSO,badge-qe text-white`
        * - |time| 45 min
          - |aiida| :aiida-blue:`Intermediate`


.. panels::
    :header: panel-header-text
    :body: bg-light
    :footer: bg-light border-0

    ------
    :column: col-lg-6

    .. link-button:: https://aiida.readthedocs.io/projects/aiida-core/en/latest/howto/write_workflows.html#extending-workflows
        :type: url
        :text: Extending work chains
        :classes: btn-light text-left stretched-link font-weight-bold
    ^^^^^^^^^^^^

    Work chains are designed to be modular and reusable.
    This how-to *from the AiiDA documentation* explains how to efficiently extend our work chains.

    +++++++++++++
    .. list-table::
        :widths: 50 50
        :class: footer-table
        :header-rows: 0

        * - |time| 30 min
          - |aiida| :aiida-blue:`Intermediate`

    ------
    :column: col-lg-6

    .. link-button:: errors
        :type: ref
        :text: Dealing with errors
        :classes: btn-light text-left stretched-link font-weight-bold
    ^^^^^^^^^^^^

    This module explains how to deal with errors in AiiDA workflows, and how to automatically recover from issues that occur for your calculations.

    +++++++++++++
    .. list-table::
        :widths: 50 50
        :class: footer-table
        :header-rows: 0

        * - |time| 60 min
          - |aiida| :aiida-orange:`Advanced`


.. panels::
    :header: panel-header-text
    :body: bg-light
    :footer: bg-light border-0

    ------
    :column: col-lg-6

    .. link-button:: https://filedn.com/lsOzB8TTUIDz2WkFj8o6qhp/memes/mossfire.gif
        :type: url
        :text: Input validation
        :classes: btn-light text-left stretched-link font-weight-bold
    ^^^^^^^^^^^^

    **Under construction** 🔨

    Here we explain how to write a *validator* that can check inputs before running a calculation or workflow.

    +++++++++++++
    .. list-table::
        :widths: 50 50
        :class: footer-table
        :header-rows: 0

        * - |time| 20 min
          - |aiida| :aiida-blue:`Intermediate`

.. toctree::
    :hidden:

    workfunction
    workchain
    debugging
    realworld
    validation
    errors
