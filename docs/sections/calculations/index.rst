Calculation processes
=====================

.. rst-class:: header-text

    In this section you can find modules that explain the concepts related to running calculations in AiiDA.

.. rst-class:: center-panel

    .. panels::
        :header: header-text
        :body: bg-light
        :footer: bg-light border-0

        ------
        :column: col-lg-12

        .. link-button:: basics
            :type: ref
            :text: Calculation Basics
            :classes: btn-light text-left stretched-link font-weight-bold
        ^^^^^^^^^^^^

        *"All which is beautiful and noble is the result of reason and calculation."* |br|
        *-- Charles Baudelaire*

        The basic module on calculations covers the two different types of calculation processes, and when to use which.

        +++++++++++++
        |time| 30 min

.. panels::
    :header: header-text
    :body: bg-light
    :footer: bg-light border-0

    ------
    :column: col-lg-6

    .. link-button:: functions
        :type: ref
        :text: Calculation Functions
        :classes: btn-light text-left stretched-link font-weight-bold
    ^^^^^^^^

    *"Form follows function."* |br|
    *-- Louis Sullivan*

    The ``calcfunction`` decorator is an easy way of converting regular Python functions into *calculation functions* that are tracked in the provenance.

    +++
    |time| 15 min

    ---
    :column: col-lg-6

    .. link-button:: calcjobs
        :type: ref
        :text: Calculation Jobs
        :classes: btn-light text-left stretched-link font-weight-bold
    ^^^^^^^^^^^^

    *"It's the job that's never started as takes longest to finish."* |br|
    *-- Samwise Gamgee*

    For more serious tasks that might take longer to finish, we want a more powerful tool.
    The ``CalcJob`` serves this purpose.

    +++++++++++++
    |time| 20 min

    ---
    :column: col-lg-6

    :link-badge:`https://www.youtube.com/watch?v=dQw4w9WgXcQ, "Quantum ESPRESSO",cls=badge-qe text-white,tooltip=Go to the Quantum ESPRESSO version.`

    ---
    :column: col-lg-6

    :link-badge:`https://aiida-quantumespresso.readthedocs.io/en/latest/user_guide/get_started/examples/pw_tutorial.html, "Quantum ESPRESSO",cls=badge-qe text-white,tooltip=Go to the Quantum ESPRESSO version.`
    :link-badge:`https://aiida-vasp.readthedocs.io/en/latest/calculations/vasp.html, "VASP",cls=badge-vasp text-white, tooltip=Go to the VASP version.`

.. toctree::
    :hidden:

    basics
    functions
    calcjobs
