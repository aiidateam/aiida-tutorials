Fundamentals
============

.. rst-class:: header-text

    Here we explain the fundamental AiiDA concepts and tools that are every user should first master.
    Once you have completed the modules on this page, you are free to start exploring the functionality of AiiDA in the other tutorial sections.

.. rst-class:: center-panel

    .. panels::
        :body: bg-light
        :header: panel-header-text
        :footer: bg-light border-0

        ------
        :column: col-lg-12

        .. link-button:: basics
            :type: ref
            :text: AiiDA Basics
            :classes: btn-light text-left stretched-link font-weight-bold
        ^^^^^^^^^^^^

        *"The secret to getting ahead is getting started."* |br|
        *-- Mark Twain*

        The basic AiiDA tutorial covers the concept of provenance, and gives a short introduction to data nodes, calculations and workflows.

        +++++++++++++
        .. list-table::
            :widths: 50 50
            :class: footer-table
            :header-rows: 0

            * - |time| 30 min
              - Basic


.. panels::
    :body: bg-light
    :header: panel-header-text
    :footer: bg-light border-0

    ------
    :column: col-lg-6

    .. link-button:: querying
        :type: ref
        :text: Querying
        :classes: btn-light text-left stretched-link font-weight-bold
    ^^^^^^^^

    *"They call me the seeker."* |br|
    *-- Roger Daltrey, The Who*

    One of the main features of AiiDA is that all your data is stored in a linked graph via the provenance. Here we explain how to query your database using the links in this graph, as well as other ticks and tips.

    +++
    .. list-table::
        :widths: 50 50
        :class: footer-table
        :header-rows: 0

        * - |time| 45 min
          - Basic

    ---
    :column: col-lg-6

    .. link-button:: entry_points
        :type: ref
        :text: Entry Points
        :classes: btn-light text-left stretched-link font-weight-bold
    ^^^^^^^^^^^^

    *"Hodor!"* |br|
    *-- Hodor*

    Entry points are the identifier of each node or calculation type, and are a very important concept for understanding how to use the extensibility of AiiDA.

    +++++++++++++
    .. list-table::
        :widths: 50 50
        :class: footer-table
        :header-rows: 0

        * - |time| 30 min
          - Basic

    ---
    :column: col-lg-6

    :link-badge:`https://aiida-tutorials.readthedocs.io/en/tutorial-2020-intro-week/source/sections/data.html, "Quantum ESPRESSO",cls=badge-danger text-white,tooltip=Go to the Quantum ESPRESSO version.`


.. toctree::
    :hidden:

    Basics <basics>
    entry_points
    querying
