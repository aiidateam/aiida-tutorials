.. _BIGMAP_2020_QE:

Quantum ESPRESSO
================

Now that we've covered the basics, let's continue with a quick demo of how AiiDA can make your life easier as a computational scientist.

.. note::

  Throughout this part of the tutorial, we'll be using the ``verdi`` command line interface.
  Here's couple of tricks that will make your life easier:

  * The ``verdi`` command supports **tab-completion**:
    In the terminal, type ``verdi``, followed by a space and press the 'Tab' key twice to show a list of all the available sub commands.
  * For help on ``verdi`` or any of its subcommands, simply append the ``--help/-h`` flag:

    .. code-block:: console

        $ verdi -h

Importing a structure and inspecting it
---------------------------------------

Let's download a structure from the `Crystallography Open Database <http://crystallography.net/cod/>`_ and import it into AiiDA.

.. note::

   You can view the structure `online <http://crystallography.net/cod/9008565.html>`_.

You can download the file and import it with the following two commands:

.. code-block:: console

    $ wget http://crystallography.net/cod/9008565.cif
    $ verdi data structure import ase 9008565.cif

Remember that each piece of data in AiiDA gets a PK number (a "primary key") that identifies it in your database.
This is printed out on the screen by the ``verdi data structure import`` command.
Mark it down, as we are going to use it in the next commands.

.. note::

   In the next commands, replace the string ``<PK>`` with the appropriate PK number.

Let us first inspect the node you just created:

.. code-block:: console

    $ verdi node show <PK>

You will get in output some information on the node, including its type (``StructureData``, the AiiDA data type for storing crystal structures), a label and a description (empty for now, can be changed), a creation time (``ctime``) and a last modification time (``mtime``), the PK of the node and its UUID (universally unique identifier).

.. note::

  **When should I use the PK and when should I use the UUID?**

  A **PK** is a short integer identifying the node and therefore easy to remember.
  However, the same PK number (e.g., PK=10) might appear in two different databases referring to two completely different pieces of data.

  A **UUID** is a hexadecimal string that might look like this::

     d11a4829-3e19-4978-bfcf-c28ddeb0891e

  A UUID has instead the nice feature to be globally unique: even if you export your data and a colleague imports it, the UUIDs will remain the same (while the PKs will typically be different).

  Therefore, use the UUID to keep a long-term reference to a node.
  Feel free to use the PK for quick, everyday use (e.g. to inspect a node).

.. note::

  All AiiDA commands accepting a PK can also accept a UUID. Check this by trying the command before, this time with ``verdi node show <UUID>``.

  Note the following:

  - AiiDA does not require the full UUID, but just the first part of it, as long as only one node starts with the string you provide.
    E.g., in the example above, you could also say ``verdi node show d11a4829-3e19``.
    Most probably, instead, ``verdi node show d1`` will return an error, since most probably you have more than one node starting with the string ``d1``.

  - By default, if what you pass is a valid integer, AiiDA will assume it is a PK; if at least one of the characters is not a digit, then AiiDA will assume it is (the first part of) a UUID.

  - How to solve the issue, then, when the first part of the UUID is composed only by digits (e.g. in ``2495301c-dd00-42d6-92e4-1a8c171bbb4a``)?
    Indeed, using ``verdi node show 24953`` would look for a node with ``PK=24953``.
    As a solution, just add a dash, e.g. ``verdi node show 24953-`` so that AiiDA will consider this as the beginning of the UUID.

  - Note that you can put the dash in any part of the string, and you don't need to respect the typical UUID pattern with 8-4-4-4-12 characters per section: AiiDA will anyway first strip all dashes, and then put them back in the right place, so e.g. ``verdi node show 24-95-3`` will give you the same result as ``verdi node show 24953-``.

  Try to use again ``verdi node show`` on the ``StructureData`` node above, just with the first part of the UUID (that you got from the first call to ``verdi node show`` above).

``StructureData`` can be exported to file in various formats.
As an example, let's export the structure in XSF format and visualize it with XCrySDen:

  .. code-block:: console

    $ verdi data structure export --format=xsf <PK> > exported.xsf
    $ xcrysden --xsf exported.xsf

  You should be visualize to see the Si supercell (8 atoms) that we downloaded from the COD database (in CIF format), imported into AiiDA and exported back into a different format (XSF).

Running a calculation
---------------------

The following short python script sets up a self-consistent field calculation for the Quantum ESPRESSO code:

.. literalinclude:: include/snippets/demo_calcjob.py

Download the :download:`demo_calcjob.py <include/snippets/demo_calcjob.py>` script to your working directory.
It contains a few placeholders for you to fill in:

 #. the VM already has a number of codes preconfigured. Use ``verdi code list`` to find the label for the "PW" code and use it in the script.
 #. replace the PK of the structure with the one you obtained
 #. the VM already contains a number of pseudopotential families. Replace the PP family name with the one for the "SSSP efficiency" library found via ``verdi data upf listfamilies``.

Then submit the calculation using:

.. code-block:: console

    $ verdi run demo_calcjob.py

From this point onwards, the AiiDA daemon will take care of your calculation: creating the necessary input files, running the calculation, and parsing its results.

In order to be able to do this, the AiiDA daemon must be running: to check this, you can run the command:

.. code-block:: console

    $ verdi daemon status

and, if the daemon is not running, you can start it with

.. code-block:: console

    $ verdi daemon start

It should take less than one minute to complete.

Analyzing the outputs of a calculation
--------------------------------------

Let's have a look how your calculation is doing:

.. code-block:: console

   $ verdi process list  # shows only running processes
   $ verdi process list --all  # shows all processes

Again, your calculation will get a PK, which you can use to get more information on it:

.. code-block:: console

   $ verdi process show <PK>

As you can see, AiiDA has tracked all the inputs provided to the calculation, allowing you (or anyone else) to reproduce it later on.
AiiDA's record of a calculation is best displayed in the form of a provenance graph

.. figure:: include/images/demo_calc.png
   :width: 100%

   Provenance graph for a single Quantum ESPRESSO calculation.

You can generate such a provenance graph for any calculation or data in AiiDA by running:

... code-block:: console

  $ verdi node graph generate <PK>

Try to reproduce the figure using the PK of your calculation.

You might wonder what happened under the hood, e.g. where to find the actual input and output files of the calculation.
You will learn more about this later -- until then, here are a few useful commands:

.. code-block:: console

   $ verdi calcjob inputcat <PK>  # shows the input file of the calculation
   $ verdi calcjob outputcat <PK>  # shows the output file of the calculation
   $ verdi calcjob res <PK>  # shows the parsed output

A few questions you could answer using these commands (optional)
 * How many atoms did the structure contain?
   How many electrons?
 * How many k-points were specified? How many k-points were actually computed? Why?
 * How many SCF iterations were needed for convergence?
 * How long did Quantum ESPRESSO actually run (wall time)?

From calculations to workflows
------------------------------

AiiDA can help you run individual calculations but it is really designed to help you run workflows that involve several calculations, while automatically keeping track of the provenance for full reproducibility.

As the final step, we are going to launch the ``PwBandStructure`` workflow of the ``aiida-quantumespresso`` plugin.

.. literalinclude:: include/snippets/demo_bands.py

Download the :download:`demo_bands.py <include/snippets/demo_bands.py>` snippet and run it using

.. code-block:: console

  $ verdi run demo_bands.py

This workflow will:

  #. Determine the primitive cell of the input structure
  #. Run a calculation on the primitive cell to relax both the cell and the atomic positions (``vc-relax``)
  #. Refine the symmetry of the relaxed structure, and find a standardised primitive cell using SeeK-path_
  #. Run a self-consistent field calculation on the refined structure
  #. Run a band structure calculation at fixed Kohn-Sham potential along a standard path between high-symmetry k-points determined by SeeK-path_

The workflow uses the PBE exchange-correlation functional with suitable pseudopotentials and energy cutoffs from the `SSSP library version 1.1 <https://www.materialscloud.org/discover/sssp/table/efficiency>`_.

.. _SeeK-path: https://www.materialscloud.org/work/tools/seekpath

.. K-point mesh is selected to have a minimum k-point density of 0.2 Å-1
   A Marzari-Vanderbilt smearing of 0.02 Ry is used for the electronic occupations

The workflow should take ~10 minutes on your virtual machine.
You may notice that ``verdi process list`` now shows more than one entry.
While you wait for the workflow to complete,
let's start exploring its provenance.

The full provenance graph obtained from ``verdi node graph generate`` will already be rather complex (you can try!),
so let's try browsing the provenance interactively instead.

Start the AiiDA REST API:

.. code-block:: console

  $ verdi restapi

and open the |provenance browser| (from the browser inside the virtual machine).

.. |provenance browser| raw:: html

   <a href="https://www.materialscloud.org/explore/ownrestapi?base_url=http://127.0.0.1:5000/api/v3" target="_blank">Materials Cloud provenance browser</a>

.. note::

   As of September 2019, the Materials Cloud provenance browser is still being developed, so some features might still not be
   available or work as expected.

.. note::

   The provenance browser is a Javascript application that connects to the AiiDA REST API.
   Your data never leaves your computer.

.. some general comment on importance of the graph?
.. a sentence on how to continue from here

Browse your AiiDA database.
 * Start by finding your Quantum ESPRESSO calculation (the type of node is called
   a ``CalcJobNode`` in AiiDA, since it is run as a job on a scheduler).
   Select ``Calculations`` in the left menu to filter for calculations only.
 * Inspect the raw inputs and outputs of the calculation, and use the provenance
   browser to explore the input and output nodes of the calculation and the whole
   provenance of your simulations.

.. note::

     When perfoming calculations for a publication, you can export your provenance graph using ``verdi export create`` and upload it to the `Materials Cloud Archive <https://archive.materialscloud.org/>`_, enabling your peers to explore the provenance of your calculations online.

Once the workchain is finished, use ``verdi process show <PK>`` to inspect the ``PwBandStructureWorkChain`` and find the PK of its ``band_structure`` output.
Use this to produce a PDF of the band structure:

.. code-block:: console

   $ verdi data bands export --format mpl_pdf --output band_structure.pdf <PK>

.. figure:: include/images/si_bands.png
   :width: 80%

   Band structure computed by the ``PwBandStructure`` workchain.

.. note::
   The ``BandsData`` node does contain information about the Fermi energy, so the energy zero in your plot will be arbitrary.
   You can produce a plot with the Fermi energy set to zero (as above) using the following code in a jupyter notebook:

   .. code-block:: ipython

        %matplotlib inline
        import aiida
        aiida.load_profile()

        from aiida.orm import load_node

        scf_params = load_node(<PK>)  # REPLACE with PK of "scf_parameters" output
        fermi_energy = scf_params.dict.fermi_energy

        bands = load_node(<PK>)  # REPLACE with PK of "band_structure" output
        bands.show_mpl(y_origin=fermi_energy, plot_zero_axis=True)

What next?
----------

You now have a first taste of the type of problems AiiDA tries to solve.
Here are some options for how to continue:

* Continue with the :ref:`in-depth tutorial<2020_Intro_Week_Homepage>`.
* Download the `Quantum Mobile`_ virtual machine and try running the tutorial on your laptop instead.
* Try `setting up AiiDA`_ directly on your laptop.

.. _setting up AiiDA: https://aiida.readthedocs.io/projects/aiida-core/en/latest/intro/install_system.html#intro-get-started-system-wide-install
.. _Quantum Mobile: https://github.com/marvel-nccr/quantum-mobile/releases/tag/20.03.1
