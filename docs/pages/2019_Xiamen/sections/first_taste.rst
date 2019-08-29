A first taste
=============

Let's start with a quick demo of how AiiDA can make your life easier as a computational scientist.

We'll be using the ``verdi`` command-line interface,
which lets you manage your AiiDA installation, inspect the contents of your database,  control running calculations and more.

 * The ``verdi`` command supports **tab-completion**:
   In the terminal, type ``verdi``, followed by a space and press the 'Tab' key twice to show a list of all the available sub commands.
 * For help on ``verdi`` or any of its subcommands, simply append the ``--help/-h`` flag:

   .. code:: bash

       verdi -h

Importing a structure and running a calculation
-----------------------------------------------

Let's download a structure from the `Crystallography Open Database <http://crystallography.net/cod/>`_ and import it into AiiDA:

.. code:: bash

    wget http://crystallography.net/cod/9008565.cif
    verdi data structure import ase 9008565.cif

Each piece of data in AiiDA gets a PK number (and a UUID, more about this later).
The PK allows you to easily reuse a piece of data anywhere in AiiDA.
Remember the PK of the structure, which we will now use to run our first calculation.

.. note::

   You can view the structure either `online <http://crystallography.net/cod/9008565.html>`_
   or use ``jmol 9008565.cif`` locally.

.. Let jason/jianxing test speed of SSH forwarding - potentially mention jupyter

The following short python script sets up a self-consistent field calculation for the Quantum ESPRESSO code:

.. literalinclude:: include/snippets/demo_calcjob.py

Download the :download:`demo_calcjob.py <include/snippets/demo_calcjob.py>` script to your working directory.
It contains a few placeholders for you to fill in:

 #. the VM already has a number of codes preconfigured. Use ``verdi code list`` to find the label for the "PW" code and use it in the script.
 #. replace the PK of the structure with the one you obtained
 #. the VM already contains a number of pseudopotential families. Replace the PP family name with the one for the "SSSP efficiency" library found via ``verdi data upf listfamilies``.

Then submit the calculation using:

.. code:: bash

    verdi run demo_calcjob.py

From this point onwards, the AiiDA daemon will take care of your calculation: creating the input files, running the calculation, and parsing its results.

Analyzing the outputs of a calculation
--------------------------------------

Let's have a look how your calculation is doing:

.. code:: bash

   verdi process list  # shows only running processes
   verdi process list --all  # shows all processes

Again, your calculation will get a PK, which you can use to get more information on it:

.. code:: bash

   verdi process show <PK>

As you can see, AiiDA has tracked all the inputs provided to the calculation, making sure you (or anyone else) will be able to reproduce it.
One way to look inside the inputs themselves is:

.. code:: bash

   verdi calcjob inputcat # (compare with python file)

Once the calculation has finished (should take ~1 min), you can look at the outputs as well:

.. code:: bash

   verdi calcjob outputcat <PK>
   verdi calcjob res <PK>

AiiDA's record of the calculation is best displayed in the form of a provenance graph

.. figure:: include/images/demo_calc.png
   :width: 100%

   Provenance graph for a single Quantum ESPRESSO calculation.

You can generate such a graph for any calculation or data in AiiDA by running:

.. code:: bash

  verdi node graph generate <PK>



Moving to a different computer
------------------------------

Now, this Quantum ESPRESSO calculation ran on your (virtual) machine.
This is fine for tests, but for production calculations you'll typically want to run on a remote compute cluster.
In AiiDA, moving a calculation from one computer to another means changing one line of code.

For the purposes of this tutorial, you'll run on your neighbor's computer.
Ask your neighbor for the IP address of their VM.
Then, download the :download:`neighbor.yml <include/configuration/neighbor.yml>` setup template, replace the placeholder by the IP address and let AiiDA know about this computer by running:

.. .. literalinclude:: include/configuration/neighbor.yml

.. code:: bash

  verdi computer setup --config neighbor.yml

.. note::

    If you're completing this tutorial at a later time and have no partner machine,
    simply use "localhost" instead of the IP address.

AiiDA is now aware of the existence of the computer but you'll still need to let AiiDA
know how to connect to it.
AiiDA does this via `SSH <https://en.wikipedia.org/wiki/Secure_Shell>`_ keys.
Your tutorial VM already contains a private SSH key for connecting to the ``compute`` user of your neighbor's machine,
so all that is left is to configure it in AiiDA.

Download the :download:`neighbor-config.yml <include/configuration/neighbor-config.yml>` configuration template and run:

.. .. literalinclude:: include/configuration/neighbor-config.yml

.. code:: bash

  verdi computer configure ssh neighbor --config neighbor-config.yml --non-interactive

.. note:: Both ``verdi computer setup`` and ``verdi computer configure`` can be used interactively without
  configuration files, which are provided here just to avoid typing errors.

AiiDA should now have access to your neighbor's computer. Let's quickly test this:

.. code:: bash

  verdi computer test neighbor

Finally, let AiiDA know about the **code** we are going to use.
We've again prepared a template that looks as follows:

.. Add template for code
.. literalinclude:: include/configuration/qe.yml

Download the :download:`qe.yml <include/configuration/qe.yml>` code template and run:

.. code:: bash

  verdi code setup --config qe.yml
  verdi code list  # note the label of the new code you just set up!

Now modify the code label in your ``demo_calcjob.py`` script to the label of your new code and simply run another calculation using ``verdi run demo_calcjob.py``.

To see what is going on, AiiDA provides a command that lets you jump to the folder of the directory of the calculation on the remote computer:

.. code:: bash

  verdi process list --all  # get PK of new calculation
  verdi calcjob gotocomputer <PK>

Have a look around. 
 * Do you recognize the different files? 
 * Have a look at the submission script ``_aiidasubmit.sh``.
   Compare it to the submission script of your previous calculation.
   What are the differences?

From calculations to workflows
------------------------------

AiiDA can help you run individual calculations but it is really designed to help you run workflows that involve several calculations, while automatically keeping track of the provenance for full reproducibility.

As the final step, we are going to launch the ``PwBandStructure`` workflow of the ``aiida-quantumespresso`` plugin.

.. literalinclude:: include/snippets/demo_bands.py

Download the :download:`demo_bands.py <include/snippets/demo_bands.py>` snippet and run it using

.. code:: bash

  verdi run demo_bands.py

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

.. code:: bash

  verdi restapi

and open the `Materials Cloud provenance browser <https://www.materialscloud.org/explore/ownrestapi?base_url=http://127.0.0.1:5000/api/v3>`_.

.. note::

  The provenance browser is a Javascript application that connects to the AiiDA REST API.
  Your data never leaves your computer.

.. some general comment on importance of the graph?
.. a sentence on how to continue from here

Browse your AiiDA database.
 * ... Wait for Snehal/Elsa to add Workflows capability before completing this

What next?
----------

You now have a first taste of the type of problems AiiDA tries to solve.
Here are some options for how to continue:

 * Continue with the in-depth tutorial and learn more about the ``verdi``, ``verdi shell`` and ``python`` interfaces to AiiDA.
   There is more than enough material to keep you busy for a day.
 * Download `Quantum Mobile`_ virtual machine and try running the tutorial on your laptop instead. This will let you take the materials home and continue in your own time.
 * Try `setting up AiiDA directly on your laptop <https://aiida-core.readthedocs.io/en/latest/install/quick_installation.html>`_.

   .. note:: **For advanced Linux & python users only**.
     AiiDA depends on a number of services and software that require some skill to set up. 
     Unfortunately, we don't have the human resources to help you solve
     issues related to your setup in a tutorial context.
     
 * Continue your work from other parts of the workshop, chat with participants and enjoy yourself :-)


 .. _Quantum Mobile: https://github.com/marvel-nccr/quantum-mobile/releases/tag/19.08.0
