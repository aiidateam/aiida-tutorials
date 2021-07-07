
(workflows-realworld)=

# Real-world example - Equation of state

Now that we've discussed the concepts of workflows in AiiDA using some basic examples, let's move on to something more interesting: calculating the equation of state of silicon.
An equation of state consists of calculating the total energy (E) as a function of the unit cell volume (V).
The minimal energy is reached at the equilibrium volume.
Equivalently, the equilibrium is defined by a vanishing pressure: {math}`p=-dE/dV`.
In the vicinity of the minimum, the functional form of the equation of state can be approximated by a parabola.
Such an approximation greatly simplifies the calculation of the bulk modulus, which is proportional to the second derivative of the energy (a more advanced treatment requires fitting the curve with, e.g., the Birch–Murnaghan expression).

:::{note}

The approach of the workflows in this module is not necessarily the optimal one!
However, the material is meant be instructive in understanding how to write work chains before you get started on your own.

:::

## Importing a structure from the COD

First, we'll need the structure of bulk silicon.
Instead of loading the structure from a `.cif` file, we show you how to load it from the Crystallography Open Database (COD).
Similar to data, calculation, and workflows, a database importer class can be loaded using the corresponding factory and entry point:

```{code-block} ipython

In [1]: from aiida.plugins import DbImporterFactory
   ...: CodDbImporter = DbImporterFactory('cod')

```

Now that we have the `CodDbImporter` class loaded, let's initialize an instance of the class:

```{code-block} ipython

In [2]: cod = CodDbImporter()

```

Next, we'll load the conventional unit cell of silicon, which has the COD id = 1526655:

```{code-block} ipython

In [3]: results = cod.query(id='1526655')
   ...: structure = results[0].get_aiida_structure()

```

Let's have a look at the `structure` variable:

```{code-block} ipython

In [4]: structure
Out[4]: <StructureData: uuid: 3d4ab03b-4149-4c31-88ef-180640f1f79a (unstored)>

```

We can see that the `structure` variable contains an instance of `StructureData`, but that it hasn't been stored in the AiiDA database.
Before doing so, let's double check that we have the right structure.
The `StructureData` class has several methods for obtaining information about the structure, such as `get_formula()`:

```{code-block} ipython

In [5]: structure.get_formula()
Out[5]: 'Si8'

```

That looks alright!
Let's store the node in the database:

```{code-block} ipython

In [6]: structure.store()
Out[6]: <StructureData: uuid: 3d4ab03b-4149-4c31-88ef-180640f1f79a (pk: 2804)>

```

## Rescaling the structure

For the equation of state you need another function that takes as input a `StructureData` object and a rescaling factor, and returns a `StructureData` object with the rescaled lattice parameter:

:::{margin}

{{ download }} {download}`Download the Python file! <include/code/realworld/rescale.py>`

:::

```{literalinclude} include/code/realworld/rescale.py
:language: python
```

This calculation function should be familiar to you from the {ref}`section on calculation function from the work functions module <workflows-workfunction-calcfunction>`.
Copy the code snippet above into a Python file, (e.g. `rescale.py`).
Next, open a `verdi shell`, load the `StructureData` node for silicon that you just stored, and generate a set of rescaled structures:

:::{margin}
Don't forget to replace the `<PK>` with that of your structure!
:::

```{code} ipython

In [1]: from rescale import rescale
   ...:
   ...: structure = load_node(pk=<PK>)  # If you still have the structure variable loaded, not need to load it again!
   ...: rescaled_structures = [rescale(structure, Float(factor)) for factor in (0.98, 0.99, 1.0, 1.01, 1.02)]

```

:::{note}

Notice that we have supplied the `rescale` method with two inputs that are both `Data` nodes: `StructureData` and `Float`.

:::

Now let's check the contents of the `rescaled_structures` variable:

```{code-block} ipython

In [2]: rescaled_structures
Out[2]:
[<StructureData: uuid: a1801ec8-35c8-4e1d-bbbf-36fbcef7d034 (pk: 2807)>,
 <StructureData: uuid: e2714063-63ce-492b-b003-b05323c70a22 (pk: 2810)>,
 <StructureData: uuid: 842aa50b-c6ce-429c-b089-96a1480cea9f (pk: 2813)>,
 <StructureData: uuid: 78bb6406-ec94-425d-a396-9a7cc7ffbacf (pk: 2816)>,
 <StructureData: uuid: 8f9c876e-d5e9-4018-9bb5-9e52c335fe0c (pk: 2819)>]

```

Notice that all of the `StructureData` nodes of the rescaled structures are already stored in the database with their own PK.
This is because they are the output nodes of the `rescale` calculation function.

(intro-workflow-eos-work-functions)=

## Equation of state work function

Now that we have our initial structure and a calculation function for rescaling the unit cell, we can put this together with the `PwCalculation` from the session on running calculations to calculate the equation of state.
For this part of the tutorial, we provide some utility functions that get the correct pseudopotentials and generate the input for a `PwCalculation`:

{{ download }} {download}`Download the utils.py file!<include/code/realworld/utils.py>`

These inputs are defined in a similar way to how you have prepared them in the {ref}`running computations<calculations-basics>` hands on.

:::{important}

The workflow scripts for the rest of this section rely on the methods in `rescale.py` and `utils.py` to function.
Make sure the Python files with the workflows are in the same directory as these two files.

:::

In the script shown below, a work _function_ has been implemented that generates a scaled structure and calculates its energy for a range of 5 scaling factors:

```{literalinclude} include/code/realworld/eos_workfunction.py
:language: python

```

Copy the contents of this script into a Python file, for example `eos_workfunction.py` , or simply {download}`download <include/code/realworld/eos_workfunction.py>` it.
Next, let's open up a `verdi shell` and run the equation of state workflow. In case you no longer have it stored, load the silicon structure you imported earlier using its PK:

```{code-block} ipython

In [1]: structure = load_node(pk=<PK>)

```

Next, load the Quantum ESPRESSO pw code you used previously to run calculations:

```{code-block} ipython

In [2]: code = load_code('pw@localhost')

```

To run the workflow, we also have to specify the label of the family of pseudopotentials as an AiiDA `Str` node:

```{code-block} ipython

In [3]: pseudo_family_label = Str('SSSP/1.1/PBE/efficiency')

```

Finally, we are ready to import the `run_eos()` work function and run it!

```{code-block} ipython

In [4]: from eos_workfunction import run_eos_wf
   ...: result = run_eos_wf(code, pseudo_family_label, structure)

```

The work function will start running and print one line of output for each scale factor used.
Once it is complete, the output will look something like this:

```{code-block} ipython

Running run_eos_wf<2821>
Running a scf for Si8 with scale factor 0.96
Running a scf for Si8 with scale factor 0.98
Running a scf for Si8 with scale factor 1.0
Running a scf for Si8 with scale factor 1.02
Running a scf for Si8 with scale factor 1.04

```

Similar to the simple arithmetic work function run in the {ref}` work function module <workflows-workfunction>`, running the `eos_wf` work function means that the Python interpreter will be blocked during the whole workflow.
In this case, this will take the time required to launch the calculations, the actual time needed by Quantum ESPRESSO to perform the calculation and the time taken to retrieve the results.
If you interrupt the workflow at any point, you will experience some unpleasant consequences: intermediate calculation results are potentially lost and it is extremely difficult to restart a workflow from the exact place where it stopped.
This is exactly the motivation for writing such a workflow as a _work chain_.

That said, we can still have a look at the result!

```{code-block} ipython

In [5]: result
Out[5]:
<Dict: uuid: 4a8cdde5-a2ff-4c97-9a13-28096b1d9b91 (pk: 2878)>

```

We can see that the work function returns a `Dict` node with the results for the equation of state.
Let's have a look at the contents of this node:

```{code-block} ipython

In [6]: result.get_dict()
Out[6]:
{'eos': [[137.84870014835, -1240.4759003187, 'eV'],
  [146.64498086438, -1241.4786547651, 'eV'],
  [155.807721341, -1242.0231198534, 'eV'],
  [165.34440034884, -1242.1847659475, 'eV'],
  [175.26249665852, -1242.0265883524, 'eV']]}

```

We can see that the dictionary contains the volume, calculated energy and its units for each scaled structure.
Of course, this information is much better represented with a graph, so let's plot the equation of state and fit it with a Birch-Murnaghan equation.
For this purpose, we have provided the `plot_eos` script in the `utils.py` file that takes the PK of the `run_eos_wf` work function as an input and plots the equation of state:

```{code-block} ipython

In [7]: from utils import plot_eos
   ...: plot_eos(<PK>)

```

(workflows-writing-workchains-eos-workchain)=

## Submitting the workflow: Workchains

Clearly, when writing workflows that involve the use of an *ab initio* code like Quantum ESPRESSO, it is better to use a work chain.
Below you can find an **incomplete** snippet for the corresponding `EquationOfState` work chain.
It is almost completely implemented, all that it is missing is its `define` method.

```{code-block} python
# -*- coding: utf-8 -*-
"""Equation of State WorkChain."""
from aiida.engine import WorkChain, ToContext, calcfunction
from aiida.orm import Code, Dict, Float, Str, StructureData, load_group
from aiida.plugins import CalculationFactory

from rescale import rescale
from utils import generate_scf_input_params

PwCalculation = CalculationFactory("quantumespresso.pw")
scale_facs = (0.96, 0.98, 1.0, 1.02, 1.04)
labels = ["c1", "c2", "c3", "c4", "c5"]


@calcfunction
def get_eos_data(**kwargs):
    """Store EOS data in Dict node."""
    eos = [
        (result.dict.volume, result.dict.energy, result.dict.energy_units)
        for label, result in kwargs.items()
    ]
    return Dict(dict={"eos": eos})


class EquationOfState(WorkChain):
    """WorkChain to compute Equation of State using Quantum ESPRESSO."""

    @classmethod
    def define(cls, spec):
        """Specify inputs and outputs."""
        # ADD THE DEFINE METHOD

    def run_eos(self):
        """Run calculations for equation of state."""
        # Create basic structure and attach it as an output
        structure = self.inputs.structure

        calculations = {}

        pseudo_family = load_group(self.inputs.pseudo_family_label.value)

        for label, factor in zip(labels, scale_facs):

            rescaled_structure = rescale(structure, Float(factor))
            inputs = generate_scf_input_params(
                rescaled_structure, self.inputs.code, pseudo_family
            )

            self.report(
                "Running an SCF calculation for {} with scale factor {}".format(
                    structure.get_formula(), factor
                )
            )
            calcjob_node = self.submit(PwCalculation, **inputs)
            calculations[label] = calcjob_node

        # Ask the workflow to continue when the results are ready and store them in the context
        return ToContext(**calculations)

    def results(self):
        """Process results."""
        inputs = {
            label: self.ctx[label].get_outgoing().get_node_by_label("output_parameters")
            for label in labels
        }
        eos = get_eos_data(**inputs)

        # Attach Equation of State results as output node to be able to plot the EOS later
        self.out("eos", eos)

```

:::{warning}

WorkChains need to be defined in a **separate file** from the script used to run them.
E.g. save your WorkChain in `eos_workchain.py` and use `from eos_workchain import EquationOfState` to import the work chain in your script.

:::

Let's reiterate some differences between the `run_eos_wf` work function and the `EquationOfState`:

- Instead of using a `workfunction`-decorated function you need to define a class, inheriting from a prototype class called `WorkChain` that is provided by AiiDA in the `aiida.engine` module.

  ```{literalinclude} include/code/realworld/eos_workchain.py
  :language: python
  :lines: 25

  ```

- For the `WorkChain`, you need to split your main code into methods, which are the steps of the workflow.
  ```{literalinclude} include/code/realworld/eos_workchain.py
  :language: python
  :lines: 41-42

  ```
  ```{literalinclude} include/code/realworld/eos_workchain.py
  :language: python
  :lines: 68-69

  ```
  Here we have to decide where should the code be split for the equation of state workflow.
  The splitting points should be put where you would normally block the execution of the script for collecting results in a standard work function.
  For example here we split after submitting the `PwCalculation`'s.

- Any submission within the workflow should not call the normal `run` or `submit` functions, but `self.submit` to which you have to pass the process class, and a dictionary of inputs.
  ```{literalinclude} include/code/realworld/eos_workchain.py
  :language: python
  :lines: 62

  ```
  This submission in `run_eos` returns a `calcjob_node` that represents actual calculation, but at that point in time we have only just launched the calculation to the daemon and it is not yet completed.

- We need to add these `calcjob_node` to the context, so that in the next step of the workchain, when the calculations are in fact completed, we can access their results and continue the work.
  To do this, we can use the `ToContext` class:
  ```{literalinclude} include/code/realworld/eos_workchain.py
  :language: python
  :lines: 65-66

  ```
  This class takes a dictionary, where the values are the calcjob_nodes and the keys will be the names under which the corresponding calculations will be made available in the context when they are done.
  By `return`ing the `ToContext` object in `run_eos`, the work chain will implicitly wait for the results of all the `calcjob_node`s you have specified, and then call the next step *only when all calcjob_node have completed*.

- In the `results` step, the results are obtained from the `ctx` attribute through `self.ctx`:
  ```{literalinclude} include/code/realworld/eos_workchain.py
  :language: python
  :lines: 70-73

  ```
  Since the context is nothing more than a special kind of dictionary, you can also access the value of a context variable as `self.ctx.varname` instead of `self.ctx['varname']`.

- While in normal process functions you attach output nodes to the node by invoking the *return* statement, the work chain calls `self.out(link_name, node)` for each node you want to return.
  An advantage of this different syntax is that you can start emitting output nodes already in the middle of the execution, and not necessarily at the very end as it happens for normal functions (`return` is always the last instruction executed in a function or method).

::: {note}

  Once you have called `self.out(link_name, node)` on a given `link_name`, you can no longer call `self.out()` on the same `link_name`: this will raise an exception.

:::

### Exercise

As an exercise, try to complete the `define` method.
In this method you specify the main information on the workchain, in particular:

- The *inputs* that the workchain expects.
  This is obtained by means of the `spec.input()` method, which provides as the key feature the automatic validation of the input types via the `valid_type` argument.
  The same holds true for outputs, as you can use the `spec.output()` method to state what output types are expected to be returned by the workchain.
- The `outline` consisting in a list of 'steps' that you want to run, put in the right sequence.
  This is obtained by means of the method `spec.outline()` which takes as input the steps.
  *Note*: in this example we just split the main execution in two sequential steps, that is, first `run_eos` then `results`.

You can look at the `define` method of the `MultiplyAddWorkChain` {ref}`as an example <workflows-workchain-define>`.
If you get stuck, you can also download the complete script {download}`here <include/code/realworld/eos_workchain.py>`.

Once you have completed the define method, you can submit the `EquationOfState` to the daemon.
However, in this case the work chain will need to be globally importable so the daemon can load it.
To achieve this, the directory containing the work chain definition (i.e. the Python file) needs to be in the `PYTHONPATH` in order for the AiiDA daemon to find it.
When your `eos_workchain.py` is in e.g. `/home/aiida/workflows`, add a line `export PYTHONPATH=$PYTHONPATH:/home/max/workchains` to your `.bashrc` in the home directory.
Or, if the `.py` file is in your current directory:

```{code-block} bash

$ echo "export PYTHONPATH=\$PYTHONPATH:$PWD" >> ~/.bashrc

```

Next, it is **very important** to restart the daemon, so it can successfully set up the `PYTHONPATH` and find the `EquationOfState` work chain:

```{code-block} bash

$ verdi daemon restart --reset

```

Once the daemon has been restarted, it is time to *submit* the `EquationOfState` work chain from the `verdi shell`:

```{code-block} ipython

In [1]: from eos_workchain import EquationOfState
   ...: from aiida.engine import submit
   ...: submit(EquationOfState, code=load_code('pw@localhost'), pseudo_family_label=Str('SSSP/1.1/PBE/efficiency'), structure=load_node(pk=<PK>))
Out[1]: <WorkChainNode: uuid: 9e5c7c48-a47c-49fc-a8ab-fff081f250ee (pk: 665) (eos.workchain.EquationOfState)>

```

Note that similar as for the `MultiplyAddWorkChain`, the `submit` function returns the `WorkChain` instance for our equation of state workflow.
Now, leave the verdi shell and check the status of the work chain with `verdi process list`.
Depending on what stage of the work chain you are in, you will see something like the following output:

```{code-block} bash

(aiida) max@quantum-mobile:~/wf_basic$ verdi process list
  PK  Created    Process label    Process State    Process status
----  ---------  ---------------  ---------------  ----------------------------------------------------
 346  26s ago    EquationOfState  ⏵ Waiting        Waiting for child processes: 352, 358, 364, 370, 376
 352  25s ago    PwCalculation    ⏵ Waiting        Monitoring scheduler: job state RUNNING
 358  25s ago    PwCalculation    ⏵ Waiting        Monitoring scheduler: job state RUNNING
 364  24s ago    PwCalculation    ⏵ Waiting        Monitoring scheduler: job state RUNNING
 370  24s ago    PwCalculation    ⏵ Waiting        Monitoring scheduler: job state RUNNING
 376  23s ago    PwCalculation    ⏵ Waiting        Monitoring scheduler: job state RUNNING

Total results: 6

Info: last time an entry changed state: 20s ago (at 21:00:35 on 2020-06-07)

```

:::{note}

If you run into issues, it might be helpful to have a look at the {ref}`debugging module <workflows-debugging>`.

:::
