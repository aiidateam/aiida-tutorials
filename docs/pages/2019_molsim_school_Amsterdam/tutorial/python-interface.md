# The AiiDA python interface

AiiDA is written in python, and while the `verdi` command line interface
provides handy shortcuts for everyday operations, AiiDA provides its
full power only via the python interface.

## Using the python interface

There are three practical ways of using the python interface:

 1. python scripts that `import` the `aiida` python package
 2. the interactive `verdi shell`
 3. `Jupyter` notebooks

For this tutorial we recommend using the `verdi shell` (explained below)
but if you're already familiar with `Jupyter` notebooks you may use those as well.
We will get back to option 1 (python scripts) towards the end of the tutorial.

### The verdi shell

The `verdi shell` is a customized ipython shell, where all the AiiDA classes,
methods and functions are already accessible. Type in the terminal

```console
$ verdi shell
```

The `verdi shell` is handy for everyday AiiDA-based operations, e.g. creating,
querying and using AiiDA objects.
You would typically use two terminals, one for the
`verdi shell` and one to execute bash commands.

> **Note**
> Press `Ctrl+Shift+T` in order to open a new terminal tab.
> Don't forget to `workon aiida` in the new tab before using the shell.

### Jupyter notebooks

Start a jupyter notebook server:

```console
$ jupyter notebook
```

In the new browser window, select `New -> Python 2` (top right corner).
You are now inside a jupyter notebook, consisting of cells where you can type
portions of python code. The code will not be executed until you press
`Shift+Enter` from within a cell.

In order to load the same environment as in the `verdi shell`, type `%aiida`
in the first cell and execute it.

> **Note**
> The `verdi shell` and the `jupyter notebook` are completely equivalent.
> Use either according to your personal preference.

You will still need sometimes to type command-line instructions in
the terminal.
Either keep a terminal open on the side or use execute terminal commands
directly from the `verdi shell` or `jupyter notebook` by prefixing the
command by an exclamation mark:

```python
!verdi profile list
```

## Loading a node

Most AiiDA objects are represented by nodes, identified in the database
by their PK number (an integer). You can access a node using the following
command in the shell:

```python
node = load_node(<PK>)
```

> **Note**
> In the following, we'll use a dark gray border to indicate python code
> and a light gray border to indicate the terminal.

Load one of the calculation nodes you played around with before.
Then get the density computed with the command

```python
node.out.output_parameters.get_dict()
```

You can also type

```python
node.res.
```

and then press `TAB` to directly access the keys of the output dictionary.
