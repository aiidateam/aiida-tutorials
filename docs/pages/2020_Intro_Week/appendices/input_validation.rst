.. note::

    These appendices consist of optional exercises, and are mentioned in earlier parts of the tutorial.
    Go through them only if you have time.

.. _2020:appendix_input_validation:

Calculation input validation
============================

This appendix shows additional ways to debug errors with Quantum ESPRESSO, namely how to take advantage of a powerful tool to validate the input to Quantum ESPRESSO and possibly suggest the correct name to misspelled keywords.

There are various reasons why you might end up providing a wrong input to a Quantum ESPRESSO calculation.
Let's check, for example, this input dictionary, where we inserted two mistakes:

.. code:: python

    parameters_dict = {
        'CTRL': {
            'calculation': 'scf',
            'restart_mode': 'from_scratch',
        },
        'SYSTEM': {
            'nat': 2,
            'ecutwfc': 30.,
            'ecutrho': 200.,
        },
        'ELECTRONS': {
            'conv_thr': 1.e-6,
        }
    }

The two mistakes in the dictionary are the following:

-  We wrote a wrong namelist name (``CTRL`` instead of ``CONTROL``).
-  We inserted the number of atoms explicitly: while that is indeed how the
   number of atoms is specified in Quantum ESPRESSO, in AiiDA this key is reserved by the system,
   since this information is already contained within the ``StructureData``.

After we correct the dictionary ``parameters_dict``, we could run the calculation directly.
Alternatively, we can use a tool of the the ``aiida-quantumespresso`` plugin, the 'input helper', which checks the inputs before submitting the calculation.

In your script, after you define ``parameters_dict``,
you can validate it with the following command (note that you need to pass also an input crystal structure,
``structure``, to allow the validator to perform all the needed checks):

.. code:: python

    PwCalculation = CalculationFactory('quantumespresso.pw')
    validated_dict = PwCalculation.input_helper(parameters_dict, structure=structure)
    parameters = Dict(dict=validated_dict)


The ``input_helper``  method will check for the correctness of the input parameters.
If misspelling or incorrect keys are detected, the method raises an exception,
which stops the script before submitting the calculation and thus allows for a more effective debugging.

With this utility, you can also provide a list of keys,
without providing the namelists (useful if you don't remember where to put some variables in the input file).
Hence, you can provide to ``input_helper`` a dictionary like this one:

.. code:: python

    parameters_dict = {
        'calculation': 'scf',
        'tstress': True,
        'tprnfor': True,
        'ecutwfc': 30.,
        'ecutrho': 200.,
        'conv_thr': 1.e-6,
    }

    validated_dict = PwCalculation.input_helper(
        parameters_dict,
        structure=structure,
        flat_mode=True
    )

If you print ``validated_dict``, it will look like the following:

.. code:: python

    {
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
            'conv_thr': 1.e-6,
        }
    }
