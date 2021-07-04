
## (Optional section) Comments

AiiDA offers the possibility to attach comments to a any node, in order to be able to remember more easily its details.
Node with UUID prefix `ce81c420` should have no comments, but you can add a very instructive one by typing in the terminal:

```{code-block} console

$ verdi node comment add "vc-relax of a BaTiO3 done with QE pw.x" -N <IDENTIFIER>

```

Now, if you ask for a list of all comments associated to that calculation by typing:

```{code-block} console

$ verdi node comment show <IDENTIFIER>

```

the comment that you just added will appear together with some useful information such as its creator and creation date.
We let you play with the other options of `verdi node comment` command to learn how to update or remove comments.

===

# Running workflows

AiiDA can help you run individual calculations, but it is really designed to help you run workflows that involve several calculations, while automatically keeping track of the provenance for full reproducibility.

To see all currently available workflows in your installation, you can run the following command:

```{code-block} console

$ verdi plugin list aiida.workflows

```

We are going to run the `PwBandsWorkChain` workflow of the `aiida-quantumespresso` plugin.
You can see it on the list as `quantumespresso.pw.bands`, which is the *entry point* of this work chain.
This is a fully automated workflow that will:

1. Run a calculation on the cell to relax both the cell and the atomic positions (`vc-relax`).
2. Refine the symmetry of the relaxed structure, and find a standardized cell using [SeeK-path][seek-path].
3. Run a self-consistent field calculation on the refined structure.
4. Run a band structure calculation at a fixed Kohn-Sham potential along a standard path between high-symmetry k-points determined by [SeeK-path][seek-path].

In order to run it, we will again open the `verdi shell`.
We will then load the work chain using its entry point and the `WorkflowFactory`:

```{code-block} ipython

In [1]: PwBandsWorkChain = WorkflowFactory('quantumespresso.pw.bands')

```

Setting up the inputs one by one as we did for the pw.x calculation in the previous section can be quite tedious.
Instead, we are going to use one of the protocols that has been set up for the workflow.
To do this, all we need to provide is the code and initial structure we are going to run:

```{code-block}

In [2]: code = load_code(<CODE_PK>)
   ...: structure = load_node(<STRUCTURE_PK>)

```

Be sure to replace the `<CODE_PK>` and `<STRUCTURE_PK>` with those of the code and structure we used in the first section.
Next, we use the `get_builder_from_protocol()` method to obtain a prepopulated builder for the workflow:

```{code-block} ipython

In [3]: builder = PwBandsWorkChain.get_builder_from_protocol(code=code, structure=structure)

```

The default protocol uses the PBE exchange-correlation functional with suitable pseudopotentials and energy cutoffs from the [SSSP library version 1.1][sssp library version 1.1] we installed earlier.
Finally, we just need to submit the builder in the same way as we did for the calculation:

```{code-block} ipython

In [4]: from aiida.engine import submit
   ...: workchain_node = submit(builder)

```

And done!
Just like that, we have prepared and submitted an automated process to obtain the band structure of silicon.
If you want to check the status of the calculation, you can exit the `verdi shell` and run:

```{code-block} console

$ verdi process list
  PK  Created    Process label     Process State    Process status
----  ---------  ----------------  ---------------  ---------------------------------------
 113  19s ago    PwBandsWorkChain  ⏵ Waiting        Waiting for child processes: 115
 115  15s ago    PwRelaxWorkChain  ⏵ Waiting        Waiting for child processes: 118
 118  13s ago    PwBaseWorkChain   ⏵ Waiting        Waiting for child processes: 123
 123  11s ago    PwCalculation     ⏵ Waiting        Monitoring scheduler: job state RUNNING

Total results: 4

Info: last time an entry changed state: 8s ago (at 23:32:21 on 2021-02-09)

```

You may notice that `verdi process list` now shows more than one entry: indeed, there are a couple of calculations and sub-workflows that need to be run.
The total workflow should take about 5-10 minutes to finish.

While we wait for the workflow to complete, we can start learning about how to explore the provenance of an AiiDA database.

## Inspecting the work chain

Use `verdi process show <PK>` to inspect the `PwBandsWorkChain` and find the PK of its `band_structure` output.
Instead of relying on the explore tool, we can also plot the band structure using the `verdi shell`:

```{code-block} console

$ verdi data bands export --format mpl_pdf --output band_structure.pdf <PK>

```

Use the `evince` command or the JupyterHub file manager to open the `band_structure.pdf` file.
It should look similar to the one shown here:

:::{figure} include/images/si_bands.png
:width: 100%

Band structure computed by the `PwBandsWorkChain`.

:::

Finally, the `verdi process status` command prints a *hierarchical* overview of the processes called by the work chain:

```{code-block} console

$ verdi process status <PK>
PwBandsWorkChain<113> Finished [0] [7:results]
    ├── PwRelaxWorkChain<115> Finished [0] [3:results]
    │   ├── PwBaseWorkChain<118> Finished [0] [7:results]
    │   │   ├── create_kpoints_from_distance<119> Finished [0]
    │   │   └── PwCalculation<123> Finished [0]
    │   └── PwBaseWorkChain<132> Finished [0] [7:results]
    │       ├── create_kpoints_from_distance<133> Finished [0]
    │       └── PwCalculation<137> Finished [0]
    ├── seekpath_structure_analysis<144> Finished [0]
    ├── PwBaseWorkChain<151> Finished [0] [7:results]
    │   ├── create_kpoints_from_distance<152> Finished [0]
    │   └── PwCalculation<156> Finished [0]
    └── PwBaseWorkChain<164> Finished [0] [7:results]
        └── PwCalculation<167> Finished [0]

```

The bracket `[7:result]` indicates the current step in the outline of the `PwBandsWorkChain` (step 7, with name `result`).
The `process status` is particularly useful for debugging complex work chains, since it helps pinpoint where a problem occurred.

Congratulations on finishing the first part of the tutorial!
In the next section, we'll look at how to organize and query your data.

===

Imagine that we often perform a complex procedure (workflow) that involves many steps.
The workflow is always the same but the inputs may change.
For example, let us consider that the workflow consists of three calculations using three different codes where each subsequent code uses the output of the previous one:

1. Run code 1
2. Run code 2
3. Run code 3

When we do this by hand, we are actually doing many more steps than described above.
For example, we usually prepare the input parameters and check the outputs of each step.
Therefore, a more realistic description of the workflow could look like:

1. Prepare and check the input for code 1
2. Run code 1
3. Check the output from code 1
4. Prepare input for code 2
5. Run code 2
6. Check the output from code 2
7. Prepare input for code 3
8. Run code 3
9. Check the output from code 3
10. Parse and save selected data

Thus, in general, a careful scientist is doing many steps when performing a workflow by hand.
To automatize this process, we need to write a workflow that executes these steps.
Ideally, these workflows should be modular, so that they can be used as steps in the outline of more complex workflows.

In this module, you will learn step-by-step how to write workflows in AiiDA.

===

## Workflows in AiiDA

A workflow in AiiDA is a {ref}`process <topics:processes:concepts>` that calls other workflows and calculations and optionally *returns* data and as such can encode the logic of a typical scientific workflow.
Currently, there are two ways of implementing a workflow process:

* {ref}`work functions<topics:workflows:concepts:workfunctions>`
* {ref}`work chains<topics:workflows:concepts:workchains>`

The main difference between them is that *work functions* are completely executed by the AiiDA daemon, whereas  a *work chain* can submit calculation jobs that can be e.g. run through a scheduler that is periodically monitored by the daemon.
Furthermore, a work chain is split into steps which have checkpoints in between from which a work chain can be restarted in case the daemon is shut down.
Thus, *work functions* should be used for fast workflows that won't keep the AiiDA daemon very busy, otherwise, a *work chain* is in order.

:::{note}

For more details on the concept of a workflow, and the difference between a work function and a work chain, please see the corresponding {ref}`topics section<topics:workflows:concepts>` in the AiiDA documentation.

:::

Here we present a brief introduction on how to write both workflow types.

===

### Launching a work chain

To launch a work chain, you can either use the `run` or `submit` functions.
For either function, you need to provide the class of the work chain as the first argument, followed by the inputs as keyword arguments.
To make things a little easier, we have added these basic arithmetic functions to {}`aiida-core`, along with a set of entry points, so they can be loaded using a factory.
Start the `verdi shell` up and load the `MultiplyAddWorkChain` using the `WorkflowFactory`:

```{code-block} ipython

In [1]: MultiplyAddWorkChain = WorkflowFactory('arithmetic.multiply_add')

```

The `WorkflowFactory` is a useful and robust tool for loading workflows based on their *entry point*, e.g. `'arithmetic.multiply_add'` in this case.
Using the `run` function, or "running", a work chain means it is executed in the same system process as the interpreter in which it is launched:

```{code-block} ipython

In [2]: from aiida.engine import run
   ...: add_code = load_code(label='add@tutor')
   ...: results = run(MultiplyAddWorkChain, x=Int(2), y=Int(3), z=Int(5), code=add_code)

```

Alternatively, you can first construct a dictionary of the inputs, and pass it to the `run` function by taking advantage of [Python's automatic keyword expansion](<https://docs.python.org/3/tutorial/controlflow.html#unpacking-argument-lists>):

```{code-block} ipython

In [3]: inputs = {'x': Int(1), 'y': Int(2), 'z': Int(3), 'code': add_code}
   ...: results = run(MultiplyAddWorkChain, **inputs)

```

This is particularly useful in case you have a workflow with a lot of inputs.
In both cases, running the `MultiplyAddWorkChain` workflow returns the **results** of the workflow, i.e. a dictionary of the nodes that are produced as outputs, where the keys of the dictionary correspond to the labels of each respective output.

:::{note}

Similar to other processes, there are multiple functions for launching a work chain.
See the section on {ref}`launching processes for more details<topics:processes:usage:launching>`.

:::

Since *running* a workflow will block the interpreter, you will have to wait until the workflow is finished before you get back control.
Moreover, you won't be able to turn your computer or even your terminal off until the workflow has fully terminated, and it is difficult to run multiple workflows in parallel.
So, it is advisable to *submit* more complex or longer work chains to the daemon:

```{code-block} ipython

In [5]: from aiida.engine import submit
   ...:
   ...: add_code = load_code(label='add@tutor')
   ...: inputs = {'x': Int(1), 'y': Int(2), 'z': Int(3), 'code': add_code}
   ...:
   ...: workchain_node = submit(MultiplyAddWorkChain, **inputs)

```

Note that when using `submit` the work chain is not run in the local interpreter but is sent off to the daemon and you get back control instantly.
This allows you to submit multiple work chains at the same time and the daemon will start working on them in parallel.
Once the `submit` call returns, you will not get the result as with `run`, but you will get the **node** that represents the work chain:

```{code-block} ipython

In [6]: workchain_node
Out[6]: <WorkChainNode: uuid: 17fbe11e-b71b-4ffe-a08e-0d5e3b1ae5ed (pk: 2787) (aiida.workflows:arithmetic.multiply_add)>

```

Submitting a work chain instead of directly running it not only makes it easier to execute multiple work chains in parallel but also ensures that the progress of a work chain is not lost when you restart your computer.

:::{important}

In contrast to work chains, work *functions* cannot be submitted to the daemon, and hence can only be *run*.

:::

If you are unfamiliar with the inputs of a particular `WorkChain`, a convenient tool for setting up the work chain is the {ref}`process builder<topics:processes:usage:builder>`.
This can be obtained by using the `get_builder()` method, which is implemented for every `CalcJob` and `WorkChain`:

```{code-block} ipython

In [1]: from aiida.plugins import WorkflowFactory, DataFactory
   ...: Int = DataFactory('int')
   ...: MultiplyAddWorkChain = WorkflowFactory('arithmetic.multiply_add')
   ...: builder = MultiplyAddWorkChain.get_builder()

```

To explore the inputs of the work chain, you can use tab autocompletion by typing `builder.` and then hitting `TAB`.
If you want to get more details on a specific input, you can simply add a `?` and press enter:

```{code-block} ipython

In [2]: builder.x?
Type:        property
String form: <property object at 0x119ad2dd0>
Docstring:   {"name": "x", "required": "True", "valid_type": "<class 'aiida.orm.nodes.data.int.Int'>", "non_db": "False"}

```

Here you can see that the `x` input is required, needs to be of the `Int` type, and is stored in the database (`"non_db": "False"`).

Using the builder, the inputs of the `WorkChain` can be provided one by one:

```{code-block} ipython

In [3]: builder.code = load_code(label='add@tutor')
   ...: builder.x = Int(2)
   ...: builder.y = Int(3)
   ...: builder.z = Int(5)

```

Once the *required* inputs of the workflow have been provided to the builder, you can either run the work chain or submit it to the daemon:

```{code-block} ipython

In [4]: from aiida.engine import submit
   ...: workchain_node = submit(builder)

```

:::{note}

For more detail on the process builder, see the {ref}`corresponding topics section<topics:processes:usage:builder>`.

:::
