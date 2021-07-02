
(workflows-realworld)=

# Real-world example - Equation of state

Now that we've discussed the concepts of workflows in AiiDA using some basic examples, let's move on to something more interesting: calculating the equation of state of silicon.
An equation of state consists of calculating the total energy (E) as a function of the unit cell volume (V).
The minimal energy is reached at the equilibrium volume.
Equivalently, the equilibrium is defined by a vanishing pressure: {math}`p=-dE/dV`.
In the vicinity of the minimum, the functional form of the equation of state can be approximated by a parabola.
Such an approximation greatly simplifies the calculation of the bulk modulus, which is proportional to the second derivative of the energy (a more advanced treatment requires fitting the curve with, e.g., the Birch–Murnaghan expression).

First, we'll need the structure of bulk silicon.
Instead of constructing the structure manually, we'll load it from the Crystallography Open Database (COD).
Similar to data, calculation, and worfklows, a database importer class can be loaded using the corresponding factory and entry point:

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

We can see that the `structure` variable contains an instance of `StructureData`, but that it hasn't been stored in the AiiDA database. Let's do that now:

```{code-block} ipython

In [5]: structure.store()
Out[5]: <StructureData: uuid: 3d4ab03b-4149-4c31-88ef-180640f1f79a (pk: 2804)>

```

For the equation of state you need another function that takes as input a `StructureData` object and a rescaling factor, and returns a `StructureData` object with the rescaled lattice parameter:

```{literalinclude} include/code/rescale.py
:language: python

```

Of course, this *regular* Python function won't be stored in the provenance graph, so we need to decorate it with the `calcfunction` decorator.
Copy the code snippet above into a Python file, (e.g. {download}`rescale.py <include/code/rescale.py>`), and add the `calcfunction` decorator to the `rescale` function.

Once the `rescale` function has been decorated, it's time to put it to the test!
Open a `verdi shell`, load the `StructureData` node for silicon that you just stored, and generate a set of rescaled structures:

```{code} ipython

In [1]: from rescale import rescale
   ...:
   ...: initial_structure = load_node(pk=2804)
   ...: rescaled_structures = [rescale(initial_structure, Float(factor)) for factor in (0.98, 0.99, 1.0, 1.1, 1.2)]

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

## Running the equation of state workflow

Now that we have our initial structure and a calculation function for rescaling the unit cell, we can put this together with the `PwCalculation` from the session on running calculations to calculate the equation of state.
For this part of the tutorial, we provide some utility functions that get the correct pseudopotentials and generate the input for a `PwCalculation` in {download}`common_wf.py <include/code/common_wf.py>`.
This is done in a similar way to how you have prepared the inputs in the {ref}`running computations<calculations-basics>` hands on.

:::{important}

The workflow scripts for the rest of this section rely on the methods in `rescale.py` and `common_wf.py` to function.
Make sure the Python files with the workflows are in the same directory as these two files.

:::

In the script shown below, a work function has been implemented that generates a scaled structure and calculates its energy for a range of 5 scaling factors:

```{literalinclude} include/code/eos_workfunction.py
:language: python

```

Copy the contents of this script into a Python file, for example `eos_workfunction.py` , or simply {download}`download <include/code/eos_workfunction.py>` it.
Next, let's open up a `verdi shell` and run the equation of state workflow. First, load the silicon structure you imported earlier using its PK:

```{code-block} ipython

In [1]: initial_structure = load_node(pk=2804)

```

Next, load the Quantum ESPRESSO pw code you used previously to run calculations:

```{code-block} ipython

In [2]: code = load_code('qe-6.5-pw@localhost')

```

To run the workflow, we also have to specify the family of pseudopotentials as an AiiDA `Str` node:

```{code-block} ipython

In [3]: pseudo_str = Str('SSSP')

```

Finally, we are ready to import the `run_eos()` work function and run it!

```{code-block} ipython

In [4]: from eos_workfunction import run_eos_wf
   ...: result = run_eos_wf(code, pseudo_str, initial_structure)

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

Let's have a look at the result!

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
For this purpose, we have provided the `plot_eos` script in the `common_wf.py` file that takes the PK of the work function as an input and plots the equation of state:

```{code-block} ipython

In [7]: from common_wf import plot_eos
   ...: plot_eos(2821)

```

:::{note}

This plot can take a bit of time to appear on your local machine with X-forwarding.

:::

(workflows-writing-workchains-eos-workchain)=

## Submitting the workflow: Workchains

Similar to the simple arithmetic work function above, running the `eos_wf` work function means that the Python interpreter will be blocked during the whole workflow.
In this case, this will take the time required to launch the calculations, the actual time needed by Quantum ESPRESSO to perform the calculation and the time taken to retrieve the results.
Perhaps you killed the calculation and you experienced the unpleasant consequences: intermediate calculation results are potentially lost and it is extremely difficult to restart a workflow from the exact place where it stopped.

Clearly, when writing workflows that involve the use of an *ab initio* code like Quantum ESPRESSO, it is better to use a work chain.
Below you can find an incomplete snippet for the `EquationOfState` work chain.
It is almost completely implemented, all that it is missing is its `define` method.

```{code-block} python

# -*- coding: utf-8 -*-
"""Equation of State WorkChain."""
from aiida.engine import WorkChain, ToContext, calcfunction
from aiida.orm import Code, Dict, Float, Str, StructureData
from aiida.plugins import CalculationFactory

from rescale import rescale
from common_wf import generate_scf_input_params

PwCalculation = CalculationFactory('quantumespresso.pw')
scale_facs = (0.96, 0.98, 1.0, 1.02, 1.04)
labels = ['c1', 'c2', 'c3', 'c4', 'c5']


@calcfunction
def get_eos_data(**kwargs):
    """Store EOS data in Dict node."""
    eos = [(result.dict.volume, result.dict.energy, result.dict.energy_units)
        for label, result in kwargs.items()]
    return Dict(dict={'eos': eos})


class EquationOfState(WorkChain):
    """WorkChain to compute Equation of State using Quantum Espresso."""

    @classmethod
    def define(cls, spec):

        #
        # TODO: WRITE THE DEFINE METHOD AS AN EXERCISE
        #

    def run_eos(self):
        """Run calculations for equation of state."""
        # Create basic structure and attach it as an output
        structure = self.inputs.structure

        calculations = {}

        for label, factor in zip(labels, scale_facs):

            rescaled_structure = rescale(structure, Float(factor))
            inputs = generate_scf_input_params(rescaled_structure, self.inputs.code,
                                            self.inputs.pseudo_family)

            self.report(
                'Running an SCF calculation for {} with scale factor {}'.
                format(structure.get_formula(), factor))
            future = self.submit(PwCalculation, **inputs)
            calculations[label] = future

        # Ask the workflow to continue when the results are ready and store them in the context
        return ToContext(**calculations)

    def results(self):
        """Process results."""
        inputs = {
            label: self.ctx[label].get_outgoing().get_node_by_label(
                'output_parameters')
            for label in labels
        }
        eos = get_eos_data(**inputs)

        # Attach Equation of State results as output node to be able to plot the EOS later
        self.out('eos', eos)

```

:::{warning}

WorkChains need to be defined in a **separate file** from the script used to run them.
E.g. save your WorkChain in `eos_workchain.py` and use `from eos_workchain import EquationOfState` to import the work chain in your script.

:::

To start, note the following differences between the `run_eos_wf` work function and the `EquationOfState`:

- Instead of using a `workfunction`-decorated function you need to define a class, inheriting from a prototype class called `WorkChain` that is provided by AiiDA in the `aiida.engine` module.
- For the `WorkChain`, you need to split your main code into methods, which are the steps of the workflow.
  Where should the code be split for the equation of state workflow?
  Well, the splitting points should be put where you would normally block the execution of the script for collecting results in a standard work function.
  For example here we split after submitting the `PwCalculation`'s.
- Note again the use of the attribute `ctx` through `self.ctx`, which is called the *context* and is inherited from the base class `WorkChain`.
  A python function or process function normally just stores variables in the local scope of the function.
  For instance, in the example of {ref}`this subsection<workflows-writing-workchains-eos-workchain>`, you stored the completed calculations in the `calculations` dictionary, that was a local variable.

  In work chains, instead, to preserve variables between different steps, you need to store them in a special dictionary called *context*.
  As explained above, the context variable `ctx` is inherited from the base class `WorkChain`, and at each step method you just need to update its content.
  AiiDA will take care of saving the context somewhere between workflow steps (on disk, in the database, depending on how AiiDA was configured).
  For your convenience, you can also access the value of a context variable as `self.ctx.varname` instead of `self.ctx['varname']`.
- Any submission within the workflow should not call the normal `run` or `submit` functions, but `self.submit` to which you have to pass the process class, and a dictionary of inputs.
- The submission in `run_eos` returns a future and not the actual calculation, because at that point in time we have only just launched the calculation to the daemon and it is not yet completed.
  Therefore it literally is a 'future' result.
  Yet we still need to add these futures to the context, so that in the next step of the workchain, when the calculations are in fact completed, we can access them and continue the work.
  To do this, we can use the `ToContext` class.
  This class takes a dictionary, where the values are the futures and the keys will be the names under which the corresponding calculations will be made available in the context when they are done.
  See how the `ToContext` object is created and returned in `run_eos`.
  By doing this, the workchain will implicitly wait for the results of all the futures you have specified, and then call the next step *only when all futures have completed*.
- While in normal process functions you attach output nodes to the node by invoking the *return* statement, in a work chain you need to call `self.out(link_name, node)` for each node you want to return.
  The advantage of this different syntax is that you can start emitting output nodes already in the middle of the execution, and not necessarily at the very end as it happens for normal functions (*return* is always the last instruction executed in a function or method).
  Also, note that once you have called `self.out(link_name, node)` on a given `link_name`, you can no longer call `self.out()` on the same `link_name`: this will raise an exception.

As an exercise, try to complete the `define` method.
Do do this, you need to implement a `define` classmethod that always takes `cls` and `spec` as inputs.
In this method you specify the main information on the workchain, in particular:

- The *inputs* that the workchain expects.
  This is obtained by means of the `spec.input()` method, which provides as the key feature the automatic validation of the input types via the `valid_type` argument.
  The same holds true for outputs, as you can use the `spec.output()` method to state what output types are expected to be returned by the workchain.
- The `outline` consisting in a list of 'steps' that you want to run, put in the right sequence.
  This is obtained by means of the method `spec.outline()` which takes as input the steps.
  *Note*: in this example we just split the main execution in two sequential steps, that is, first `run_eos` then `results`.

You can look at the `define` method of the `MultiplyAddWorkChain` {ref}`as an example <workflows-workchain-define>`.
If you get stuck, you can also download the complete script {download}`here <include/code/eos_workchain.py>`.

Once the work chain is complete, let's start by *running* it.
For this you once again have to use the function `run` passing as arguments the `EquationOfState` class and the inputs as key-value arguments:

```{code-block}

In [1]: from eos_workchain import EquationOfState
   ...: from aiida.engine import run
   ...: result = run(EquationOfState, code=load_code('qe-6.5-pw@localhost'), pseudo_family=Str('SSSP'), structure=load_node(pk=2804))
06/19/2020 12:02:04 PM <11810> aiida.orm.nodes.process.workflow.workchain.WorkChainNode: [REPORT] [541|EquationOfState|run_eos]: Running an SCF calculation for Si8 with scale factor 0.96
06/19/2020 12:02:05 PM <11810> aiida.orm.nodes.process.workflow.workchain.WorkChainNode: [REPORT] [541|EquationOfState|run_eos]: Running an SCF calculation for Si8 with scale factor 0.98
06/19/2020 12:02:05 PM <11810> aiida.orm.nodes.process.workflow.workchain.WorkChainNode: [REPORT] [541|EquationOfState|run_eos]: Running an SCF calculation for Si8 with scale factor 1.0
06/19/2020 12:02:06 PM <11810> aiida.orm.nodes.process.workflow.workchain.WorkChainNode: [REPORT] [541|EquationOfState|run_eos]: Running an SCF calculation for Si8 with scale factor 1.02
06/19/2020 12:02:07 PM <11810> aiida.orm.nodes.process.workflow.workchain.WorkChainNode: [REPORT] [541|EquationOfState|run_eos]: Running an SCF calculation for Si8 with scale factor 1.04

```

While the workflow is running, open a different terminal and check what is happening to the calculations using `verdi process list`.
You will see that after a few seconds the calculations are all submitted to the scheduler and can potentially run at the same time.
Once the work chain is completed, you can check the result:

```{code-block} ipython

In [2]: result
Out[2]: {'eos': <Dict: uuid: eedffd9f-c3d4-4cc8-9af5-242ede5ac23b (pk: 2937)>}

```

As a final exercise, instead of running the `EquationOfState`, we will submit it to the daemon.
However, in this case the work chain will need to be globally importable so the daemon can load it.
To achieve this, the directory containing the WorkChain definition needs to be in the `PYTHONPATH` in order for the AiiDA daemon to find it.
When your `eos_workchain.py` is in `/home/max/workchains`, add a line `export PYTHONPATH=$PYTHONPATH:/home/max/workchains` to the `/home/max/.virtualenvs/aiida/bin/activate` script.
Or, if it is in your current directory:

```{code-block} bash

$ echo "export PYTHONPATH=\$PYTHONPATH:$PWD" >> /home/max/.virtualenvs/aiida/bin/activate

```

Next, it is **very important** to restart the daemon, so it can successfully find the `EquationOfState` work chain:

```{code-block} bash

$ verdi daemon restart --reset

```

Once the daemon has been restarted, it is time to *submit* the `EquationOfState` work chain from the `verdi shell`:

```{code-block} ipython

In [1]: from eos_workchain import EquationOfState
   ...: from aiida.engine import submit
   ...: submit(EquationOfState, code=load_code('qe-6.5-pw@localhost'), pseudo_family=Str('SSSP'), structure=load_node(pk=2804))
Out[1]: <WorkChainNode: uuid: 9e5c7c48-a47c-49fc-a8ab-fff081f250ee (pk: 665) (eos.workchain.EquationOfState)>

```

Note that similar as for the `MultiplyAddWorkChain`, the `submit` function returns the `WorkChain` instance for our equation of state workflow.
Now, quickly leave the verdi shell and check the status of the work chain with `verdi process list`.
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
