.. _BIGMAP_2020_QE:

Quantum ESPRESSO
================

Now that we've covered the basics, let's continue with a quick demo of how AiiDA can make your life easier as a computational scientist.

Importing a structure and inspecting it
---------------------------------------

Let's download a structure from the `Crystallography Open Database <http://crystallography.net/cod/>`_ and import it into AiiDA.

.. note::

    You can also view the structure online `here <http://crystallography.net/cod/9008565.html>`_.

First, download the file and from the COD with ``wget``:

.. code-block:: console

    $ wget http://crystallography.net/cod/9008565.cif
    --2020-11-25 11:32:32--  http://crystallography.net/cod/9008565.cif
    Resolving crystallography.net (crystallography.net)... 158.129.170.82
    Connecting to crystallography.net (crystallography.net)|158.129.170.82|:80... connected.
    HTTP request sent, awaiting response... 200 OK
    Length: 4948 (4.8K) [chemical/x-cif]
    Saving to: ‘9008565.cif’

    9008565.cif          100%[=====================>]   4.83K  --.-KB/s    in 0s

    2020-11-25 11:32:32 (351 MB/s) - ‘9008565.cif’ saved [4948/4948]

Next, you can import it with the ``verdi`` CLI.

.. code-block:: console

    $ verdi data structure import ase 9008565.cif
      Successfully imported structure Si8 (PK = 208)

Remember that each piece of data in AiiDA gets a PK number (a "primary key") that identifies it in your database.
This is printed out on the screen by the ``verdi data structure import`` command.
It's a good idea to mark it down, but should you forget, you can always have a look at the structures in the database using:

.. code-block:: console

    $ verdi data structure list
      Id  Label    Formula
    ----  -------  ---------
     208           Si8

    Total results: 1

.. important::

    Throughout this section, remember to replace the string ``<PK>`` with the appropriate PK number.

Let us first inspect the node you just created:

.. code-block:: console

    $ verdi node show <PK>
    Property     Value
    -----------  ------------------------------------
    type         StructureData
    pk           208
    uuid         434ed140-ba67-4dc3-9537-1794012fb827
    label
    description
    ctime        2020-11-25 10:32:48.878762+00:00
    mtime        2020-11-25 10:32:48.894992+00:00

You can see some information on the node, including its type (``StructureData``, the AiiDA data type for storing crystal structures), a label and a description (empty for now, can be changed), a creation time (``ctime``) and a last modification time (``mtime``), the PK of the node and its UUID (universally unique identifier).

``StructureData`` can be exported from the database to a file in various formats.
As an example, let's export the structure in XSF format of `XCrySDen`_:

.. code-block:: console

    $ verdi data structure export --format=xsf <PK> > exported.xsf

You can copy the file to your local machine and open it with `XCrySDen`_, or simply have a look at the structure using ASE's `visualization tools`_ with:

.. code-block:: console

    $ verdi data structure show <PK>

This can take some time due to the X forwarding, but after a while you should be able to see the Si supercell (8 atoms) that we downloaded from the COD database (in CIF format), imported into AiiDA and exported back into a different format (XSF).

Running a calculation
---------------------

The following short Python script sets up a self-consistent field calculation for the `Quantum ESPRESSO`_ code:

.. literalinclude:: include/snippets/demo_calcjob.py

Download the :download:`demo_calcjob.py <include/snippets/demo_calcjob.py>` script to your working directory.

**Exercise:** The ``demo_calcjob.py`` script contains a few placeholders for you to fill in:

    #. the VM already has a number of codes preconfigured. Use ``verdi code list`` to find the label for the `pw.x` code and replace ``<CODE LABEL>`` in the script.
    #. replace ``<STRUCTURE PK>`` with the PK of the structure you imported.
    #. the VM already contains a number of pseudopotential families. Replace ``<PP FAMILY>`` with the one for the "SSSP efficiency" library found via ``verdi data upf listfamilies``.

Finally, submit the calculation using:

.. code-block:: console

    $ verdi run demo_calcjob.py
    Submitted CalcJob with PK=211

From this point onwards, the AiiDA daemon will take care of your calculation: creating the necessary input files, running the calculation, and parsing its results.

In order to be able to do this, the AiiDA daemon must of course be running: to check this, you can run the command:

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

    $ verdi process list -a
      PK  Created    Process label             Process State    Process status
    ----  ---------  ------------------------  ---------------  ----------------
     185  2h ago     multiply                  ⏹ Finished [0]
     189  2h ago     ArithmeticAddCalculation  ⏹ Finished [0]
     194  2h ago     ArithmeticAddCalculation  ⏹ Finished [0]
     201  2h ago     MultiplyAddWorkChain      ⏹ Finished [0]
     202  2h ago     multiply                  ⏹ Finished [0]
     204  2h ago     ArithmeticAddCalculation  ⏹ Finished [0]
     211  47s ago    PwCalculation             ⏹ Finished [0]

    Total results: 7

    Info: last time an entry changed state: 12s ago (at 12:28:25 on 2020-11-25)

Once again you can use the PK of the calculation to get more information on it:

.. code-block:: console

    $ verdi process show <PK>
    Property     Value
    -----------  ------------------------------------
    type         PwCalculation
    state        Finished [0]
    pk           211
    uuid         6dd985a9-be25-405d-830b-6dd41d06b820
    label
    description
    ctime        2020-11-25 12:27:50.675531+00:00
    mtime        2020-11-25 12:28:26.051858+00:00
    computer     [1] localhost

    Inputs      PK    Type
    ----------  ----  -------------
    pseudos
        Si      95    UpfData
    code        3     Code
    kpoints     210   KpointsData
    parameters  209   Dict
    structure   208   StructureData

    Outputs              PK  Type
    -----------------  ----  --------------
    output_band         214  BandsData
    output_parameters   216  Dict
    output_trajectory   215  TrajectoryData
    remote_folder       212  RemoteData
    retrieved           213  FolderData

As you can see, AiiDA has tracked all the inputs provided to the calculation, allowing you (or anyone else) to reproduce it later on.
AiiDA's record of a calculation is best displayed in the form of a provenance graph:

.. figure:: include/images/demo_calc.png
    :width: 100%

    Provenance graph for a single `Quantum ESPRESSO`_ calculation.

Try to reproduce the figure using the PK of your calculation based on what you learned `in the basics section <BIGMAP_2020_Basics:calcfunction:graph>`_.

Let's have a look at one of the outputs: the ``output_parameters``.
You can get the contents of this dictionary easily using the ``verdi shell``:

.. code-block:: ipython

    In [1]: node = load_node(232)

    In [2]: d = node.get_dict()

    In [3]: d['energy']
    Out[3]: -1242.9739990626

Moreover, you can also easily access the input and output files of the calculation using the ``verdi`` CLI:

.. code-block:: console

    $ verdi calcjob inputls <PK>     # Shows the list of input files
    $ verdi calcjob inputcat <PK>    # Shows the input file of the calculation
    $ verdi calcjob outputls <PK>    # Shows the list of output files
    $ verdi calcjob outputcat <PK>   # Shows the output file of the calculation
    $ verdi calcjob res <PK>         # Shows the parser results of the calculation

**Exercise:** A few questions you could answer using these commands (optional):

    * How many atoms did the structure contain? How many electrons?
    * How many k-points were specified? How many k-points were actually computed? Why?
    * How many SCF iterations were needed for convergence?
    * How long did `Quantum ESPRESSO`_ actually run (wall time)?

From calculations to workflows
------------------------------

AiiDA can help you run individual calculations but it is really designed to help you run workflows that involve several calculations, while automatically keeping track of the provenance for full reproducibility.

As the final step, we are going to launch the ``PwBandStructure`` workflow of the ``aiida-quantumespresso`` plugin.

.. literalinclude:: include/snippets/demo_bands.py

Download the :download:`demo_bands.py <include/snippets/demo_bands.py>` snippet and run it using

.. code-block:: console

    $ verdi run demo_bands.py

This workflow will:

    #. Determine the primitive cell of the input structure.
    #. Run a calculation on the primitive cell to relax both the cell and the atomic positions (``vc-relax``).
    #. Refine the symmetry of the relaxed structure, and find a standardised primitive cell using SeeK-path_.
    #. Run a self-consistent field calculation on the refined structure.
    #. Run a band structure calculation at fixed Kohn-Sham potential along a standard path between high-symmetry k-points determined by SeeK-path_.

The workflow uses the PBE exchange-correlation functional with suitable pseudopotentials and energy cutoffs from the `SSSP library version 1.1 <https://www.materialscloud.org/discover/sssp/table/efficiency>`_.

.. K-point mesh is selected to have a minimum k-point density of 0.2 Å-1
   A Marzari-Vanderbilt smearing of 0.02 Ry is used for the electronic occupations

The workflow should take ~10 minutes on your virtual machine.
You may notice that ``verdi process list`` now shows more than one entry:

.. code-block:: console

    $ verdi process list
      PK  Created    Process label             Process State    Process status
    ----  ---------  ------------------------  ---------------  --------------------------------------
     218  6s ago     PwBandStructureWorkChain  ⏵ Waiting        Waiting for child processes: 233
     233  4s ago     PwBandsWorkChain          ⏵ Waiting        Waiting for child processes: 235
     235  3s ago     PwRelaxWorkChain          ⏵ Waiting        Waiting for child processes: 238
     238  2s ago     PwBaseWorkChain           ⏵ Waiting        Waiting for child processes: 244
     244  1s ago     PwCalculation             ⏵ Waiting        Monitoring scheduler: job state QUEUED

    Total results: 5

    Info: last time an entry changed state: 0s ago (at 12:45:40 on 2020-11-25)

While you wait for the workflow to complete, let's start exploring its provenance.

The full provenance graph obtained from ``verdi node graph generate`` will already be rather complex (you can try!), so let's try browsing the provenance interactively instead.

Start the AiiDA REST API:

.. code-block:: console

    $ verdi restapi

and open the |provenance browser|.

.. |provenance browser| raw:: html

    <a href="https://www.materialscloud.org/explore/ownrestapi?base_url=http://127.0.0.1:5000/api/v4" target="_blank">Materials Cloud provenance browser</a>

.. note::

    The provenance browser is a Javascript application that connects to the AiiDA REST API.
    Your data never leaves your computer.

.. some general comment on importance of the graph?
.. a sentence on how to continue from here

Browse your AiiDA database:

    * Start by finding your `Quantum ESPRESSO`_ calculation (the type of node is called a ``CalcJobNode`` in AiiDA, since it is run as a job on a scheduler).
    * Select ``Calculations`` in the left menu to filter for calculations only.
    * Inspect the raw inputs and outputs of the calculation, and use the provenance browser to explore the input and output nodes of the calculation and the whole provenance of your simulations.

.. note::

    When perfoming calculations for a publication, you can export your provenance graph (meaning all the content of the nodes and their connections) into an archive file using ``verdi export create``, and then upload it to the `Materials Cloud Archive`_, enabling your peers to explore the provenance of your calculations online.

Once the workchain is finished, use ``verdi process show <PK>`` to inspect the ``PwBandStructureWorkChain`` and find the PK of its ``band_structure`` output.
Use this to produce a PDF of the band structure:

.. code-block:: console

   $ verdi data bands export --format mpl_pdf --output band_structure.pdf <PK>

.. figure:: include/images/si_bands.png
   :width: 100%

   Band structure computed by the ``PwBandStructureWorkChain``.

.. note::
   The ``BandsData`` node does contain information about the Fermi energy, so the energy zero in your plot will be arbitrary.
   You can produce a plot with the Fermi energy set to zero (as above) using the following steps in the ``verdi shell``.
   Just look for the ``scf_parameters`` and ``band_structure`` output nodes of the ``PwBandStructureWorkChain`` using ``verdi process show`` and replace them in the following code:

   .. code-block:: ipython

        In [1]: scf_params = load_node(<PK>)  # PK of the `scf_parameters` node
           ...: fermi_energy = scf_params.dict.fermi_energy
           ...: bands = load_node(<PK>)  # PK of the `band_structure` node
           ...: bands.show_mpl(y_origin=fermi_energy, plot_zero_axis=True)



What next?
----------

You now have a first taste of the type of problems AiiDA tries to solve.
Here are some options for how to continue:

* Continue with the :ref:`in-depth tutorial<2020_Intro_Week_Homepage>`.
* Download the `Quantum Mobile`_ virtual machine and try running the tutorial on your laptop instead.
* Try `setting up AiiDA`_ directly on your laptop.

.. Links

.. _setting up AiiDA: https://aiida.readthedocs.io/projects/aiida-core/en/latest/intro/install_system.html#intro-get-started-system-wide-install
.. _Quantum Mobile: https://github.com/marvel-nccr/quantum-mobile/releases/tag/20.03.1
.. _visualization tools: https://wiki.fysik.dtu.dk/ase/ase/visualize/visualize.html
.. _XCrySDen: http://www.xcrysden.org/
.. _Quantum ESPRESSO: https://www.quantum-espresso.org/
.. _SeeK-path: https://www.materialscloud.org/work/tools/seekpath
.. _Materials Cloud Archive: https://archive.materialscloud.org/
