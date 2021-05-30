(calculation-calcjobs)=
# Calculation jobs

In this section we'll be learning how to run external codes with AiiDA through calculation plugins.

We will use the [Quantum ESPRESSO](<https://www.quantum-espresso.org/>) package to launch a simple [density functional theory](<https://en.wikipedia.org/wiki/Density_functional_theory>) calculation of a silicon crystal using the {doi}`PBE exchange-correlation functional <10.1103/PhysRevLett.77.3865>` and check its results.
In doing so, we will intentionally introduce some bogus input parameters in order to show how to 'manually' debug problems when encountering errors.
Workflows, which you'll see later in this tutorial, can help you avoid these issues systematically.

Note that besides the [aiida-quantumespresso](<https://github.com/aiidateam/aiida-quantumespresso>) plugin, AiiDA comes with plugins for many other codes, all of which are listed in the [AiiDA plugin registry](<https://aiidateam.github.io/aiida-registry/>).

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

## The AiiDA daemon

First of all, check that the AiiDA daemon is actually running.
The AiiDA daemon is a program that

> > * runs continuously in the background
> * waits for new calculations to be submitted
> * transfers the inputs of new calculations to your compute resource
> * checks the status of your calculation on the compute resource, and
> * retrieves the results from the compute resource

Check the status of the daemon process by typing in the terminal:

```{code-block} console

$ verdi daemon status

```

If the daemon is running, the output should look like

```{code-block} bash

Profile: quicksetup
Daemon is running as PID 2050 since 2019-04-30 12:37:12
Active workers [1]:
  PID    MEM %    CPU %  started
-----  -------  -------  -------------------
 2055    2.147        0  2019-04-30 12:37:12
Use verdi daemon [incr | decr] [num] to increase / decrease the amount of workers

```

If this is not the case, type in the terminal

```{code-block} console

$ verdi daemon start

```

to start the daemon.

## Creating and launching calculations

In the following, we'll be working in the `verdi shell`.
As you go along, feel free to keep track of your commands by copying them into a python script `test_pw.py`.

::::{note}

The `verdi shell` imports a number of AiiDA internals so that you as the user don't have to.
You can also make those available to a python script, by running it using

```{code-block} console

$ verdi run <scriptname>

```

::::

Every calculation sent to a cluster is linked to a *code*, which describes the executable file as we saw earlier.
We also saw how to list all codes available using

```{code-block} console

$ verdi code list

```

In this part of the tutorial we are interested in running the `pw.x` executable of Quantum ESPRESSO, i.e. in codes for the `quantumespresso.pw` plugin. If you have many codes for different executables, you can filter only those using a specific plugin with the command:

```{code-block} console

$ verdi code list -P quantumespresso.pw

```

Pick the correct codename (`qe-6.5-pw@localhost` if you followed the instructions earlier) and load it in the `verdi shell`:

```{code-block} ipython

In [1]: code = load_code("<codename>")

```

:::{note}

`load_code` returns an object of type `Code`, which is the general AiiDA class for describing simulation codes.

:::

Let's build the inputs for a new `PwCalculation` (defined by the `quantumespresso.pw` plugin) using a "builder", a class provided by AiiDA that will help you out:

```{code-block} ipython

In [2]: builder = code.get_builder()

```

As the first step, assign a (short) label or a (long) description to your calculation, that you might find convenient in the future.

```{code-block} ipython

In [3]: builder.metadata.label = "PW test"
   ...: builder.metadata.description = "My first AiiDA calc with Quantum ESPRESSO on Si"

```

This information will be saved in the database for later queries or inspection.
Note that you can press TAB after writing `builder.` to see all inputs available for this calculation.
In order to figure out which data type is expected for a particular input, such as `builder.structure`, and whether the input is optional or required, use `builder.structure?`.

Now, specify the number of machines (a.k.a. cluster nodes) you are going to run on and the maximum time allowed for the calculation.
The general options grouped under `builder.metadata.options` are independent of the code or plugin, and will be passed to the scheduler that handles the queue on your compute resource.

```{code-block} ipython

In [4]: builder.metadata.options.resources = {'num_machines': 1}
   ...: builder.metadata.options.max_wallclock_seconds = 30 * 60

```

Again, to see the list of available options, type `builder.metadata.options.` and hit the TAB button.

### Preparation of inputs

A Quantum ESPRESSO calculation needs a number of inputs:

1. [Pseudopotentials](<https://en.wikipedia.org/wiki/Pseudopotential>)
2. a structure
3. a mesh in reciprocal space (k-points)
4. a number of input parameters

These are mirrored in the inputs of the `aiida-quantumespresso` plugin (see [documentation](<https://aiida-quantumespresso.readthedocs.io/en/stable/user_guide/calculation_plugins/pw.html>)).
We'll start with the structure, k-points, and pseudopotentials and leave the input parameters as the last thing to setup.

:::{admonition} Exercise

Use what you learned in the basics section to load the `structure` and `kpoints` inputs for your calculation:

* Use a silicon crystal {ref}`structure<matsci-structure>`.
* Define a `2x2x2` mesh of {ref}`k-points<matsci-kpoints>`.

Note: If you just copy and paste code that you executed previously, this may result in duplication of information on your database.
In fact, you can re-use an existing structure stored in your database [^f1].
Use a combination of the bash command `verdi data structure list` and the python function `load_node()` to get an object representing the structure created earlier.

:::

### Attaching the input information to the calculation

Once you've created a `structure` node and a `kpoints` node, attach it to the calculation:

```{code-block} ipython

In [5]: builder.structure = structure
   ...: builder.kpoints = kpoints

```

:::{note}

The builder accepts both *stored* and *unstored* data nodes.
AiiDA will take care of storing the unstored nodes upon submission.
If you decide not to submit, nothing will be stored in the database.

:::

PWscf also needs information on the pseudopotentials, in the form of a dictionary, where keys are the names of the elements and the values are the corresponding `UpfData` objects containing the information on the pseudopotential.
However, instead of creating the dictionary by hand, we can use a helper function that picks the right pseudopotentials for our structure from a pseudopotential *family*.
You can list the preconfigured families within the IPython shell using:

```{code-block} ipython

In [6]: !verdi data upf listfamilies

```

Pick the one you {ref}`configured in the basics hands on<matsci-pseudos>` (the `SSSP` family) and link the correct pseudopotentials to the calculation using the command:

```{code-block} ipython

In [7]: from aiida.orm.nodes.data.upf import get_pseudos_from_structure
   ...: builder.pseudos = get_pseudos_from_structure(structure, '<PSEUDO_FAMILY_NAME>')

```

Print the content of the `pseudos` namespace with `print(builder.pseudos)` to see what the helper function created.

### Preparing and debugging input parameters

Finally, we need to specify a number of input parameters (i.e. plane wave cutoffs, convergence thresholds, etc.) to launch the Quantum ESPRESSO calculation.
The structure of the parameter dictionary closely follows the structure of the [PWscf input file](<https://www.quantum-espresso.org/Doc/INPUT_PW.html>).

Since these are often the parameters to tune in a calculation, let's **introduce a few mistakes intentionally** and use this part of the tutorial to learn how to debug problems.

Define a set of input parameters for Quantum ESPRESSO, preparing a dictionary of the form:

```{code-block} ipython

In [8]: parameters_dict = {
   ...:     'CONTROL': {
   ...:         'calculation': 'scf',
   ...:     },
   ...:     'SYSTEM': {
   ...:         'ecutwfc': 30.,
   ...:         'ecutrho': 200.,
   ...:         'mickeymouse': 240.,
   ...:     },
   ...:     'ELECTRONS': {
   ...:         'conv_thr': 1.e-14,
   ...:         'electron_maxstep': 3,
   ...:     },
   ...: }

```

This dictionary is almost a valid input for the Quantum ESPRESSO plugin, except for an invalid key `mickeymouse`. When Quantum ESPRESSO receives an unrecognized key, it will stop.
By default, the AiiDA plugin will *not* validate your input and simply pass it on to the code.

We have also introduced a combination of a very high accuracy (`'conv_thr': 1.e-14`) coupled with a very low maximum number of self consistent iterations (`'electron_maxstep': 3`).
This means that even if we eliminate the invalid key, the calculation will not converge and will not be successful, despite there not being any other mistake in the parameters dictionary.

Let's wrap the `parameters_dict` python dictionary in an AiiDA `Dict` node, and set it as the input of name `parameters`. We'll see what happens.

```{code-block} ipython

In [9]: builder.parameters = Dict(dict=parameters_dict)

```

### Simulate submission

At this stage, you have created in memory (it's not yet stored in the database) the input of the graph shown below.
The outputs will be created by the daemon later on.

:::{figure} include/images/si-graph-full.png
:alt: true

:::

In order to check which input files AiiDA creates, we can perform a *dry run* of the submission process.
Let's tell the builder that we want a dry run and that we don't want to store the provenance of the dry run:

```{code-block} ipython

In [10]: builder.metadata.dry_run = True
    ...: builder.metadata.store_provenance = False

```

It's time to run:

```{code-block} ipython

In [11]: from aiida.engine import run
    ...: run(builder)

```

::::{note}

Instead of using the builder, you can also simply pass the calculation class as the first argument, followed by the inputs as keyword arguments, e.g.:

```{code-block} python

run(PwCalculation, structure=structure, pseudos={'Si': pseudo_node}, ....)

```

The builder is simply a convenience wrapper providing tab-completion in the shell and automatic help strings.

::::

This creates a folder of the form `submit_test/[date]-0000[x]` in the current directory.
Open a second terminal and:

> > * open the input file `aiida.in` within this folder
> * compare it to input data nodes you created earlier
> * verify that the {}`pseudo` folder contains the needed pseudopotentials
> * have a look at the submission script `_aiidasubmit.sh`

:::{note}

The files created by a dry run are only intended for  inspection
and cannot be used to correct the inputs of your calculation.

:::

### Submitting the calculation

Up to now we've just been playing around and our calculation has been kept in memory and not in the database.
Now that we have inspected the input files and convinced ourselves that Quantum ESPRESSO will have all the information it needs to perform the calculation, we will submit the calculation properly.
Doing so will make sure that all inputs are stored in the database, will run and store the calculation and link the outputs to it.

Let's revert the following values in our builder to their defaults:

```{code-block} ipython

In [12]: builder.metadata.dry_run = False
    ...: builder.metadata.store_provenance = True

```

And then rely on the submit machinery of AiiDA,

```{code-block} ipython

In [13]: from aiida.engine import submit
    ...: calculation = submit(builder)

```

As soon as you have executed these lines, the `calculation` variable contains a `PwCalculation` instance, already submitted to the daemon.

:::{note}

You may have noticed that we used `submit` here instead of `run`.
The difference is that `submit` will hands over the calculation to the daemon running in the background, while `run` will execute all tasks in the current shell.

All processes in AiiDA (you will soon get to know more) can be "launched" using one of available functions:

> > * run
> * run_get_node
> * run_get_pk
> * submit

which are explained in more detail in the [online documentation](<https://aiida.readthedocs.io/projects/aiida-core/en/v1.3.0/topics/processes/usage.html?highlight=run_get_pk#launching-processes>).

:::

The calculation is now stored in the database and was assigned a "database primary key" or `pk` (`calculation.pk`) as well as a UUID (`calculation.uuid`).
See the {ref}`previous section <2019-aiida-identifiers>` for more details on these identifiers.

To preserve the integrity of the data provenance, AiiDA will prevent you from changing the core content ("attributes") of a stored node.
There is an "extras" section though, which is writable after storage, to allow you to set additional information, e.g. as a way of labelling nodes and providing information for querying.

For example, let's add an extra attribute called `element`, with value `Si`:

```{code-block} ipython

In [14]: calculation.set_extra("element", "Si")

```

In the mean time, after you submitted your calculation, the daemon picked it up and started to: generate the input files, submit the calculation to the queue, wait for it to run and finish, retrieve the output files, parse them, store them in the database and set the state of the calculation to `Finished`.

:::{note}

If the daemon is not running, the calculation will remain in the `NEW` state until you start the daemon.

:::

### Checking the status of the calculation

You can check the calculation status from the command line in your second terminal:

```{code-block} console

$ verdi process list

```

If you don't see any calculation in the output, the calculation you submitted has already finished.

:::{note}

Since you are running your DFT calculation directly on the VM, `verdi` commands can be a bit slow until the calculation finishes.

:::

By default, the command only prints calculations that are still active [^f2].
Let's also list your finished calculations (and limit those only to the one created in the past day):

```{code-block} console

$ verdi process list -a -p1

```

as explained in the first section.

Similar to the dry run, we can also inspect the input files of the *actual* calculation:

```{code-block} console

$ verdi calcjob inputls <pk_number> -c

```

for the `pk_number` of your calculation. This will show the contents of the input directory (`-c` prints directories in color).
Check the content of input files with

```{code-block} console

$ verdi calcjob inputcat <pk_number> | less

```

## Troubleshooting

Your calculation should end up in a finished state, but with some error: this is represented by a non-zero error code in brackets near the "Finished" status of the State:

```{code-block} console

$ verdi process list -a -p1
  PK  Created    Process label    Process State     Process status
----  ---------  ---------------  ----------------  ----------------
2060  5m ago     PwCalculation    ⏹ Finished [305]
...
# Anything but [0] after the Finished state signals a failure

```

This was expected, since we used an invalid key in the input parameters.
Situations like this happen in real life, so AiiDA provides tools to trace back to the source of the problem and correct it.

In general for any calculation (both successful and failed) you can get a more detailed summary by running:

```{code-block} console

$ verdi process show <pk_number>
Property     Value
-----------  --------------------------------------------------------------------------------
type         PwCalculation
state        Finished [305] Both the stdout and XML output files could not be read or parsed.
pk           2060
uuid         95a58902-9c2a-47a7-b858-a058a2ea76e5
label        PW test
description  My first AiiDA calc with Quantum ESPRESSO on Si
ctime        2020-06-30 07:16:45.987116+00:00
mtime        2020-06-30 07:19:55.964423+00:00
computer     [2] localhost

Inputs      PK    Type
----------  ----  -------------
pseudos
    Si      2043  UpfData
code        2056  Code
kpoints     2058  KpointsData
parameters  2059  Dict
structure   2057  StructureData

Outputs              PK  Type
-----------------  ----  --------------
output_parameters  2064  Dict
output_trajectory  2063  TrajectoryData
remote_folder      2061  RemoteData
retrieved          2062  FolderData

Log messages
---------------------------------------------
There are 4 log messages for this calculation
Run 'verdi process report 2060' to see them

```

The last part of the output alerts you to the fact that there are some log messages waiting for you, if you run `verdi process report <pk>`.

If you read the report, you will see that it says that the output files could not be parsed.
In this case you can also try inspecting directly the output file of PWscf.

```{code-block} console

$ verdi calcjob outputcat <pk_number> | less

```

You will see an error message complaining about the `mickeymouse` line in the input.

Let's now correct our input parameters dictionary by leaving out the invalid key and see if our calculation succeeds:

```{code-block} ipython

In [15]: parameters_dict = {
    ...:    "CONTROL": {
    ...:        "calculation": "scf",
    ...:    },
    ...:    "SYSTEM": {
    ...:        "ecutwfc": 30.,
    ...:        "ecutrho": 200.,
    ...:    },
    ...:    "ELECTRONS": {
    ...:        "conv_thr": 1.e-14,
    ...:        'electron_maxstep': 3,
    ...:    }
    ...: }
    ...: builder.parameters = Dict(dict=parameters_dict)
    ...: calculation = submit(builder)

```

(Note: If you have been using the separate script approach, modify the script to remove the faulty input and run it again).

Use `verdi process list -a -p1` to verify that the error code is different now.
You can check again the outputs and the reports with the tools explained in this section and try to fix it yourself before going on to the next.

### Restarting calculations

It turns out that your last calculation did not converge because we stopped the self-consistency iteration cycle before it converged (3).
In this simple case, you could just re-run the calculation from scratch with a sufficient number of iterations, but for expensive calculations (including a structural relaxation or molecular dynamics), you would like instead to restart your calculation from the previous one to save time.

For this purpose, `CalcJobNode` provides the `get_builder_restart` method.
Just like the `get_builder` method of the `Code` or of the `Process` class, this creates an instance of the `ProcessBuilder`, but with all inputs already pre-populated from those of the "parent" node.

Let us load the node of the calculation job that we want to restart in a `verdi shell` and create a new builder from it:

```{code-block} ipython

In [1]: failed_calculation = load_node(<PK>)
   ...: restart_builder = failed_calculation.get_builder_restart()

```

Type `restart_builder` and press Enter to verify that all inputs have already been set to those that were used for the original calculation.
Let's give the new calculation some more steps in the SCF cycle in order to let it converge:

```{code-block} ipython

In [2]: parameters = restart_builder.parameters.get_dict()
   ...: parameters['ELECTRONS']['electron_maxstep'] = 80

```

The `aiida-quantumespresso` plugin supports restarting a calculation by setting the corresponding `restart_mode` and attaching the remote working directory of the previous calculations as the `parent_folder` input [^f3]:

```{code-block} ipython

In [3]: parameters['CONTROL']['restart_mode'] = 'restart'
   ...: restart_builder.parent_folder = failed_calculation.outputs.remote_folder
   ...: restart_builder.parameters = Dict(dict=parameters)

```

Note that we've created a new `Dict` node for the modifed parameters since the original input is stored in the database and immutable.

Finally, let's label this calculation as a restarted one and submit the new calculation:

```{code-block} ipython

In [4]: from aiida.engine import submit
   ...: restart_builder.metadata.label = 'Restart from PwCalculation<{}>'.format(failed_calculation.pk)
   ...: calculation = submit(restart_builder)

```

Inspect the restarted calculation to verify that, this time, it completes successfully.
You should see a "finished" status with exit code zero when running `verdi process list -a -p1`.

## Calculation results

The results of a calculation can be accessed directly from the calculation node using the following:

```{code-block} console

$ verdi calcjob res <IDENTIFIER>

```

which will print the output dictionary of the 'scalar' results parsed by AiiDA at the end of the calculation.
Note that this is actually a shortcut for:

```{code-block} console

$ verdi data dict show <IDENTIFIER>

```

where `IDENTIFIER` refers to the `Dict` node attached as an output of the calculation node, with link name `output_parameters`.
By looking at the output of the command, what is the total energy (`energy`) of the calculation you have run?
What are its units?

Similarly to what you did for the calculation inputs, you can access the output files via the commands:

```{code-block} console

$ verdi calcjob outputls <IDENTIFIER>

```

and

```{code-block} console

$ verdi calcjob outputcat <IDENTIFIER>

```

Use the latter to verify that the energy that you have found in the last step has been extracted correctly from the output file.

:::{tip}

Filter the lines containing the string 'energy', e.g. using `grep`, to isolate the relevant lines.

:::

The results of calculations are stored in two ways: `Dict` objects are stored in the database, which makes querying them very convenient, whereas `ArrayData` objects are stored on the disk.
The choice of what to store in `Dict` and `ArrayData` nodes is made by the parser of `pw.x` implemented in the [aiida-quantumespresso](<https://github.com/aiidateam/aiida-quantumespresso>) plugin.

The `TrajectoryData` output node is a type of `ArrayData`.
Once more, use the command `verdi data array show <IDENTIFIER>` to determine the energy obtained from calculation you ran.
This time you will need to use the identifier of the output `TrajectoryData` of the calculation, with link name `output_trajectory`.
As you might have realized, the difference now is that the whole series of values of the energy calculated after each ionic step are stored.
Of course, as we simply ran an `scf` calculation, there is only one value here, but as an exercise, you can restart the calculation with:

```{code-block} python

parameters['CONTROL']['calculation'] = 'vc-relax'

```

And once again check the `TrajectoryData` output node with link name `output_trajectory`.

The output of calculation jobs can also be obtained via the `verdi shell`.
For example, note down the PK of the calculation so that you can load it in the `verdi shell` and check the total energy with the commands:

```{code-block} ipython

In [1]: calculation = load_node(<PK>)

```

Then get the energy of the calculation with the command:

```{code-block} ipython

In [2]: calculation.res.energy
Out[2]: -308.31214469484

```

You can also type

```{code-block} ipython

In [3]: calculation.res.

```

and then press `TAB` to see all the available results of the calculation.

Besides writing input files, running the software for you, storing the output files, and connecting it all together in your provenance graph, many AiiDA plugins will parse the output of your code and make output values of interest available through an output dictionary node (as depicted in the graph above).
In the case of the `aiida-quantumespresso` plugin this output node is available at `calculation.outputs.output_parameters` and you can access all the available attributes (not only the energy) using:

```{code-block} ipython

In [4]: calculation.outputs.output_parameters.attributes

```

While the name of this output dictionary node can be chosen by the plugin, AiiDA provides the "results" shortcut `calculation.res` that plugin developers can use to provide what they consider the result of the calculation (so, in this case, `calculation.res.energy` is just a shortcut to `calculation.outputs.output_parameters.attributes['energy']`).

:::{rubric} Footnotes

:::

[^f1]: In order to avoid duplication of KpointsData, you would first need to learn how to query the database, therefore we will ignore this issue for now.

[^f2]: A process is considered active if it is either `Created`, `Running` or `Waiting`. If a process is no longer active, but terminated, it will have a state `Finished`, `Killed` or `Excepted`.

[^f3]: The `parent_folder` input for reusing the remote working folder of a previous calculation is specific to the `aiida-quantumespresso` plugin, but similar patterns are used in other plugins.
  The `PwCalculation` `CalcJob` plugin will copy the `outdir` of the parent simulation into the appropriate location, where Quantum ESPRESSO's `pw.x` executable looks for wavefunctions, charge densities, etc.
  This allows to keep the checkpoint files (which may be large) on the remote machine, while still recording the provenance of the new calculation in the AiiDA graph as: `parent_calculation --> remote_folder --> restart_calculation`.

[^f4]: We purposefully do not provide advanced commands for crystal structure manipulation in AiiDA, because python packages that accomplish such tasks already exist (such as ASE or pymatgen).
