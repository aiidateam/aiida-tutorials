Calculation input validation
============================

This appendix shows additional ways to debug possible errors with QE, how to use a useful tool that we included in AiiDA to validate the input to Quantum ESPRESSO (and possibly suggest the correct name to mispelled keywords)

There are various reasons why you might end up providing a wrong input to a Quantum ESPRESSO calculation. Let’s check for example this input dictionary, where we inserted two mistakes:

``` python
parameters_dict = {
    "CTRL": {
        "calculation": "scf",
        "restart_mode": "from_scratch",
    },
    "SYSTEM": {
        "nat": 2,
        "ecutwfc": 30.,
        "ecutrho": 200.,
    },
    "ELECTRONS": {
        "conv_thr": 1.e-6,
    }
}
```

The two mistakes in the dictionary are the following. First, we wrote a wrong namelist name (’CTRL’ instead of ’CONTROL’). Second, we inserted the number of atoms explicitly: while that is how the number of atoms is specified in Quantum ESPRESSO, in AiiDA this key is reserved by the system: in fact this information is already contained in the StructureData. Modify the script with this ParameterData. In this case, we use a tool (the input validator that we provide in AiiDA) to check the input file before submitting. Therefore, the behavior will be slightly different from the previous example: the plugin will check for some keys and will refuse to submit the calculation. This kind of mistakes is revealed by either

- Submitting a calculation. You will see the calculation ending up in the SUBMISSIONFAILED status. Check therefore the logs to recognize the source of the error.

- Submitting a test. You will not be able to successfully create the test and the traceback will guide you to the problem.

Over the time this kind of trivial mistakes can be annoying, but they can be avoided with a utility function that checks the “grammar” of the input parameters. In your script, after you defined the parameters\_dict, you can validate it with the command (note that you need to pass also the input crystal structure, `s`, to allow the validator to perform all needed checks):

``` python
PwCalculation = CalculationFactory('quantumespresso.pw')
validated_dict = PwCalculation.input_helper(parameters_dict, structure=s)
parameters = ParameterData(dict=validated_dict)
```

The `input_helper` method will check for the correctness of the input parameters. If misspelling or incorrect keys are detected, the method raises an exception, which stops the script before submitting the calculation and thus allows for a more effective debugging.

With this utility, you can also provide a list of keys, without providing the namelists (useful if you don’t remember where to put some variables in the input file). Hence, you can provide to `input_helper()` a dictionary like this one:

``` python
parameters_dict = {
    'calculation': 'scf',
    'tstress': True,
    'tprnfor': True,
    'ecutwfc': 30.,
    'ecutrho': 200.,
    'conv_thr': 1.e-6,
}
validated_dict = PwCalculation.input_helper(
    parameters_dict, structure=s, flat_mode=True)
```

If you print the `validated_dict`, it will look like:

``` python
{
    "CONTROL": {
        "calculation": "scf",
        "tstress": True,
        "tprnfor": True,
    },
    "SYSTEM": {
        "ecutwfc": 30.,
        "ecutrho": 200.,
    },
    "ELECTRONS": {
        "conv_thr": 1.e-6,
    }
 }
```
