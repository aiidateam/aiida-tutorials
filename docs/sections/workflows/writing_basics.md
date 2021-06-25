(workflows-writing-basics)=

# Writing Workflows

(**TODO: Fix content so it focuses on writing workflows and move other content elsewhere**)

:::::{important}

In order to launch the workflows of this section, we will be using the computers and codes set up in the first two hands-on sessions.
You should make sure that your default profile is set to the profile which you set up during these sessions (see {ref}`fundamentals-setup-profile`).
You can do this using:

```{code-block} console

$ verdi profile setdefault <PROFILE_NAME>
Success: <PROFILE_NAME> set as default profile

```

Where `<PROFILE_NAME>` is the name of the profile you set up (`quicksetup` by default).
You should now have the following codes available:

```{code-block} console

$ verdi code list
# List of configured codes:
# (use 'verdi code show CODEID' to see the details)
* pk 5 - add@tutor
* pk 2083 - qe-6.5-pw@localhost

```

:::::

The aim of this tutorial is to introduce how to write and launch workflows in AiiDA.

In this section, you will learn to:

1. Understand how to add simple python functions to the AiiDA database.
2. Learn how to write and launch a simple workflow in AiiDA.
3. Learn how to write and launch a workflow using checkpoints: the work chain.
4. Apply these concepts to calculate the equation of state of silicon.

:::{note}

To focus on the AiiDA concepts, the initial examples in this hands-on are purposefully kept very simple.
At the end of the section, you can find a more extensive real-world example.

:::

## Workflows

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

### Workflow in AiiDA

A workflow in AiiDA is a {ref}`process <topics:processes:concepts>` that calls other workflows and calculations and optionally *returns* data and as such can encode the logic of a typical scientific workflow.
Currently, there are two ways of implementing a workflow process:

* {ref}`work functions<topics:workflows:concepts:workfunctions>`
* {ref}`work chains<topics:workflows:concepts:workchains>`

The main difference between them is that *work functions* are completely executed by the AiiDA daemon, whereas  a *work chain* can submit calculation jobs that can be e.g. run through a scheduler that is periodically monitored by the daemon.
Thus, *work functions* should be used for fast workflows that won't keep the AiiDA daemon very busy, otherwise, a *work chain* is in order.

:::{note}

For more details on the concept of a workflow, and the difference between a work function and a work chain, please see the corresponding {ref}`topics section<topics:workflows:concepts>` in the AiiDA documentation.

:::

Here we present a brief introduction on how to write both workflow types.

### Work function

A *work function* is a process function that calls one or more calculation functions and *returns* data that has been *created* by the calculation functions it has called.
Moreover, work functions can also call other work functions, allowing you to write nested workflows.
Writing a work function, whose provenance is automatically stored, is as simple as writing a Python function and decorating it with the {func}`~aiida.engine.processes.functions.workfunction` decorator:

```{literalinclude} include/code/add_multiply.py
:language: python
:start-after: start-marker

```

It is important to reiterate here that the {func}`~aiida.engine.processes.functions.workfunction`-decorated `add_multiply()` function does not *create* any new data nodes.
The `add()` and `multiply()` calculation functions create the `Int` data nodes, all the work function does is *return* the results of the `multiply()` calculation function.
Moreover, both calculation and work functions can only accept and return data nodes, i.e. instances of classes that subclass the {class}`~aiida.orm.nodes.data.data.Data` class.

:::{note}

In the above example, we created a workflow just to add then multiply two numbers.
Please, keep in mind that in real situations instead of simple addition or multiplication, we would have complex calculations such as a DFT calculation or a data analysis.

:::


Copy the code snippet above and put it into a Python script (e.g. {download}`add_multiply.py <include/code/add_multiply.py>`).
In the terminal, go inside the folder where you stored the script (`cd \MY\PATH`).
Next, import the add_multiply work function in the `verdi shell`:

```{code-block} ipython

In [1]: from add_multiply import add_multiply

```


Once again, running a work function is as simple as calling a typical Python function: simply call it with the required input arguments:

```{code-block} ipython

In [2]: result = add_multiply(Int(2), Int(3), Int(5))

```

Here, the `add_multiply` work function returns the output `Int` node and we assign it to the variable `result`.
Note that - similar to a calculation function - the input arguments of a work function must be an instance of `Data` node, or any of its subclasses.
Just calling the `add_multiply` function with regular integers will result in a `ValueError`, as these cannot be stored in the provenance graph.

:::{note}

Although the example above shows the most straightforward way to run the `add_and_multiply` work function, there are several other ways of running processes that can return more than just the result.
For example, the `run_get_node` function from the AiiDA engine returns both the result of the workflow and the work function node.
See the {ref}`corresponding topics section for more details <topics:processes:usage:launching>`.

:::


When we check the AiiDA list of processes (including those that are _terminated_ with `-a / --all`):

```{code-block} console
$ verdi process list -a -p 1
  PK  Created    Process label    Process State    Process status
----  ---------  ---------------  ---------------  ----------------
...
1859  1m ago     add_multiply     ⏹ Finished [0]
1860  1m ago     add              ⏹ Finished [0]
1862  1m ago     multiply         ⏹ Finished [0]
```

Copy the PK of the `add_multiply` work function and check its status with `verdi process status <PK>` (in the above example, the PK is `1859`):
```{code-block}
add_multiply<1859> Finished [0]
    ├── add<1860> Finished [0]
    └── multiply<1862> Finished [0]
```

Finally, you can also check the details of the inputs and outputs of the work function:
```{code-block} console
$ verdi process show <PK>
Property     Value
-----------  ------------------------------------
type         add_multiply
state        Finished [0]
pk           1859
uuid         c65df725-6065-40ec-8343-6ee9ef68ca9a
label        add_multiply
description
ctime        2021-06-07 14:48:06.342948+00:00
mtime        2021-06-07 14:48:06.835870+00:00

Inputs      PK  Type
--------  ----  ------
x         1856  Int
y         1857  Int
z         1858  Int

Outputs      PK  Type
---------  ----  ------
result     1863  Int

Called      PK  Type
--------  ----  --------
CALL      1860  add
CALL      1862  multiply
```

Notice that each input and output to the work function `add_multiply` is stored as a node.

### Work chain

The simple work function that we ran in the previous section was launched by a Python script that needs to be running for the whole time of the execution.
If you had killed the main Python process during this time, the workflow would not have terminated correctly.
This is not a significant issue when running these simple examples, but when you start running workflows that take longer to complete, this can become a real problem.

In order to overcome this limitation, AiiDA allows you to insert checkpoints, where the main code defining a workflow can be stopped (you can even shut down the machine on which AiiDA is running!).
We call these workflows with checkpoints _work chains_ because, as you will see, they basically amount to splitting a work function into a chain of steps.
Each step is then run by the daemon, in a way similar to the remote calculations.

When the workflow you want to run is more complex and takes longer to finish, it is better to write a work chain.

#### Constructing our first work chain

Next, we are going to work on an example of a work chain.
We will start with a very simple work chain which we then modify step by step to introduce new features.
Our first mission is to write a work chain that receives a single input and passes it as the output.
Let's get started by creating a file for our work chain (e.g. `my_first_workchain.py`), and adding the following piece of code:

```{literalinclude} include/code/new_scripts/my_first_workchain_1_output_input.py
:language: python
:lines: 1-15
```

Writing a work chain in AiiDA requires creating a class that inherits from the {class}`~aiida.engine.processes.workchains.workchain.WorkChain` class, as shown above.
You can give the work chain any valid Python class name, but the convention is to have it end in {class}`~aiida.engine.processes.workchains.workchain.WorkChain` so that it is always immediately clear what it references.
For this most basic example, we chose `OutputInputWorkChain`, since it simply passes the input `Int` node as an output.

##### Define method

The most important method to implement for every work chain is the `define()` method.
This class method must always start by calling the `define()` method of its parent class (the [`super()`](https://realpython.com/python-super/) function referes to the parent class).
The `define()` method is used to _define_ the specifications of the work chain, which are contained in the work chain `spec`:

The **inputs** are specified using the `spec.input()` method:

```{literalinclude} include/code/new_scripts/my_first_workchain_1_output_input.py
:language: python
:lines: 13
```

  The first argument of the `input()` method is a string that specifies the label of the input, in this case `'x'`.
  The `valid_type` keyword argument allows you to specify the required node type of the input.
  Other keyword arguments allow the developer to set a default for the input, or indicate that an input should not be stored in the database, see {ref}`the process topics section <topics:processes:usage:spec>` for more details.

:::{note}

All inputs and outputs of a work chain must be [AiiDA data types](https://aiida.readthedocs.io/projects/aiida-core/en/latest/topics/data_types.html) so they can be stored as a `Node` in the AiiDA database.

:::

The **outline** is specified using the `spec.outline()` method:
```{literalinclude} include/code/new_scripts/my_first_workchain_1_output_input.py
:language: python
:lines: 14
```
  The outline of the workflow is constructed from the methods of the work chain class.
  For the `OutputInputWorkChain`, the outline is a single step.
  As we will see later, it's possible of course to include multiple steps and add logic directly in the outline in order to define more complex workflows as well.
  See the {ref}`work chain outline section <topics:workflows:usage:workchains:define_outline>` for more details.

The **outputs** are specified using the `spec.output()` method:
```{literalinclude} include/code/new_scripts/my_first_workchain_1_output_input.py
:language: python
:lines: 15
```
  This method is very similar in its usage to the `input()` method, and just like the inputs you can have many outputs.

:::{note}

For more information on the `define()` method and the process spec, see the {ref}`corresponding section in the topics <topics:processes:usage:defining>`.

:::{margin} **Further reading**
For more information on the `define()` method and the process spec, see the {ref}`corresponding section in the topics <topics:processes:usage:defining>`.
:::

##### Defining the steps in the outline

Hopefully you now understand how to _define_ your work chain using the `define()` method.
Of course, we still have to instruct the work chain what to actually do for each _step_ in the `outline`.
This is done by adding them as methods to the work chain class.
Let's do this for our single step, i.e., `result`:

```{literalinclude} include/code/new_scripts/my_first_workchain_1_output_input.py
:language: python
:emphasize-lines: 17-21
```

As you can see, we defined the `result()` method in the class scope.
In this step, we are simply declaring the output labeled `workchain_result`, and passing to it the input label `x`.
As the work chain input is an `Int` node, the output also satisfies this condition.

Now we should be ready to run our first work chain!

##### Run the work chain

In the terminal, navigate to the folder where you saved the script with your first work chain and open a `verdi shell`:

```{code-block} ipython
In [1]: from aiida.engine import run
In [2]: from my_first_workchain import OutputInputWorkChain
In [3]: result = run(OutputInputWorkChain, x=Int(4) )
In [4]: result
Out[2]:
{'product': <Int: uuid: 9c5c29de-6176-41fe-a051-672a5348e631 (pk: 1909) value: 4>}
```

Note that, if you had tried to pass as input an integer, for example with:
```{code-block} ipython
...
In [3]: result = run(OutputInputWorkChain, x=4 )
```
that would have raised an error as a Python integer is not an AiiDA data type.

Exit the `verdi shell` and check the list of processes with `verdi process list`, using `-a/--all` to also see _terminated_ processes and `-p/--past-days 1` to only see processes _created_ in the past day:
```{code-block} console
$ verdi process list -a -p 1
...
1982  2m ago     OutputInputWorkChain  ⏹ Finished [0]
```
Also check the status of the process that corresponds to the work chain `OutputInputWorkChain`:
```{code-block} console
$ verdi process process status 1982
OutputInputWorkChain<1982> Finished [0] [None]
```
And show some details about the inputs and outputs with:
```{code-block} console
$ verdi process show 1982
Property     Value
-----------  ------------------------------------
type         OutputInputWorkChain
state        Finished [0]
pk           1982
uuid         da86a26e-9b8b-4ab2-94ae-84016a17152a
label
description
ctime        2021-06-19 23:13:59.238930+00:00
mtime        2021-06-19 23:13:59.431924+00:00

Inputs      PK  Type
--------  ----  ------
x         1981  Int

Outputs             PK  Type
----------------  ----  ------
workchain_result  1981  Int
```
Observe that the PK of the input is the same as the output.
That is because our first work chain did not create any data, but just passed the input as the output.

#### How **not** to create data

Our next goal is to write a work chain that receives two inputs, adds them together, and outputs the sum.
For that, let's update the work chain in the `my_first_workchain.py` file that we have just created.
We will make the following changes (highlighted):

```{literalinclude} include/code/new_scripts/my_first_workchain_2_wrong_add.py
:language: python
:emphasize-lines: 5,14,21,23
```

Here, the first thing we did was to update the name of the work chain to `AddWorkChain` to better represent its new functionality.
Next, we declared a new input in the `define()` method:

```{literalinclude} include/code/new_scripts/my_first_workchain_2_wrong_add.py
:language: python
:lines: 14
```
After that, in the `result()` method, we added the two inputs and declared the sum as the output:

```{literalinclude} include/code/new_scripts/my_first_workchain_2_wrong_add.py
:language: python
:lines: 21-23
```

##### Run the work chain

We can now try to run the work chain as we have done before for the `OutputInputWorkChain`.
For example, navigate to the folder where you have the work chain Python script, open a `verdi shell` session and execute:

```{code-block} ipython
In [1]: from aiida.engine import run
In [2]: from my_first_workchain import AddWorkChain
In [3]: result = run(AddWorkChain, x=Int(4), y=Int(3) )

```
If everything went according to plan, you must have got a `ValueError` like this:

```{code-block} ipython
...
----> 3 result = run(AddWorkChain, x=Int(4), y=Int(3) )
...
ValueError: Workflow<AddWorkChain> tried returning an unstored `Data` node. This likely means new `Data` is being created inside the workflow. In order to preserve data provenance, use a `calcfunction` to create this node and return its output from the workflow
```
As the error message explains, the work chain is trying to create new `Data`.
However, in order to preserve the _data_ provenance, data can only be created by `calculation functions` or `calculation jobs`.
So, to correctly create the new data inside the work chain, we'll have to add a calculation function to our script.

#### Creating data with calculation function

Here, we demonstrate how to process and create new data in a work chain using a `calculation function`.
To do this, we'll define a calculation function that adds the two numbers together and call this function inside a work chain step.
You can see the highlighted changes below:

```{literalinclude} include/code/new_scripts/my_first_workchain_3_add_calcfunc.py
:language: python
:emphasize-lines: 2, 5-7, 27
```
We first imported the `calcfunction` _decorator_ from the aiida engine.
Then, we defined the `addition()` function outside the work chain scope, then we decorated it with `@calcfunction`:

```{literalinclude} include/code/new_scripts/my_first_workchain_3_add_calcfunc.py
:language: python
:pyobject: addition
```
And finally, we added the two inputs using the _calculation function_ that we have just declared:

```{literalinclude} include/code/new_scripts/my_first_workchain_3_add_calcfunc.py
:language: python
:lines: 27
```

This will ensure that the `Int` node created by the addition is part of the data provenance.

##### Run the work chain

Let's run the work chain that uses the `addition` calculation function.
Once again make sure you are in the folder where you have the work chain Python script, open the `verdi shell` and execute:

```{code-block} ipython
In [1]: from aiida.engine import run
In [2]: from my_first_workchain import AddWorkChain
In [3]: result = run(AddWorkChain, x=Int(4), y=Int(3) )
In [4]: result
Out[4]: {'workchain_result': <Int: uuid: 21cf16e9-58dc-4566-bbd7-b170fcd628ee (pk: 1990) value: 7>}

```

You can now close the `verdi shell` session and check the information about the work chain that we just ran:

```{code-block} console
$ verdi process list -a -p 1
...
1988  49s ago    AddWorkChain     ⏹ Finished [0]
1989  49s ago    addition         ⏹ Finished [0]
```

Also check the status of the process that corresponds to the work chain `AddWorkChain`:

```{code-block} console
$ verdi process process status 1988
AddWorkChain<1988> Finished [0] [None]
    └── addition<1989> Finished [0]
```
Notice that now we see a branch in the work chain tree, which indicates that a process (the `addition` _calculation function_) was called by the `AddWorkChain`.
Next, you can obtain some details about the in- and outputs with:

```{code-block} console
:emphasize-lines: 15-16,20
$ verdi process show 1988
Property     Value
-----------  ------------------------------------
type         AddWorkChain
state        Finished [0]
pk           1988
uuid         18ffdcfa-395c-4579-be82-a038ee0bbc22
label
description
ctime        2021-06-22 14:57:21.074444+00:00
mtime        2021-06-22 14:57:21.444217+00:00

Inputs      PK  Type
--------  ----  ------
x         1986  Int
y         1987  Int

Outputs             PK  Type
----------------  ----  ------
workchain_result  1990  Int

Called      PK  Type
--------  ----  ------
CALL      1989  addition
```

Note that the output has its own `PK`, which is different of both inputs.
That is because it is a new data node that was created by the calculation function called by the work chain.

#### Context

When writing your work chain, you may need to pass data between different steps in the outline.
This can be achieved using the context dictionary.
Our new work chain will have the same goal as before, adding its two inputs.
But this time, we will create two steps in the `outline`, one to actually add the inputs and thus creating new data, and another step just to pass the result as an output.
The code will look like this:

```{literalinclude} include/code/new_scripts/my_first_workchain_4_pass_context.py
:language: python
:emphasize-lines: 20, 23, 30, 36
```
We added an extra step called `add` in the `outline` to be executed before `result`:
```{literalinclude} include/code/new_scripts/my_first_workchain_4_pass_context.py
:language: python
:lines: 20
```

Then, we defined the new `add()` method:

```{literalinclude} include/code/new_scripts/my_first_workchain_4_pass_context.py
:language: python
:pyobject: AddWorkChain.add
```
Instead of passing the result of the addition (`summation`) directly as an output, we added it to the work chain **context** using `self.ctx`:

```{literalinclude} include/code/new_scripts/my_first_workchain_4_pass_context.py
:language: python
:lines: 30
```

By doing so, the information stored in the context can now be used by another step of the outline.
In our example, the `self.ctx.summation` is passed as the `workchain_result` output in the `result()` step:

```{literalinclude} include/code/new_scripts/my_first_workchain_4_pass_context.py
:language: python
:pyobject: AddWorkChain.result
```

#### Adding more complexity

Increasing the level of complexity, we want to write a work chain which receives three inputs, multiply the first two inputs and add to that result the value of the third input.
Also, we want the work chain to output both the product of the first two inputs and the final result.
Keep in mind that in real-life examples, in the steps where we are doing mere arithmetic, one shoudl expect complex tasks such as running an external code.
Our code may seem like this:

```{literalinclude} include/code/new_scripts/my_first_workchain_5_multiply_calcfunc.py
:language: python
:emphasize-lines: 10-12, 15, 25-26, 28, 30, 42, 52
```

This work chain above, we first defined a `calculation function` to receive and multiply two inputs using the `@calcfunction` decorator:

```{literalinclude} include/code/new_scripts/my_first_workchain_5_multiply_calcfunc.py
:language: python
:pyobject: multiplication
```

We gave an appropriate name to our work chain, i.e., `MultiplyAddWorkChain()`.
Then, we declared one more input labelled `z`  (to make three in total), and another output labelled `product` (totalizing two outputs) :

```{literalinclude} include/code/new_scripts/my_first_workchain_5_multiply_calcfunc.py
:language: python
:lines: 25
```
```{literalinclude} include/code/new_scripts/my_first_workchain_5_multiply_calcfunc.py
:language: python
:lines: 28
```

Then, we added another step in the outline, i.e., `multiply`, to be executed before the `add` step:

```{literalinclude} include/code/new_scripts/my_first_workchain_5_multiply_calcfunc.py
:language: python
:lines: 26
```

Next, we defined the method that corresponds to this new step:

```{literalinclude} include/code/new_scripts/my_first_workchain_5_multiply_calcfunc.py
:pyobject: MultiplyAddWorkChain.multiply
```

Here, the actual processing of data is performed by the `calculation function` that we defined in the beginning named `multiplication()`.
The output of `multiplication()` was passed to the context as `self.ctx.product`.
Then, in the second step of the outline, `add`, we used the result stored in the context and the third input of the work chain as inputs for the calculation function `addition()`:

```{literalinclude} include/code/new_scripts/my_first_workchain_5_multiply_calcfunc.py
:language: python
:lines: 42
```
whose result was also stored in the context:

```{literalinclude} include/code/new_scripts/my_first_workchain_5_multiply_calcfunc.py
:language: python
:lines: 45
```

Finally, in the method `result()`, we declared the two outputs, the product that resulted from the multiplication of the first two inputs, and the final result that consists of the product added of the third input:

```{literalinclude} include/code/new_scripts/my_first_workchain_5_multiply_calcfunc.py
:language: python
:lines: 51-52
```

Now, run your work chain and examine the results to see if they are equivalent to that of the section {ref}`Creating data with calculation function<Creating data with calculation function>`.

#### Work chain with Calculation Jobs

Until now, we have written work chains that create data via `calculation function` processes.
These processes are executed by the same machine process that is executing the work chain.
The full potential of a work chain is only accessed when it creates independent processes to execute the varios steps of the outline, such as running an external code.
This is achieved through an AiiDA process called `calculation job` ({class}`~aiida.engine.processes.calcjobs.calcjob.CalcJob`).
The execusion of the calculation jobs are managed and controlled by the AiiDA **daemons**.

Here, we demonstrate how to include calculation jobs in our work chain.
We are going to use the example in Section {ref}`Two calculation functions and more outputs<Two calculation functions and more outputs>` and replace the `addition` calculation function.
The resulting code looks like this:

```{literalinclude} include/code/new_scripts/my_first_workchain_6_calcjob.py
:language: python
:emphasize-lines: 1-5, 24, 41-46, 48, 54
```

Let us break down what we did.
First, we imported the {class}`~aiida.engine.processes.calcjobs.calcjob.CalcJob` that we plan on using with the help of the `CalculationFactory`:

```{literalinclude} include/code/new_scripts/my_first_workchain_6_calcjob.py
:language: python
:lines: 5
```

We also declared a new input, which is a code:

```{literalinclude} include/code/new_scripts/my_first_workchain_6_calcjob.py
:language: python
:lines: 24
```

(**TODO: Somebody needs to try and explain this idea of passing a code as an input, then running a calc job process which executes the code...**)


In the `add()` method, which is the second step in the outline of the work chain, instead of a calculation function, we are submitting the {class}`~aiida.engine.processes.calcjobs.calcjob.CalcJob` named `ArithmeticAddCalculation`:

```{literalinclude} include/code/new_scripts/my_first_workchain_6_calcjob.py
:language: python
:pyobject: MultiplyAddWorkChain.add
```

When submitting this calculation job to the daemon, it is **essential** to use the submit method from the work chain instance via `self.submit()`.
Since the result of the addition is only available once the calculation job is finished, the `submit()` method returns the {class}`~aiida.orm.nodes.process.calculation.calcjob.CalcJobNode` of the *future* `ArithmeticAddCalculation` process.
To tell the work chain to wait for this process to finish before continuing the workflow, we return the `ToContext` class, where we have passed a dictionary to specify that the future calculation job node `calc_job_node` should be assigned to the `'summation_calc_job'` context key.

Once the `add` step is complete, the work chain will execute the `result` step.
The result of the addition performed by the `ArithmeticAddCalculation` calculation job is found in the dictionary under the key `outputs`.
Among the outputs of the calculation job, we want the one labbed `sum` to declare it as the work chain output:

```{literalinclude} include/code/new_scripts/my_first_workchain_6_calcjob.py
:language: python
:lines: 54
```

##### Run the work chain

Now, it is time to run our work chain.
In order that the AiiDA daemon knows where to find the work chain, we need to add its directory to the `PYTHONPATH`.
Navigate until that directory in the terminal and execute (adjusting the path for your python environment):

```{code-block} console
$ echo "export PYTHONPATH=\$PYTHONPATH:$PWD" >> /home/max/.virtualenvs/aiida/bin/activate
$ verdi daemon restart --reset
```

Check if you have setup the `add` code:

```{code-block} console
$ verdi code list
# List of configured codes:
# (use 'verdi code show CODEID' to see the details)
* pk 1912 - add@localhost

```

Setup the computer and code if needed:

```{code-block} console
$ verdi computer setup --config computer.yml
$ verdi computer configure local localhost
$ verdi code setup --config code_add.yml
```

In the `verdi shell`, run:
```{code-block} console
In [1]: from aiida.engine import submit
In [2]: from multiply_add_workchain_calcjob import MultiplyAddWorkChain
In [3]: add_code = load_code(label='add@localhost')
In [4]: inputs = {'x': Int(1), 'y': Int(2), 'z': Int(3), 'code': add_code}
In [5]: workchain_node = submit(MultiplyAddWorkChain, **inputs)
```

Now, go and check the last processes, the status of the `MultiplyAddWorkChain`, and show some details about the inputs and outputs.


#### Checks and validation


* the **exit codes** of the work chain, specified using the `spec.exit_code()` method.
  Exit codes are used to clearly communicate known failure modes of the work chain to the user.
  The first and second arguments define the `exit_status` of the work chain in case of failure (`400`) and the string that the developer can use to reference the exit code (`ERROR_NEGATIVE_NUMBER`).
  A descriptive exit message can be provided using the `message` keyword argument.
  For the `MultiplyAddWorkChain`, we demand that the final result is not a negative number, which is checked in the `validate_result` step of the outline.

```{literalinclude} include/code/multiply_add.py
:language: python
:pyobject: MultiplyAddWorkChain.validate_result
:dedent: 4

```

Once the `ArithmeticAddCalculation` calculation job is finished, the next step in the work chain is to validate the result, i.e. verify that the result is not a negative number.
After the `addition` node has been extracted from the context, we take the `sum` node from the `ArithmeticAddCalculation` outputs and store it in the `result` variable.
In case the value of this `Int` node is negative, the `ERROR_NEGATIVE_NUMBER` exit code - defined in the `define()` method - is returned.
Note that once an exit code is returned during any step in the outline, the work chain will be terminated and no further steps will be executed.

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

## Equation of state

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

### Running the equation of state workflow

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

(workflows-writing-basics-eos-workchain)=

### Submitting the workflow: Workchains

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
  For instance, in the example of {ref}`this subsection<workflows-writing-basics-eos-workchain>`, you stored the completed calculations in the `calculations` dictionary, that was a local variable.

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

You can look at the `define` method of the `MultiplyAddWorkChain` {ref}`as an example <workflows-writing-basics-define>`.
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

:::{rubric} Footnotes

:::

[^f1]: In simple words, a decorator is a function that modifies the behavior of another function. In python, a function can be decorated by adding a line of the form `@decorating_function_name` on the line just before the `def` line of the decorated function. If you want to know more, there are many online resources explaining python decorators.
