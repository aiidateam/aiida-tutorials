Verdi command line
==================

This part of the tutorial will help to familiarize you with the
command-line utility ``verdi``, one of the most common ways to interact
with AiiDA. ``verdi`` with its subcommands enables a variety of
operations such as inspecting the status of ongoing or terminated
calculations, showing the details of calculations, computers, codes, or
data structures, access the input and the output of a calculation, etc.
Similar to the ``bash`` shell, verdi command support Tab completion. Try
right now to type ``verdi``, followed by a space, in a terminal and tap
Tab twice to have a list of subcommands. Whenever you need the
explanation of any command add ``--help/-h`` flag in front it. Finally,
fields enclosed in angular brackets, such as ``<pk>``, are placeholders
to be replaced by the actual value of that field (an integer, a string
etc...).

The list of processes
---------------------

Let us try our first ``verdi`` commands. Type in the terminal

.. code:: console

    verdi process list

(Note: the first time you run this command, it might take a few seconds
as it is the first time you are accessing the database in the virtual
machine. Subsequent calls will be faster). This will print the list of
ongoing processes (calculations or workchains), which should be empty.
The first output line should look like

.. code:: console

    PK    Created    State    Process label    Process status
    ----  ---------  -------  ---------------  ----------------
    
    Total results: 0
    
    Info: last time an entry changed state: never

In order to print a list with all processes that finished correctly
in the AiiDA database, you can use the ``-S/--process-state`` flag as follows:

.. code:: console

    verdi process list --process-state finished

Another very typical option combination allows to get processes in
*any* state (flag ``-a/--all``) generated in the past ``NUM`` days
(``-p/--past-days <NUM>``): e.g., for process in the past 1 day:
``verdi process list -p1 -a``. Each row of the output identifies a process and shows some
information about it. For a more detailed list of properties, choose one
row by noting down its PK (primary key) number (first column of the
output) and type in the terminal

.. code:: console

    verdi process show <pk>

The output depends on the specific pk chosen and should inform you about
the input nodes (e.g. pseudopotentials, kpoints, initial structure,
etc.), and output nodes (e.g. output structure, output parameters,
etc.).

**PKs/IDs vs. UUIDs**: Beside the (integer) PK, very convenient to
reference a calculation or data node in your database, every node has a
UUID (Universally Unique ID) to identify it, that is preserved even when
you share some nodes with coworkers—while the PK will most likely
change. You can see the UUID in the output of ``verdi process show``
or ``verdi node show``. Moreover, if you have already a UUID and you
want to get the corresponding PK in your database, you can use
``verdi node show <UUID>``, as we are going to do now.

Let us now consider the node with
``UUID = ce81c420-7751-48f6-af8e-eb7c6a30cec3``, which identifies a
relaxation of a BaTiO\ :sub:`3` unit cell run with Quantum Espresso ``pw.x``.
You can check the information on this node and get the PK with:

.. code:: console

    Property       Value
    -------------  ------------------------------------
    type           CalcJobNode
    pk             17
    uuid           ce81c420-7751-48f6-af8e-eb7c6a30cec3
    label
    description
    ctime          2019-04-18 10:51:16.710803+00:00
    mtime          2019-04-18 10:51:51.012617+00:00
    process state  Finished
    exit status    0
    computer       [1] localhost-direct
    
    Called by      PK  Type
    -----------  ----  -------------
    CALL_CALC       4  WorkChainNode
    
    Inputs         PK    Type
    -------------  ----  -------------
    pseudos
        Ba         26    UpfData
        O          27    UpfData
        Ti         1     UpfData
    code           10    Code
    kpoints        16    KpointsData
    parameters     15    Dict
    parent_folder  9     RemoteData
    settings       14    Dict
    structure      3     StructureData
    
    Outputs              PK  Type
    -----------------  ----  --------------
    output_band          23  BandsData
    output_parameters    22  Dict
    output_structure     20  StructureData
    output_trajectory    21  TrajectoryData
    remote_folder        18  RemoteData
    retrieved            19  FolderData

*Keep in mind that you can also use just a part (beginning) of the UUID,
as long as it is unique, to show the node information information.* For
example, to display the above information, you could also type
``verdi node show ce81c420``. In what follows, we are going to
mention only the prefixes of the UUIDs since they are sufficient to
identify the correct node.

A typical AiiDA graph
---------------------

AiiDA stores inputs required by a calculation as well as the its outputs
in the database. These objects are connected in a graph that looks like
:numref:`fig_graph_input_only`. We suggest that you have a look to the figure before
going ahead.

.. _fig_graph_input_only:
.. figure:: include/images/verdi_graph/batio3/graph-inputonly.png 
   :width: 100%

   Graph with all inputs (data, circles; and code, diamond) to
   the Quantum Espresso calculation (square) that you will create in
   :ref:`calculations` section of this tutorial. 
   
.. figure:: include/images/verdi_graph/batio3/graph-full.png 
   :width: 100%

   Same as above, but also with the outputs that the daemon will create and
   connect automatically.
   The RemoteData node is created during submission and can be thought as a
   symbolic link to the remote folder in which the calculation runs on the
   cluster. The other nodes are created when the calculation has finished,
   after retrieval and parsing. The node with linkname “retrieved” contains
   the raw output files stored in the AiiDA repository; all other nodes are
   added by the parser. Additional nodes (symbolized in gray) can be added
   by the parser (e.g., an output StructureData if you performed a
   relaxation calculation, a TrajectoryData for molecular dynamics, …).

You can create a similar graph for any calculation node by using the
utility ``verdi graph generate <pk>/<uuid>``. For example, before you obtained
information (in text form) for ``UUID = ce81c420``. To visualize similar
information in graph(ical) form, run (replacing ``<pk>`` or ``<uuid>`` with the PK or UUID
of the node respectively):

.. code:: console

    verdi graph generate <pk>/<uuid>

This command will create the file ``<pk>.dot`` that can be rendered by
means of the utility ``dot``. If you now type

.. code:: console

    dot -Tpdf -o <pk>.pdf <pk>.dot

you will create a pdf file ``<pk>.pdf``. You can open this file on the
Amazon machine by using ``evince`` or, if you feel that the ssh
connection is too slow, copy it via ``scp`` to your local machine. To do
so, if you are using Linux/Mac OS X, you can type in your *local*
machine:

.. code:: console

    scp aiidatutorial:<path_with_the_graph_pdf> <local_folder>

and then open the file. Alternatively, you can use graphical software to
achieve the same, for instance: WinSCP on Windows, Cyberduck on the Mac,
or the “Connect to server” option in the main menu after clicking on the
desktop for Ubuntu.

Spend some time to familiarize yourself with the graph structure. Choose
the root node (highlighted in blue) and trace back the parent
calculation which produced the structure used as an input. This is an
example of a Quantum ESPRESSO pw.x calculation, where the input
structure was actually obtained as the output of a previous calculation.
We will now inspect the different elements of this graph.

Inspecting the nodes of a graph
-------------------------------

Dict and CalcJobNode
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Now, let us have a closer look at the some of the nodes appearing in the
graph. Choose the node of the type ``Dict`` with input link
name ``parameters`` (to double check, it should have UUID ``d1bbe1ea``)
and type in the terminal:

.. code:: console

    verdi data dict show <pk>

A ``Dict`` contains a dictionary (i.e., key–value pairs),
stored in the database in a format ready to be queried (we will learn
how to run queries later on in this tutorial). The command above will
print the content dictionary, containing the parameters used to define
the input file for the calculation. You can compare the dictionary with
the content of the raw input file to Quantum ESPRESSO (that was
generated by AiiDA) via the command

.. code:: console

    verdi calcjob inputcat <pk>

where you substitute the pk of the calculation node. Check the
consistency of the parameters written in the input file and those stored
in the ``Dict`` node. Even if you don’t know the meaning of the
input flags of a Quantum ESPRESSO calculation, you should be able to see
how the input dictionary has been converted to Fortran namelists.

The previous command just printed the content of the “default” input
file ``aiida.in``. To see a list of all the files used to run a
calculation (input file, submission script, etc.) instead type

.. code:: console

    verdi calcjob inputls <pk>

(Adding a ``--color`` flag allows you to easily distinguish files from
folders by a different coloring).

Once you know the name of the file you want to visualize, you can call
the ``verdi calcjob inputcat [PATH]`` command specifying the path. For
instance, to see the submission script, you can do:

.. code:: console

    verdi calcjob inputcat <pk> _aiidasubmit.sh

StructureData
~~~~~~~~~~~~~

Now let us focus on StructureData objects, representing a crystal
structure. We can consider for instance the input structure to the
calculation we were considering before (it should have UUID prefix
``3a4b1270``). Such objects can be inspected interactively by means of
an atomic viewer such as the one provided by ``ase``. AiiDA however
supports several other viewers such as ``xcrysden``, ``jmol``, and
``vmd``. Type in the terminal

.. code:: console

    verdi data structure show --format ase <pk>

to show the selected structure (it will take a few seconds to appear,
and you can rotate the view with the right mouse button—if you receive
some errors, make sure you started your SSH connection with the ``-X``
or ``-Y`` flag).

Alternatively, especially if showing them interactively is too slow over
SSH, you can export the content of a structure node in various popular
formats such as ``xyz`` or ``xsf``. This is achieved by typing in the
terminal

.. code:: console

    verdi data structure export --format xsf <pk>  >  <pk>.xsf

You can open the generated ``xsf`` file and observe the cell and the
coordinates. Then, you can then copy ``<pk>.xsf`` from the Amazon
machine to your local one and then visualize it, e.g. with xcrysden (if
you have it installed):

.. code:: console

    xcrysden --xsf <pk>.xsf

Codes and computers
~~~~~~~~~~~~~~~~~~~

Let us focus now on the nodes of type ``Code``. A code represents (in
the database) the actual executable used to run the calculation. Find
the pk of such a node in the graph and type

.. code:: console

    verdi code show <pk>

The command prints information on the plugin used to interface the code
to AiiDA, the remote machine on which the code is executed, the path of
its executable, etc. To show a list of all available codes type

.. code:: console

    verdi code list

If you want to show all codes, including hidden ones and those created
by other users, use ``verdi code list -a -A``. Now, among the entries of
the output you should also find the code just shown.

Similarly, the list of computers on which AiiDA can submit calculations
is accessible by means of the command

.. code:: console

    verdi computer list -a

(``-a`` shows all computers, also the one imported in your database but
that you did not configure, i.e., to which you don’t have access).
Details about each computer can be obtained by the command

.. code:: console

    verdi computer show <COMPUTERNAME>

Now you have the tools to answer the question:

What is the scheduler installed on the computer where the calculations
of the graph have run?

Calculation results
~~~~~~~~~~~~~~~~~~~

The results of a calculation can be accessed directly from the
calculation node. Type in the terminal

.. code:: console

    verdi calcjob res <pk>

which will print the output dictionary of the “scalar” results parsed by
AiiDA at the end of the calculation. Note that this is actually a
shortcut for

.. code:: console

    verdi data dict show <pk2>

where ``pk2`` refers to the Dict node attached as an output of
the calculation node, with link name ``output_parameters``.

By looking at the output of the command, what is the Fermi energy of the
calculation with UUID prefix ``ce81c420``?

Similarly to what you did for the calculation inputs, you can access the
output files via the commands

.. code:: console

    verdi calcjob outputls <pk>

and

.. code:: console

    verdi calcjob outputcat <pk>

Use the latter to verify that the Fermi energy that you have found in
the last step has been extracted correctly from the output file (Hint:
filter the lines containing the string “Fermi”, e.g. using ``grep``, to
isolate the relevant lines).

The results of calculations are stored in two ways: ``Dict``
objects are stored in the database, which makes querying them very
convenient, whereas ``ArrayData`` objects are stored on the disk. Once
more, use the command ``verdi data array show <pk>`` to know the Fermi
energy obtained from calculation with UUID prefix ``ce81c420`` (you need
to use, this time, the PK of the output ArrayData of the calculation,
with link name ``output_trajectory_array``). As you might have realized
the difference now is that the whole series of values of the Fermi
energy calculated after each relax/vc-relax step are stored. (The choice
of what to store in ``Dict`` and ``ArrayData`` nodes is made by
the parser of ``pw.x`` implemented in the ``aiida-quantumespresso``
plugin.)

(Optional section) Comments
~~~~~~~~~~~~~~~~~~~~~~~~~~~

AiiDA offers the possibility to attach comments to a any node,
in order to be able to remember more easily its details. Node with UUID
prefix ce81c420 has no comment already defined, but you can add a very
instructive one by typing in the terminal

.. code:: console

    verdi comment add "vc-relax of a BaTiO3 done with QE pw.x" -N <pk>

Now, if you ask for a list of all comments associated to that
calculation by typing

.. code:: console

    verdi comment show <pk>

the comment that you just added will appear together with some useful
information such as its creator and creation date. We let you play with
the other options of ``verdi comment`` command to learn how to update or
remove comments.

AiiDA groups of calculations
----------------------------

In AiiDA, calculations (and more generally nodes) can be organized in
groups, which are particularly useful to assign a set of calculations or
data to a common project. This allows you to have quick access to a
whole set of calculations with no need for tedious browsing of the
database or writing complex scripts for retrieving the desired nodes.
Type in the terminal

.. code:: console

    verdi group list

to show a list of the groups that already exist in the database. Choose
the PK of the group named ``tutorial_pbesol`` and look at the
calculations that it contains by typing

.. code:: console

    verdi group show <pk>

In this case, we have used the name of the group to organize
calculations according to the pseudopotential that has been used to
perform them. Among the rows printed by the last command you will be
able to find the calculation we have been inspecting until now.

If, instead, you want to know all the groups to which a specific node
belomngs, you can run

.. code:: console

    verdi group list -N/--node <pk>
