Up to now, we have only presented cases in which we were passing wrong input parameters to the calculations, which required us to modify the input scripts and relaunch calculations from scratch. There are several other scenarios in which, more generally, we need to restart calculations from the last step that they have executed. For example when we run molecular dynamics, we might want to add more time steps than we initially thought, or as another example you might want to refine the relaxation of a structure with tighter parameters.

In this section, you will learn how to restart and/or modify a calculation that has run previously. As an example, let us first submit a total energy calculation using a parameters dictionary of the form:

``` python
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
```

and submit the calculation with this input. In this case, we set a very low number of self consistent iterations (3), too small to be able to reach the desired accuracy of 10\(^{-14}\): therefore the calculation will not reach a complete end and will be flagged in a FAILED state. However, there is no mistake in the parameter dictionary.

Now, create a new script file, where you will try to restart and correct the input dictionary. We first load the calculation that has just failed (let’s call it `c1`)

``` python
old_calc = load_node(PK)
```

(take care of using the correct PK). Then, create a new Builder `builder` which is set to reuse all inputs from the previous step, with a few adaptations to the input parameters that might be needed by the code to properly deal with restarts.

``` python
from aiida_quantumespresso.utils.restart import create_restart_pw
builder = create_restart_pw(                                     
   old_calc,                            
   use_output_structure=False,  
   restart_from_beginning=False, 
   force_restart=True)
```

The flag usage (most of them are optional) is:

-   `use_output_structure`: if True and `old_calc` has an output structure, the new calculation will use it as input;

-   `restart_from_beginning`: if False the new calculation will start from the charge density of `old_calc`, it will start from the beginning otherwise;

-   `force_restart`: if True, the new calculation will be created even if `old_calc` is not in a FINISHED job state.

Since this calculation has exactly the same parameters of before, we have to modify the input parameters and increase `electron_maxstep` to a larger value. To this aim, let’s load the dictionary of values and change it

``` python
old_parameters = builder.parameters
parameters_dict = old_parameters.get_dict()
parameters_dict['ELECTRONS']['electron_maxstep'] = 100
```

Note that you cannot modify the `old_parameters` object: it has been used by calculation `c1` and is saved in the database; hence a modification would break the provenance. We have to create a new ParameterData and pass it to c2:

``` python
ParameterData = DataFactory('parameter')
new_parameters = ParameterData(dict=parameters_dict)
builder.parameters = new_parameters
```

Now you can launch the new calculation

``` python
from aiida.work.run import submit    
new_calc = submit(builder)
print new_calc.pk
```

that this time can proceed until the end and return converged total energy. Using the restart method, the script is much shorter than the one needed to launch a new one from scratch: you didn’t need to define pseudopotentials, structures and k-points, which are the same as before. You can indeed inspect the new calculation to check that now it actually completed successfully.

