*These appendices consist of optional exercises, and are mentioned
in earlier parts of the tutorial. Go through them only if you
have time.*

Restarting calculations
=======================

Up till now, we have presented several cases where, for example, the wrong input parameters were passed to a calculation, causing it to fail.
Often we had to retype a lot of code, to setup a new calculation with the correct inputs.
In addition, there are many real-life scenarios where one would need to restart calculations from completed calculations with largely the same inputs.
For example when we run molecular dynamics, we might want to add more time steps than we initially thought, or as another example you might want to refine the relaxation of a structure with tighter parameters.

In this section, you will learn how to relaunch a calculation from one that has already completed, while having the chance to add or change inputs before launching it.
As an example, let us first submit a total energy calculation using a parameters dictionary of the form:

.. code:: python

    parameters_dict = {
        'CONTROL': {
            'calculation': 'scf',
            'tstress': True,
            'tprnfor': True,
        },
        'SYSTEM': {
            'ecutwfc': 30.,
            'ecutrho': 200.,
        },
        'ELECTRONS': {
            'conv_thr': 1.e-14,
            'electron_maxstep': 3,
        },
    }

In this case, we set a very low number of self consistent iterations (3), which is too small to be able to reach the desired accuracy of 10\ :sup:`-14`.
This means the calculation will not converge and will not be successful, despite there not being any actual mistake in the parameters dictionary.

To easily restart from the previous calculation, instead of retyping all the inputs, you can simply use the ``get_builder_restart`` method of the ``CalcJobNode``.
Just like the ``get_builder`` method of the ``Process`` class, this will create an instance of the ``ProcessBuilder``, except this one will have all the inputs pre-populated based on the node.
To do so, simply load the node of a terminated calculation job in a ``verdi shell``, that you want to restart from, e.g.:

.. code:: python

    failed_calculation = load_node(<pk>)
    restart_builder = failed_calculation.get_builder_restart()

If you simply type ``restart_builder``, you can see that all the inputs have already been set to those that were used for the original calculation.
The only thing that now remains to be done, is to replace those inputs that caused the failure in the first place.

.. code:: python

    parameters = dict(restart_builder.parameters.dict)['ELECTRONS']['electron_maxstep'] = 80
    restart_builder.parameters = Dict(dict=parameters)

Simply giving the calculation some more steps in the convergence cycle will probably already fix the problem.

.. note::

    We have to create a new ``Dict`` node as we are changing its contents, and the original input is immutable as it would break the provenance.

However, in this Quantum ESPRESSO example even more can be done, by using the results of the previous calculation to speed up the restart.
To do so, we simply have to set the input ``parent_folder`` to the remote working directory of the old calculation, i.e.:

.. code:: python

    parameters = dict(restart_builder.parameters.dict)['CONTROL']['restart_mode'] = 'restart'
    restart_builder.parameters = Dict(dict=parameters)
    restart_builder.parent_folder = failed_calculation.outputs.remote_folder

Note that this particular step is specific to a ``PwCalculation``, but the restart builder concept works for any calculation class.
Any of the inputs can be changed or set.
For example, you may also want to record that this calculation is a restart, in addition to the provenance graph, by setting the label or description:

.. code:: python

    restart_builder.metadata.label = 'Restart from PwCalculation<{}>'.format(failed_calculation.pk)

Ultimately whatever needs to be changed for the restart is up to you, but the restart builder makes it a lot easier.
Finally, to submit the restart, since it is a process builder, it works exactly as any other builder:

.. code:: python

    from aiida.engine import launch
    results, node = launch.run.get_node(restart_builder)

You can now inspect the restarted calculation to verify that this time it actually completed successfully.
Using the restart builder, the required code to setup a calculation is much shorter than the one needed to launch a new one from scratch.
There is no need to load or create many of the inputs such as the pseudopotentials, structures and k-points,
because they were reused from the first calculation.
