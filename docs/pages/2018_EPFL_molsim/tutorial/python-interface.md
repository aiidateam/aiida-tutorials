The AiiDA python interface[shell]
=================================

In this section we will use an interactive python environment with all
the basic AiiDA classes already loaded. There are two variants of this:

The first is a customized ipython shell where all the AiiDA classes,
methods and functions are accessible. Type in the terminal

```bash
verdi shell
```

For everyday AiiDA-based operations, i.e. creating, querying and using
AiiDA objects, the <span>`verdi shell`</span> is probably the best tool.
You would usually use two terminals, one for the
<span>`verdi shell`</span> and one to execute bash commands.

The second option is based on `jupyter` notebooks and is great for
tutorial purposes. Double click on the `Jupyter Apps` icon on the
Desktop to start a jupyter notebook server. After a few seconds, the
browser will open and display the home app. Click on `File Browser` and
select `New -> Python 2` (top right corner). You are now inside a
jupyter notebook, made of cells where you can type portions of python
code. The code will not be executed until you press `Shift+Enter` from
within a cell. Type in the first cell

and execute it. This will set exactly the same environment as the
<span>`verdi shell`</span>. The notebook will be automatically saved
upon any modification and when you think you are done, you can export
your notebook in many formats by going to `File -> Download as`. We
suggest you to have a look to the drop-down menus `Insert` and `Cell`
where you will find the main commands to manage the cells of your
notebook. **The <span>`verdi shell`</span> and the
<span>`jupyter`</span> notebook are completely equivalent. Use either
according to your personal convenience.**

Note: you will still need sometimes to type command-line instructions in
<span>`bash`</span> in the first terminal you opened today. To
differentiate these from the commands to be typed in the
<span>`verdi shell`</span>, the latter will be marked in this document
by a vertical line on the left, like:

```python
some verdi shell command
```

while command-line instructions in <span>`bash`</span> to be typed on a
terminal will be encapsulated between horizontal lines:

```bash
some bash command
```

Alternatively, to avoid changing terminal, you can execute
<span>`bash`</span> commands within the <span>`verdi shell`</span> or
the notebook adding an exclamation mark before the command itself

```python
!some bash command
```

Loading a node[load~n~ode]
--------------------------

Most AiiDA objects are represented by nodes, identified in the database
by its pk number (an integer). You can access a node using the following
command in the shell:

```python
node = load_node(<PK>)
```

Load a node using one of the calculation pks visible in the graph you
displayed in the previous section of the tutorial. Then get the energy
of the calculation with the command

```python
node.out.output_parameters.get_dict()
```

You can also type

```python
node.out.
```

and then press <span>`TAB`</span> to see all the possible output results
of the calculation.
