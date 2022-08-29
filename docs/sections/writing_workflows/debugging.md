(workflows-debugging)=

# Debugging work chains

In this section, we highlight a series of common issues you may encounter when writing work chains with AiiDA, and explain how to debug them.

:::{admonition} I can't import my work chain!

When trying to import a work chain in the IPython terminal, you get a `No module named ...` error message:

```{code-block} ipython
In [1]: from addcalcjobworkchain import AddCalcjobWorkChain
---------------------------------------------------------------------------
ModuleNotFoundError                       Traceback (most recent call last)
<ipython-input-1-03fcc3f6b521> in <module>
----> 1 from addcalcjobworkchain import AddCalcjobWorkChain

ModuleNotFoundError: No module named 'addcalcjobworkchain'
```

:::

:::{dropdown} **How to debug**

There are a couple of ways of making sure you can import your work chain.
A straightforward way is making sure that the Python `.py` file is in the current directory when you start the `verdi shell`.
Alternatively, you can add the directory that contains the work chain definition to the `PYTHONPATH` environment variable.
You can do this directly in the terminal using:

```{code-block} console
$ export PYTHONPATH=/path/to/workchain/directory/:$PYTHONPATH
```

Where `/path/to/workchain/directory/` must be replaced by the path to your workchain directory.
To make sure this persists when you open a new terminal, you can add the above line to the `.bashrc` file in your `$HOME` directory.

:::


:::{admonition} My work chain is stuck in the `Created` state!

You've submitted your work chain, but no matter how long you wait, the process stays in the `Created` state:

```{code-block} console
$ verdi process list
  PK  Created    Process label         Process State    Process status
----  ---------  --------------------  ---------------  ----------------
2745  7s ago     OutputInputWorkChain  ⏹ Created

Total results: 1

Info: last time an entry changed state: 7s ago (at 01:36:44 on 2021-07-07)
Warning: the daemon is not running
```

:::

:::{dropdown} **How to debug**

As the warning indicates, this most likely means that the process was created and it is ready to be run, but the daemon is not running.
In this case, your process will stay in that state indefinitely.
Check the daemon status with:

```{code-block} console
$ verdi daemon status
Profile: my_aiida_profile
The daemon is not running
```

If, as above, the daemon is not running, start it with:

```{code-block} console
$ verdi daemon start
Starting the daemon... RUNNING
```

:::

:::{admonition} The changes I made in my work chain have no effect!

You've just added an extra step, fixed a bug, updated an input, etc. in your work chain, but when you resubmit the work chain for testing, nothing seems to have changed.

:::

:::{dropdown} **How to debug**

When updating an existing work chain or adding a new one, it is necessary to restart the daemon every time after you've made changes.
This is to ensure that the daemon can load the new version of the code in memory.
You can use the following command to do so:

```{code-block} console
$ verdi daemon restart --reset
Profile: default
Waiting for the daemon to shut down... OK
Starting the daemon... RUNNING
```

```{figure} include/images/debugging/daemon_restart.jpeg
:width: 400px

Charlie knows best.

```

Note that this is _only_ necessary if you are submitting your work chain.
If you are running it in the IPython kernel, restarting the daemon is not necessary because it won't be executed by the daemon.
However, you may have to reopen the `verdi shell` session or restart the kernel of the Jupyter notebook you are running.

:::

:::{admonition} My work chain is `Finished`, but the exit code is not zero!

Your work chain has completed and is in a `Finished` state, but the exit code is different from zero:

```{code-block} console
$ verdi process list -a -p 1
  PK  Created    Process label                 Process State     Process status
----  ---------  ----------------------------  ----------------  ----------------
 575  8D ago     PwRelaxWorkChain              ⏹ Finished [401]
 578  8D ago     PwBaseWorkChain               ⏹ Finished [300]
 579  8D ago     create_kpoints_from_distance  ⏹ Finished [0]
 583  8D ago     PwCalculation                 ⏹ Finished [305]

Total results: 4

Info: last time an entry changed state: 2m ago (at 01:36:44 on 2021-07-07)
```

:::

:::{dropdown} **How to debug**

You can inspect the work-chain report with:

```{code-block} console
$ verdi process report <PK>
2021-06-28 08:52:01 [132 | REPORT]: [575|PwRelaxWorkChain|run_relax]: launching PwBaseWorkChain<578>
2021-06-28 08:52:02 [133 | REPORT]:   [578|PwBaseWorkChain|run_process]: launching PwCalculation<583> iteration #1
2021-06-28 08:54:16 [138 | REPORT]:   [578|PwBaseWorkChain|report_error_handled]: PwCalculation<583> failed with exit status 305: Both the stdout and XML output files could not be read or parsed.
2021-06-28 08:54:16 [139 | REPORT]:   [578|PwBaseWorkChain|report_error_handled]: Action taken: unrecoverable error, aborting...
2021-06-28 08:54:16 [140 | REPORT]:   [578|PwBaseWorkChain|inspect_process]: PwCalculation<583> failed but a handler detected an unrecoverable problem, aborting
2021-06-28 08:54:16 [141 | REPORT]:   [578|PwBaseWorkChain|on_terminated]: remote folders will not be cleaned
2021-06-28 08:54:17 [142 | REPORT]: [575|PwRelaxWorkChain|inspect_relax]: relax PwBaseWorkChain failed with exit status 300
2021-06-28 08:54:20 [143 | REPORT]: [575|PwRelaxWorkChain|on_terminated]: cleaned remote folders of calculations: 583
```

This will usually give you a good idea of what went wrong.
In the above work chain, it seems the `PwCalculation` could not read or parse _both_ the `stdout` and `.xml` files from `pw.x`:

```{code-block} bash
2021-06-28 08:54:16 [138 | REPORT]:   [578|PwBaseWorkChain|report_error_handled]: PwCalculation<583> failed with exit status 305: Both the stdout and XML output files could not be read or parsed.
```

This usually means the calculation didn't complete.
To understand what went wrong, you can use the `verdi calcjob outputcat` command to see the `stdout`:

```{code-block} console
$ verdi calcjob outputcat <PK> | less
```

Note that this is "piped" (`|`) to the `less` command, since this file can be quite large and hence flood the terminal.

```{code-block} bash
 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
     Error in routine check_para_diag (8):
     Too few bands for required ndiag
 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

     stopping ...
```

In this case, it seems our calculation did not have enough bands.

:::

:::{admonition} My work chain is in the `Excepted` state!

You submitted your work chain, but don't see it when executing `verdi process list`.
When you check for _all_ processes, you see it's in an `Excepted` state:

```{code-block} console
$ verdi process list -a -p 1
  PK  Created    Process label         Process State    Process status
----  ---------  --------------------  ---------------  ----------------
2745  2m ago     OutputInputWorkChain  ⨯ Excepted

Total results: 1

Info: last time an entry changed state: 2m ago (at 01:36:44 on 2021-07-07)
```

:::

:::{dropdown} **How to debug**

Exceptions when developing work chains are common, and there are several reasons why a work chain could be in an `Excepted` state.
To get more information on what is going wrong, you can use `verdi process report`:

```{code-block} console
$ verdi process report <PK>
(...)
  File "/opt/conda/lib/python3.7/site-packages/aiida/engine/persistence.py", line 50, in load_object
    raise ImportError(f"module '{module_name}' from identifier '{identifier}' could not be loaded")
ImportError: module 'my_first_workchain' from identifier 'my_first_workchain:OutputInputWorkChain' could not be loaded
```

In this case, it seems that the `OutputInputWorkChain` was submitted to the daemon, but it couldn't find the work chain.
The {ref}`section on submitting work chains <workflows-workchain-submit-workchain>` explains how to add the directory to the `PYTHONPATH` in a persistent manner, so the daemon can find it.

In case there is some issue in the code, the work chain will also end up in the `Excepted` state.
Using `verdi process report` will give you the final Traceback so you can understand where the issue lies.
:::

## Wrong data type for the input

Here, we demonstrate what happens if you input a wrong data type to a work chain in the running or submission process.
For that, we consider the `OutputInputWorkChain` written in the {ref}`Work chain section <workflows-workchain>`.

{{ download }} **{download}`You can download the script here. <include/code/debugging/my_first_workchain_1_output_input.py>`**

After downloading the work chain script to your computer where you are running AiiDA, navigate to the folder where you have saved the script and run in the `verdi shell`

```{code-block} ipython
In [1]: from aiida.engine import run
In [2]: from my_first_workchain_1_output_input import OutputInputWorkChain
In [3]: result = run(OutputInputWorkChain, x=4)
---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
<ipython-input-5-118afb74821c> in <module>
----> 1 result = run(OutputInputWorkChain, x=4)
...
ValueError: Error occurred validating port 'inputs.x': value 'x' is not of the right type. Got '<class 'int'>', expected '<class 'aiida.orm.nodes.data.int.Int'>'
```

In the third command line, we tried to run the `OutputInputWorkChain` passing a Python integer as the input.
However, the work chain is expecting an AiiDA integer data type, which can be created using the `Int()` class.
See the declaration of the input of the `OutputInputWorkChain`:

```{literalinclude} include/code/debugging/my_first_workchain_1_output_input.py
:language: python
:lines: 13
```

When writing a work chain, specifying which type of data is expected is the first step of creating robust work chains.

The problem can be corrected as in the following example:
```{code-block} ipython
In [1]: from aiida.engine import run
In [2]: from my_first_workchain_1_output_input import OutputInputWorkChain
In [3]: result = run(OutputInputWorkChain, x=Int(4))
```

## Passing wrong data type to the output

Modify the `OutputWorkChain` declaring the output label `workchain_result` as of the type `Float`:

```{literalinclude} include/code/debugging/my_first_workchain_2_wrong_output.py
:language: python
:emphasize-lines: 1,15
```

The script will then try to output an `Int` where a `Float` is expected instead.
Run the following in the `verdi shell` to see what error this will generate:

```{code-block} ipython
In [1]: from aiida.engine import run
In [2]: from my_first_workchain_1_output_input import OutputInputWorkChain
In [3]: result = run(OutputInputWorkChain, x=Int(4) )
07/05/2021 12:52:48 PM <25305> aiida.orm.nodes.process.workflow.workchain.WorkChainNode: [REPORT] [382|OutputInputWorkChain|on_except]: Traceback (most recent call last):
  File "/home/fdossantos/venv/aiida_git/lib/python3.8/site-packages/plumpy/process_states.py", line 229, in execute
    result = self.run_fn(*self.args, **self.kwargs)
  File "/home/fdossantos/venv/aiida_git/lib/python3.8/site-packages/aiida/engine/processes/workchains/workchain.py", line 194, in run
    return self._do_step()
  File "/home/fdossantos/venv/aiida_git/lib/python3.8/site-packages/aiida/engine/processes/workchains/workchain.py", line 211, in _do_step
    finished, stepper_result = self._stepper.step()
  File "/home/fdossantos/venv/aiida_git/lib/python3.8/site-packages/plumpy/workchains.py", line 250, in step
    return True, self._fn(self._workchain)
  File "/home/fdossantos/codes/aiida-tutorials/docs/sections/workflows/include/code/debugging/my_first_workchain_2_wrong_output.py", line 21, in result
    self.out("workchain_result", self.inputs.x)
  File "/home/fdossantos/venv/aiida_git/lib/python3.8/site-packages/aiida/engine/processes/process.py", line 354, in out
    return super().out(output_port, value)
  File "/home/fdossantos/venv/aiida_git/lib/python3.8/site-packages/plumpy/processes.py", line 79, in func_wrapper
    return func(self, *args, **kwargs)
  File "/home/fdossantos/venv/aiida_git/lib/python3.8/site-packages/plumpy/processes.py", line 1254, in out
    raise ValueError(msg)
ValueError: Error validating output 'uuid: 3fb97fdd-5b3f-4742-9ff8-aa604c91f055 (pk: 381) value: 4' for port 'workchain_result': value 'workchain_result' is not of the right type. Got '<class 'aiida.orm.nodes.data.int.Int'>', expected '<class 'aiida.orm.nodes.data.float.Float'>'

---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
<ipython-input-3-2c36ef047bf6> in <module>
----> 1 result = run(OutputInputWorkChain, x=Int(4) )
...
```

Of course, to correct this problem you have to make sure that you declared the right data types for the inputs and outputs, and that your work chain passes the right data nodes to the outputs.
Declaring the data type of the output is another good-practice towards robust work chains.

## Wrong output label

Now, remove the modifications of the previous section as to obtain the original `OutputInputWorkChain`.
Next, we will mimic a mistake when passing the output.
Alter your script file to match the example below:

```{literalinclude} include/code/debugging/my_first_workchain_3_wrong_label.py
:language: python
:emphasize-lines: 21
```

Note that in the `define` method, we specified an output labelled `workchain_result`.
In the `result` step, the work chain is trying to record an output labelled `workchain_output`, which was not declared.
If we try to run the work chain, we get the following error:

```{code-block} ipython
In [1]: from aiida.engine import run
In [2]: from my_first_workchain_1_output_input import OutputInputWorkChain
In [3]: result = run(OutputInputWorkChain, x=Int(4) )
07/05/2021 01:02:24 PM <26497> aiida.orm.nodes.process.workflow.workchain.WorkChainNode: [REPORT] [384|OutputInputWorkChain|on_except]: Traceback (most recent call last):
  File "/home/fdossantos/venv/aiida_git/lib/python3.8/site-packages/plumpy/process_states.py", line 229, in execute
    result = self.run_fn(*self.args, **self.kwargs)
  File "/home/fdossantos/venv/aiida_git/lib/python3.8/site-packages/aiida/engine/processes/workchains/workchain.py", line 194, in run
    return self._do_step()
  File "/home/fdossantos/venv/aiida_git/lib/python3.8/site-packages/aiida/engine/processes/workchains/workchain.py", line 211, in _do_step
    finished, stepper_result = self._stepper.step()
  File "/home/fdossantos/venv/aiida_git/lib/python3.8/site-packages/plumpy/workchains.py", line 250, in step
    return True, self._fn(self._workchain)
  File "/home/fdossantos/codes/aiida-tutorials/docs/sections/workflows/include/code/debugging/my_first_workchain_3_wrong_label.py", line 21, in result
    self.out("workchain_output", self.inputs.x)
  File "/home/fdossantos/venv/aiida_git/lib/python3.8/site-packages/aiida/engine/processes/process.py", line 354, in out
    return super().out(output_port, value)
  File "/home/fdossantos/venv/aiida_git/lib/python3.8/site-packages/plumpy/processes.py", line 79, in func_wrapper
    return func(self, *args, **kwargs)
  File "/home/fdossantos/venv/aiida_git/lib/python3.8/site-packages/plumpy/processes.py", line 1254, in out
    raise ValueError(msg)
ValueError: Error validating output 'uuid: 584c88c4-bfb5-465f-a4d6-d455ce4e1f73 (pk: 383) value: 4' for port 'outputs': Unexpected ports {'workchain_output': <Int: uuid: 584c88c4-bfb5-465f-a4d6-d455ce4e1f73 (pk: 383) value: 4>}, for a non dynamic namespace
...
```

The error message explains that the work chain received an output called `workchain_output`, which was unexpected, since it was not declared in the spec.
It is possible to activate a dynamic namespace where you don't need to declare the outputs in the `define()` method.
However, this feature is to be avoided unless you have a very good reason for doing so.
