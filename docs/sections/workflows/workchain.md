(workflows-workchain)=

# Work chains

The main disadvantage of work functions is that they cannot be interrupted during their execution.
If at any point during runtime the Python process is killed, the workflow is not able to terminate correctly.
This is not a significant issue when running simple scripts, but when you start running workflows with steps that take longer to complete, this can become a real problem.

In order to overcome this limitation, AiiDA allows you to insert checkpoints, where the main code defining a workflow can be interrupted and you can even shut down the machine on which AiiDA is running.
We call these workflows with checkpoints _work chains_ because, as you will see, they basically amount to splitting a work function into a chain of steps.

In this module, you will learn step-by-step how to write work chains in AiiDA.

:::{note}

To focus on the AiiDA concepts, the examples in this module are purposefully kept very simple.
In a later module on writing workflows, you will see a real-world example of a work chain that calculates the equation of state of a material.

:::

## Constructing our first work chain

We will start with a very simple work chain which we then modify step by step to introduce new features.
A very basic example to start with is a work chain that receives a single input and passes it as the output.
To get started, create a Python file for the work chain (e.g. `my_first_workchain.py`), and add the following piece of code:

```{literalinclude} include/code/new_scripts/my_first_workchain_1_output_input.py
:language: python
:lines: 1-15
```

Writing a work chain in AiiDA requires creating a class that inherits from the {class}`~aiida.engine.processes.workchains.workchain.WorkChain` class, as shown in the code snippet above.
You can give the work chain any valid Python class name, but the convention is to have it end in {class}`~aiida.engine.processes.workchains.workchain.WorkChain` so that it is always immediately clear what it references.
For this basic example, we chose `OutputInputWorkChain`, since it simply passes the input `Int` node as an output.
We will now explain the basic components of this toy example in detail.

(workflows-workchain-define)=

### Define method

:::{margin} {{ python }} **Class methods**
A class method can be called from the class itself, as well as all instances of that class.
You can find more information and a basic example [here](https://pythonbasics.org/classmethod/).
:::

The most important method to implement for every work chain is the `define()` _class method_:

```{literalinclude} include/code/new_scripts/my_first_workchain_1_output_input.py
:language: python
:lines: 8-11
:dedent: 4
```

:::{margin} {{ python }} **The `super()` function**
In simple terms, the `super()` function returns a temporary instance of the parent class (in this case {class}`~aiida.engine.processes.workchains.workchain.WorkChain`) that allows you to call its methods.
If you're curious, an in-depth explanation of `super()` can be found [here](https://realpython.com/python-super/).
:::

This _class method_ must always start by calling the `define()` method of its parent class using the `super()` function.
The `define()` method is used to define the _specifications_ of the work chain, which are contained in the work chain `spec`.
In the `define()` method, we can see three aspects of the work chain are specified:

* The **inputs** are specified using the `spec.input()` method:

  ```{literalinclude} include/code/new_scripts/my_first_workchain_1_output_input.py
  :language: python
  :lines: 13
  :dedent: 8
  ```

  The first argument of the `input()` method is a string that specifies the label of the input, in this case `'x'`.
  The `valid_type` keyword argument allows you to specify the required node type of the input.
  For the `'x'` input of this work chain, only `Int` nodes are accepted. <br/><br/>

* The **outline** is specified using the `spec.outline()` method:

  ```{literalinclude} include/code/new_scripts/my_first_workchain_1_output_input.py
  :language: python
  :lines: 14
  :dedent: 8
  ```

  The outline of the workflow is constructed from the methods of the work chain class.
  For the `OutputInputWorkChain`, the outline is a single step: `result`.
  Later in this module we'll be adding more steps to the outline. <br/><br/>

* The **outputs** are specified using the `spec.output()` method:

  ```{literalinclude} include/code/new_scripts/my_first_workchain_1_output_input.py
  :language: python
  :lines: 15
  :dedent: 8
  ```

  This method is very similar in its usage to the `input()` method, and just like the inputs you can have several outputs.
  For now, you can see that our work chain will output a single `Int` node with the label `'workchain_result'`.

:::{margin} {{ aiida }} **Further reading**
For more information on the `define()` method and the process spec, see the {ref}`corresponding section in the topics <topics:processes:usage:defining>`.
:::

:::{note}
All inputs and outputs of a work chain must be [AiiDA data types](https://aiida.readthedocs.io/projects/aiida-core/en/latest/topics/data_types.html) so they can be stored as a `Node` in the AiiDA database.
:::

### Adding the steps in the outline

Now that we've seen how to define the `spec` of the work chain using the `define()` method, let's instruct the work chain on what to actually do for the `result` _step_ in the `outline`.
This is done by adding each step as a method to the work chain class.
Let's do this for our single `result` step:

:::{margin}
{{ download }} **{download}`Download the script! <include/code/new_scripts/my_first_workchain_1_output_input.py>`**
:::

```{literalinclude} include/code/new_scripts/my_first_workchain_1_output_input.py
:language: python
:emphasize-lines: 17-21
```

As you can see, we defined `result()` as a method of the `OutputInputWorkChain` class.
In this step, we are simply passing the input, stored in `self.inputs.x`, to the output labeled `workchain_result`:

```{literalinclude} include/code/new_scripts/my_first_workchain_1_output_input.py
:language: python
:lines: 21
:dedent: 8
```

Two things are happening in this line:

* The `x` input is obtained from the inputs using `self.inputs.x`, i.e. as an _attribute_ from `self.inputs`.
* Using the `out()` method, this input is attached as an output of the work chain with link label `workchain_result`.
  As the `x` work chain input is already an `Int` node, the `valid_type` condition is immediately satisfied.

Add the `result` method to the `OutputInputWorkChain` class in your `my_first_workchain.py` file.
Now you should be ready to run your first work chain!

### Run the work chain

In the terminal, navigate to the folder where you saved the `my_first_workchain.py` file with the `OutputInputWorkChain` work chain and open a `verdi shell`.
Then run the work chain as you have seen in the **TODO ADD LINK**:

```{code-block} ipython
In [1]: from aiida.engine import run
In [2]: from my_first_workchain import OutputInputWorkChain
In [3]: result = run(OutputInputWorkChain, x=Int(4) )
```

This should complete almost instantaneously, we're just passing an input after all!
Let's see what's stored in the `result` variable:

```{code-block} ipython
In [4]: result
Out[4]:
{'workchain_result': <Int: uuid: ed5106ef-8eff-4e87-b2e9-ce6770a6b9a3 (pk: 4665) value: 4>}
```

You can see that the `run()` method has returned a dictionary whose _key_ corresponds to the output link label (`'workchain_result'`) and whose _value_ is the `Int` node that has been passed as an output in the work chain.

Exit the `verdi shell` and check the list of processes with `verdi process list`, using `-a/--all` to also see all _terminated_ processes and `-p/--past-days 1` to only see processes _created_ in the past day:
```{code-block} console
$ verdi process list -a -p 1
...
1982  2m ago     OutputInputWorkChain  ⏹ Finished [0]
```

Grab the PK of the `OutputInputWorkChain` and show some details about the inputs and outputs using `verdi process show`:

```{code-block} console
$ verdi process show <PK>
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

### Exercises

(1) Generate the provenance graph of the `OutputInputWorkChain`.
Is it what you would expect?

(2) Try to pass an integer for the `x` input when running the `OutputInputWorkChain`, instead of an `Int` _node_.
What happens?

:::{dropdown} **Solution**

Running the following in the `verdi shell`:

```{code-block} ipython
In [1]: from aiida.engine import run
In [2]: from my_first_workchain import OutputInputWorkChain
In [3]: result = run(OutputInputWorkChain, x=4 )
```

Will result in a rather large error message.
Don't read the entire thing!
The important part is at the bottom:

```{code-block} ipython
ValueError: Error occurred validating port 'inputs.x': value 'x' is not of the right type.
Got '<class 'int'>', expected '<class 'aiida.orm.nodes.data.int.Int'>'
```

We can see that an error is raised that indicates that the Python integer (`<class 'int'>`) is not of the right type (`<class 'aiida.orm.nodes.data.int.Int'>`).

:::

## How **not** to create data

Our next goal is to try and write a work chain that receives two inputs, adds them together, and outputs the sum.
In a first attempt do this, open the `my_first_workchain.py` file and make the following changes (highlighted):

```{literalinclude} include/code/new_scripts/my_first_workchain_2_wrong_add.py
:language: python
:emphasize-lines: 5,14,21,23
```

As you can see, the first change is to update the name of the work chain to `AddWorkChain` to better represent its new functionality.
Next, we declared a new input in the `define()` method:

```{literalinclude} include/code/new_scripts/my_first_workchain_2_wrong_add.py
:language: python
:lines: 14
```

The `y` input is simply a second `Int` node that we will add to `x`.
This is now done in the `result()` method, where we added the two inputs and attached the sum (`summation`) as the new output of the work chain:

```{literalinclude} include/code/new_scripts/my_first_workchain_2_wrong_add.py
:language: python
:lines: 21-23
```

Note that the summation of two `Int` nodes results in a new (and _unstored_) `Int` node (try it in the `verdi shell`!).

### Run the work chain

Let's see what happens when we try to run the work chain as we have done before for the `OutputInputWorkChain`.
Navigate to the folder where you have the work chain Python file (`my_first_workchain.py`) and open a `verdi shell` session to execute:

```{code-block} ipython
In [1]: from aiida.engine import run
In [2]: from my_first_workchain import AddWorkChain
In [3]: result = run(AddWorkChain, x=Int(4), y=Int(3))
```

Unfortunately, the command fails!
The `ValueError` at the end of the stack trace explains what went wrong:

```{code-block} python
...
----> 3 result = run(AddWorkChain, x=Int(4), y=Int(3) )
...
ValueError: Workflow<AddWorkChain> tried returning an unstored `Data` node.
This likely means new `Data` is being created inside the workflow.
In order to preserve data provenance, use a `calcfunction` to create this node and return its output from the workflow
```

:::{margin} {{ aiida }} **Further reading**
For more information on the difference between _data_ and _logical_ provenance, see the {ref}`corresponding section in the topics <topics:provenance:concepts>`.
:::

As the error message explains, the work chain is trying to create new `Data`.
However, in order to preserve the _data_ provenance, data can only be created by `calculation functions` or `calculation jobs`.
So, to correctly create the new data inside the work chain, we'll have to add a calculation function to our script.

(workflows-workchain-creating-data)=

## Creating data with calculation function

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

### Run the work chain

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

### Exercises

Got back and check the status of the process that corresponds to the work chain `OutputInputWorkChain`:
```{code-block} console
$ verdi process process status 1982
OutputInputWorkChain<1982> Finished [0] [None]
```

## Context

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

(workflows-workchain-adding-complexity)=

## Adding more complexity

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

Now, run your work chain and examine the results to see if they are equivalent to that of the section {ref}`Creating data with calculation function<workflows-workchain-creating-data>`.

## Work chain with Calculation Jobs

Until now, we have written work chains that create data via `calculation function` processes.
These processes are executed by the same machine process that is executing the work chain.
The full potential of a work chain is only accessed when it creates independent processes to execute the varios steps of the outline, such as running an external code.
This is achieved through an AiiDA process called `calculation job` ({class}`~aiida.engine.processes.calcjobs.calcjob.CalcJob`).
The execusion of the calculation jobs are managed and controlled by the AiiDA **daemons**.

Here, we demonstrate how to include calculation jobs in our work chain.
We are going to use the example in Section {ref}`Two calculation functions and more outputs<workflows-workchain-adding-complexity>` and replace the `addition` calculation function.
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

### Run the work chain

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

:::{rubric} Footnotes

:::

[^f1]: In simple words, a decorator is a function that modifies the behavior of another function. In python, a function can be decorated by adding a line of the form `@decorating_function_name` on the line just before the `def` line of the decorated function. If you want to know more, there are many online resources explaining python decorators.