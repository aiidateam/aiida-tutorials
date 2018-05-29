Using the verdi command line
============================

This part of the tutorial will help you familiarize with the command
line utility <span>`verdi`</span>, one of the most common ways to
interact with AiiDA. <span>`verdi`</span> with its subcommands enables a
variety of operations such as inspecting the status of ongoing or
terminated calculations, showing the details of calculations, computers,
codes, or data structures, access the input and the output of a
calculation, etc. Similar to the `bash` shell, verdi command support Tab
compltion. Try right now to type <span>`verdi`</span> in a terminal and
tap Tab twice to have a list of subcommands. Whenever you need the
explanation of a command type <span>`verdi help`</span> or add
<span>`-h`</span> flag if you are using any of the <span>`verdi`</span>
subcommands. Finally, fields enclosed in angular brackets, such as
`<pk>`, are placeholders to be replaced by the actual value of that
field (an integer, a string, etc...).

The list of calculations
------------------------

Let us try our first <span>`verdi`</span> commands. Type in the terminal

```bash
verdi calculation list
```

(Note: the first time you run this command, it might take some seconds
as it is the first time you are accessing the database in the virtual
machine. Following calls will be faster). This will print the list of
ongoing calculations, which should be empty. The first output line
should look like

```bash
# Last daemon state_updater check: 0h:00m:18s ago (at 17:17:26 on 2016-05-31)
```

In order to print a list with all calculations that finished correctly
in the AiiDA database, you can use the <span>`-a/--all-states`</span>
and <span>`-A/--all-users`</span> flag as follows:

```bash
verdi calculation list –all-states –all-users
```

Another very typical option combination allows to get calculations in
*any* state (flag <span>`-a`</span>) d in the past
<span>`NUM`</span> days (<span>`-p <NUM>`</span>): e.g., for calculation
in the past 1 day: <span>`verdi calculation list -p1 -a`</span>.

Each row of the output identifies a calculation and shows several
information about it. For a more detailed list of properties, choose one
row by noting down its pk number and type in the terminal

```bash
verdi calculation show <pk>
```

The output depends on the specific pk chosen and should inform you about
the input nodes (e.g. initial structure, settings etc.), the output
nodes (e.g. output parameters, etc.). An example of RASPA calculation
(pk=3006) output is provided below

    -----------  ------------------------------------
    type         RaspaCalculation
    pk           3006
    uuid         b09ee4b0-8bfe-4083-9371-09b47bf98dce
    label
    description
    ctime        2018-05-07 01:31:29.906303+00:00
    mtime        2018-05-07 10:33:39.871720+00:00
    computer     [1] deneb-lsmo
    code         raspa
    -----------  ------------------------------------
    ##### INPUTS:
    Link label      PK  Type
    ------------  ----  -------------
    parameters    2757  ParameterData
    structure     2886  CifData
    ##### OUTPUTS:
    Link label           PK  Type
    -----------------  ----  -------------
    remote_folder      3314  RemoteData
    retrieved          1132  FolderData
    output_parameters  1131  ParameterData
    component_0        1130  ParameterData

A typical AiiDA graph
---------------------

Note that pk number shown in the examples may be different for your
database.

AiiDA stores in the database the inputs required by a calculation as
well as the its outputs.

![Dependency graph of a Raspa calculation.](/assets/2018_EPFL_molsim/raspa_sample_graph.png "Dependency graph of a Raspa calculation.")

You can create a similar graph for any calculation node by using the
utility <span>`verdi graph  <pk>`</span>. For example, before
you obtained information (in text form) for `pk=3006`. To visualize
similar information in graph(ical) form, run (replacing
<span>`<pk>`</span> with your number):

```bash
verdi graph  <pk>
```

This command creates the file <pk>.dot that can be rendered by means
of the utility <span>`dot`</span>. Convert it to PDF and have a look:

```bash
dot -Tpdf -o <pk>.pdf <pk>.dot 
evince <pk>.pdf
```

Spend some time to familiarize with the graph structure. Identify the
root node (highlighted in blue) and trace back the structure used as an
input. This is an example of a Raspa calculation. We will now inspect
the different elements of this graph.

Inspecting the nodes of a graph
-------------------------------

### ParameterData and Calculations

Now, let us have a closer look to the some of the nodes appearing in the
graph. Choose the node of the type `ParameterData` with input link name
`parameters` (ex. pk=2757) and type in the terminal:

```bash
verdi data parameter show <pk>
```

A `ParameterData` contains a dictionary (i.e., key–value pairs), stored
in the database in a format ready to be queried (we will learn how to
run queries later on in this tutorial). The command above will print the
content dictionary, containing the parameters used to define the input
file for the calculation. You can compare the dictionary with the
content of the raw input file to Raspa (that was d by AiiDA) via
the command

```bash
verdi calculation inputcat <pk>
```

where you substitute the pk of the calculation node (e.g. pk=3006).
Check the consistency of the parameters written in the input file and
those stored in the ParameterData node. Even if you don’t know the
meaning of the input flags of a Raspa calculation, you should be able to
see how the input dictionary has been converted into the input file.

The previous command just printed the content of the “default” input
file `simulation.input`. To see a list of all the files used to run a
calculation (input file, submission script, etc.) type instead

```bash
verdi calculation inputls <pk>
```

(Adding a `--color` flag allows you to easily distinguish files from
folders by a different coloring).

Once you know the name of the file you want to visualize, you can call
the <span>`verdi calculation inputcat`</span> command specifying the
path. For instance, to see the submission script, you can do:

```bash
verdi calculation inputcat <pk> -p ~a~iidasubmit.sh
```

### CifData

Now let us focus on CifData objects, such as node pk=2886 of the graph.
A CifData object contains a crystal structure and can be inspected
interactively using viewers like `jmol` or `vesta`. Type in the terminal

```bash
verdi data cif show –format jmol 2886
```

to show the selected structure.

### Codes and computers

Let us focus now on the nodes of type `code`. A code represents (in the
database) the actual executable used to run the calculation. Find the pk
of such a node in the graph and type

```bash
verdi code show <pk>
```

The command prints information on the plugin used to interface the code
to AiiDA, the remote machine on which the code is executed, the path of
its executable, etc. To have a list of all available codes type

```bash
verdi code list -a -A
```

Among the entries of the output you should also find the code just
shown.

Similarly, the list of computers on which AiiDA can submit calculations
is accessible by means of the command

```bash
verdi computer list -a
```

(<span>`-a`</span> shows all computers, also the one imported in your
database but that you did not configure, i.e., to which you don’t have
access). Details about each computer can be obtained by the command

```bash
verdi computer show <COMPUTERNAME>
```

Now you have the tools to answer the question:

What is the scheduler installed on the computer where the calculations
of the graph have run?

### Calculation results

The results of a calculation can be accessed directly from the
calculation node. Type in the terminal

```bash
verdi calculation res <pk>
```

which will print the output dictionary of the “scalar” results parsed by
AiiDA at the end of the calculation. Note that this is actually a
shortcut for

```bash
verdi data parameter show <pk2>
```

where `pk2` refers to the ParameterData node attached as an output of
the calculation node, with link name `output_parameters`.

By looking at the output of the command, what is the averate total
energy of the calculation having pk=3006?

One can access the component-specific output parameters in the same way
(using pk = 1130 that corresponds to the component 0, methane)

```bash
verdi data parameter show <pk2>
```

Similarly to what you did for the calculation inputs, you can access the
output files via the commands

```bash
verdi calculation outputls <pk>
```

and

```bash
verdi calculation outputcat -p <filename> <pk>
```

Use the latter to verify that the average total energy that you have
found in the last step has been extracted correctly from the output file
(Hint: filter the lines containing the string “Total energy”, e.g. using
`grep Total energy: -A 8 `, to isolate the relevant lines).

