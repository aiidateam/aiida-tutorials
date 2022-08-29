 (workflows-workfunction)=
 # Work functions

A *work function* is the simplest of the two types of workflows in AiiDA.
It can call one or more calculations and *return* data that has been *created* by the calculation it has called.
Moreover, work functions can also call other workflows, allowing you to write nested workflows.

In this section, you will learn to:

1. Understand how to add simple Python functions to the provenance.
2. Learn how to write and launch a simple workflow in AiiDA.

 (workflows-workfunction-calcfunction)=

## Calculation functions

:::{margin} {{ python }} **Decorators**

A decorator can be used to add functionality to an existing function.
You can read more about them [here](https://pythonbasics.org/decorators/).

:::

Calculation functions are a great way to keep track of steps that are part of your scientific workflow and written in Python to the provenance of AiiDA.
In order to do so, you have to add a `calcfunction` decorator to the Python function.
A simple example is the `multiply` calculation function from the {ref}`AiiDA basics section <started-basics-calcfunction>`:

```{code-block} python
from aiida.engine import calcfunction

@calcfunction
def multiply(x, y):
    return x * y
```

In a sense, this example is _deceptively_ simple.
Let's consider a slightly more complicated example: a `rescale` function that takes an ASE `Atoms` structure and rescales the unit cell with a certain `scale` factor:

```{code-block} python
def rescale(structure, scale):

    new_cell = structure.get_cell() * scale
    structure.set_cell(new_cell, scale_atoms=True)

    return structure
```

Open a `verdi shell` or Jupyter notebook (with the AiiDA magic: `%aiida`) and use the code snippet above to define the `rescale` function.
Next, load _any_ `StructureData`, for example using the `QueryBuilder`:

```{code-block} ipython
In [2]: from aiida.orm import StructureData
   ...: structure = QueryBuilder().append(StructureData).first()[0]
```

In order to test the method, we need to convert the `StructureData` into an ASE `Atoms` instance.
This can be easily done using the `get_ase()` method:

```{code-block} ipython
In [3]: ase_structure = structure.get_ase()
```

Let's have a look at what structure we found:

```{code-block} ipython
In [4]: ase_structure
Out[4]: Atoms(symbols='NaNbO3', pbc=True, cell=[3.9761497211, 3.9761497211, 3.9761497211], masses=...)
```

Next, use the `rescale` function to double the lattice vectors of the unit cell:

```{code-block} ipython
In [5]: rescale(ase_structure, 2)
Out[5]: Atoms(symbols='NaNbO3', pbc=True, cell=[7.9522994422, 7.9522994422, 7.9522994422], masses=...)
```

Great!
That all seems to be working as expected.
Now it's time to convert our Python function into a calculation function.

### Working with nodes

Try to adapt the `rescale` function above into a calculation function by adding a `calcfunction` decorator:

```{code-block} python
from aiida.engine import calcfunction

@calcfunction
def rescale(structure, scale):

    new_cell = structure.get_cell() * scale
    structure.set_cell(new_cell, scale_atoms=True)

    return structure
```

Maybe you already see why just adding the `calcfunction` decorator is not sufficient.
Trying to run the method again with the `ase_structure` and `2` scaling factor will fail, since neither are a `Data` node:

```{code-block} ipython
In [7]: rescale(ase_structure, 2)
(...)
ValueError: Error occurred validating port 'inputs.structure': value 'structure' is not of the right type.
Got '<class 'ase.atoms.Atoms'>', expected '(<class 'aiida.orm.nodes.data.data.Data'>,)'
```

However, passing the originally imported `StructureData` stored in `structure` and `Float(2)` won't work either:

```{code-block} ipython
In [8]: rescale(structure, Float(2))
(...)
AttributeError: 'StructureData' object has no attribute 'get_cell'
```

The reason for these failures is that we need to adjust the `rescale` function further, to make sure it can both accept AiiDA nodes as _inputs_, as well as _returns_ an AiiDA node:

```{literalinclude} include/code/realworld/rescale.py
:language: python
:emphasize-lines: 12, 14-15, 20
```

Let's explain the required changes in more detail:

```{literalinclude} include/code/realworld/rescale.py
:language: python
:lines: 12
```

Here the `StructureData` class is imported, since we need it later to convert the ASE `Atoms` structure into a `StructureData` node so we can output it.

```{literalinclude} include/code/realworld/rescale.py
:language: python
:lines: 14-15
```

These two lines simply convert the inputs, which _have_ to be AiiDA nodes, into the corresponding ASE `Atoms` structure and the Python `float` base type that we need to scale the unit cell.

```{literalinclude} include/code/realworld/rescale.py
:language: python
:lines: 20
```

After the `ase_structure` has been rescaled, we need to convert it back into a `StructureData` node that is then _returned_ by the `rescale` function as an output.

So, in reality we have to do two things in order to adapt a regular Python function into a calculation function that can be tracked in the provenance:

1. Add the `calcfunction` decorator.
2. Make sure the function expects and returns AiiDA {class}`~aiida.orm.nodes.data.data.Data` nodes.
  This often involves converting the input nodes into other Python objects, and converting the result of the analysis back into an AiiDA {class}`~aiida.orm.nodes.data.data.Data` node.

### Exercises

(1) Run the calculation function version of `rescale` with AiiDA nodes as inputs.
Convert the output `StructureData` node back into an ASE `Atoms` structure.
Is the result what you expected?

:::{dropdown} **Solution**

After redefining the `rescale` method with the code snippet above, running the calculation function with our originally imported `StructureData` node and a `Float` node works without a hitch:

```{code-block} ipython
In [10]: new_structure = rescale(structure, Float(2))
```

Converting this into an ASE `Atoms` object using the `get_ase()` method:

```{code-block} ipython
In [11]: new_structure.get_ase()
Out[11]: Atoms(symbols='NaNbO3', pbc=True, cell=[7.9522994422, 7.9522994422, 7.9522994422], masses=...)
```

we can see that the lattice cell vectors are twice as large as initially, which is the desired result.

:::

(2) Why was the `multiply` function so deceptively simple?
  That is, why was conversion to/from AiiDA nodes not an issue there?

:::{dropdown} **Solution**

In the case of the `multiply` function, the `x` and `y` inputs are simply multiplied using `*`.
Since `x` and `y` are AiiDA `Int` nodes, this results in a new `Int` node whose value is the product of the two nodes:

```{code-block} ipython
In [12]: Int(2) * Int(3)
Out[12]: <Int: uuid: cfff6b68-69a2-47e2-8feb-cbd039bb0588 (unstored) value: 6>
```

You can see that the result of multiplying two `Int` nodes is simply another `Int` node.
This can then be directly returned in the `multiply` method, avoiding the conversion issues we encountered for the `rescale` example.

:::

(3) Since calculation functions are tracked in the provenance, you should be able to find those you have just run using the `verdi process list` command.
If you've tried the _incorrect_ `rescale` calculation function above, this list will contain one `Excepted` result.
Use what you've learned in the {ref}`Troubleshooting module <calculations-errors>` to figure out what went wrong here.

:::{dropdown} **Solution**

Looking at _all_ processes that have completed _in the last day_:

```{code-block} console
$ verdi process list -a -p 1
  PK  Created    Process label    Process State    Process status
----  ---------  ---------------  ---------------  ----------------
(...)
2732  7m ago     rescale          ⨯ Excepted
2734  7m ago     rescale          ⏹ Finished [0]
```

Looking at the process report:

```{code-block} console
$ verdi process report <PK>
2021-07-06 23:20:04 [122]: [2732|rescale|on_except]: Traceback (most recent call last):
  File "/opt/conda/lib/python3.7/site-packages/plumpy/process_states.py", line 230, in execute
    result = self.run_fn(*self.args, **self.kwargs)
  File "/opt/conda/lib/python3.7/site-packages/aiida/engine/processes/functions.py", line 395, in run
    result = self._func(*args, **kwargs)
  File "/tmp/ipykernel_2974/3046260054.py", line 6, in rescale
    new_cell = structure.get_cell() * scale
AttributeError: 'StructureData' object has no attribute 'get_cell'
```

It's clear that this corresponds to the case where we attempted to pass a `StructureData`, but the function failed since the `get_cell()` method is defined for the `Atoms` class, not the `StructureData` one.

:::

## Writing a work function

Writing a work function whose provenance is automatically stored can be achieved by writing a Python function and decorating it with the {func}`~aiida.engine.processes.functions.workfunction` decorator:

:::{margin}

{{ download }} {download}`Download the Python file! <include/code/add_multiply.py>`

:::

```{literalinclude} include/code/add_multiply.py
:language: python
:start-after: start-marker
```

It is important to reiterate here that the {func}`~aiida.engine.processes.functions.workfunction`-decorated `add_multiply()` function does not *create* any new data nodes.
The `add()` and `multiply()` calculation functions create the `Int` data nodes, all the work function does is *return* the results of the `multiply()` calculation function.
Moreover, both calculation and work functions can only accept and return data nodes, i.e. instances of classes that subclass the {class}`~aiida.orm.nodes.data.data.Data` class.

Copy the code snippet above and put it into a Python file (e.g. `add_multiply.py`), or download it directly using the link next to it.
In the terminal, navigate to the folder where you stored the script.
Next, import the add_multiply work function in the `verdi shell`:

```{code-block} ipython

In [1]: from add_multiply import add_multiply

```


Similar to a calculation function, running a work function is as simple as calling a typical Python function: simply call it with the required input arguments:

```{code-block} ipython

In [2]: result = add_multiply(Int(2), Int(3), Int(5))

```

Here, the `add_multiply` work function returns the output `Int` node and we assign it to the variable `result`.
Again, note that the input arguments of a work function must be an instance of a {class}`~aiida.orm.nodes.data.data.Data` node, or any of its subclasses.
Just calling the `add_multiply` function with regular integers will result in a `ValueError`, as these cannot be stored in the provenance graph.

:::{margin} {{ aiida }} **Further reading**

Although the example above shows the most straightforward way to run the `add_and_multiply` work function, there are several other ways of running processes that can return more than just the result.
For example, the `run_get_node` function from the AiiDA engine returns both the result of the workflow and the work function node.
See the {ref}`corresponding topics section for more details <topics:processes:usage:launching>`.

:::

When we check the AiiDA list of _all_ processes that have terminated _in the past day_:

```{code-block} console
$ verdi process list -a -p 1
  PK  Created    Process label    Process State    Process status
----  ---------  ---------------  ---------------  ----------------
...
1859  1m ago     add_multiply     ⏹ Finished [0]
1860  1m ago     add              ⏹ Finished [0]
1862  1m ago     multiply         ⏹ Finished [0]
```

Copy the PK of the `add_multiply` work function and check its status with `verdi process status` (in the above example, the PK is `1859`):
```{code-block}
$ verdi process status <PK>
add_multiply<1859> Finished [0]
    ├── add<1860> Finished [0]
    └── multiply<1862> Finished [0]
```

Finally, you can also check the details of the inputs and outputs of the work function:

```{code-block} console
$ verdi process show <PK>
```

Notice that each input and output to the work function `add_multiply` is stored as a node, and that the work chain has `CALLED` both the `add` and `multiply` calculation functions:

```{code-block} console
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

### Exercise

Let's look at multiple ways to generate the provenance graph and what this can teach us.

(1) Generate the provenance graph of the `add_multiply` work function without any additional options.
Does anything seem missing here?

:::{dropdown} **Solution**

You should know the correct command by now:

```{code-block} console
$ verdi node graph generate <PK>
```

You might notice here that there are no links between the `Int` nodes and the calculation functions called by the work function.
These are not shown by default, but in the next exercise you'll use an option to do so.

```{figure} include/images/workfunction/add_multiply_default.png
:width: 400px

Default provenance graph for the `add_multiply` work function.

```

:::

(2) Try to generate the provenance graph again, but this time with the `-i, --process-in` option.
You can use `verdi node graph generate --help` for more information about the various options of this command.

:::{dropdown} **Solution**

By using the `-i, --process-in` option, you can see that the `INPUT_CALC` links missing from the previous provenance graph are now included:

```{code-block} console
$ verdi node graph generate -i <PK>
```

```{figure} include/images/workfunction/add_multiply_all.png
:width: 500px

Provenance graph for the `add_multiply` work function using the `-i, --process-in` option.

```

:::

(3) Finally, try to generate the _data_ provenance by:

1. Targetting the `multiply` calculation function instead of the `add_multiply` method.
2. Using the `-l, --link-types` option to select the `data` links only.

:::{dropdown} **Solution**

Use the `-l` option with `data` as an argument:

```{code-block} console
$ verdi node graph generate -l data <PK>
```

Note that `<PK>` here should be replaced by the PK of the `multiply` calculation function!
We now only see the _data_ provenance, i.e. the workflows are no longer in the provenance graph.

```{figure} include/images/workfunction/multiply_data_only.png
:width: 400px

Provenance graph for the `multiply` calculation function when only selecting the data provenance with the `-l, --link-types` option.

```

:::
