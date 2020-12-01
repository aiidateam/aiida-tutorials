.. _BIGMAP_2020_browse:

Browsing your database
======================

This final section of the tutorial is optional, and has the purpose of introducing a couple of ways in which you can browse an AiiDA database.

There are two main reasons you may want to browse a database.
The first one is to get a general idea of the content of it, for which the explore tool of the `Materials Cloud <https://www.materialscloud.org/explore/menu>`_ can be of great use.
The second one is a more specific search with the purpose of gathering more particular and well defined results.
For this second purpose, we recommend direct queries via the ``QueryBuilder``.

.. note::

  Although we introduce them for different purposes, both of these tools can ultimately be used for general exploration or more specific searches.
  Even more, proper knowledge of how to use of the querybuilder may also be essential when creating running scripts and even workflows.

Exploring the database
----------------------

Placeholder for the future content.


Querying the database
---------------------

Copy content here. The note could probably go next to the wget of the database (maybe that part will go before the "exploring" section above).

.. note::

    When perfoming calculations for a publication, you can export your provenance graph (meaning all the content of the nodes and their connections) into an archive file using ``verdi export create``, and then upload it to the `Materials Cloud Archive`_, enabling your peers to explore the provenance of your calculations online.


What next?
----------

You now have a first taste of the type of problems AiiDA tries to solve.
Here are some options for how to continue:

* Continue with the :ref:`in-depth tutorial<2020_Intro_Week_Homepage>`.
* Download the `Quantum Mobile`_ virtual machine and try running the tutorial on your laptop instead.
* Try `setting up AiiDA`_ directly on your laptop.

.. dropdown:: Remember your workchain!

   If you started this section while waiting for you workchain to finish running, remember you still need to obtain the band structure to finish that section!
   Here is the relevant information to do so:

   Once the workchain is finished, use ``verdi process show <PK>`` to inspect the ``PwBandStructureWorkChain`` and find the PK of its ``band_structure`` output.
   Use this to produce a PDF of the band structure:

   .. code-block:: console

     $ verdi data bands export --format mpl_pdf --output band_structure.pdf <PK>

   .. figure:: include/images/si_bands.png
     :width: 80%

     Band structure computed by the ``PwBandStructure`` workchain.


.. _setting up AiiDA: https://aiida.readthedocs.io/projects/aiida-core/en/latest/intro/install_system.html#intro-get-started-system-wide-install
.. _Quantum Mobile: https://github.com/marvel-nccr/quantum-mobile/releases/tag/20.03.1
.. _ngrok: https://ngrok.com/
.. _Quantum ESPRESSO: https://www.quantum-espresso.org/
.. _Materials Cloud Archive: https://archive.materialscloud.org/
