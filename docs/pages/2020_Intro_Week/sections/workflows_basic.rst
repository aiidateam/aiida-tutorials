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
However, we can use the ``@calcfunction`` decorator [#f1]_  provided by AiiDA to automatically make it part of the provenance graph.
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
    Out[3]: <Int: uuid: bf07e69f-87aa-4cca-b7f4-450d81d673df (pk: 5) value: 12>

The ``multiply`` calculation function *creates* a new ``Int`` node, and automatically stores it in the database.

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
Writing a work function, whose provenance is automatically stored, is as simple as writing a Python function and decorating it with the :class:`~aiida.engine.processes.functions.workfunction` decorator:

.. literalinclude:: include/snippets/workflows_add_multiply.py
    :language: python
    :start-after: start-marker

It is important to reiterate here that the :class:`~aiida.engine.processes.functions.workfunction`-decorated ``add_multiply()`` function does not *create* any new data nodes.
The ``add()`` and ``multiply()`` calculation functions create the ``Int`` data nodes, all the work function does is *return* the results of the ``multiply()`` calculation function.
Moreover, both calculation and workflow functions can only accept and return data nodes, i.e. instances of classes that subclass the :class:`~aiida.orm.nodes.data.data.Data` class.

Once again, running a work function is as simple as calling a typical Python function: simply call it with the required input arguments:

.. code-block:: ipython

    result = add_multiply(Int(2), Int(3), Int(5))

Here, the ``add_multiply`` work function returns the output ``Int`` node and we assign it to the variable ``result``.
Note that the input arguments of a work function must be an instance of ``Data`` node, or any of its subclasses.
Just calling the ``add_multiply`` function with regular integers will result in a ``ValueError``, as these cannot be stored in the provenance graph.

.. note::

    Although the example above shows the most straightforward way to run the ``add_and_multiply`` work function, there are several other ways of running processes that can return more than just the result.
    For example, the ``run_get_node`` function from the AiiDA engine returns both the result of the workflow and the work function node.
    See the :ref:`corresponding topics section for more details <topics:processes:usage:launching>`.

Work chain
----------

When the workflow you want to run is more complex and takes longer to finish, it is better to write a *work chain*.
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

To launch a work chain, you can either use the ``run`` or ``submit`` functions.
For either function, you need to provide the class of the work chain as the first argument, followed by the inputs as keyword arguments.
Using the ``run`` function, or "running", a work chain means it is executed in the same system process as the interpreter in which it is launched:

.. code-block:: python

    from aiida.engine import run
    from aiida.plugins import WorkflowFactory, DataFactory
    Int = DataFactory('int')
    MultiplyAddWorkChain = WorkflowFactory('arithmetic.multiply_add')

    add_code = load_code(label='add')

    results = run(MultiplyAddWorkChain, x=Int(2), y=Int(3), z=Int(5), code=add_code)

Alternatively, you can first construct a dictionary of the inputs, and pass it to the ``run`` function by taking advantage of `Python's automatic keyword expansion <https://docs.python.org/3/tutorial/controlflow.html#unpacking-argument-lists>`_:

.. code-block:: python

    inputs = {'x': Int(1), 'y': Int(2), 'z': Int(3), 'code': add_code}
    results = run(MultiplyAddWorkChain, **inputs)

This is particularly useful in case you have a workflow with a lot of inputs.
In both cases, running the ``MultiplyAddWorkChain`` workflow returns the **results** of the workflow, i.e. a dictionary of the nodes that are produced as outputs, where the keys of the dictionary correspond to the labels of each respective output.

.. note::

    Similar to other processes, there are multiple functions for launching a work chain.
    See the section on :ref:`launching processes for more details<topics:processes:usage:launching>`.

Since *running* a workflow will block the interpreter, you will have to wait until the workflow is finished before you get back control.
Moreover, you won't be able to turn your computer or even your terminal off until the workflow has fully terminated, and it is difficult to run multiple workflows in parallel.
So, it is advisable to *submit* more complex or longer work chains to the daemon:

.. code-block:: python

    from aiida.engine import submit
    from aiida.plugins import WorkflowFactory, DataFactory
    Int = DataFactory('int')
    MultiplyAddWorkChain = WorkflowFactory('arithmetic.multiply_add')

    add_code = load_code(label='add')
    inputs = {'x': Int(1), 'y': Int(2), 'z': Int(3), 'code': add_code}

    workchain_node = submit(MultiplyAddWorkChain, **inputs)

Note that when using ``submit`` the work chain is not run in the local interpreter but is sent off to the daemon and you get back control instantly.
This allows you to submit multiple work chains at the same time and the daemon will start working on them in parallel.
Once the ``submit`` call returns, you will not get the result as with ``run``, but you will get the **node** that represents the work chain.
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


OLD
===

Imagine having a function that takes as input a string of the name of a chemical element and generates the corresponding bulk structure as a ``StructureData`` object.
The function might look like the following snippet:

.. literalinclude:: include/snippets/workflows_create_diamond_fcc.py
    :language: python

For the equation of state you need another function that takes as input a ``StructureData`` object and a rescaling factor, and returns a ``StructureData`` object with the rescaled lattice parameter:

.. literalinclude:: include/snippets/workflows_rescale.py
    :language: python

In order to generate the rescaled starting structures, say for five different lattice parameters you would combine the two functions.
Open a ``verdi shell``, define the two functions from the previous snippets and enter the following commands:

.. code:: python

    initial_structure = create_diamond_fcc('Si')
    rescaled_structures = [rescale(initial_structure, factor) for factor in (0.98, 0.99, 1.0, 1.1, 1.2)]

and store them in the database:

.. code:: python

    initial_structure.store()
    for structure in rescaled_structures:
       structure.store()

As expected, all the structures that you have created are not linked in any manner as you can verify via the ``get_incoming()``/``get_outgoing()`` methods of the ``StuctureData`` class.
Instead, you would like these objects to be connected as sketched in :numref:`2019_sintef_fig_provenance_process_functions`.

.. _2019_sintef_fig_provenance_process_functions:
.. figure:: include/images/process_functions.png

   Typical graphs created by using calculation and work functions.
   (a) The calculation function ``create_structure`` takes a ``Str`` object as input and returns a single ``StructureData`` object which is used as input for the calculation function ``rescale`` together with a ``Float`` object.
   This latter calculation function returns another ``StructureData`` object, defining a crystal with a rescaled lattice constant.
   (b) Graph generated by a work function that calls two calculation functions.
   A wrapper work function ``create_rescaled`` calls serially the calculation functions ``create_structure`` and ``rescale``.
   This relationship is stored via ``CALL`` links.


Now that you are familiar with AiiDA, you know that the way to connect two data nodes is through a calculation.
In order to 'wrap' python functions and automate the generation of the needed links, in AiiDA we provide you with what we call 'process functions'.
There are two variants of process functions:

 * calculation functions
 * work functions

These operate mostly the same, but they should be used for different purposes, which will become clear later.
A normal function can be converted to a calculation function by using the ``@calcfunction`` decorator [#f1]_ that takes care of storing the execution as a calculation and adding the links between the input and output data nodes.

To turn the original functions ``create_diamond_fcc`` and ``rescale`` into calculation functions, simply change the definition as follows:

.. code:: python

    # Add this import
    from aiida.engine import calcfunction

    # Add decorators
    @calcfunction
    def create_diamond_fcc(element):
        ... (same as above)

    @calcfunction
    def rescale(structure, scale):
        ... (same as above)

Note that the only change is that the function definitions were 'decorated' with the ``@calcfunction`` line.
This is the only thing that is necessary to transform the plain python functions magically into fully-fledged AiiDA process functions.

.. note::

    The only additional change necessary, is that process function input and outputs need to be ``Data`` nodes, so that they can be stored in the database.
    AiiDA objects such as ``StructureData``, ``Dict``, etc. carry around information about their provenance as stored in the database.
    This is why we must use the special database-storable types ``Float``, ``Str``, etc. as shown in the snippet below.

Try now to run the following script:

.. code:: python

    from aiida.orm import Float, Str
    initial_structure = create_diamond_fcc(Str('Si'))
    rescaled_structures = [rescale(initial_structure, Float(factor)) for factor in (0.98, 0.99, 1.0, 1.1, 1.2)]

and check now that the output of ``initial_structure`` as well as the input of the rescaled structures point to an intermediate node, representing the execution of the calculation function, see :numref:`2019_sintef_fig_provenance_process_functions`.
For instance, you can check that the output links of ``initial_structure`` are the five ``rescale`` calculations:

.. code:: python

    initial_structure.get_outgoing().all_nodes()

which outputs

.. code:: bash

    [<CalcFunctionNode: uuid: 9bc5e0f5-fbe4-4fad-a0d1-cf5893dac132 (pk: 437) (abc.rescale)>,
     <CalcFunctionNode: uuid: 338858ce-779b-455a-8fad-6ac71ba0d1e3 (pk: 434) (abc.rescale)>,
     <CalcFunctionNode: uuid: 0c601f8c-aa49-4957-bea1-cd796de4a323 (pk: 431) (abc.rescale)>,
     <CalcFunctionNode: uuid: bbe4fab4-6939-4f05-8bcd-5120e03ddade (pk: 428) (abc.rescale)>,
     <CalcFunctionNode: uuid: d5e68e04-8ab7-4f3a-90ff-a61f7fd4c247 (pk: 425) (abc.rescale)>]

and the inputs of each ``CalcFunctionNode`` 'rescale' are obtained with:

.. code:: python

    for structure in initial_structure.get_outgoing().all_nodes():
        print(structure.get_incoming().all_nodes())

that will return

.. code:: bash

    [<StructureData: uuid: 65f50f4c-9925-4362-9c6e-f82eea83f6ce (pk: 423)>, <Float: uuid: 2adb3204-4686-4f6f-a1f5-dc2df7d4aff7 (pk: 436) value: 1.2>]
    [<StructureData: uuid: 65f50f4c-9925-4362-9c6e-f82eea83f6ce (pk: 423)>, <Float: uuid: 047406f8-c72c-4e7f-8fb2-947b81a60652 (pk: 433) value: 1.1>]
    [<StructureData: uuid: 65f50f4c-9925-4362-9c6e-f82eea83f6ce (pk: 423)>, <Float: uuid: 06c4a6d8-e1a2-4ddc-851d-0fe70860a96b (pk: 430) value: 1.0>]
    [<StructureData: uuid: 65f50f4c-9925-4362-9c6e-f82eea83f6ce (pk: 423)>, <Float: uuid: 1e1a3af3-7c76-41ff-b002-2885121cbd9e (pk: 427) value: 0.99>]
    [<StructureData: uuid: 65f50f4c-9925-4362-9c6e-f82eea83f6ce (pk: 423)>, <Float: uuid: 0f0cef0b-f1fd-4bf4-b264-78a84ebd5db8 (pk: 424) value: 0.98>]

Function nesting
~~~~~~~~~~~~~~~~
Calculation functions can be 'chained' together by wrapping them together in a work function.
The work function works almost exactly the same as a calculation function, except that it cannot 'create' data, but rather is used to 'call' calculation functions that do the calculations for it.
The calculation functions that it calls will be automatically linked in the provenance graph through 'call' links.
As an example, let us combine the two previously defined calculation functions by means of a wrapper work function called 'create_rescaled' that takes as input the element and the rescale factor.

Type in your shell (or modify the functions defined in ``create_rescale.py`` and then run):

.. include:: include/snippets/workflows_create_rescaled.py
    :code: python

and create an already rescaled structure by typing

.. code:: python

    rescaled = create_rescaled(element=Str('Si'), scale=Float(0.98))

Now inspect the input links of ``rescaled``:

.. code:: ipython

    In [6]: rescaled.get_incoming().all_nodes()
    Out[6]:
    [<WorkFunctionNode: uuid: d6afac0e-d1b3-4d66-9689-8b3347e6e315 (pk: 441) (abc.create_rescaled)>,
     <CalcFunctionNode: uuid: 83b94be8-ded5-4dcf-a929-3d57301d4dde (pk: 444) (abc.rescale)>]

The object ``rescaled`` has two incoming links, corresponding to *two* different calculations as input.
These correspond to the calculations 'create_rescaled' and 'rescale' as shown in :numref:`2019_sintef_fig_provenance_process_functions`.
To see the 'call' link, inspect now the outputs of the ``WorkFunctionNode`` which corresponds to the ``create_rescaled`` work function.
Write down its ``<pk>`` (in general, it will be different from 441), then in the shell load the corresponding node and inspect the outputs:

.. code:: ipython

    In [12]: node = load_node(<pk>)
    In [13]: node.get_outgoing().all()

You should be able to identify the two children calculations as well as the final structure (you will see the process nodes linked via CALL links: these are process-to-process links representing the fact that ``create_rescaled`` called two calculation functions).
The graphical representation of what you have in the database should match :numref:`2019_sintef_fig_provenance_process_functions`.

.. _2019_sintef_sync:

Run a simple workflow
---------------------
Let us now use the work and calculation functions that we have just created to build a simple workflow to calculate the equation of state of silicon.
We will consider five different values of the lattice parameter obtained rescaling the experimental minimum, ``a=5.431``, by a factor in ``[0.96, 0.98, 1.0, 1.02, 1.04]``.
We will write a simple script that runs a series of five calculations and at the end returns the volume and the total energy corresponding to each value of the lattice parameter.
For your convenience, besides the functions that you have written so far in the file ``create_rescale.py``, we provide you with some other utilities to get the correct pseudopotential and to generate a pw input file, in :download:`common_wf.py <../scripts/common_wf.py>`.

We have already created the following script, which you can :download:`download <../scripts/simple_sync_workflow.py>`, but please go through the lines carefully and make sure you understand them.
We suggest that you first have a careful look at it before running it:

.. include:: ../scripts/simple_sync_workflow.py
    :code: python

If you look into the previous piece of code, you will notice that the way we submit a QE calculation is slightly different from what you have seen in the first part of the tutorial.
The following:

.. code:: python

    calculations[label] = run(PwCalculation, **inputs)

runs in the current python session (without the daemon), waits for its completion and returns the output in the user-defined variable ``result``.
The latter is a dictionary whose values are the output nodes generated by the work function, with the link labels as keys.
For example once the function is finished, in order to access the total energy, we need to access the ``Dict`` node which is linked via the 'output_parameters' link (see again Fig. 1 of Day 1 Tutorial, to see inputs and outputs of a Quantum ESPRESSO calculation).
Once the right node is retrieved as ``result['output_parameters']``, we need to get the ``energy`` attribute.
The global operation is achieved by the command

.. code:: python

    result['output_parameters'].dict.energy

To collect these results from the various calculations into a single data node, we need one final calculation function to do so.
Since the ``run_eos_wf`` is a 'workflow'-like processes, which cannot create data, this operation **cannot** simply be done in the work function body itself.
To keep the provenance **we have to** do this through a calculation function.
This is done by the ``create_eos_dictionary`` calculation function, that receives as inputs, the output parameters nodes from the completed calculations:

.. code:: python

    @calcfunction
    def create_eos_dictionary(**kwargs):
        """Create a single `Dict` node from the `Dict` output parameters of completed `PwCalculations`.

        The dictionary will contain a list of tuples, where each tuple contains the volume, total energy and its units
        of the results of a calculation.

        :return: `Dict` node with the equation of state results
        """
        eos = [(result.dict.volume, result.dict.energy, result.dict.energy_units) for label, result in kwargs.items()]
        return Dict(dict={'eos': eos})

It constructs a new ``Dict`` node that contains a single value ``eos`` which is a list of tuples with the relevant data for each calculation.
If you were to inspect the returned data node, with for example ``verdi data dict show`` you would see something like:

.. code:: bash

    {
        "eos": [
            [
                40.04786949775,
                -308.193208771881,
                "eV"
            ],
            [
                37.6927343883263,
                -307.990673492459,
                "eV"
            ],
            [
                35.4317918679613,
                -307.666113525946,
                "eV"
            ],
            [
                45.048406674717,
                -308.308206255253,
                "eV"
            ],
            [
                42.4991194939683,
                -308.293522312459,
                "eV"
            ]
        ]
    }

As you see, the function ``run_eos_wf`` has been decorated as a work function to keep track of the provenance.
To run the workflow it suffices to call the function ``run_eos_wf`` in a python script providing the required input parameters.
For simplicity, we have included few lines at the end of the script that invoke the function with a static choice of parameters:

.. code:: python

    def run_eos(code=load_code('qe-6.4.1-pw@localhost'), pseudo_family='SSSP', element='Si'):
        return run_eos_wf(code, Str(pseudo_family), Str(element))

    if __name__ == '__main__':
        run_eos()

To get a reference to the node that represents the function execution, we can ask the ``run`` function to return the node, in addition to the results.
Instead of calling the work function to run it, we can use the method ``run_get_node``:

.. code:: python

    results, node = run_eos_wf.run_get_node(code, Str(pseudo_family), Str(element))
    print('run_eos_wf<{}> completed'.format(node.pk))

Run the workflow:

.. code:: bash

    verdi run simple_sync_workflow.py

The command above locks the shell until the full workflow has completed (we will see in a moment how to avoid this).
While the function is running, you can use (in a different shell) the command ``verdi process list`` to show ongoing and finished processes.
You can 'grep' for the ``<pk>`` you are interested in.
Additionally, you can use the command ``verdi process status <pk>`` to show the tree of the calculatino functions called by the root work function with a given ``<pk>``.

Wait for the work function to finish, then call the function ``plot_eos(<pk>)`` that we provided in the file ``common_wf.py`` to plot the equation of state and fit it with a Birch–Murnaghan equation.

.. _2019_sintef_wf_multiple_calcs:

Run multiple calculations
-------------------------

You should have noticed that the calculations for different lattice parameters are executed serially, although they might perfectly be executed in parallel because their inputs and outputs are not connected in any way.
In the language of workflows, these calculations are executed in a synchronous (or blocking) way, whereas we would like to have them running *asynchronously* (i.e., in a non-blocking way, to run them in parallel).
One way to achieve this, is to submit the calculation to the daemon using the ``submit`` function.
Make a copy of the script ``simple_sync_workflow.py`` that we worked on in the previous section and name it ``simple_submit_workflow.py``.
To make the new script work asynchronously, simply change the following subset of lines:

.. code:: python

    from aiida.engine import run

    [...]

    for label, factor in zip(labels, scale_factors):

        [...]

        calculations[label] = run(PwCalculation, **inputs)

    [...]

    inputs = {label: result['output_parameters'] for label, result in calculations.items()}
    eos = create_eos_dictionary(**inputs)

    [...]

replacing them with

.. code:: python

    from aiida.engine import submit
    from time import sleep

    [...]

    for label, factor in zip(labels, scale_factors):
        [...]

        # Replace `run` with `submit`
        calculations[label] = submit(PwCalculation, **inputs)

    [...]

    # Wait for the calculations to finish
    for calculation in calculations.values():
        while not calculation.is_finished:
            sleep(1)

    inputs = {label: node.get_outgoing().get_node_by_label('output_parameters') for label, node in calculations.items()}
    eos = create_eos_dictionary(**inputs)

The main differences are:

-  ``run`` is replaced by ``submit``
-  The return value of ``submit`` is not a dictionary describing the outputs of the calculation, but it is the node that represents the execution of that calculation.
-  Each calculation starts in the background and calculation nodes are added to the ``calculations`` dictionary.
-  At the end of the loop, when all calculations have been launched with ``submit``, another loop is used to wait for all calculations to finish before gathering the results as the final step.

In the next section we will show you another way to achieve this, which has the added bonus that it introduces checkpoints in the work function, from which the process can be resumed should it be interrupted.
After applying the modifications, run the script.
You will see that all calculations start at the same time, without waiting for the previous ones to finish.

If in the meantime you run ``verdi process status <pk>``, all five calculations are already shown as output.
Also, if you run ``verdi process list``, you will see how the calculations are submitted to the scheduler.

.. _2019_sintef_workchainsimple:

Workchains, or how not to get lost if your computer shuts down or crashes
-------------------------------------------------------------------------

The simple workflows that we have used so far have been launched by a python script that needs to be running for the whole time of the execution, namely the time in which the calculations are submitted, and the actual time needed by Quantum ESPRESSO to perform the calculation and the time taken to retrieve the results.
If you had killed the main python process during this time, the workflow would not have terminated correctly.
Perhaps you killed the calculation and you experienced the unpleasant consequences: intermediate calculation results are potentially lost and it is extremely difficult to restart a workflow from the exact place where it stopped.

In order to overcome this limitation, in AiiDA we have implemented a way to insert checkpoints, where the main code defining a workflow can be stopped (you can even shut down the machine on which AiiDA is running!).
We call these work functions with checkpoints 'work chains' because, as you will see, they basically amount to splitting a work function in a chain of steps.
Each step is then ran by the daemon, in a way similar to the remote calculations.

Here below you can find the basic rules that allow you to convert your workfunction-based script to a workchain-based one and a snippet example focusing on the code used to perform the calculation of an equation of state.

.. include:: ../scripts/equation_of_state.py
    :code: python

.. warning::

    WorkChains need to be defined in a **separate file** from the script used to run them.
    E.g. save your WorkChain in ``workchains.py`` and use ``from workchains import MyWorkChain`` to import it in your script.

    Furthermore, the directory containing the WorkChain definition needs to be in the ``PYTHONPATH`` in order for the AiiDA daemon to find it.
    If your ``workchains.py`` sits in ``/home/max/workchains``, add a line ``export PYTHONPATH=$PYTHONPATH:/home/max`` to the ``/home/max/.virtualenvs/aiida/bin/activate`` script, followed by ``verdi daemon restart``.

-   Instead of using decorated functions you need to define a class, inheriting from a prototype class called ``WorkChain`` that is provided by AiiDA in the ``aiida.engine`` module.

-   Within your class you need to implement a ``define`` classmethod that always takes ``cls`` and ``spec`` as inputs.
    Here you specify the main information on the workchain, in particular:

    -   The *inputs* that the workchain expects.
        This is obtained by means of the ``spec.input()`` method, which provides as the key feature the automatic validation of the input types via the ``valid_type`` argument.
        The same holds true for outputs, as you can use the ``spec.output()`` method to state what output types are expected to be returned by the workchain.

    -   The ``outline`` consisting in a list of 'steps' that you want to run, put in the right sequence.
        This is obtained by means of the method ``spec.outline()`` which takes as input the steps.
        *Note*: in this example we just split the main execution in two sequential steps, that is, first ``run_eos`` then ``results``.
        However, more complex logic is allowed, as will be explained in :ref:`another section<2019_sintef_convpressure>`.

-   You need to split your main code into methods, with the names you specified before into the outline (``run_eos`` and ``results`` in this example).
    Where exactly should you split the code?
    Well, the splitting points should be put where you would normally block the execution of the script for collecting results in a standard work function, namely whenever you call the method ``.result()``.
    Each method should accept only one parameter, ``self``, e.g. ``def step_name(self)``.

-   You will notice that the methods reference the attribute ``ctx`` through ``self.ctx``, which is called the *context* and is inherited from the base class ``WorkChain``.
    A python function or process function normally just stores variables in the local scope of the function.
    For instance, in the example of :ref:`this subsection<2019_sintef_sync>`, you stored the completed calculations in the ``calculations`` dictionary, that was a local variable.

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

.. code:: python

    from aiida.engine import run
    run(EquationOfState, element=Str('Si'), code=load_code('qe-6.4.1-pw@localhost'), pseudo_family=Str('SSSP'))

While the workflow is running, you can check (in a different terminal) what is happening to the calculations using ``verdi process list``.
You will see that after a few seconds the calculations are all submitted to the scheduler and can potentially run at the same time.

.. warning::

    The calculations launched by the work chain will now be submitted to the daemon, instead of run in the same interpreter
    However, by using ``run`` on the work chain itself, it will still not be able to restart.
    To make the work chain save its checkpoints, you should use the ``submit`` launcher instead.

As an additional exercise (optional), instead of running the main workflow ``EquationOfState``, try to submit it.
Note that the file where the work chains is defined will need to be globally importable (so the daemon knows how to load it) and you need to launch it (with ``submit``) from a different python file.
The easiest way to achieve this is typically to embed the workflow inside a python package.

.. note::

    As good practice, you should try to keep the steps as short as possible in term of execution time.
    The reason is that the daemon can be stopped and restarted only between execution steps and not if a step is in the middle of a long execution.

Finally, as an optional exercise if you have time, you can jump to :ref:`this appendix<2019_sintef_convpressure>`, which shows how to introduce more complex logic into your work chains (if conditionals, while loops etc.).
The exercise will show how to realize a convergence loop to obtain the minimum-volume structure in a EOS using the Newton's algorithm.

.. note::

    You might see warnings that say ``Exception trying to save checkpoint, this means you will not be able to restart in case of a crash until the next successful checkpoint``.
    These are generated by the ``PwCalculation`` which is unable to save a checkpoint because it is not in a so called 'importable path'.
    Simply put, this means that if AiiDA were to try and reload the class it wouldn't know which file to find it in.
    To get around this you could simply put the workchain in a different file that is in the 'PYTHONPATH' and then launch it by importing it in your launch file.
    In this way AiiDA knows where to find it next time it loads the checkpoint.


.. rubric:: Footnotes

.. [#f1] In simple words, a decorator is a function that modifies the behavior of another function. In python, a function can be decorated by adding a line of the form ``@decorating_function_name`` on the line just before the ``def`` line of the decorated function. If you want to know more, there are many online resources explaining python decorators.


The ultimate aim of this section is to create a workflow to calculate the equation of state of silicon.
This is a very common task for an *ab initio* researcher.
An equation of state consists in calculating the total energy (E) as a function of the unit cell volume (V).
The minimal energy is reached at the equilibrium volume.
Equivalently, the equilibrium is defined by a vanishing pressure (p=-dE/dV).
In the vicinity of the minimum, the functional form of the equation of state can be approximated by a parabola.
Such an approximation greatly simplifies the calculation of the bulk modulus, that is proportional to the second derivative of the energy (a more advanced treatment requires fitting the curve with, e.g., the Birch–Murnaghan expression).

The process of calculating an equation of state puts together several operations.
First, we need to define and store in the AiiDA database the basic structure of, e.g., bulk Si.
Next, one has to define several structures with different lattice parameters.
Those structures must be connected between them in the database, in order to ensure that their provenance is recorded.
In other words, we want to be sure that in the future we will know that if we find a bunch of rescaled structures in the database, they all descend from the same one.
How to link two nodes in the database in an easy way is the subject of :ref:`2019_sintef_provenancewf`.

In the following sections, the newly created structures will then serve as an input for total energy calculations performed, in this tutorial, with Quantum ESPRESSO.
This task is very similar to what you have done in the previous part of the tutorial.
Finally, you will fit the resulting energies as a function of volume to get the bulk modulus.
As the EOS task is very common, we will show how to automate its computation with workflows, and how to deal with both serial and parallel (i.e., independent) execution of multiple tasks.
Finally, we will show how to introduce more complex logic in your workflows such as loops and conditional statements (:ref:`see this section<2019_sintef_convpressure>`), with an example on a convergence loop to find iteratively the minimum of an EOS.