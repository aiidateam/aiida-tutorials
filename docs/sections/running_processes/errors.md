(calculations-errors)=

# Troubleshooting

In this section we will intentionally introduce some bad input parameters when setting up our calculation.
This will allow us to illustrate how to manually debug problems that might arise while managing your computations with AiiDA.
You will learn where to look for the information of the errors and the steps you need to take to correct the issue.
In later tutorial sections you can then learn how to systematize this error handling when designing complex workflows.

:::{attention}

In the next subsection, you will need to set up a `calcjob` and then `run` or `submit` it to explore its results.
You will have to do some parts of this procedure on your own, including the creation and manipulation of `StructureData`, `UpfData` ([pseudopotentials](<https://en.wikipedia.org/wiki/Pseudopotential>)), and `KpointsData` nodes.

Moreover, you are assumed to already have installed and configured the `pw.x` code from Quantum ESPRESSO and its corresponding AiiDA plugin (`aiida-quantumespresso`).

If you are not sure how to do this, please first go through the previous tutorial section on {ref}`running computations<calculations-basics>`.

:::

## Calculation setup

The first step for this will be to set up a calculation for the `pw.x` code of the Quantum ESPRESSO package.
You will do so by loading and configuring the builder for the corresponding plugin.
Remember that you can run `verdi code list` to check what codes you have available and their information.

```{code-block} ipython

In [1]: code_pw = load_code(<CODE_PK>)
   ...: builder = code_pw.get_builder()

```

You will need to set the rest of the inputs by yourself, the most critical being `structure`, `kpoints`, `pseudos` and the `resources` options under the builder's `metadata`.
An incomplete example of how to set these parameters are shown below.

```{code-block} ipython

In [2]: builder.structure = ...
   ...: builder.kpoints = ...
   ...: builder.pseudos = ...
   ...: builder.metadata.options.resources = {'num_machines': 1}

```

:::{attention}

The `resources` provided above will work for a locally hosted code, which should typically be the case for this tutorial.
If you are running these tests on a cluster, you may need to set up account permissions or other options (you can consult the section for [schedulers](https://aiida.readthedocs.io/projects/aiida-core/en/latest/topics/schedulers.html) of the AiiDA documentation for further information).

:::

For the `structure` you can download the following {download}`silicon crystal<include/data/Si.cif>` and import it into your database.
If you have already done so previously (as it is used in other tutorial sections), you may want to use that pre-existing node instead of saving a new node with repeated information.
To do so you may search for its PK by running `verdi data core.structure list` and then use the function `load_node()` to retrieve it.

For the `pseudos` (or [pseudopotentials](https://en.wikipedia.org/wiki/Pseudopotential)), you can use the `SSSP/1.3/PBE/efficiency` family of the `aiida-pseudo` package.
If you already have it installed, it is enough to use the `load_group()` function and then the `get_pseudos()` method of the loaded pseudo group.

The set of `kpoints` can be simply created by using the methods of the `KpointsData` node class to define a `2x2x2` mesh and store it in a new node.

The last thing you need to specify are the input parameters, for which you will be using use the following content:

```{code-block} ipython

In [3]: parameters_dictionary = {
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

This dictionary is almost a valid input for Quantum ESPRESSO, except for an invalid key `mickeymouse`.
By default, the AiiDA plugin will simply pass your input to the code *without* doing any validation, but when Quantum ESPRESSO receives the unrecognized keyword it will stop and throw an error.

We have also introduced a combination of a very high accuracy (`'conv_thr': 1.e-14`) coupled with a very low maximum number of self consistent iterations (`'electron_maxstep': 3`).
This means that even if you eliminate the invalid key, the calculation will not converge and will not be successful, despite there not being any other mistake in the `parameters_dictionary`.

Finally, wrap the standard Python dictionary `parameters_dictionary` in an AiiDA `Dict` node, and set it as the builder's `parameters` input:

```{code-block} ipython

In [4]: builder.parameters = Dict(parameters_dictionary)

```

This wrapping is necessary for AiiDA to include it in the database and therefore the provenance graph.

## Simulating submissions

In order to check which input files AiiDA creates, we can perform a *dry run* of the submission process.
Let's tell the builder that we want a dry run and that we do not want to store the provenance of the dry run:

```{code-block} ipython

In [5]: builder.metadata.dry_run = True
   ...: builder.metadata.store_provenance = False

```

It is time to run the calculation through the created builder:

```{code-block} ipython

In [6]: from aiida.engine import run
   ...: run(builder)

```

:::{important}

Since we'll be correcting the builder later, don't exit the `verdi shell`, else you'll have to execute the commands again.
Instead, open a new terminal to follow the instructions below.

:::

This creates a folder of the form `submit_test/[date]-0000[x]` in the current directory.
The folder contains all the inputs as they would be used by AiiDA to run the code in the target computer.
You can open a second terminal and do the following quick checks before continuing:

* open the input file `aiida.in` within this folder
* compare it to the input data nodes you created earlier
* verify that the `pseudo` folder contains the needed pseudopotentials
* have a look at the submission script `_aiidasubmit.sh`

:::{note}

The files created by a dry run are only intended for inspection and there is no point in applying any correction to them directly.
AiiDA will re-create the input files from the input nodes at the time of any subsequent submission, so you have to make sure that it is those input nodes that have the correct content.

:::

## Troubleshooting calculations

Now that we have inspected the input files and convinced ourselves that Quantum ESPRESSO will have all the information it needs, let's revert the following values in the builder to their defaults:

```{code-block} ipython

In [7]: builder.metadata.dry_run = False
   ...: builder.metadata.store_provenance = True

```

And submit the calculation properly:

```{code-block} ipython

In [8]: from aiida.engine import submit
   ...: calculation = submit(builder)

```

You can now check the calculation status from the command line:

```{code-block} console

$ verdi process list -a -p1
  PK  Created    Process label    Process State     Process status
----  ---------  ---------------  ----------------  ----------------
2060  5m ago     PwCalculation    ⏹ Finished [305]
...
# Anything but [0] after the Finished state signals a failure

```

Your calculation should end up in a `Finished` state, but in this case the _exit code_ of the calculation, found after the `Finished` state, is `[305]` instead of zero (`[0]`).
This indicates that the process did not complete successfully, which was expected since we used an invalid key in the input parameters.

:::{note}

If the daemon is not running, the calculation will remain in the `Created` state until you start it by executing `verdi daemon start` in the command line.

:::

Situations like this happen frequently in real life, so AiiDA provides tools to help you trace back to the source of the problem and correct it.


### Checking the logs

First start by using `verdi process show` to display a more detailed summary of the process:

```{code-block} console

$ verdi process show <PK>

```

```{code-block} bash
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

The last part of the output alerts you to the fact that there are some log messages waiting for you, if you run `verdi process report <PK>`.

If you read the report, you will see that it says that the output files could not be parsed.
In this case you can also try inspecting directly the output file of PWscf.

```{code-block} console

$ verdi calcjob outputcat <PK> | less

```

You will see an error message complaining about the `mickeymouse` line in the input:

```{code-block}
     Reading input from aiida.in

 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
     Error in routine  read_namelists (1):
      bad line in namelist &system: "  mickeymouse =   2.4000000000d+02" (error could be in the previous line)
 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

     stopping ...
```

### Checking the inputs

To verify and/or further investigate any information gathered by looking at the logs and outputs, it is sometimes convenient to take a look at the inputs used.
Similar to when we tried the dry run, we can also inspect the input files that AiiDA made to run the *actual* calculation.
We can first check the content of the calculation folder by running:

```{code-block} console

$ verdi calcjob inputls <PK> -c

```

This will list the files and subfolders inside of the input directory (`-c` prints folders in color).
You can also check the content of the input file with:

```{code-block} console

$ verdi calcjob inputcat <PK> | less

```

Again we see that, in effect, the `mickeymouse` keyword is effectively being used inside of the input file.
Having verified this in mutiple ways, let's now correct our input `parameters_dictionary` by leaving out the invalid key and see if our calculation succeeds:

```{code-block} ipython

In [9]: parameters_dictionary = {
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
   ...: builder.parameters = Dict(parameters_dictionary)
   ...: calculation = submit(builder)

```

Use `verdi process list -a -p1` to verify that the error code is different now.
You can check again the outputs and the reports with the tools explained in this section and try to fix it yourself before going on to the next.

:::{note}

Curious which exit codes are defined for the `PwCalculation` plugin?
You can see all exit codes for a calculation job using the `verdi plugin list` command:

```{code-block} console

verdi plugin list aiida.calculations quantumespresso.pw

```

:::


## Restarting calculations

It turns out that your last calculation did not converge because we stopped the self-consistency iteration cycle before it converged (by only setting a max of 3 cycles).
In this simple case, you could just re-run the calculation from scratch with a sufficient number of iterations and it would solve the problem, but for expensive procedures (including a structural relaxation or molecular dynamics) you may instead want to run a restart from the latest calculation to save time.

For this purpose, `CalcJobNode` provides the `get_builder_restart()` method.
This is similar to the `get_builder()` method of the `Code` or of the `Process` class used above, but with all inputs already pre-populated from those of the original calculation.

Let us load the node of the calculation job that we want to restart in a `verdi shell` and create a new builder from it:

```{code-block} ipython

In [10]: failed_calculation = load_node(<PK>)
    ...: restart_builder = failed_calculation.get_builder_restart()

```

Type `restart_builder` and press Enter to verify that all inputs have already been set to those that were used for the original calculation.
Let's give the new calculation some more steps in the SCF cycle in order to let it converge:

```{code-block} ipython

In [11]: parameters = restart_builder.parameters.get_dict()
    ...: parameters['ELECTRONS']['electron_maxstep'] = 80

```

:::{important}

Remember that nodes are immutable: once they are stored in the database, their content can no longer be modified.
If you need to do a correction like this one, you can't do it directly on the node: you have to take its content, modify that, and then use that to create a new corrected node.

:::

The `aiida-quantumespresso` plugin supports restarting a calculation by setting the corresponding `restart_mode` and attaching the remote working directory of the previous calculations as the `parent_folder` input:

```{code-block} ipython

In [12]: parameters['CONTROL']['restart_mode'] = 'restart'
    ...: restart_builder.parent_folder = failed_calculation.outputs.remote_folder
    ...: restart_builder.parameters = Dict(parameters)

```

:::{note}

The `parent_folder` input for reusing the remote working folder of a previous calculation is specific to the `aiida-quantumespresso` plugin, but similar patterns are used in other plugins.
The `PwCalculation` `CalcJob` plugin will copy the `outdir` of the parent simulation into the appropriate location, where Quantum ESPRESSO's `pw.x` executable looks for wavefunctions, charge densities, etc.
This allows to keep the checkpoint files (which may be large) on the remote machine, while still recording the provenance of the new calculation in the AiiDA graph as: `parent_calculation --> remote_folder --> restart_calculation`.

:::

Finally, let's label this calculation as a restarted one and submit the new calculation:

```{code-block} ipython

In [13]: from aiida.engine import submit
    ...: restart_builder.metadata.label = 'Restart from PwCalculation<{}>'.format(failed_calculation.pk)
    ...: calcjob_node = submit(restart_builder)

```

Inspect the restarted calculation to verify that, this time, it completes successfully.
You should see a "Finished" status with exit code zero (`0`) when running `verdi process list - a -p1`.

:::{important} **Key takeaways**

 - When a process fails, it will return a non-zero **exit code**.
 - The logs of any process can be shown using `verdi process report`.
   More clues of what went wrong in a failed calculation can be obtained by exploring the output files using `verdi calcjob outputcat`.
 - A fully populated builder with the same inputs can be obtained with the `get_builder_restart()` method of any calcjob node.

:::
