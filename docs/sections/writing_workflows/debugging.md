(workflows-debugging)=

# Debugging work chains

In this section, we reproduce a series of common mistakes you may commit yourself when writing your AiiDA work chains.

## AiiDA daemon

### Daemon not running

Sometimes, after submitting a work chain, the process status will read as _created_.
This means that the process was created and it is ready to be run.
However, if there is no daemon running, your process will continue with that status indefinetely.
Check if that is the case with

```{code-block} console
$ verdi daemon status
Profile: my_aiida_profile
The daemon is not running
```

In case the daemon is not running, start it with
```{code-block} console
$ verdi daemon start
Starting the daemon... RUNNING
```

### WorkChain not in the `PYTHONPATH`

When trying to import a work chain, if you get a `No module named ...` error message, e.g.,

```{code-block} ipython
In [1]: from addcalcjobworkchain import AddCalcjobWorkChain
---------------------------------------------------------------------------
ModuleNotFoundError                       Traceback (most recent call last)
<ipython-input-1-03fcc3f6b521> in <module>
----> 1 from addcalcjobworkchain import AddCalcjobWorkChain

ModuleNotFoundError: No module named 'addcalcjobworkchain'
```

you need to make sure the directory containing the work-chain definition is in the `PYTHONPATH`.

You can add the folder in which you have your Python file defining the WorkChain to the `PYTHONPATH` directly in the terminal through:

```{code-block} console
$ export PYTHONPATH=/path/to/workchain/directory/:$PYTHONPATH
```

For a more persistent result, you can add the path through the python-environment activation script.
In this way, the daemon will always know where to find your work chain even if your restart your computer.

After this, it is **very important** to restart the daemon.

### Restart the daemon

When updating an existing work chain file or adding a new one, it is necessary to restart the daemon every time after all changes have taken place.
For that use this following command

```{code-block} console
$ verdi daemon restart --reset
Profile: default
Waiting for the daemon to shut down... OK
Starting the daemon... RUNNING
```

Note, this is necessary if you are submitting your work chain.
If you are just running it, restarting the daemon is not necessary because it won't be executed by the daemon.
However, you may have to reopen the `verdi shell` session.

## Reading the report

You have examen the status of your work chain using the `verdi process list -a` command.
If you work chain has a status of `Finished` but with an exiting code other than zero, you can inspect the work-chain report with

```{code-block} console
$ verdi process report <PK>
2021-05-06 09:22:01 [4386 | REPORT]: [12945|PwBaseWorkChain|run_process]: launching PwCalculation<12950> iteration #1
2021-05-06 09:26:04 [4389 | REPORT]: [12945|PwBaseWorkChain|report_error_handled]: PwCalculation<12950> failed with exit status 501: Then ionic minimization cycle converged but the thresholds are exceeded in the final SCF.
2021-05-06 09:26:04 [4390 | REPORT]: [12945|PwBaseWorkChain|report_error_handled]: Action taken: ionic convergence thresholds met except in final scf: consider structure relaxed.
2021-05-06 09:26:04 [4391 | REPORT]: [12945|PwBaseWorkChain|results]: work chain completed after 1 iterations
2021-05-06 09:26:04 [4392 | REPORT]: [12945|PwBaseWorkChain|inspect_process]: PwCalculation<12950> failed but a handler detected an unrecoverable problem, aborting
2021-05-06 09:26:04 [4393 | REPORT]: [12945|PwBaseWorkChain|on_terminated]: remote folders will not be cleaned
```

## Wrong data type for the input

Here, we demonstrate what happens if you input a wrong data type to an work chian in the running or submission process.
For that, we consider the `OutputInputWorkChain` written in the {ref}`Work chain section <workflows-workchain>`.

{{ download }} **{download}`You can download the script here. <include/code/debugging/my_first_workchain_1_output_input.py>`**

After downloading the work-chain script in your computer where you are running AiiDA, navigate to the folder where you have saved the script and run in the `verdi shell`

```{code-block} ipython
In [1]: from aiida.engine import run
In [2]: from my_first_workchain_1_output_input import OutputInputWorkChain
In [3]: result = run(OutputInputWorkChain, x=4 )
---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
<ipython-input-5-118afb74821c> in <module>
----> 1 result = run(OutputInputWorkChain, x=4 )
...
ValueError: Error occurred validating port 'inputs.x': value 'x' is not of the right type. Got '<class 'int'>', expected '<class 'aiida.orm.nodes.data.int.Int'>'
```

In the third command line, we tried to run the OutputInputWorkChain passing an python integer as the input.
However, the work chain is expecting an AiiDA integer data type, which can be created with the `Int()` method of the `data.int` class.
See the declaration of the input of the `OutputInputWorkChain`:

```{literalinclude} include/code/debugging/my_first_workchain_1_output_input.py
:language: python
:lines: 13
```

When writing a work chain, specifying which type of data is expect is the first step of creating robust work chains.

The problem can be correct as in the following example:
```{code-block} ipython
In [1]: from aiida.engine import run
In [2]: from my_first_workchain_1_output_input import OutputInputWorkChain
In [3]: result = run(OutputInputWorkChain, x=Int(4) )
```

## Passing wrong data type to the output

Modify the `OutputWorkChain` declaring the output label `workchain_result` as of the type `Float`:

```{literalinclude} include/code/debugging/my_first_workchain_2_wrong_output.py
:language: python
:emphasize-lines: 1,15
```

The script will then try to output an `Int` where it is expected a `Float`.
Run the following in the `verdi shell` to see which kind of problem this may cause:

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

Of course, to correct this problem you have to make sure that you declared the right data types for the inputs and outputs, and that your work chain are passing the right data nodes to the outputs.
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
In the `result` step, the work chain is try to pass to an output labelled `workchain_output`, which was not declared.
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

The error message explains that the work chian expected a `workchain_output`.
It is possible to activate a dynamic namespace where you don't need to declare the outputs in the `define()` method.
However, this feature is to be avoided whenever possible.
