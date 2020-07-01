.. _2020_virtual_intro:workflow_basic:

*****************
Workflows: Basics
*****************

The aim of this tutorial is to introduce how to write and launch workflows in AiiDA.

In this section, you will learn to:

1. Understand how to add simple python functions to the AiiDA database.
2. Learn how to write and launch a simple workflow in AiiDA.
3. Learn how to write and launch a workflow using checkpoints: the work chain.
4. Apply these concepts to calculate the equation of state of silicon.

.. note::

    To focus on the AiiDA concepts, the initial examples in this hands-on are purposefully kept very simple.
    At the end of the section you can find a more extensive real-world example.

.. _2020_virtual_intro:workflow_basic:process_function:

Process functions: a way to generalize provenance in AiiDA
==========================================================

Now that you are familiar with AiiDA, you know that the way to connect two data nodes is through a calculation.
In order to 'wrap' python functions and automate the generation of the needed links, in AiiDA we provide you with what we call 'process functions'.
There are two variants of process functions:

 * calculation functions
 * work functions

These operate mostly the same, but they should be used for different purposes, which will become clear later.
A normal function can be converted to a calculation function by using a `Python decorator <https://docs.python.org/3/glossary.html#term-decorator>`_ that takes care of storing the execution as a calculation and adding the links between the input and output data nodes.

Let's say you want to multiply two ``Int`` data nodes.
The following Python function:

.. code-block:: python

    def multiply(x, y):
        return x * y

will give the desired result when applied to two ``Int`` nodes, but the calculation will not be stored in the provenance graph.
However, we can use the ``@calcfunction`` decorator [#f1]_ provided by AiiDA to automatically make it part of the provenance graph.
Start up the AiiDA IPython shell again using ``verdi shell`` and execute the following code snippet:

.. code-block:: ipython

    In [1]: from aiida.engine import calcfunction
       ...:
       ...: @calcfunction
       ...: def multiply(x, y):
       ...:     return x * y

Besides adding the ``@calcfunction`` decorator, it is also necessary to make sure that the process function inputs and outputs are ``Data`` nodes, so that they can be stored in the database.
Try executing the ``multiply`` calculation function with regular integers:

.. code-block:: ipython

    In [2]: multiply(3, 4)

This will return a ``ValueError``, as the inputs of the calculation function must be subclasses of the ``Data`` class.
If we pass the ``multiply`` function two ``Int`` nodes instead:

.. code-block:: ipython

    In [3]: multiply(Int(3), Int(4))
    Out[3]: <Int: uuid: 627ae988-5bf5-46e9-993c-39e7c195a58b (pk: 2754) value: 12>

In this case, the ``multiply`` calculation function *creates* a new ``Int`` node, and automatically stores it in the database.

.. note::
    For the simple ``multiply`` example, the output is guaranteed to be an ``Int`` node if the inputs are ``Int`` nodes.
    However, for more complex calculation functions you need to make sure that the function returns a ``Data`` node.

Workflows
=========

A workflow in AiiDA is a :ref:`process <topics:processes:concepts>` that calls other workflows and calculations and optionally *returns* data and as such can encode the logic of a typical scientific workflow.
Currently, there are two ways of implementing a workflow process:

 * :ref:`work functions<topics:workflows:concepts:workfunctions>`
 * :ref:`work chains<topics:workflows:concepts:workchains>`

Here we present a brief introduction on how to write both workflow types.

.. note::

    For more details on the concept of a workflow, and the difference between a work function and a work chain, please see the corresponding :ref:`topics section<topics:workflows:concepts>` in the AiiDA documentation.

Work function
-------------

A *work function* is a process function that calls one or more calculation functions and *returns* data that has been *created* by the calculation functions it has called.
Moreover, work functions can also call other work functions, allowing you to write nested workflows.
Writing a work function, whose provenance is automatically stored, is as simple as writing a Python function and decorating it with the :func:`~aiida.engine.processes.functions.workfunction` decorator:

.. literalinclude:: include/snippets/workflows_add_multiply.py
    :language: python
    :start-after: start-marker

It is important to reiterate here that the :func:`~aiida.engine.processes.functions.workfunction`-decorated ``add_multiply()`` function does not *create* any new data nodes.
The ``add()`` and ``multiply()`` calculation functions create the ``Int`` data nodes, all the work function does is *return* the results of the ``multiply()`` calculation function.
Moreover, both calculation and work functions can only accept and return data nodes, i.e. instances of classes that subclass the :class:`~aiida.orm.nodes.data.data.Data` class.

Copy the code snippet above and execute it in the ``verdi shell``, or put it into a Python script (e.g. :download:`add_multiply.py <include/snippets/workflows_add_multiply.py>`) and import the add_multiply work function in the ``verdi shell``:

.. code-block:: ipython

    In [1]: from add_multiply import add_multiply

Once again, running a work function is as simple as calling a typical Python function: simply call it with the required input arguments:

.. code-block:: ipython

    In [2]: result = add_multiply(Int(2), Int(3), Int(5))

Here, the ``add_multiply`` work function returns the output ``Int`` node and we assign it to the variable ``result``.
Note that - similar to a calculation function - the input arguments of a work function must be an instance of ``Data`` node, or any of its subclasses.
Just calling the ``add_multiply`` function with regular integers will result in a ``ValueError``, as these cannot be stored in the provenance graph.

.. note::

    Although the example above shows the most straightforward way to run the ``add_and_multiply`` work function, there are several other ways of running processes that can return more than just the result.
    For example, the ``run_get_node`` function from the AiiDA engine returns both the result of the workflow and the work function node.
    See the :ref:`corresponding topics section for more details <topics:processes:usage:launching>`.

Work chain
----------

The simple work function that we ran in the previous section was launched by a python script that needs to be running for the whole time of the execution.
If you had killed the main python process during this time, the workflow would not have terminated correctly.
This is not a significant issue when running these simple examples, but when you start running workflows that take longer to complete, this can become a real problem.

In order to overcome this limitation, in AiiDA we have implemented a way to insert checkpoints, where the main code defining a workflow can be stopped (you can even shut down the machine on which AiiDA is running!).
We call these work functions with checkpoints 'work chains' because, as you will see, they basically amount to splitting a work function in a chain of steps.
Each step is then run by the daemon, in a way similar to the remote calculations.

When the workflow you want to run is more complex and takes longer to finish, it is better to write a work chain.
Writing a work chain in AiiDA requires creating a class that inherits from the :class:`~aiida.engine.processes.workchains.workchain.WorkChain` class.
Below is an example of a work chain that takes three integers as inputs, multiplies the first two and then adds the third to obtain the final result:

.. literalinclude:: include/snippets/workflows_multiply_add.py
    :language: python
    :start-after: start-marker

You can give the work chain any valid Python class name, but the convention is to have it end in :class:`~aiida.engine.processes.workchains.workchain.WorkChain` so that it is always immediately clear what it references.
Let's go over the methods of the ``MultiplyAddWorkChain`` one by one:

.. literalinclude:: include/snippets/workflows_multiply_add.py
    :language: python
    :pyobject: MultiplyAddWorkChain.define
    :dedent: 4

The most important method to implement for every work chain is the ``define()`` method.
This class method must always start by calling the ``define()`` method of its parent class.
Next, the ``define()`` method should be used to define the specifications of the work chain, which are contained in the work chain ``spec``:

* the **inputs**, specified using the ``spec.input()`` method.
  The first argument of the ``input()`` method is a string that specifies the label of the input, e.g. ``'x'``.
  The ``valid_type`` keyword argument allows you to specify the required node type of the input.
  Other keyword arguments allow the developer to set a default for the input, or indicate that an input should not be stored in the database, see :ref:`the process topics section <topics:processes:usage:spec>` for more details.
* the **outline** or logic of the workflow, specified using the ``spec.outline()`` method.
  The outline of the workflow is constructed from the methods of the :class:`~aiida.engine.processes.workchains.workchain.WorkChain` class.
  For the ``MultiplyAddWorkChain``, the outline is a simple linear sequence of steps, but it's possible to include actual logic, directly in the outline, in order to define more complex workflows as well.
  See the :ref:`work chain outline section <topics:workflows:usage:workchains:define_outline>` for more details.
* the **outputs**, specified using the ``spec.output()`` method.
  This method is very similar in its usage to the ``input()`` method.
* the **exit codes** of the work chain, specified using the ``spec.exit_code()`` method.
  Exit codes are used to clearly communicate known failure modes of the work chain to the user.
  The first and second arguments define the ``exit_status`` of the work chain in case of failure (``400``) and the string that the developer can use to reference the exit code (``ERROR_NEGATIVE_NUMBER``).
  A descriptive exit message can be provided using the ``message`` keyword argument.
  For the ``MultiplyAddWorkChain``, we demand that the final result is not a negative number, which is checked in the ``validate_result`` step of the outline.

.. note::

    For more information on the ``define()`` method and the process spec, see the :ref:`corresponding section in the topics <topics:processes:usage:defining>`.

The ``multiply`` method is the first step in the outline of the ``MultiplyAddWorkChain`` work chain.


.. literalinclude:: include/snippets/workflows_multiply_add.py
    :language: python
    :pyobject: MultiplyAddWorkChain.multiply
    :dedent: 4

This step simply involves running the calculation function ``multiply()``, on the ``x`` and ``y`` **inputs** of the work chain.
To store the result of this function and use it in the next step of the outline, it is added to the *context* of the work chain using ``self.ctx``.

.. literalinclude:: include/snippets/workflows_multiply_add.py
    :language: python
    :pyobject: MultiplyAddWorkChain.add
    :dedent: 4

The ``add()`` method is the second step in the outline of the work chain.
As this step uses the ``ArithmeticAddCalculation`` calculation job, we start by setting up the inputs for this :class:`~aiida.engine.processes.calcjobs.calcjob.CalcJob` in a dictionary.
Next, when submitting this calculation job to the daemon, it is important to use the submit method from the work chain instance via ``self.submit()``.
Since the result of the addition is only available once the calculation job is finished, the ``submit()`` method returns the :class:`~aiida.orm.nodes.process.calculation.calcjob.CalcJobNode` of the *future* ``ArithmeticAddCalculation`` process.
To tell the work chain to wait for this process to finish before continuing the workflow, we return the ``ToContext`` class, where we have passed a dictionary to specify that the future calculation job node should be assigned to the ``'addition'`` context key.

.. warning::

    Never use the global ``submit()`` function to submit calculations to the daemon within a :class:`~aiida.engine.processes.workchains.workchain.WorkChain`.
    Doing so will raise an exception during runtime.
    See the :ref:`topics section on work chains<topics:workflows:usage:workchains:submitting_sub_processes>` for more details.

.. note::
    Instead of passing a dictionary, you can also initialize a ``ToContext`` instance by passing the future process as a keyword argument, e.g. ``ToContext(addition=calcjob_node)``.
    More information on the ``ToContext`` class can be found in :ref:`the topics section on submitting sub processes<topics:workflows:usage:workchains:submitting_sub_processes>`.


.. literalinclude:: include/snippets/workflows_multiply_add.py
    :language: python
    :pyobject: MultiplyAddWorkChain.validate_result
    :dedent: 4

Once the ``ArithmeticAddCalculation`` calculation job is finished, the next step in the work chain is to validate the result, i.e. verify that the result is not a negative number.
After the ``addition`` node has been extracted from the context, we take the ``sum`` node from the ``ArithmeticAddCalculation`` outputs and store it in the ``result`` variable.
In case the value of this ``Int`` node is negative, the ``ERROR_NEGATIVE_NUMBER`` exit code - defined in the ``define()`` method - is returned.
Note that once an exit code is returned during any step in the outline, the work chain will be terminated and no further steps will be executed.

.. literalinclude:: include/snippets/workflows_multiply_add.py
    :language: python
    :pyobject: MultiplyAddWorkChain.result
    :dedent: 4

The final step in the outline is to pass the result to the outputs of the work chain using the ``self.out()`` method.
The first argument (``'result'``) specifies the label of the output, which corresponds to the label provided to the spec in the ``define()`` method.
The second argument is the result of the work chain, extracted from the ``Int`` node stored in the context under the ``'addition'`` key.

Launching a work chain
----------------------

Before we can launch the ``MultiplyAddWorkChain``, we still have to set up the ``Code`` the work chain uses to add two numbers together:

.. code-block:: console

    $ verdi code setup -L add --on-computer --computer=localhost -P arithmetic.add --remote-abs-path=/bin/bash -n

This command sets up a code with *label* ``add`` on the *computer* ``localhost``, using the *plugin* ``arithmetic.add``.

To launch a work chain, you can either use the ``run`` or ``submit`` functions.
For either function, you need to provide the class of the work chain as the first argument, followed by the inputs as keyword arguments.
To make things a little easier, we have added these basic arithmetic functions to `aiida-core`, along with a set of entry points, so they can be loaded using a factory.
Start up the ``verdi shell`` and load the ``MultiplyAddWorkChain`` using the ``WorkflowFactory``:

.. code-block:: ipython

    In [1]: MultiplyAddWorkChain = WorkflowFactory('arithmetic.multiply_add')

The ``WorkflowFactory`` is a useful and robust tool for loading workflows based on their *entry point*, e.g. ``'arithmetic.multiply_add'`` in this case.
Using the ``run`` function, or "running", a work chain means it is executed in the same system process as the interpreter in which it is launched:

.. code-block:: ipython

    In [2]: from aiida.engine import run
       ...: add_code = load_code(label='add')
       ...: results = run(MultiplyAddWorkChain, x=Int(2), y=Int(3), z=Int(5), code=add_code)

Alternatively, you can first construct a dictionary of the inputs, and pass it to the ``run`` function by taking advantage of `Python's automatic keyword expansion <https://docs.python.org/3/tutorial/controlflow.html#unpacking-argument-lists>`_:

.. code-block:: ipython

    In [3]: inputs = {'x': Int(1), 'y': Int(2), 'z': Int(3), 'code': add_code}
       ...: results = run(MultiplyAddWorkChain, **inputs)

This is particularly useful in case you have a workflow with a lot of inputs.
In both cases, running the ``MultiplyAddWorkChain`` workflow returns the **results** of the workflow, i.e. a dictionary of the nodes that are produced as outputs, where the keys of the dictionary correspond to the labels of each respective output.

.. note::

    Similar to other processes, there are multiple functions for launching a work chain.
    See the section on :ref:`launching processes for more details<topics:processes:usage:launching>`.

Since *running* a workflow will block the interpreter, you will have to wait until the workflow is finished before you get back control.
Moreover, you won't be able to turn your computer or even your terminal off until the workflow has fully terminated, and it is difficult to run multiple workflows in parallel.
So, it is advisable to *submit* more complex or longer work chains to the daemon:

.. code-block:: ipython

    In [5]: from aiida.engine import submit
       ...:
       ...: add_code = load_code(label='add')
       ...: inputs = {'x': Int(1), 'y': Int(2), 'z': Int(3), 'code': add_code}
       ...:
       ...: workchain_node = submit(MultiplyAddWorkChain, **inputs)

Note that when using ``submit`` the work chain is not run in the local interpreter but is sent off to the daemon and you get back control instantly.
This allows you to submit multiple work chains at the same time and the daemon will start working on them in parallel.
Once the ``submit`` call returns, you will not get the result as with ``run``, but you will get the **node** that represents the work chain:

.. code-block:: ipython

    In [6]: workchain_node
    Out[6]: <WorkChainNode: uuid: 17fbe11e-b71b-4ffe-a08e-0d5e3b1ae5ed (pk: 2787) (aiida.workflows:arithmetic.multiply_add)>

Submitting a work chain instead of directly running it not only makes it easier to execute multiple work chains in parallel, but also ensures that the progress of a workchain is not lost when you restart your computer.

.. important::

    In contrast to work chains, work *functions* cannot be submitted to the daemon, and hence can only be *run*.

If you are unfamiliar with the inputs of a particular ``WorkChain``, a convenient tool for setting up the work chain is the :ref:`process builder<topics:processes:usage:builder>`.
This can be obtained by using the ``get_builder()`` method, which is implemented for every ``CalcJob`` and ``WorkChain``:

.. code-block:: ipython

    In [1]: from aiida.plugins import WorkflowFactory, DataFactory
       ...: Int = DataFactory('int')
       ...: MultiplyAddWorkChain = WorkflowFactory('arithmetic.multiply_add')
       ...: builder = MultiplyAddWorkChain.get_builder()

To explore the inputs of the work chain, you can use tab autocompletion by typing ``builder.`` and then hitting ``TAB``.
If you want to get more details on a specific input, you can simply add a ``?`` and press enter:

.. code-block:: ipython

    In [2]: builder.x?
    Type:        property
    String form: <property object at 0x119ad2dd0>
    Docstring:   {"name": "x", "required": "True", "valid_type": "<class 'aiida.orm.nodes.data.int.Int'>", "non_db": "False"}

Here you can see that the ``x`` input is required, needs to be of the ``Int`` type and is stored in the database (``"non_db": "False"``).

Using the builder, the inputs of the ``WorkChain`` can be provided one by one:

.. code-block:: ipython

    In [3]: builder.code = load_code(label='add')
       ...: builder.x = Int(2)
       ...: builder.y = Int(3)
       ...: builder.z = Int(5)

Once the *required* inputs of the workflow have been provided to the builder, you can either run the work chain or submit it to the daemon:

.. code-block:: ipython

    In [4]: from aiida.engine import submit
       ...: workchain_node = submit(builder)

.. note::

    For more detail on the process builder, see the :ref:`corresponding topics section<topics:processes:usage:builder>`.

Equation of state
=================

Now that we've discussed the concepts of workflows in AiiDA using some basic examples, let's move on to something more interesting: calculating the equation of state of silicon.
An equation of state consists in calculating the total energy (E) as a function of the unit cell volume (V).
The minimal energy is reached at the equilibrium volume.
Equivalently, the equilibrium is defined by a vanishing pressure: :math:`p=-dE/dV`.
In the vicinity of the minimum, the functional form of the equation of state can be approximated by a parabola.
Such an approximation greatly simplifies the calculation of the bulk modulus, that is proportional to the second derivative of the energy (a more advanced treatment requires fitting the curve with, e.g., the Birch–Murnaghan expression).

First, we'll need the structure of bulk silicon.
Instead of constructing the structure manually, we'll load it from the Crystallography Open Database (COD).
Similar to data, calculation and worfklows, a database importer class can be loaded using the corresponding factory and entry point:

.. code-block:: ipython

    In [1]: from aiida.plugins import DbImporterFactory
       ...: CodDbImporter = DbImporterFactory('cod')

Now that we have the ``CodDbImporter`` class loaded, let's initialize an instance of the class:

.. code-block:: ipython

    In [2]: cod = CodDbImporter()

Next, we'll load the conventional unit cell of silicon, which has the COD id = 1526655:

.. code-block:: ipython

    In [3]: results = cod.query(id='1526655')
       ...: structure = results[0].get_aiida_structure()

Let's have a look at the ``structure`` variable:

.. code-block:: ipython

    In [4]: structure
    Out[4]: <StructureData: uuid: 3d4ab03b-4149-4c31-88ef-180640f1f79a (unstored)>

We can see that the ``structure`` variable contains an instance of ``StructureData``, but that it hasn't been stored in the AiiDA database. Let's do that now:

.. code-block:: ipython

    In [5]: structure.store()
    Out[5]: <StructureData: uuid: 3d4ab03b-4149-4c31-88ef-180640f1f79a (pk: 2804)>

For the equation of state you need another function that takes as input a ``StructureData`` object and a rescaling factor, and returns a ``StructureData`` object with the rescaled lattice parameter:

.. literalinclude:: include/snippets/workflows_rescale.py
    :language: python

Of course, this *regular* Python function won't be stored in the provenance graph, so we need to decorate it with the ``calcfunction`` decorator.
Copy the code snippet above into a Python file, (e.g. :download:`rescale.py <include/snippets/workflows_rescale.py>`), and add the ``calcfunction`` decorator to the ``rescale`` function.

Once the ``rescale`` function has been decorated, it's time to put it to the test!
Open a ``verdi shell``, load the ``StructureData`` node for silicon that you just stored, and generate a set of rescaled structures:

.. code:: python

    In [1]: from rescale import rescale
       ...:
       ...: initial_structure = load_node(pk=2804)
       ...: rescaled_structures = [rescale(initial_structure, Float(factor)) for factor in (0.98, 0.99, 1.0, 1.1, 1.2)]

.. note::

    Notice that we have supplied the ``rescale`` method with two inputs that are both ``Data`` nodes: ``StructureData`` and ``Float``.

Now let's check the contents of the ``rescaled_structures`` variable:

.. code-block:: ipython

    In [2]: rescaled_structures
    Out[2]:
    [<StructureData: uuid: a1801ec8-35c8-4e1d-bbbf-36fbcef7d034 (pk: 2807)>,
     <StructureData: uuid: e2714063-63ce-492b-b003-b05323c70a22 (pk: 2810)>,
     <StructureData: uuid: 842aa50b-c6ce-429c-b089-96a1480cea9f (pk: 2813)>,
     <StructureData: uuid: 78bb6406-ec94-425d-a396-9a7cc7ffbacf (pk: 2816)>,
     <StructureData: uuid: 8f9c876e-d5e9-4018-9bb5-9e52c335fe0c (pk: 2819)>]

Notice that all of the ``StructureData`` nodes of the rescaled structures are already stored in the database with their own PK.
This is because they are the output nodes of the ``rescale`` calculation function.

.. _2020_intro_workflow_eos_work_functions:

Running the equation of state workflow
--------------------------------------

Now that we have our initial structure and a calculation function for rescaling the unit cell, we can put this together with the ``PwCalculation`` from the session on running calculations to calculate the equation of state.
For this part of the tutorial, we provide some utility functions that get the correct pseudopotentials and generate the input for a ``PwCalculation`` in :download:`common_wf.py <../scripts/common_wf.py>`.

.. important::

    The workflow scripts for the rest of this section rely on the methods in ``rescale.py`` and ``common_wf.py`` to function.
    Make sure the Python files with the workflows are in the same directory as these two files.

In the script shown below, a work function has been implemented that generates a scaled structure and calculates its energy for a range of 5 scaling factors:

.. literalinclude:: include/snippets/workflows_eos_workfunction.py
    :language: python

Copy the contents of this script into a Python file, for example ``workfunctions.py``.
Next, let's open up a ``verdi shell`` and run the equation of state workflow. First, load the silicon structure you imported earlier using its PK:

.. code-block:: ipython

    In [1]: initial_structure = load_node(pk=2804)

Next, load the Quantum ESPRESSO pw code you used previously to run calculations:

.. code-block:: ipython

    In [2]: code = load_code('qe-6.5-pw@localhost')

To run the workflow, we also have to specify the family of pseudopotentials as an AiiDA ``Str`` node:

.. code-block:: ipython

    In [3]: pseudo_str = Str('SSSP')

Finally, we are ready to import the ``run_eos()`` work function and run it!

.. code-block:: ipython

    In [4]: from workfunctions import run_eos_wf
       ...: result = run_eos_wf(code, pseudo_str, initial_structure)

The work function will start running and print one line of output for each scale factor used.
Once it is complete, the output will look something like this:

.. code-block:: ipython

    Running run_eos_wf<2821>
    Running a scf for Si8 with scale factor 0.96
    Running a scf for Si8 with scale factor 0.98
    Running a scf for Si8 with scale factor 1.0
    Running a scf for Si8 with scale factor 1.02
    Running a scf for Si8 with scale factor 1.04

Let's have a look at the result!

.. code-block:: ipython

    In [5]: result
    Out[5]:
    <Dict: uuid: 4a8cdde5-a2ff-4c97-9a13-28096b1d9b91 (pk: 2878)>

We can see that the work function returns a ``Dict`` node with the results for the equation of state.
Let's have a look at the contents of this node:

.. code-block:: ipython

    In [6]: result.get_dict()
    Out[6]:
    {'eos': [[137.84870014835, -1240.4759003187, 'eV'],
      [146.64498086438, -1241.4786547651, 'eV'],
      [155.807721341, -1242.0231198534, 'eV'],
      [165.34440034884, -1242.1847659475, 'eV'],
      [175.26249665852, -1242.0265883524, 'eV']]}

We can see that the dictionary contains the volume, calculated energy and its units for each scaled structure.
Of course, this information is much better represented with a graph, so let's plot the equation of state and fit it with a Birch-Birch–Murnaghan equation.
For this purpose, we have provided the ``plot_eos`` script in the ``common_wf.py`` file that takes the PK of the work function as an input and plots the equation of state:

.. code-block:: ipython

    In [7]: from common_wf import plot_eos
       ...: plot_eos(2821)

Submitting the workflow: Workchains
-----------------------------------

Similar to the simple arithmetic work function above, running the ``eos_wf`` work function means that the Python interpreter will be blocked during the whole workflow.
In this case, this will take the time required to launch the calculations, the actual time needed by Quantum ESPRESSO to perform the calculation and the time taken to retrieve the results.
Perhaps you killed the calculation and you experienced the unpleasant consequences: intermediate calculation results are potentially lost and it is extremely difficult to restart a workflow from the exact place where it stopped.

Clearly, when writing workflows that involve the use of an *ab initio* code like Quantum ESPRESSO, it is better to use a work chain.
Below you can find the basic rules that allow you to convert your workfunction-based script to a workchain-based one and a snippet example focusing on the code used to perform the calculation of an equation of state.

.. include:: include/snippets/workflows_eos_workchain.py
    :code: python

.. warning::

    WorkChains need to be defined in a **separate file** from the script used to run them.
    E.g. save your WorkChain in ``workchains.py`` and use ``from workchains import MyWorkChain`` to import it in your script.

-   Instead of using decorated functions you need to define a class, inheriting from a prototype class called ``WorkChain`` that is provided by AiiDA in the ``aiida.engine`` module.

-   Within your class you need to implement a ``define`` classmethod that always takes ``cls`` and ``spec`` as inputs.
    Here you specify the main information on the workchain, in particular:

    -   The *inputs* that the workchain expects.
        This is obtained by means of the ``spec.input()`` method, which provides as the key feature the automatic validation of the input types via the ``valid_type`` argument.
        The same holds true for outputs, as you can use the ``spec.output()`` method to state what output types are expected to be returned by the workchain.

    -   The ``outline`` consisting in a list of 'steps' that you want to run, put in the right sequence.
        This is obtained by means of the method ``spec.outline()`` which takes as input the steps.
        *Note*: in this example we just split the main execution in two sequential steps, that is, first ``run_eos`` then ``results``.

-   You need to split your main code into methods, with the names you specified before into the outline (``run_eos`` and ``results`` in this example).
    Where exactly should you split the code?
    Well, the splitting points should be put where you would normally block the execution of the script for collecting results in a standard work function, namely whenever you call the method ``.result()``.
    Each method should accept only one parameter, ``self``, e.g. ``def step_name(self)``.

-   You will notice that the methods reference the attribute ``ctx`` through ``self.ctx``, which is called the *context* and is inherited from the base class ``WorkChain``.
    A python function or process function normally just stores variables in the local scope of the function.
    For instance, in the example of :ref:`this subsection<2020_intro_workflow_eos_work_functions>`, you stored the completed calculations in the ``calculations`` dictionary, that was a local variable.

    In work chains, instead, to preserve variables between different steps, you need to store them in a special dictionary called *context*.
    As explained above, the context variable ``ctx`` is inherited from the base class ``WorkChain``, and at each step method you just need to update its content.
    AiiDA will take care of saving the context somewhere between workflow steps (on disk, in the database, depending on how AiiDA was configured).
    For your convenience, you can also access the value of a context variable as ``self.ctx.varname`` instead of ``self.ctx['varname']``.

-   Any submission within the workflow should not call the normal ``run`` or ``submit`` functions, but ``self.submit`` to which you have to pass the process class, and a dictionary of inputs.

-   The submission in ``run_eos`` returns a future and not the actual calculation, because at that point in time we have only just launched the calculation to the daemon and it is not yet completed.
    Therefore it literally is a 'future' result.
    Yet we still need to add these futures to the context, so that in the next step of the workchain, when the calculations are in fact completed, we can access them and continue the work.
    To do this, we can use the ``ToContext`` class.
    This class takes a dictionary, where the values are the futures and the keys will be the names under which the corresponding calculations will be made available in the context when they are done.
    See how the ``ToContext`` object is created and returned in ``run_eos``.
    By doing this, the workchain will implicitly wait for the results of all the futures you have specified, and then call the next step *only when all futures have completed*.

-   *Return values*: While in normal process functions you attach output nodes to the node by invoking the *return* statement, in a workchain you need to call ``self.out(link_name, node)`` for each node you want to return.
    Of course, if you have already prepared a dictionary of outputs, you can just use the following syntax:

    .. code:: python

        self.out_many(retdict)  # Keys are link names, value the nodes

    The advantage of this different syntax is that you can start emitting output nodes already in the middle of the execution, and not necessarily at the very end as it happens for normal functions (*return* is always the last instruction executed in a function or method).
    Also, note that once you have called ``self.out(link_name, node)`` on a given ``link_name``, you can no longer call ``self.out()`` on the same ``link_name``: this will raise an exception.

Finally, the workflow has to be run.
For this you have to use the function ``run`` passing as arguments the ``EquationOfState`` class and the inputs as key-value arguments.
For example, you can execute:

.. code-block::

    In [1]: from workchains import EquationOfState
       ...: from aiida.engine import run
       ...: run(EquationOfState, code=load_code('qe-6.5-pw@localhost'), pseudo_family=Str('SSSP'), structure=load_node(pk=2804))
    06/19/2020 12:02:04 PM <11810> aiida.orm.nodes.process.workflow.workchain.WorkChainNode: [REPORT] [541|EquationOfState|run_eos]: Running an SCF calculation for Si8 with scale factor 0.96
    06/19/2020 12:02:05 PM <11810> aiida.orm.nodes.process.workflow.workchain.WorkChainNode: [REPORT] [541|EquationOfState|run_eos]: Running an SCF calculation for Si8 with scale factor 0.98
    06/19/2020 12:02:05 PM <11810> aiida.orm.nodes.process.workflow.workchain.WorkChainNode: [REPORT] [541|EquationOfState|run_eos]: Running an SCF calculation for Si8 with scale factor 1.0
    06/19/2020 12:02:06 PM <11810> aiida.orm.nodes.process.workflow.workchain.WorkChainNode: [REPORT] [541|EquationOfState|run_eos]: Running an SCF calculation for Si8 with scale factor 1.02
    06/19/2020 12:02:07 PM <11810> aiida.orm.nodes.process.workflow.workchain.WorkChainNode: [REPORT] [541|EquationOfState|run_eos]: Running an SCF calculation for Si8 with scale factor 1.04

While the workflow is running, open a different terminal and check what is happening to the calculations using ``verdi process list``.
You will see that after a few seconds the calculations are all submitted to the scheduler and can potentially run at the same time.
Once the work chain is completed, the equation of state dictionary will be printed:

.. code-block:: ipython

    Out[1]: {'eos': <Dict: uuid: eedffd9f-c3d4-4cc8-9af5-242ede5ac23b (pk: 2937)>}

As a final exercise, instead of running the ``EquationOfState``, we will submit it to the daemon.
However, in this case the work chain will need to be globally importable so the daemon can load it.
To achieve this, the directory containing the WorkChain definition needs to be in the ``PYTHONPATH`` in order for the AiiDA daemon to find it.
If your ``workchains.py`` sits in ``/home/max/workchains``, add a line ``export PYTHONPATH=$PYTHONPATH:/home/max`` to the ``/home/max/.virtualenvs/aiida/bin/activate`` script.

.. code-block:: bash

    $ echo "export PYTHONPATH=\$PYTHONPATH:$PWD" >> /home/max/.virtualenvs/aiida/bin/activate

Next, it is **very important** to restart the daemon, so it can successfully find the ``EquationOfState`` work chain:

.. code-block:: bash

    $ verdi daemon restart --reset

Once the daemon has been restarted, it is time to *submit* the ``EquationOfState`` work chain from the ``verdi shell``:

.. code-block:: ipython

    In [1]: from workchains import EquationOfState
       ...: from aiida.engine import submit
       ...: submit(EquationOfState, code=load_code('qe-6.5-pw@localhost'), pseudo_family=Str('SSSP'), structure=load_node(pk=2804))
    Out[1]: <WorkChainNode: uuid: 9e5c7c48-a47c-49fc-a8ab-fff081f250ee (pk: 665) (eos.workchain.EquationOfState)>

Note that similar as for the ``MultiplyAddWorkChain``, the ``submit`` function returns the ``WorkChain`` instance for our equation of state workflow.
Now, quickly leave the verdi shell and check the status of the work chain with ``verdi process list``.
Depending on what stage of the work chain you are in, you will see something like the following output:

.. code-block:: bash

    (aiida) max@quantum-mobile:~$ verdi process list
      PK  Created    Process label    Process State    Process status
    ----  ---------  ---------------  ---------------  ---------------------------------------
     186  3h ago     run_eos_wf       ⏵ Running
     665  34s ago    EquationOfState  ⏵ Waiting        Waiting for child processes: 689, 695
     689  32s ago    PwCalculation    ⏵ Waiting        Monitoring scheduler: job state RUNNING
     695  31s ago    PwCalculation    ⏵ Waiting        Monitoring scheduler: job state QUEUED

    Total results: 4

    Info: last time an entry changed state: 8s ago (at 11:36:01 on 2020-06-19)

.. rubric:: Footnotes

.. [#f1] In simple words, a decorator is a function that modifies the behavior of another function. In python, a function can be decorated by adding a line of the form ``@decorating_function_name`` on the line just before the ``def`` line of the decorated function. If you want to know more, there are many online resources explaining python decorators.
