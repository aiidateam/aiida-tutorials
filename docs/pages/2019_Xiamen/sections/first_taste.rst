A first taste
=============

We're going to start with a quick demo of a few ways of how AiiDA can make your life easier as a computational scientist.

We'll be using the ``verdi`` command-line interface (CLI),
which lets you manage your AiiDA installation, inspect the contents of your database,  control running calculations and more.

 * The ``verdi`` command supports **tab-completion**:
   In the terminal, type ``verdi``, followed by a space and press the 'Tab' key twice to show a list of all the available sub commands.
 * For help on ``verdi`` or any of its subcommands, simply append the ``--help/-h`` flag:

   .. code:: bash

       verdi -h

For more details on ``verdi`` see `AiiDA's documentation <https://aiida-core.readthedocs.io/en/latest/verdi/verdi_user_guide.html>`_.


Importing a structure and running a calculation
-----------------------------------------------

Let's download a structure from the Crystallography Open Database and import it into AiiDA:

.. code:: bash

    wget http://crystallography.net/cod/9008565.cif
    verdi data structure import ase 9008565.cif

Each piece of data in AiiDA gets a PK number and a UUID.
These identifiers allow you to easily reuse a piece of data anywhere in AiiDA.
Remember the PK of the structure, which we will now use to run our first calculation.

.. note::

   You can view the structure either `online <http://crystallography.net/cod/9008565.html>`_
   or use ``jsmol 9008565.cif`` locally.

.. Let jason/jianxing test speed of SSH forwarding - potentially mention jupyter

The following short python script :download:`demo_calcjob.py <include/snippets/demo_calcjob.py>` contains a few placeholders for you to fill in:

.. literalinclude:: include/snippets/demo_calcjob.py

Copy the ``demo_calcjob.py`` script to your working directory and replace the placeholders.
Then submit the calculation using:

.. code:: bash

    verdi run demo_calcjob.py

From this point onwards, the AiiDA daemon will take care of your calculation.

Analyzing the outputs of a calculation
--------------------------------------

.. code:: bash

   verdi process list
   verdi calcjob inputcat # (compare with python file)
   verdi process list -a
   verdi calcjob outputcat
   verdi calcjob res

Provenance

.. code:: bash

   verdi node show

.. + put  pdf in web site + point out that this makes it reproducible)

Moving to a different computer
------------------------------

Now, this Quantum ESPRESSO calculation ran on your (virtual) machine, which was already pre-configured in AiiDA.
This works fine for test calculations but for production runs you'll need to run on a compute cluster.

For the purposes of this tutorial, you'll run on your neighbor's computer.
ask IP address of your neighbor

.. Add template to download (they just need to replace IP address


.. literalinclude:: include/configuration/neighbor.yml


.. note::

    If you're completing this tutorial at a later time and have no partner machine,
    simply use "localhost" instead.

.. literalinclude:: include/configuration/neighbor-config.yml

.. code:: bash

  verdi computer setup --config neighbor.yml
  verdi computer configure ssh neighbor --config neighbor-config.yml --non-interactive
  verdi computer test

.. Add template for code
.. literalinclude:: include/configuration/qe.yml

.. code:: bash

  verdi code setup
  verdi code list

Now, modify the code label in your ``demo_calcjob.py`` script to use your newly set up code
and run it again.

.. code:: bash

  verdi process list


To see what is going on, AiiDA provides a command that lets you jump to the folder of the 
calculation on the remote computer:

.. code:: bash

  verdi calcjob gotocomputer

Have a look at the submission script ``...sh``.
Notice the SLURM directives.

From calculations to workflows
------------------------------

AiiDA can help you run individual calculations but AiiDA is really designed to
help you run workflows that involve several calculations, while automatically
keeping track of the provenance for full reproducibility.

As the final step, we're going to launch the ``PwBandStructure`` workflow of the ``aiida-quantumespresso`` plugin.

.. Add another python snippet

.. code:: bash

  verdi run demo_bands.py
  verdi process list

This workflow will:

  #. Determine the primitive cell of the input structure
  #. Run a calculation on the primitive cell to relax both the cell and the atomic positions (``vc-relax``)
  #. Refine the symmetry of the relaxed structure, and find a standardised primitive cell using 2019_xmn_seekpath_.
  #. Run a self-consistent field calculation on the refined structure
  #. Run a band structure calculation at fixed Kohn-Sham potential along a standard path between high-symmetry k-points determined by 2019_xmn_seekpath_.

The workflow uses the PBE exchange-correlation functional with suitable pseudopotentials and energy cutoffs from the `SSSP library version 1.1 <https://www.materialscloud.org/discover/sssp/table/efficiency>`_


.. _2019_xmn_seekpath: https://www.materialscloud.org/work/tools/seekpath

.. K-point mesh is selected to have a minimum k-point density of 0.2 Å-1
.. A Marzari-Vanderbilt smearing of 0.02 Ry is used for the electronic occupations

 will take ~X minutes on your virtual machine.

While you wait for the workflow to complete (it should take ~X minutes on your virtual machine), 
let's have a look at the provenance generated:

.. Add figure with provenance generated

Once your workflow is completed, you can generate such a graph using

.. code:: bash

  verdi graph generate ...

You can also browse your provenance graph interactively using the `Materials Cloud provenance browser <https://www.materialscloud.org/explore/connect?...`.

.. note::

  The provenance browser is a Javascript application that connects to the AiiDA REST API,
  which is already running as a system service on the tutorial VMs.
  In other contexts you can always start it with ``verdi restapi``

.. some general comment on importance of the graph?
.. a sentence on how to continue from here

