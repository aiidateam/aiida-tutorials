(quantum-espresso-run-workflows)=

# Running workflows

AiiDA can help you run individual calculations, but it is really designed to help you run workflows that involve several of them, while automatically keeping track of the provenance for full reproducibility.

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


## Submitting a work chain

In order to run this work chain, we will again open the `verdi shell`.
We will then load the work chain using its entry point and the `WorkflowFactory`:

```{code-block} ipython

In [1]: PwBandsWorkChain = WorkflowFactory('quantumespresso.pw.bands')

```

Setting up the inputs one by one as we did for the pw.x calculation in the previous section can be quite tedious.
Instead, we are going to use one of the protocols that has been set up for the workflow.
To do this, all we need to provide is the code and initial structure we are going to run:

:::{margin}
Replace `<CODE_PK>` and `<STRUCTURE_PK>` with those of the code and structure you used in the base module of this section.
:::

```{code-block} ipython

In [2]: code = load_code(<CODE_PK>)
   ...: structure = load_node(<STRUCTURE_PK>)

```

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
We will now see how to follow its execution and check the results.

## Monitoring the process

If you want to check the status of the workflow, you can exit the `verdi shell` and run `verdi process list` just like you did for calculations:

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

Another way of getting information on the processes of a workchain in a way that shows the *hierarchical* overview of the calls is by running `verdi process status`.
If your workchain is still running, you will get a partial output compared to the one shown below:

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


## Displaying the results

Once the work chain has finished running, use `verdi process show <PK>` to inspect the `PwBandsWorkChain` and find the PK of its `band_structure` output.
We can also plot the band structure using the `verdi shell`:

```{code-block} console

$ verdi data bands export --format mpl_pdf --output band_structure.pdf <PK>

```

Use the `evince` command or the JupyterHub file manager to open the `band_structure.pdf` file.
It should look similar to the one shown here:

:::{figure} include/images/si_bands.png
:width: 100%

Band structure computed by the `PwBandsWorkChain`.

:::

:::{important} **What we learnt**

 - Work chains can be prepared from a builder and submitted just like calculations.
 - The method `get_builder_from_protocol()` can return a pre-populated builder from minimal inputs.
 - In addition to `verdi process list`, you can see a hierarchical overview of a workflow by using `verdi process status`

:::
