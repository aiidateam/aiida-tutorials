(calculation-calcjobs)=

# Calculation jobs

So far we've covered the AiiDA basics using data nodes and processes involving simple arithmetic.
In the second part of this session, we'll have a look at some more interesting data structures and calculations, based on some examples using Quantum ESPRESSO.

## Importing data

Before we start running Quantum ESPRESSO calculations ourselves, which is the topic of the next session, we are going to look at an AiiDA database already created by someone else.
Let's import one from the web:

```{code-block} console

$ verdi import https://object.cscs.ch/v1/AUTH_b1d80408b3d340db9f03d373bbde5c1e/marvel-vms/tutorials/aiida_tutorial_2020_07_perovskites_v0.9.aiida

```

As mentioned previously, AiiDA databases contain not only *results* of calculations but also their inputs and information on how a particular result was obtained.
This information, the *data provenance*, is stored in the form of a *directed acyclic graph* (DAG).
In the following, we are going to introduce you to different ways of browsing this graph and will ask you to find out some information regarding the database you just imported.

(provenance-graph)=

## The provenance graph

{numref}`fig-qe-calc-graph` shows a typical example of a Quantum ESPRESSO calculation represented in an AiiDA graph.
Have a look to the figure and its caption before moving on.

(fig-qe-calc-graph)=

```{figure} include/images/batio3-graph-full.png
:width: 100%

Graph with all inputs (data, circles; and code, diamond) to the Quantum ESPRESSO calculation (square) that you will create in this module.
Besides the inputs, the graph also shows the outputs that the engine will create and connect automatically.
The `RemoteData` node is created during submission and can be thought as a symbolic link to the remote folder in which the calculation runs on the cluster.
The other nodes are created when the calculation has finished, after retrieval and parsing.
The node with linkname `retrieved` contains the relevant raw output files stored in the AiiDA repository; all other nodes are added by the parser.
Additional nodes (symbolized in gray) can be added by the parser: e.g., an output `StructureData` if you performed a relaxation calculation, a `TrajectoryData` for molecular dynamics, etc.

```

{numref}`fig-qe-calc-graph` was drawn by hand but you can generate a similar graph automatically by passing the **identifier** of a calculation node to `verdi node graph generate <IDENTIFIER>`, or using the {ref}`graph's python API <aiida:how-to:data:visualise-provenance>`.
Remember that identifiers in AiiDA can come in several forms:

* "Primary Key" (PK): An integer, e.g. `723`, that identifies your entity within your database (automatically assigned)
* [Universally Unique Identifier](<https://en.wikipedia.org/wiki/Universally_unique_identifier#Version_4_(random)>) (UUID): A string, e.g. `ce81c420-7751-48f6-af8e-eb7c6a30cec3` that identifies your entity globally (automatically assigned)
* Label: A human-readable string, e.g. `test_qe_calculation` (manually assigned)

Any `verdi` command that expects an identifier will accept a PK, a UUID or a label (although not all entities have a label by default).
While PKs are often shorter than UUIDs and can be easier to remember, they are only unique within your database.
**Whenever you intend to share your data with others, use UUIDs to refer to nodes.**

```{note}

For UUIDs, it is sufficient to specify a subset (starting at the beginning) as long as it can already be uniquely resolved.
For more information on identifiers in `verdi` and AiiDA in general, see the [documentation](<https://aiida.readthedocs.io/projects/aiida-core/en/latest/topics/cli.html#topics-cli-identifiers>).

```

Let's generate a graph for the calculation node with UUID `ce81c420-7751-48f6-af8e-eb7c6a30cec3`:

```{code-block} console

$ verdi node graph generate ce81c420

```

This command will create the file `<PK>.dot.pdf` that can be viewed with any PDF document viewer.
See the (**TODO: FIX LINK**) in case you need a quick reminder on how to do so.

For the remainder of this section, we'll use the `verdi` CLI and the `verdi shell` to explore the properties of the `PwCalculation`, as well as its inputs.
Understanding these data types will come in handy for the section on running calculations.
We'll also introduce some new CLI commands and shell features that will be useful for the hands-on sessions that follow.

## Processes

Anything that 'runs' in AiiDA, be it calculations or workflows, is considered a `Process`.
Let's have another look at the *finished* processes in the database by passing the `-S/--process-state` flag:

```{code-block} console

$ verdi process list -S finished

```

This command will list all the processes that have a process state `Finished` and should contain a list of `PwCalculation` processes that you have just imported:

```{code-block} bash

PK    Created    Process label   Process State    Process status
----  ---------  --------------  ---------------  ----------------
...
1178  1653D ago  PwCalculaton    ⏹ Finished [0]
1953  1653D ago  PwCalculaton    ⏹ Finished [0]
1734  1653D ago  PwCalculaton    ⏹ Finished [0]
 336  1653D ago  PwCalculaton    ⏹ Finished [0]
1056  1653D ago  PwCalculaton    ⏹ Finished [0]
1369  1653D ago  PwCalculaton    ⏹ Finished [0]
...

Total results: 177

Info: last time an entry changed state: 21m ago (at 20:03:00 on 2020-07-03)

```

Note that processes can be in any of the following states:

* `Created`
* `Waiting`
* `Running`
* `Finished`
* `Excepted`
* `Killed`

The first three states are 'active' states, meaning the process is not done yet, and the last three are 'terminal' states.
Once a process is in a terminal state, it will never become active again.
The {ref}`official documentation <aiida:topics:processes:concepts:state>` contains more details on process states.

Remember that in order to list processes of *all* states, you can use the `-a/--all` flag:

```{code-block} console

$ verdi process list -a

```

This command will list all the processes that have *ever* been launched.
As your database will grow, so will the output of this command.
To limit the number of results, you can use the `-p/--past-days <NUM>` option, that will only show processes that were created `NUM` days ago.
For example, this lists all processes launched since yesterday:

```{code-block} console

$ verdi process list -a -p1

```

(aiida-identifiers)=

This will be useful in the coming days to limit the output from `verdi process list`.
Each row of the output identifies a process with some basic information about its status.
For a more detailed list of properties, you can use `verdi process show`, but to address any specific process, you need an identifier for it.

Let's revisit the process with the UUID `ce81c420-7751-48f6-af8e-eb7c6a30cec3`, this time using the CLI:

```{code-block} bash

$ verdi process show ce81c420

```

Producing the output:

```{code-block} bash

Property     Value
-----------  ------------------------------------
type         PwCalculation
state        Finished [0]
pk           630
uuid         ce81c420-7751-48f6-af8e-eb7c6a30cec3
label
description
ctime        2014-10-27 17:51:21.781045+00:00
mtime        2019-05-09 14:10:09.307986+00:00
computer     [1] daint

Inputs      PK    Type
----------  ----  -------------
pseudos
    Ba      1092  UpfData
    O       1488  UpfData
    Ti      1855  UpfData
code        631   Code
kpoints     498   KpointsData
parameters  629   Dict
settings    500   Dict
structure   1133  StructureData

Outputs                    PK  Type
-----------------------  ----  -------------
output_kpoints           1455  KpointsData
output_parameters         789  Dict
output_structure          788  StructureData
output_trajectory_array   790  ArrayData
remote_folder            1811  RemoteData
retrieved                 787  FolderData

```

Compare the in- and outputs with those visualized in the provenance graph earlier.
The PKs shown for the inputs and outputs will come in handy to get more information about those nodes, which we'll do for several inputs below.

You can also use the verdi CLI to obtain the content of the raw input file to Quantum ESPRESSO (that was generated by AiiDA) via the command:

```{code-block} console

$ verdi calcjob inputcat ce81c420

```

where you once again provide the identifier of the `PwCalculation` process, which is a *calculation job* (hence the `calcjob` subcommand).
This will print the input file of the Quantum ESPRESSO calculation, which when run through AiiDA is written to the default input file `aiida.in`.
To see a list of all the files used to run a calculation (input file, submission script, etc.) instead type:

```{code-block} console

$ verdi calcjob inputls ce81c420

```

Adding the `--color` flag helps distinguishing files from folders.
Once you know the name of the file you want to visualize, you can call the `verdi calcjob inputcat [PATH]` command specifying the path of the file to show.
For instance, to see the submission script, you can use:

```{code-block} console

$ verdi calcjob inputcat ce81c420 _aiidasubmit.sh

```

## Inputs

Here we will discuss the input nodes of the `PwCalculation` calculation job.
The `Code` node and its setup will be discussed in the next hands-on on (**TODO: FIX LINK**).

### Dict - parameters

Let's investigate some of the input and output nodes of the `PwCalculation`.
Dictionaries with various parameters are represented in AiiDA by `Dict` nodes.
From the inputs of the process, let's choose the node of type `Dict` with input link name `parameters` and type in the terminal:

```{code-block} console

$ verdi data dict show <IDENTIFIER>

```

where `<IDENTIFIER>` is the PK of the node.

A `Dict` node contains a dictionary (i.e. key–value pairs), stored in the database in a format ready to be queried.
We will learn how to run queries during the (**TODO: FIX LINK**).
The command above will print the content dictionary, containing the parameters used to define the input file for the calculation.

Check the consistency of the parameters stored in the `Dict` node with those written in the `aiida.in` input file you printed previously.
Even if you don't know the meaning of the input flags of a Quantum ESPRESSO calculation, you should be able to see how the input dictionary has been converted to Fortran namelists.

Of course, we can also load the contents of the parameters dictionary in Python. Start up a `verdi shell` and load the `Dict` node:

```{code-block} ipython

In [1]: params = load_node(PK)

```

Next, we can use the `get_dict()` method to obtain the dictionary stored in the `Dict` node:

```{code-block} ipython

In [2]: pw_dict = params.get_dict()

In [3]: pw_dict
Out[3]:
{'SYSTEM': {'nspin': 2,
  'degauss': 0.02,
  'ecutrho': 600,
  'ecutwfc': 60,
  'smearing': 'gaussian',
  'occupations': 'smearing',
  'starting_magnetization': [0.5, 0.5, 0.1]},
 'CONTROL': {'wf_collect': True,
  'calculation': 'vc-relax',
  'max_seconds': 1710,
  'restart_mode': 'from_scratch'},
 'ELECTRONS': {'conv_thr': 1e-10,
  'mixing_beta': 0.7,
  'mixing_mode': 'plain',
  'diagonalization': 'david',
  'electron_maxstep': 50}}

```

Modify the python dictionary `pw_dict` so that the wave-function cutoff is now set to 20 Ry.
Objects that are already stored in the database cannot be modified, as doing so would alter the provenance graph of connected nodes.
So, to write the modified dictionary to the database, you have to create a new object of class `Dict`.
To load any data class, we can use AiiDA's `DataFactory` and the *entry point* of the `Dict` class (`'dict'`):

```{code-block} ipython

In [4]: Dict = DataFactory('dict')
   ...: new_params = Dict(dict=pw_dict)

```

where `pw_dict` is the modified python dictionary.
Note that at this point `new_params` is not yet stored in the database.
Let's finish this example by storing the `new_params` dictionary node in the database:

```{code-block} ipython

In [5]: new_params.store()

```

```{note}

While it is also possible to import the `Dict` class directly, it is recommended to use the `DataFactory` function instead, as this is more future-proof: even if the import path of the class changes in the future, its entry point string (`'dict'`) will remain stable.

```

(virtual-intro-basic-structure)=

### StructureData

Next, let's have a look at the `StructureData` node, which represents a crystalline structure.
We can consider for instance the input structure to the calculation we were considering before (it should have the UUID `3a4b1270`).
Such objects can be inspected interactively by means of an atomic viewer such as the one provided by `ase`.
AiiDA however supports several other viewers such as `xcrysden`, `jmol`, and `vmd`.
Type in the terminal:

```{code-block} console

$ verdi data structure show --format ase <IDENTIFIER>

```

to show the selected structure, although it will take a few seconds to appear (it has to go over a tunnel on your SSH connection).
You should be able to rotate the view with the right mouse button.

```{note}

If you receive some errors, make sure your X-forwarding settings have been set up correctly, as explained in (**TODO: FIX LINK**).

```

Alternatively, especially if showing them interactively is too slow over SSH, you can export the content of a structure node in various popular formats such as `xyz`, `xsf` or `cif`.
This is achieved by typing in the terminal:

```{code-block} console

$ verdi data structure export --format xsf <IDENTIFIER> > BaTiO3.xsf

```

This outputs the structure in `xsf` format and writes it to a file.

You can open the generated `xsf` file and observe the cell and the coordinates.
Then, you can then copy `BaTiO3.xsf` from the Amazon machine to your local one and then visualize it, e.g. with [xcrysden](<http://www.xcrysden.org>) (if you have it installed):

```{code-block} console

$ xcrysden --xsf BaTiO3.xsf

```

The `StructureData` node can also be investigated using the `verdi shell`.
First, open the `verdi shell` and load the structure node:

```{code-block} ipython

In [1]: structure = load_node('3a4b1270')
In [2]: structure
Out[2]: <StructureData: uuid: 3a4b1270-82bf-4d66-a51f-982294f6e1b3 (pk: 1161)>

```

You can display its chemical formula using:

```{code-block} ipython

In [3]: structure.get_formula()
Out[3]: 'BaO3Ti'

```

or, to obtain the atomic positions and species:

```{code-block} ipython

In [4]: structure.sites
Out[4]:
[<Site: kind name 'Ba' @ 0.0,1.78886419607596e-30,0.0>,
 <Site: kind name 'Ti' @ 1.98952035955311,1.98952035955311,1.98952035955311>,
 <Site: kind name 'O' @ 1.98952035955311,1.98952035955311,0.0>,
 <Site: kind name 'O' @ 1.98952035955311,2.33671938655715e-31,1.98952035955311>,
 <Site: kind name 'O' @ 0.0,1.98952035955311,1.98952035955311>]

```

If you are familiar with [ASE](<https://wiki.fysik.dtu.dk/ase/>) and [Pymatgen](<https://pymatgen.org/>), you can convert this structure to those formats by typing either

```{code-block} ipython

In [5]: structure.get_ase()
Out[5]: Atoms(symbols='BaTiO3', pbc=True, cell=[3.97904071910623, 3.97904071910623, 3.97904071910623], masses=...)

```

```{code-block} ipython

In [6]: structure.get_pymatgen()
Out[6]:
Structure Summary
Lattice
    abc : 3.97904071910623 3.97904071910623 3.97904071910623
 angles : 90.0 90.0 90.0
 volume : 62.999216807333035
      A : 3.97904071910623 0.0 0.0
      B : 0.0 3.97904071910623 0.0
      C : 0.0 0.0 3.97904071910623
PeriodicSite: Ba (0.0000, 0.0000, 0.0000) [0.0000, 0.0000, 0.0000]
PeriodicSite: Ti (1.9895, 1.9895, 1.9895) [0.5000, 0.5000, 0.5000]
PeriodicSite: O (1.9895, 1.9895, 0.0000) [0.5000, 0.5000, 0.0000]
PeriodicSite: O (1.9895, 0.0000, 1.9895) [0.5000, 0.0000, 0.5000]
PeriodicSite: O (0.0000, 1.9895, 1.9895) [0.0000, 0.5000, 0.5000]

```

Of course, the structure above is already in our database, after we imported it at the start of this section.
In order to add new structures to your AiiDA database, you can also define a structure by hand, or import it from an online repository:

```{dropdown} Defining a structure and storing it in the database

Let’s try now to define a new structure to study, specifically a silicon crystal.
In the `verdi shell`, define a cubic unit cell as a 3 x 3 matrix, with lattice parameter `alat` = 5.4 Å:

```{code-block} ipython

In [1]: alat = 5.4
    ...: unit_cell = [[alat/2, alat/2, 0.], [alat/2, 0., alat/2], [0., alat/2, alat/2]]

```

```{note}

Default units for crystal structure cell and coordinates in AiiDA are Å (Ångström).

```

In order to store a structure in the AiiDA database, we need to create an instance of the `StructureData` class.
We can load this class using the `DataFactory`:

```{code-block} ipython

In [2]: StructureData = DataFactory('structure')

```

Now, initialize the class instance using the unit cell you defined:

```{code-block} ipython

In [3]: structure = StructureData(cell=unit_cell)

```

From now on, you can access the cell with the command

```{code-block} ipython

In [4]: structure.cell
Out[4]: [[2.7, 2.7, 0.0], [2.7, 0.0, 2.7], [0.0, 2.7, 2.7]]

```

Of course, at this point we only have an empty unit cell.
So, let's append the 2 Si atoms to the crystal structure, starting with:

```{code-block} ipython

In [5]: structure.append_atom(position=(alat/4., alat/4., alat/4.), symbols="Si")

```

for the first ‘Si’ atom.
Repeat this command for the other Si site with coordinates (0, 0, 0).
You can access and inspect the structure sites by accessing the corresponding property:

```{code-block} ipython

In [6]: structure.sites
Out[6]: [<Site: kind name 'Si' @ 1.35,1.35,1.35>, <Site: kind name 'Si' @ 0.0,0.0,0.0>]

```

If you make a mistake, start over from
`structure = StructureData(cell=the_cell)`, or equivalently use `structure.clear_kinds()` to remove all kinds (atomic species) and sites.

Alternatively, AiiDA structures can also be converted directly from ASE structures [#f1]_ using

```{code-block} ipython

In [7]: from ase.spacegroup import crystal
    ...: ase_structure = crystal('Si', [(0, 0, 0)], spacegroup=227,
    ...:             cellpar=[alat, alat, alat, 90, 90, 90], primitive_cell=True)
    ...: structure = StructureData(ase=ase_structure)

```

Now you can store the new structure object in the database with the command:

```{code-block} ipython

In [8]: structure.store()

```

```{note}

Similarly, a ``StructureData`` instance can also be intialized from a pymatgen structure using ``StructureData(pymatgen=pmg_structure)``.

```

```

```{dropdown} Importing a structure from an online repository

Another way of obtaining the silicon structure is to import it from an external (online)
repository such as the [Crystallography Open Database (COD)](http://www.crystallography.net/cod/).
Try executing the following code snippet in the `verdi shell`:

```{code-block} python

from aiida.tools.dbimporters.plugins.cod import CodDbImporter
importer = CodDbImporter()
for entry in importer.query(formula='Si', spacegroup='F d -3 m'):
    structure = entry.get_aiida_structure()
    print("Formula:", structure.get_formula())
    print("Unit cell volume:", structure.get_cell_volume())
    print()

```

This will connect to the COD database on the web, perform the query for all entries with formula `Si` and space group `Fd-3m`, fetch the results and convert them to AiiDA StructureData objects.
In this case two structures exist for `Si` in COD and both are shown.
```

(virtual-intro-basic-kpoints)=

### KpointsData

A set of k-points in the Brillouin zone is represented by an instance of the `KpointsData` class.
Look for an identifier (PK or UUID) of the `KpointsData` input node of the `PwCalculation` whose provenance graph you generated earlier, and load the node in the `verdi shell`:

```{code-block} ipython

In [1]: kpoints = load_node(<IDENTIFIER>)

```

You can get the k-points mesh using:

```{code-block} ipython

In [2]: kpoints.get_kpoints_mesh()
Out[2]: ([6, 6, 6], [0.0, 0.0, 0.0])

```

To get the full (explicit) list of k-points belonging to this mesh, use:

```{code-block} ipython

In [3]: kpoints.get_kpoints_mesh(print_list=True)
Out[3]:
array([[0.        , 0.        , 0.        ],
       [0.        , 0.        , 0.16666667],
       ...
       [0.83333333, 0.83333333, 0.66666667],
       [0.83333333, 0.83333333, 0.83333333]])

```

If this throws an `AttributeError`, it means that the kpoints instance does not represent a regular mesh but rather a list of k-points defined by their crystal coordinates (typically used when plotting a band structure).
In this case, get the list of k-points coordinates using

```{code-block} ipython

In [3]: kpoints.get_kpoints()

```

Conversely, if the `KpointsData` node *does* actually represent a mesh, this method is the one, that when called, will throw an `AttributeError`.

If you prefer Cartesian (rather than fractional) coordinates, type:

```{code-block} ipython

In [4]: kpoints.get_kpoints(cartesian=True)

```

For later use in this tutorial, let us try now to create a k-points instance, to describe a regular (2 x 2 x 2) mesh of k-points, centered at the Gamma point (i.e. without offset).
This can be done with the following set of commands:

```{code-block} ipython

In [5]: KpointsData = DataFactory('array.kpoints')
   ...: kpoints = KpointsData()
   ...: kpoints.set_kpoints_mesh([2, 2, 2])

```

Here, we first load the `KpointsData` class using the `DataFactory` and the entry point (`array.kpoints`).
Then, we create an instance of the `KpointData` class, and use the `set_kpoints_mesh()` method to set the mesh to a regular 2x2x2 Gamma-point centered mesh.

(virtual-intro-basic-pseudopotentials)=

[^f1]: We purposefully do not provide advanced commands for crystal structure manipulation in AiiDA, because python packages that accomplish such tasks already exist (such as ASE or pymatgen).
