---
myst:
   substitutions:
     seekpath: "[SeeK-path](https://www.materialscloud.org/work/tools/seekpath)"
---

(quantum-espresso-run-workflows)=

# Running workflows

AiiDA can help you run individual calculations, but it is really designed to help you run workflows that involve several sub-processes, while automatically keeping track of the provenance for full reproducibility.

To see all currently available workflows in your installation, you can run the following command:

```{code-block} console

$ verdi plugin list aiida.workflows

```

We are going to run the `PwBandsWorkChain` workflow of the `aiida-quantumespresso` plugin.
You can see it on the list as `quantumespresso.pw.bands`, which is the *entry point* of this work chain.
This is a fully automated workflow that will:

1. Run a calculation on the cell to relax both the cell and the atomic positions (`vc-relax`).
2. Refine the symmetry of the relaxed structure, and find a standardized cell using {{ seekpath }}.
3. Run a self-consistent field calculation on the refined structure.
4. Run a band structure calculation at a fixed Kohn-Sham potential along a standard path between high-symmetry k-points determined by {{ seekpath }}.


## Submitting a work chain

In order to run this work chain, open the `verdi shell` and load the work chain using its entry point and the `WorkflowFactory`:

```{code-block} ipython

In [1]: PwBandsWorkChain = WorkflowFactory('quantumespresso.pw.bands')

```

Setting up the inputs one by one as we did for the pw.x calculation in the previous section can be quite tedious.
Instead, we are going to use one of the protocols that has been set up for the workflow.
To do this, all we need to provide is the code and initial structure we are going to run:

:::{margin}

Replace `<CODE_PK>` and `<STRUCTURE_PK>` with the respective PKs of the code and structure you used in the base module of this section.

:::

```{code-block} ipython

In [2]: code = load_code(<CODE_PK>)
   ...: structure = load_node(<STRUCTURE_PK>)

```

:::{tip}

Forgot the PK of the `Code` or `StructureData` nodes?
Remember that you can use `verdi code list` and `verdi data structure list` to retrieve them!

:::

Next, we use the `get_builder_from_protocol()` method to obtain a prepopulated builder for the workflow:

```{code-block} ipython

In [3]: builder = PwBandsWorkChain.get_builder_from_protocol(code=code, structure=structure)

```

The default protocol uses the PBE exchange-correlation functional with suitable pseudopotentials and energy cutoffs from the [SSSP library version 1.1](https://www.materialscloud.org/discover/sssp/table/efficiency) we installed earlier.
Finally, we just need to submit the builder in the same way as we did for the calculation job:

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

:::{margin} {{ linux }} The `watch` command

The `watch` command in Linux executes a program periodically.
You can find out more about it [here](https://www.geeksforgeeks.org/watch-command-in-linux-with-examples/).

:::

:::{tip}

You can combine `verdi process status` with the `watch` command to continuously monitor the work chain status:

```{code-block} console
$ watch verdi process status <PK>
```

:::

The work chain might take a couple minutes to complete.
While you wait, you can try uploading your `.cif` file to the [SeeK-path tool on Materials Cloud](https://www.materialscloud.org/work/tools/seekpath).

:::{important}

The protocols and the `get_builder_from_protocol()` have only been fairly recently implemented in `aiida-quantumespresso`!
Be sure to check [the open issues on GitHub](https://github.com/aiidateam/aiida-quantumespresso/issues?q=is%3Aopen+is%3Aissue+label%3Atopic%2Fprotocol) related to this feature and run some tests before starting calculations in production.

:::

## Displaying the results

Once the work chain has finished running, use `verdi process show <PK>` to inspect the `PwBandsWorkChain` and find the PK of its `band_structure` output:

```{code-block} console
$ verdi process show <PK>
(...)
Outputs                PK  Type
-------------------  ----  -------------
band_parameters       352  Dict
band_structure        350  BandsData
primitive_structure   327  StructureData
scf_parameters        341  Dict
seekpath_parameters   325  Dict
(...)
```

Look for the PK of the output with link `band_structure` of type `BandsData`.
You can then plot the band structure using the `verdi shell`:

```{code-block} console

$ verdi data bands export --format mpl_pdf --output band_structure.pdf <PK>

```

Open the `band_structure.pdf` file with a viewer at your disposal.
It should look similar to the one shown here:

:::{figure} include/images/si_bands.png
:width: 100%

Band structure computed by the `PwBandsWorkChain`.

:::

## Customizing the inputs

Sometimes you may want to take advantage of the convenience of getting a prepopulated `builder` from the `get_builder_from_protocol()` method while still being able to customize some of the inputs.

The straightforward way to do this is by first obtaining the prepopulated `builder` and overriding its inputs with the desired values.
First use the `get_builder_from_protocol()` method to obtain the `builder`:

```{code-block} ipython

In [1]: PwBandsWorkChain = WorkflowFactory('quantumespresso.pw.bands')
   ...: code = load_code(<CODE_PK>)
   ...: structure = load_node(<STRUCTURE_PK>)
   ...: builder = PwBandsWorkChain.get_builder_from_protocol(code=code, structure=structure)

```

Next, have a look at the top-level `bands_kpoints_distance` input, used by the work chain to determine the linear density along the k-point path constructed using {{ seekpath }}:


```{code-block} ipython

In [2]: builder.bands_kpoints_distance
Out[2]: <Float: uuid: ab9eb3f6-7c61-4a6d-964c-5b55964e306c (unstored) value: 0.025>

```

Say you're only doing a test calculation, and want to increase the distance between the k-points.
Simply adapt the `Float` input to the desired value:

```{code-block} ipython

In [3]: builder.bands_kpoints_distance = Float(0.2)

```

and once again submit the `builder` to the AiiDA engine:

```{code-block} ipython

In [3]: from aiida.engine import submit
   ...: workchain_node = submit(builder)

```

Once the work chain is complete, you can have a look at the newly calculated band structure and compare it with the old one.

### Using the `overrides` argument

Adapting the `builder` might be a good option for small modifications, but for more complex and powerful customizations, the `get_builder_from_protocol()` method also offers the option to use the `overrides` argument.

:::{important}

For the following demonstration you will need the pseudo-dojo pseudopotentials you used for the exercises of the module on {ref}`running calculations <calculations-basics-structpseudo>`.
You can check if it is available and its label by running the following command in the terminal:

```{code-block} console

$ aiida-pseudo list
Label                                Type string                Count
-----------------------------------  -------------------------  -------
PseudoDojo/0.4/PBE/SR/standard/upf   pseudo.family.pseudo_dojo  72
SSSP/1.1/PBEsol/precision            pseudo.family.sssp         85
SSSP/1.1/PBEsol/efficiency           pseudo.family.sssp         85
SSSP/1.1/PBE/precision               pseudo.family.sssp         85
SSSP/1.1/PBE/efficiency              pseudo.family.sssp         85

```

If you see no pseudo-dojo entry, you can check the dropdown box below to see how to install them.

:::

:::{dropdown} **Installing the `pseudo-dojo` pseudopotentials**

You can use the tools of the `aiida-pseudo` package to easily install the pseudo-dojo pseudopotentials.
Since the default format for these pseudopotentials is _not_ UPF, you have to use the `-f, --pseudo-format` option to make sure they are installed in the correct format:

```{code-block} console
$ aiida-pseudo install pseudo-dojo -f upf
Info: downloading selected pseudopotentials archive...  [OK]
Info: downloading selected pseudopotentials metadata archive...  [OK]
Info: unpacking archive and parsing pseudos...  [OK]
Info: unpacking metadata archive and parsing metadata... [OK]
Success: installed `PseudoDojo/0.4/PBE/SR/standard/upf` containing 72 pseudopotentials
```

You should now be able to see these new pseudos when you execute `aiida-pseudo list`.

:::

Overrides allow access to some of the underlying construction features of internal methods, such as the `pseudo_family` input of the `PwBaseWorkChain`s launched by the `PwBandsWorkChain`:

```{code-block} ipython

In [2]: pseudo_family = "PseudoDojo/0.4/PBE/SR/standard/upf"
   ...: overrides = {
   ...:     'relax': {'base': {'pseudo_family': pseudo_family}},
   ...:     'scf': {'pseudo_family': pseudo_family},
   ...:     'bands': {'pseudo_family': pseudo_family},
   ...: }
   ...: builder2 = PwBandsWorkChain.get_builder_from_protocol(code=code, structure=structure, overrides=overrides)

```

By investigating the inputs, you will notice that not only the `pseudos` inputs in `builder['bands']['pw']`, `builder['scf']['pw']` and `builder['relax']['base']['pw']` are different, but also the `ecutwfc` and `ecutrho` have been adapted to the hints provided by [the Pseudo-dojo library](http://www.pseudo-dojo.org/):


```{code-block} ipython

In [3]: builder['scf']['pw']['parameters']['SYSTEM']
Out[3]:
{'nosym': False,
 'occupations': 'smearing',
 'smearing': 'cold',
 'degauss': 0.01,
 'ecutwfc': 30.0,
 'ecutrho': 240.0}

In [4]: builder2['scf']['pw']['parameters']['SYSTEM']
Out[4]:
{'nosym': False,
 'occupations': 'smearing',
 'smearing': 'cold',
 'degauss': 0.01,
 'ecutwfc': 36.0,
 'ecutrho': 144.0}

```

As a final exercise, run the `PwBandsWorkChain` with the pseudo-dojo pseudos, and compare the resulting band structure with the one obtained using the [SSSP library version 1.1](https://www.materialscloud.org/discover/sssp/table/efficiency).

:::{important} **Key takeaways**

 - Work chains can be prepared from a builder and submitted similar to calculations.
 - The method `get_builder_from_protocol()` can return a pre-populated builder from minimal inputs.
 - In addition to `verdi process list`, you can see a hierarchical overview of a workflow by using `verdi process status`.
 - You can customize the builder returned by `get_builder_from_protocol()` by providing the `overrides` optional argument.

:::

Even after only running a couple of work chains, you can already see that it becomes more and more difficult to find the data that you are looking for.
In the {ref}`"Organising your data" module <data-groups>`, you will learn how to use `Group`s to keep your database more tidy.
