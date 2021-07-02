 (workflows-workfunction)=
 # Work functions

A *work function* is the simplest of the two types of workflows in AiiDA.
It can call one or more calculation functions and *return* data that has been *created* by the calculation functions it has called.
Moreover, work functions can also call other work functions, allowing you to write nested workflows.

In this section, you will learn to:

1. Understand how to add simple python functions to the provenance.
2. Learn how to write and launch a simple workflow in AiiDA.

## Writing

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
