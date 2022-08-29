(workflows-workchain)=

# Work chains

The main disadvantage of work functions is that they cannot be interrupted during their execution.
If at any point during runtime the Python process is killed, the workflow is not able to terminate correctly.
This is not a significant issue when running simple scripts, but when you start running workflows with steps that take longer to complete, this can become a real problem.

In order to overcome this limitation, AiiDA allows you to insert checkpoints, where the main code defining a workflow can be interrupted and you can even shut down the machine on which AiiDA is running.
We call these workflows with checkpoints _work chains_ because, as you will see, they basically amount to splitting a work function into a chain of steps.

In this module, you will learn step-by-step how to write work chains in AiiDA.

:::{note}

To focus on the AiiDA concepts, the examples in this module are toy work chains that are purposefully kept very simple.
In a later module on writing workflows, you will see a real-world example of a work chain that calculates the equation of state of a material.

:::

## Constructing our first work chain

We will start with a very simple work chain which we then modify step by step to introduce new features.
A very basic example to start with is a work chain that receives a single input and passes it as the output.
To get started, create a Python file for the work chain (e.g. `my_first_workchain.py`), and add the following piece of code:

```{literalinclude} include/code/workchain/my_first_workchain_1_output_input.py
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

```{literalinclude} include/code/workchain/my_first_workchain_1_output_input.py
:language: python
:lines: 8-11
```

:::{margin} {{ python }} **The `super()` function**
In simple terms, the `super()` function returns a temporary instance of the parent class (in this case {class}`~aiida.engine.processes.workchains.workchain.WorkChain`) that allows you to call its methods.
If you're curious, an in-depth explanation of `super()` can be found [here](https://realpython.com/python-super/).
:::

This _class method_ must always start by calling the `define()` method of its parent class using the `super()` function.
The `define()` method is used to define the _specifications_ of the work chain, which are contained in the work chain `spec`.
In the `define()` method, we can see three aspects of the work chain are specified:

* The **inputs** are specified using the `spec.input()` method:

  ```{literalinclude} include/code/workchain/my_first_workchain_1_output_input.py
  :language: python
  :lines: 13
  ```

  The first argument of the `input()` method is a string that specifies the label of the input, in this case `'x'`.
  The `valid_type` keyword argument allows you to specify the required node type of the input.
  For the `'x'` input of this work chain, only `Int` nodes are accepted. <br/><br/>

* The **outline** is specified using the `spec.outline()` method:

  ```{literalinclude} include/code/workchain/my_first_workchain_1_output_input.py
  :language: python
  :lines: 14
  ```

  The outline of the workflow is constructed from the methods of the work chain class.
  For the `OutputInputWorkChain`, the outline is a single step: `result`.
  Later in this module we'll be adding more steps to the outline. <br/><br/>

* The **outputs** are specified using the `spec.output()` method:

  ```{literalinclude} include/code/workchain/my_first_workchain_1_output_input.py
  :language: python
  :lines: 15
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
{{ download }} **{download}`Download the script! <include/code/workchain/my_first_workchain_1_output_input.py>`**
:::

```{literalinclude} include/code/workchain/my_first_workchain_1_output_input.py
:language: python
:emphasize-lines: 17-21
```

As you can see, we defined `result()` as a method of the `OutputInputWorkChain` class.
In this step, we are simply passing the input, stored in `self.inputs.x`, to the output labeled `workchain_result`:

```{literalinclude} include/code/workchain/my_first_workchain_1_output_input.py
:language: python
:lines: 21
```

Two things are happening in this line:

* The `x` input is obtained from the inputs using `self.inputs.x`, i.e. as an _attribute_ from `self.inputs`.
* Using the `out()` method, this input is attached as an output of the work chain with link label `workchain_result`.
  As the `x` work chain input is already an `Int` node, the `valid_type` condition is immediately satisfied.

Add the `result` method to the `OutputInputWorkChain` class in your `my_first_workchain.py` file.
Now you should be ready to run your first work chain!

### Run the work chain

In the terminal, navigate to the folder where you saved the `my_first_workchain.py` file with the `OutputInputWorkChain` work chain and open a `verdi shell`.
Then run the work chain as you have seen in the {ref}`AiiDA basics section on running calculation jobs<started-basics-calcjobs-run>`:

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

:::{margin}
Don't forget to replace the `<PK>` with that of your work chain!
:::

```{code-block} console
$ verdi process show <PK>
```

This results in the following output:

```{code-block} console
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

Observe that the `PK` of the input is the same as the output.
That is because our first work chain did not create any data, but just passed the input as the output.

### Exercises

(1) Generate the provenance graph of the `OutputInputWorkChain`.
Is it what you would expect?

:::{margin}
Try to solve the exercises yourself before looking at the solution!
You'll learn much more that way. 🙃
:::

:::{dropdown} **Solution**

The provenance graph should look something like this:

```{figure} include/images/workchain/outputinputworkchain.png
:width: 400px

Provenance graph of the `OutputInputWorkChain`.

```

Notice how the _same_ `Int` node is both the input and output of the work chain, as expected.
Also note that labels of the _links_ (i.e. the arrows connecting the nodes) correspond to those we defined in the `spec` using the `spec.input()` and `spec.output()` methods.
:::

(2) Try to pass a plain Python integer for the `x` input when running the `OutputInputWorkChain`, instead of an `Int` _node_.
What happens?

:::{dropdown} **Solution**

Running the following in the `verdi shell`:

```{code-block} ipython
In [1]: from aiida.engine import run
In [2]: from my_first_workchain import OutputInputWorkChain
In [3]: result = run(OutputInputWorkChain, x=4)
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

```{literalinclude} include/code/workchain/my_first_workchain_2_wrong_add.py
:language: python
:emphasize-lines: 5,14,21,23
```

As you can see, the first change is to update the name of the work chain to `AddWorkChain` to better represent its new functionality.
Next, we declared a new input in the `define()` method:

```{literalinclude} include/code/workchain/my_first_workchain_2_wrong_add.py
:language: python
:lines: 14
```

The `y` input is simply a second `Int` node that we will add to `x`.
This is now done in the `result()` method, where we added the two inputs and attached the sum (`summation`) as the new output of the work chain:

```{literalinclude} include/code/workchain/my_first_workchain_2_wrong_add.py
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

<!-- ### Cleaning up

**TODO: Add example on how to kill/delete a process to clean up erroneous `AddWorkChain` run.** -->

(workflows-workchain-creating-data)=

## Creating data with calculation function

Let's fix the issue with our work chain by creating the new data using a _calculation function_.
To do this, define a calculation function that adds the two numbers together and call this function inside a work chain step.
You can see the highlighted changes below:

```{literalinclude} include/code/workchain/my_first_workchain_3_add_calcfunc.py
:language: python
:emphasize-lines: 2, 5-7, 27
```

:::{margin} {{ python }} **Decorators**
A decorator can be used to add functionality to an existing function.
You can read more about them [here](https://pythonbasics.org/decorators/).
:::

We first imported the `calcfunction` _decorator_ from the aiida engine.
Then, we defined the `addition()` function outside the work chain scope, then we decorated it with `@calcfunction`:

```{literalinclude} include/code/workchain/my_first_workchain_3_add_calcfunc.py
:language: python
:pyobject: addition
```
And finally, we added the two inputs using the `addition()` _calculation function_ that we defined above:

```{literalinclude} include/code/workchain/my_first_workchain_3_add_calcfunc.py
:language: python
:lines: 27
```

This will ensure that the `Int` node created by the addition is stored as a part of the data provenance.

### Run the work chain

Let's run the work chain that uses the `addition()` calculation function.
Once again make sure you are in the folder where you have the work chain Python script, open the `verdi shell` and execute:

```{code-block} ipython
In [1]: from aiida.engine import run
In [2]: from my_first_workchain import AddWorkChain
In [3]: result = run(AddWorkChain, x=Int(4), y=Int(3))
```

This time the run should have completed without issue!
Let's see what result was returned by the `run()` call:

```{code-block} ipython
In [4]: result
Out[4]: {'workchain_result': <Int: uuid: 21cf16e9-58dc-4566-bbd7-b170fcd628ee (pk: 1990) value: 7>}
```

Similar to the first work chain you ran, the result is a dictionary that contains the output label and output `Int` node as a key/value pair.
However, now the `Int` node is a _new_ node that was _created_ by the `addition()` calculation function.

Close the `verdi shell` session and look for the work chain you just ran:

```{code-block} console
$ verdi process list -a -p 1
...
1988  49s ago    AddWorkChain     ⏹ Finished [0]
1989  49s ago    addition         ⏹ Finished [0]
```

Next, check the _status_ of the process that corresponds to the `AddWorkChain`:

```{code-block} console
$ verdi process status <PK>
AddWorkChain<1988> Finished [0] [None]
    └── addition<1989> Finished [0]
```

Notice how there is a branch in the work chain tree, which shows that a process (the `addition()` _calculation function_) was called by the `AddWorkChain`.
Finally, you can obtain some details about the in- and outputs with:

```{code-block} console
$ verdi process show <PK>
```

```{code-block} console
:emphasize-lines: 14-15,19
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

(1) Go back and check the status of the process that corresponds to the work chain `OutputInputWorkChain`.
How is it different from the `AddWorkChain`?

:::{dropdown} **Solution**

The `OutputInputWorkChain` status is just a single line:

```{code-block} console
$ verdi process process status <PK>
OutputInputWorkChain<1982> Finished [0] [None]
```

Since in this case, no _call_ to a calculation function was made.
By contrast, the `AddWorkChain` _does_ call the `addition()` function, which automatically becomes a part of the hierarchical overview shown by `verdi process status`.

:::

(2) Generate the provenance graph of the `AddWorkChain`, and compare it to that of the `OutputInputWorkChain`.

:::{dropdown} **Solution**

The provenance graph should look something like this:

```{figure} include/images/workchain/addworkchain.png
:width: 400px

Provenance graph of the `AddWorkChain`.

```

Notice how there now is a new `Int` node, _created_ by the `addition()` calculation function (note the `CREATE` link), but _returned_ by the `AddWorkChain` (note the `RETURN` link).
You might be wondering why there are no `INPUT` links from the `Int` nodes to the calculation function.
This is because we targeted the work chain when using `verdi node graph generate`.
You can either target the `addition()` calculation function, or simply add the `-i, --process-in` option to show these links as well:

```{code-block} console
$ verdi node graph generate -i <PK>
```

The graph should look like the following:

```{figure} include/images/workchain/addworkchain_input_links.png
:width: 500px

Provenance graph of the `AddWorkChain` using `-i, --process-in`.

```

Take a bit of time to compare the information shown by `verdi process show` with the provenance graph.
Maybe also use the command to show more details for the `addition()` calculation function.

:::

(workflows-workchain-context)=

## Multiple work-chain steps - Context

So far, we have only had a single step in the outline of our work chain.
When writing work chains with multiple steps, you may need to pass data between them.
This can be achieved using the _context_.

Our new work chain will have the same goal as before, simply adding two inputs.
But this time, we will create two steps in the `outline()` call, one to actually add the inputs and thus creating new data, and another step just to pass the result as an output.
The code looks like this:

```{literalinclude} include/code/workchain/my_first_workchain_4_pass_context.py
:language: python
:emphasize-lines: 20, 23, 30, 36
```

We added an extra step called `add` in the `outline` to be executed before `result`:

```{literalinclude} include/code/workchain/my_first_workchain_4_pass_context.py
:language: python
:lines: 20
```

Which means we also have to define the `add()` method for the work chain class:

```{literalinclude} include/code/workchain/my_first_workchain_4_pass_context.py
:language: python
:pyobject: AddWorkChain.add
```

This method is essentially the same as the `result()` method from the previous version, but instead of passing the result of the addition (`summation`) directly as an output, we added it to the work chain **context** using `self.ctx`:

```{literalinclude} include/code/workchain/my_first_workchain_4_pass_context.py
:language: python
:lines: 30
```

By doing so, the information stored in the context can now be used by another step of the outline.
In our example, the `self.ctx.summation` is passed as the `workchain_result` output in the `result()` step:

```{literalinclude} include/code/workchain/my_first_workchain_4_pass_context.py
:language: python
:pyobject: AddWorkChain.result
```

(workflows-workchain-adding-complexity)=

## Exercise: Adding multiplication

Alright, now it's your turn!
Based on the concepts you've learned so far, add an extra multiplication step by doing the following:

* Rename the work chain to `MultiplyAddWorkChain`, since we'll be adding an extra multiplication step.
* Write a calculation function called `multiplication`, that takes two `Int` nodes and returns their product.
* Add a new `Int` input to the `MultiplyAddWorkChain` `spec`, labeled `'z'`.
* Add a new step to the _outline_ of the work chain called `multiply`, making sure it is the first step of the outline.
  When defining the method, use the `multiplication` calculation function to multiply the `x` and `y` inputs.
  Then pass the results to the `add` step using the context.
* In the `add()` method, sum the result of the multiplication with the third input `z` and pass the result to the context.
* In the `result()` method, output the result of the `add` step as the `'workchain_result'`.
  Also, attach the result of the multiplication as an output.
  Note that you need to declare another output for this in the `define` method.
  You can use `product` as the label for the output link, for example.

Try to adapt the `AddWorkChain` into the `MultiplyAddWorkChain` yourself, and run the final work chain to see if it works.
Once you managed to run the work chain, the `status` should have both the `multiply` and `add` calculation functions in the hierarchy:

```{code-block} console
$ verdi process status <PK>
MultiplyAddWorkChain<203> Finished [0] [2:result]
    ├── multiplication<204> Finished [0]
    └── addition<206> Finished [0]
```

You can then also generate the provenance graph and once again compare it with the details shown by `verdi process show`.

If you get stuck, we've added our solution to the exercise in the dropdown below.
As always, try to solve the exercise yourself before looking at the solution!

:::{dropdown} **Solution**

Here is the full code for the `MultiplyAddWorkChain`, with changes highlighted:

```{literalinclude} include/code/workchain/my_first_workchain_5_multiply_calcfunc.py
:language: python
:emphasize-lines: 10-12, 15, 25-26, 28, 30, 33, 36, 42, 52
```

We first defined a `calculation function` to receive and multiply two inputs using the `@calcfunction` decorator:

```{literalinclude} include/code/workchain/my_first_workchain_5_multiply_calcfunc.py
:language: python
:pyobject: multiplication
```

Next, we gave a more appropriate name to our work chain (`MultiplyAddWorkChain`), and declared one more input labelled `z` (now three in total), and another output labelled `product` (totalizing two outputs):

```{literalinclude} include/code/workchain/my_first_workchain_5_multiply_calcfunc.py
:language: python
:lines: 25
```
```{literalinclude} include/code/workchain/my_first_workchain_5_multiply_calcfunc.py
:language: python
:lines: 28
```

We also added the `multiply` step in the outline, which is executed before the `add` step:

```{literalinclude} include/code/workchain/my_first_workchain_5_multiply_calcfunc.py
:language: python
:lines: 26
```

and defined the method that corresponds to this new step:

```{literalinclude} include/code/workchain/my_first_workchain_5_multiply_calcfunc.py
:pyobject: MultiplyAddWorkChain.multiply
```

Here, the actual processing of data is performed by the `calculation function` that we defined in the beginning named `multiplication()`.
The output of `multiplication()` was passed to the context as `self.ctx.product`.
Then, in the second step of the outline, `add`, we used the result stored in the context and the third input of the work chain as inputs for the calculation function `addition()`:

```{literalinclude} include/code/workchain/my_first_workchain_5_multiply_calcfunc.py
:language: python
:lines: 42
```

whose result was also stored in the context:

```{literalinclude} include/code/workchain/my_first_workchain_5_multiply_calcfunc.py
:language: python
:lines: 45
```

Finally, in the method `result()`, we declared the two outputs, the product that resulted from the multiplication of the first two inputs, and the final result that consists of the product added of the third input:

```{literalinclude} include/code/workchain/my_first_workchain_5_multiply_calcfunc.py
:language: python
:lines: 51-52
```

That's it!
Running the work chain is similar as before, but now you must also provide an input for `z`:

```{code-block} ipython
In [1]: from aiida.engine import run
   ...: from my_first_workchain import MultiplyAddWorkChain
   ...: result = run(MultiplyAddWorkChain, x=Int(4), y=Int(3), z=Int(4))
```

and the `result` dictionary has _two_ outputs:

```{code-block} ipython
In [3]: result
Out[3]:
{'workchain_result': <Int: uuid: 8e0f6355-3c8a-4a4f-bea6-97132c9c6c89 (pk: 207) value: 16>,
 'product': <Int: uuid: bb7620f8-7b07-4518-ac78-dcca2e7014a3 (pk: 205) value: 12>}
```

:::

## Submitting calculation jobs

All work chains we have seen up to this point rely on calculation _functions_ to create data.
When running the work chain, these processes are executed by the same Python process that is executing the code in the work-chain methods.
All the functionality of the work chains above could have been implemented in a work _function_.
In fact, this would be much more simple, similar to the `add_multiply` work function shown in the {ref}`work function module <workflows-workfunction>`.

Of course, the power of a work chain lies in its ability to _submit_ other processes that can run independently while the work chain waits for them to complete.
Doing so also releases the daemon to do other tasks, which is vital when running many workflows in high-throughput.
These processes often don't run Python code - think for example of a remote code installed on a supercomputer.

Although a work chain can also submit other work chains, in this section we'll see how to submit a _calculation job_ ({class}`~aiida.engine.processes.calcjobs.calcjob.CalcJob`) inside a work chain. Starting from the `AddWorkChain` in the {ref}`section on work chain context <workflows-workchain-context>` the code below replaces the `addition` calculation function by the `ArithmeticAdd` calculation job, which ships with `aiida-core`:

:::{margin}
{{ download }} **{download}`Download the script! <include/code/workchain/addcalcjobworkchain.py>`**
:::

```{literalinclude} include/code/workchain/addcalcjobworkchain.py
:language: python
:emphasize-lines: 1-5, 17, 24-30, 32, 38
```

Let's have a closer look at each change in the code.
First, we imported the `ArithmeticAddCalculation` calculation job that we plan on using with the help of the `CalculationFactory`:

```{literalinclude} include/code/workchain/addcalcjobworkchain.py
:language: python
:lines: 3-5
```

However, it is possible to set up multiple codes in the AiiDA database that run the _same_ calculation job (a local and remote one, for example).
Hence, the user must also be able to specify _which code_ the work chain should run.
To allow this, we have added a `code` input to the work chain `spec`, which must be of type `Code`:

```{literalinclude} include/code/workchain/addcalcjobworkchain.py
:language: python
:lines: 18
```

In the `add()` method, we now _submit_ the `ArithmeticAddCalculation` calculation _job_ instead of _running_ the `addition()` calculation _function_:

```{literalinclude} include/code/workchain/addcalcjobworkchain.py
:language: python
:pyobject: AddCalcjobWorkChain.add
```

:::{important}
When submitting a calculation job or work chain inside a work chain, it is **essential** to use the submit method of the work chain via `self.submit()`.
:::

Since the result of the addition is only available once the calculation job is finished, the `submit()` method returns the {class}`~aiida.orm.nodes.process.calculation.calcjob.CalcJobNode` of the `ArithmeticAddCalculation` process.
To make sure the work chain waits for this process to finish before continuing, we return the `ToContext` container.
Here, we have specified that the calculation job node stored in `calc_job_node` should be assigned to the `'add_node'` context key.

Once the `ArithmeticAddCalculation` calculation job is finished, the work chain will execute the `result` step.
The outputs of the calculation job are stored in the `outputs` attribute of the calculation job node.
In case of the `ArithmeticAddCalculation`, the result of the addition is attached as an output using the `sum` link label, and hence can be accessed using `<calculation_job_node>.outputs.sum`.
Since we have added the calculation job node to the context under the `add_node` key, we obtain the sum using `self.ctx.add_node.outputs.sum`.
This result is then attached as the `workchain_result` output:

```{literalinclude} include/code/workchain/addcalcjobworkchain.py
:language: python
:lines: 39
```

And that's all!
Copy the _full_ code snippet for the work chain to a Python file, for example `addcalcjobworkchain.py`.
Now we're ready to launch our work chain.

(workflows-workchain-submit-workchain)=

### Submit the work chain

When _submitting_ work chains to the AiiDA daemon, it's important that it knows where to find the work chain module, i.e. the `.py` file that contains the work chain code.
To do this, we need to add the directory that contains this file to the `PYTHONPATH`.
Make sure you are in the directory that contains the `addcalcjobworkchain.py` file and execute:

```{code-block} console
$ echo "export PYTHONPATH=\$PYTHONPATH:$PWD" >> $HOME/.bashrc
$ source $HOME/.bashrc
$ verdi daemon restart --reset
```

Also double check that you have set up the `add` code used in the {ref}`AiiDA basics module <started-basics-calcjobs>`:

```{code-block} console
$ verdi code list
...
* pk 1912 - add@localhost
```

If not, you can set it up with the instructions in the dropdown below.

:::{dropdown} Set up the `add` code

Setting up the `add` code on the `localhost` computer can be done with the following command:

```{code-block} console
$ verdi code setup -L add --on-computer --computer=localhost -P core.arithmetic.add --remote-abs-path=/bin/bash -n
```

See the {ref}`calculation jobs section <started-basics-calcjobs>` in the AiiDA basics module for more details.

:::

Then open a `verdi shell` and import the `submit()` function and work chain:

```{code-block} ipython
In [1]: from aiida.engine import submit
   ...: from addcalcjobworkchain import AddCalcjobWorkChain
```

We'll also need the `add` code set up on the `localhost`.
Load it using its label:

```{code-block} ipython
In [2]: add_code = load_code(label='add@localhost')
```

Then we can submit the work chain:

```{code-block} ipython
In [3]: workchain_node = submit(AddCalcjobWorkChain, x=Int(1), y=Int(2), code=add_code)
```

Note that just like for the `self.submit()` method executed _inside_ the work chain, the bare `submit()` function also returns the process _node_:

```{code-block} ipython
In [4]: workchain_node
Out[4]: <WorkChainNode: uuid: 0936f2b4-01af-46bb-98f8-da828ce706eb (pk: 324) (addcalcjobworkchain.AddCalcjobWorkChain)>
```

In this case, it is the node of the `AddCalcjobWorkChain` we have just submitted.

### Exercises

(1) As before, generate the provenance graph of the `AddCalcjobWorkChain` and check the details of `verdi process show`.
Do you see any differences with the `AddWorkChain`?

(2) Try loading the `ArithmeticAddCalculation` node in the `verdi shell`, and browse its outputs via the `outputs` attribute and tab-completion.
Basically, after loading the node in e.g. `add_node`, type `add_node.outputs.` and then press Tab.
Do you find the `sum` output?

(3) To practice the concepts of this final section, adapt the `MultiplyAddWorkChain` so it uses the `ArithmeticAddCalculation` calculation _job_ instead of the `addition()` calculation process.
