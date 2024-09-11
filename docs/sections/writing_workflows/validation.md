(workflows-validation)=

# Input validation

When running calculation jobs or work chains, it's often easy to make mistakes when setting up the inputs.
This is especially true for more complex work chains which often have a hierarchy of multiple levels (e.g. the `PwBandsWorkChain` for Quantum ESPRESSO).
If the user has provided incorrect inputs and runs the process, it will most likely fail (or potentially worse: silently provide an incorrect result).
Better would be to catch these issues before the process is actually run or submitted to the daemon by _validating_ the inputs.

In this section we will learn about how AiiDA allows you to validate process inputs.

## Type validation

You might have already noticed that AiiDA is able to validate the node _type_ of an input.
If you pass anything but a `StructureData` to the `structure` input of the `PwCalculation`, for example:

:::{code-block} ipython
In [1]: code = load_code('pw@localhost')

In [2]: builder = code.get_builder()

In [3]: builder.structure = Int(10)
:::

This will raise an error that the input for `structure` is not of the right type:

:::{code-block} ipython
...
ValueError: invalid attribute value value 'structure' is not of the right type.
Got '<class 'aiida.orm.nodes.data.int.Int'>', expected
'<class 'aiida.orm.nodes.data.structure.StructureData'>'
:::

The reason is that when the `structure` input is defined for the `PwCalculation` spec, its `valid_type` is set to `StructureData`.
This has already been explained at the start of the {ref}`work chain section<workflows-workchain-define>`, where the `OutputInputWorkChain` specifies that the `valid_type` of the `x` input is an `Int` node:

```{literalinclude} include/code/workchain/my_first_workchain_1_output_input.py
:language: python
:emphasize-lines: 13
```

Indeed, trying to pass anything but an `Int` node to the `x` input will fail with same error as above:

```{code-block} ipython
In [1]: from outputinput import OutputInputWorkChain

In [2]: builder = OutputInputWorkChain.get_builder()

In [3]: builder.x = Float(1)
...
ValueError: invalid attribute value value 'x' is not of the right type. Got '<class 'aiida.orm.nodes.data.float.Float'>', expected '<class 'aiida.orm.nodes.data.int.Int'>'
```

But what if you want the work chain to accept _both_ `Int` and `Float` nodes?
In this case, you can simply pass a tuple with all node types that are valid to the `valid_type` argument:

```{literalinclude} include/code/validation/float_int_output_input.py
:language: python
:emphasize-lines: 13
```

Give it a try!
Now the `OutputInputWorkChain` will accept both node types without issue.

## Value validation

### Single inputs

What if we want to also make sure that the _value_ of a certain input is correct?
Imagine the input represents the maximum number of iterations you want to do in a calculation, and hence must be a positive value.
In this case, AiiDA allows you to specify a _validator_ for an input.
For example, we can add a `validator` to the `x` input of the `OutputInputWorkChain`:

```{literalinclude} include/code/validation/validated_output_input.py
:language: python
:emphasize-lines: 4-7, 18
```


:::{margin}

{{ aiida }} **Ports and Port namespaces**

You can read about the ports and port namespace concepts in the [AiiDA documentation](https://aiida.readthedocs.io/projects/aiida-core/en/latest/topics/processes/usage.html?highlight=port#ports-and-port-namespaces).

:::

:::{margin}

{{ python }} **The underscore `_` character**

The underscore character has quite a lot interesting use cases in Python!
You can find out more about them [here](https://realpython.com/python-double-underscore/).

:::

:::{note}

You may be wondering about the `_` input argument in the validator function:

```{code-block}
def validate_x(node, _):
```

The reasons for this are rather technical, but in short every validator function _must_ have a signature with two input arguments: the node and the port or port namespace of the input.
For port namespaces where a certain port has been removed when exposing the inputs in a work chain that wraps the process, the validation of this port can then be skipped.

However, for the simple validation we are doing here, the port input is not needed, and we can simply add an underscore `_` so the signature of the validator still has two inputs but the second is ignored.

:::

After adding the validator, passing a positive valued `Int` still works fine:

:::{code-block} ipython
In [1]: from outputinput import OutputInputWorkChain

In [2]: builder = OutputInputWorkChain.get_builder()

In [3]: builder.x = Int(1)
:::

But a negative `Int` will not pass the validation:

:::{code-block} ipython
In [4]: builder.x = Int(-1)
...
ValueError: invalid attribute value the `x` input must be a positive integer.
:::

It's as simple as that!
Write a function that validates the input and pass this to the `validator` keyword argument when defining the input on the `spec`.

### Top-level validation

In some cases, validation of one input may depend on the value of another input.
Imagine that for the `AddWorkChain` in the {ref}`writing work chains<workflows-workchain-creating-data>` section we want to make sure that the `x` and `y` inputs have the same sign.
In this case we cannot simply add a validator to one of the inputs, since we won't have access to the value of the other input inside the validator function.
However, we can also add validation to the top-level namespace of a process:

```{literalinclude} include/code/validation/validated_add_workchain.py
:language: python
:emphasize-lines: 9-12, 24
```

Note that the first input argument of the top-level validator method (called `inputs` here), is simply a dictionary that maps the input labels to the corresponding nodes.

## Exercise

Take the `MultiplyAddWorkChain` from the {ref}`exercise in the work chains section<workflows-workchain-adding-complexity>` and adapt/add some validation:

* Allow the `x` and `y` inputs to _also_ be `Float` nodes.
* Make sure `z` is not zero.
* Make sure the sum of `x` and `y` is not zero.

:::{dropdown} **Solution**

```{literalinclude} include/code/validation/validated_multiple_add.py
:language: python
:emphasize-lines: 14-17, 19-22, 32-35, 38-39
```

Note how the `valid_type` of the _outputs_ also has to be more flexible!

:::
